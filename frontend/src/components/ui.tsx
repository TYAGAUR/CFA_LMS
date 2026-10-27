"use client";

import { useEffect, useState, type ReactNode } from "react";
import { api, errorText } from "@/lib/api";

export function Ring({ pct, size = 54 }: { pct: number; size?: number }) {
  return (
    <div
      className="ring"
      role="img"
      aria-label={`${pct}% complete`}
      style={{ width: size, height: size, background: `conic-gradient(var(--accent) ${pct}%, var(--line) 0)` }}
    >
      <span>{pct}%</span>
    </div>
  );
}

export function Meter({ pct, label }: { pct: number; label?: string }) {
  return (
    <div className="meter" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100} aria-label={label}>
      <b style={{ width: `${Math.max(pct, 3)}%` }} />
    </div>
  );
}

export function Loading({ text = "Loading…" }: { text?: string }) {
  return (
    <p className="muted" role="status" style={{ padding: 24 }}>
      {text}
    </p>
  );
}

export function ErrorBox({ error }: { error: unknown }) {
  if (!error) return null;
  return (
    <div className="err" role="alert">
      {errorText(error)}
    </div>
  );
}

/** Minimal data hook: GET a path, expose reload. */
export function useApi<T>(path: string | null, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [loading, setLoading] = useState(!!path);
  const [tick, setTick] = useState(0);
  useEffect(() => {
    if (!path) return;
    let alive = true;
    setLoading(true);
    api<T>(path)
      .then((d) => alive && (setData(d), setError(null)))
      .catch((e) => alive && setError(e))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [path, tick, ...deps]);
  return { data, error, loading, reload: () => setTick((t) => t + 1), setData };
}

export function Field({ label, children, hint }: { label: string; children: ReactNode; hint?: string }) {
  return (
    <div>
      <label className="f">{label}</label>
      {children}
      {hint && <div className="small muted" style={{ marginTop: 4 }}>{hint}</div>}
    </div>
  );
}

export function StatusPill({ status }: { status: string }) {
  const cls =
    ["paid", "active", "published", "captured", "completed", "processed"].includes(status)
      ? "g"
      : ["failed", "cancelled", "deactivated", "amount_mismatch", "rejected", "retired", "refunded"].includes(status)
        ? "b"
        : ["created", "pending_payment", "draft", "open", "pending_guardian_consent", "in_progress", "partially_refunded"].includes(status)
          ? "w"
          : "";
  return <span className={`pill ${cls}`}>{status.replaceAll("_", " ")}</span>;
}
