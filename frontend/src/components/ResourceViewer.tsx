"use client";

import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { ErrorBox, Loading } from "./ui";

type Playback = {
  id: string;
  kind: "video" | "pdf" | "class_note" | "link";
  title: string;
  url: string | null;
  mime_type: string | null;
  duration_s: number | null;
  chapters: { start_s: number; title: string }[];
  watermark: string;
  downloadable: boolean;
  last_position_s: number;
  completed: boolean;
};

const HEARTBEAT_MS = 15000;

/** Secure playback (US-5.04/5.05): signed URL, moving watermark, unique-seconds progress. */
export function ResourceViewer({ resourceId, onProgress }: { resourceId: string; onProgress?: (completed: boolean) => void }) {
  const [pb, setPb] = useState<Playback | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [wm, setWm] = useState({ top: "8%", left: "6%" });
  const video = useRef<HTMLVideoElement>(null);
  const segStart = useRef<number | null>(null);

  useEffect(() => {
    setPb(null);
    setError(null);
    api<Playback>(`/resources/${resourceId}/playback`).then(setPb).catch(setError);
  }, [resourceId]);

  // Move the watermark every 30 s (P-07 §6).
  useEffect(() => {
    const t = setInterval(() => setWm({ top: `${8 + Math.random() * 75}%`, left: `${4 + Math.random() * 60}%` }), 30000);
    return () => clearInterval(t);
  }, []);

  async function send(body: Record<string, unknown>) {
    try {
      const r = await api<{ completed: boolean }>(`/resources/${resourceId}/progress`, { body });
      onProgress?.(r.completed);
    } catch {
      /* progress is best-effort; next heartbeat retries */
    }
  }

  // Report contiguous watched segments (max 60 s each).
  function flush(force = false) {
    const v = video.current;
    if (!v || segStart.current === null) return;
    const now = Math.floor(v.currentTime);
    const from = segStart.current;
    if (now > from && (force || now - from >= 10)) {
      void send({ from_s: from, to_s: Math.min(now, from + 60), position_s: now });
      segStart.current = now;
    }
  }

  useEffect(() => {
    const t = setInterval(() => flush(), HEARTBEAT_MS);
    return () => {
      clearInterval(t);
      flush(true);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pb?.id]);

  if (error) return <ErrorBox error={error} />;
  if (!pb) return <Loading />;

  if (pb.kind === "link") {
    return (
      <div className="card">
        <p>This resource opens on an external site.</p>
        <a className="btn" href={pb.url ?? "#"} target="_blank" rel="noopener noreferrer" onClick={() => void send({ mark_complete: true })}>
          Open {pb.title} ↗
        </a>
      </div>
    );
  }

  if (pb.kind === "video") {
    return (
      <div>
        <div className="player" onContextMenu={(e) => e.preventDefault()}>
          <video
            ref={video}
            src={pb.url ?? undefined}
            controls
            controlsList="nodownload"
            disablePictureInPicture
            preload="metadata"
            onLoadedMetadata={(e) => {
              if (pb.last_position_s) e.currentTarget.currentTime = pb.last_position_s;
            }}
            onPlay={(e) => (segStart.current = Math.floor(e.currentTarget.currentTime))}
            onPause={() => {
              flush(true);
              segStart.current = null;
            }}
            onSeeking={() => {
              flush(true);
              segStart.current = null;
            }}
            onSeeked={(e) => {
              if (!e.currentTarget.paused) segStart.current = Math.floor(e.currentTarget.currentTime);
            }}
            onEnded={() => {
              flush(true);
              segStart.current = null;
              if (!pb.duration_s) void send({ mark_complete: true });
            }}
          />
          <div className="wm" style={wm} aria-hidden>
            {pb.watermark}
          </div>
        </div>
        {pb.chapters.length > 0 && (
          <div className="row" style={{ marginTop: 10 }}>
            {pb.chapters.map((c) => (
              <button key={c.start_s} className="btn sm ghost" type="button" onClick={() => video.current && (video.current.currentTime = c.start_s)}>
                {Math.floor(c.start_s / 60)}:{String(c.start_s % 60).padStart(2, "0")} {c.title}
              </button>
            ))}
          </div>
        )}
        <p className="small muted">Your position is saved automatically. Watch at least 90% to complete it.</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ position: "relative" }}>
        <iframe className="pdf-frame" src={`${pb.url}#toolbar=0`} title={pb.title} />
        <div className="wm" style={{ ...wm, color: "rgba(33,28,132,.18)" }} aria-hidden>
          {pb.watermark}
        </div>
      </div>
      <div className="row" style={{ marginTop: 10 }}>
        <button className="btn sm good" type="button" onClick={() => void send({ mark_complete: true })} disabled={pb.completed}>
          {pb.completed ? "Marked as read ✓" : "Mark as read"}
        </button>
        {pb.downloadable && pb.url && (
          <a className="btn sm ghost" href={pb.url} download>
            Download
          </a>
        )}
      </div>
    </div>
  );
}
