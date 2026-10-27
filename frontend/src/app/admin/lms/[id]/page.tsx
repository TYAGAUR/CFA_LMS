"use client";

import { use, useMemo, useState, type FormEvent } from "react";
import { NotesRenderer } from "@/components/NotesRenderer";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { dateTime } from "@/lib/format";
import type { Block } from "@/lib/types";

type Version = { id: string; version_no: number; status: string; created_at: string; published_at: string | null; provenance: string; note: string | null };
type L = {
  id: string; lm_no: number; title: string; summary: string | null; source_ref: string | null; status: string;
  subject: { id: string; code: string; name: string };
  topics: { id: string; title: string; sort_order: number }[];
  los: { id: string; code: string; statement: string; command_word: string }[];
  content: { id: string; title: string; kind: string; current_published_version_id: string | null; versions: Version[] }[];
  resources: { id: string; kind: string; title: string; status: string; mandatory: boolean; downloadable: boolean; provenance: string; duration_s: number | null; size_bytes: number | null; url: string | null; has_file: boolean }[];
};

const TEMPLATE = JSON.stringify({
  schema: "notes/v1",
  blocks: [
    { type: "heading", level: 3, text: "Heading" },
    { type: "paragraph", inline: [{ t: "Plain text and " }, { t: "bold text", b: true }, { t: "." }] },
    { type: "list", ordered: false, items: [[{ t: "First point" }], [{ t: "Second point" }]] },
    { type: "table", header: ["Term", "Meaning"], rows: [["Cumulative", "Missed dividends build up"]] },
    { type: "callout", variant: "example", title: "Worked example", inline: [{ t: "₹1,80,000 × 3 = ₹5,40,000" }] },
    { type: "callout", variant: "watch_out", title: "Watch out", inline: [{ t: "Common exam trap." }] },
    { type: "callout", variant: "formula", title: "Formula", inline: [{ t: "PV = PMT ÷ r" }] },
    { type: "callout", variant: "fun", title: "Funny use case", inline: [{ t: "A relatable Indian example." }] },
  ],
}, null, 2);

const COMMAND_WORDS = ["describe", "explain", "calculate", "compare", "contrast", "interpret", "identify", "distinguish", "evaluate", "demonstrate", "formulate", "recommend", "justify", "analyze", "define", "discuss"];

export default function AdminLm({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { user } = useAuth();
  const toast = useToast();
  const { data: lm, error, reload } = useApi<L>(`/admin/lms/${id}`);
  const can = (p: string) => !!user?.permissions.includes(p);

  async function act(fn: () => Promise<unknown>, msg: string) {
    try {
      await fn();
      toast(msg);
      reload();
    } catch (e) {
      toast(errorText(e));
    }
  }

  if (error) return <ErrorBox error={error} />;
  if (!lm) return <Loading />;
  return (
    <>
      <div className="crumb">{lm.subject.name} › LM{lm.lm_no}</div>
      <div className="spread">
        <h1 className="h-md">{lm.title}</h1>
        <div className="row">
          <StatusPill status={lm.status} />
          {can("catalog:publish") && (
            <button className="btn sm ghost" onClick={() => act(() => api(`/admin/lms/${lm.id}`, { method: "PATCH", body: { subject_id: lm.subject.id, lm_no: lm.lm_no, title: lm.title, summary: lm.summary, source_ref: lm.source_ref, status: lm.status === "published" ? "draft" : "published" } }), "Status changed")}>
              {lm.status === "published" ? "Unpublish LM" : "Publish LM"}
            </button>
          )}
        </div>
      </div>
      <ContentSection lm={lm} canPublish={can("content:publish")} reload={reload} />
      <ResourcesSection lm={lm} canPublish={can("resource:publish")} act={act} reload={reload} />
      <TopicsLos lm={lm} act={act} />
    </>
  );
}

function ContentSection({ lm, canPublish, reload }: { lm: L; canPublish: boolean; reload: () => void }) {
  const toast = useToast();
  const [editing, setEditing] = useState<{ itemId: string | null; title: string; kind: string; json: string } | null>(null);
  const [err, setErr] = useState<unknown>(null);
  const preview = useMemo(() => {
    if (!editing) return null;
    try {
      return { ok: true as const, blocks: (JSON.parse(editing.json) as { blocks: Block[] }).blocks ?? [] };
    } catch (e) {
      return { ok: false as const, msg: (e as Error).message };
    }
  }, [editing]);

  async function openVersion(itemId: string, title: string, kind: string, versionId: string | null) {
    setErr(null);
    if (!versionId) return setEditing({ itemId, title, kind, json: TEMPLATE });
    const v = await api<{ body: unknown }>(`/admin/content-items/${itemId}/versions/${versionId}`);
    setEditing({ itemId, title, kind, json: JSON.stringify(v.body, null, 2) });
  }

  async function save(publish: boolean) {
    if (!editing) return;
    setErr(null);
    try {
      let itemId = editing.itemId;
      if (!itemId) {
        itemId = (await api<{ id: string }>("/admin/content-items", { body: { lm_id: lm.id, title: editing.title, kind: editing.kind, sort_order: lm.content.length } })).id;
      }
      await api(`/admin/content-items/${itemId}/versions`, { body: { body: JSON.parse(editing.json), publish, note: null } });
      toast(publish ? "Saved and published" : "Draft saved");
      setEditing(null);
      reload();
    } catch (e) {
      setErr(e);
    }
  }

  return (
    <div className="card">
      <div className="spread">
        <h3>Notes, infographics and revision sheets</h3>
        <button className="btn sm" onClick={() => setEditing({ itemId: null, title: "", kind: "note", json: TEMPLATE })}>New item</button>
      </div>
      <table className="data" style={{ marginTop: 8 }}>
        <thead><tr><th>Title</th><th>Kind</th><th>Versions</th><th /></tr></thead>
        <tbody>
          {lm.content.map((c) => (
            <tr key={c.id}>
              <td><b>{c.title}</b></td>
              <td>{c.kind.replace("_", " ")}</td>
              <td className="small">
                {c.versions.map((v) => (
                  <div key={v.id}>
                    v{v.version_no} <StatusPill status={v.status} /> {dateTime(v.published_at ?? v.created_at)}
                    {canPublish && v.status === "draft" && <button className="link-btn" style={{ marginLeft: 8 }} onClick={() => api(`/admin/content-items/${c.id}/versions/${v.id}/publish`, { method: "POST" }).then(() => { toast("Published"); reload(); }).catch((e) => toast(errorText(e)))}>publish</button>}
                  </div>
                ))}
              </td>
              <td><button className="btn sm ghost" onClick={() => openVersion(c.id, c.title, c.kind, c.versions[0]?.id ?? null)}>Edit (new version)</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      {editing && (
        <div style={{ marginTop: 16 }}>
          <ErrorBox error={err} />
          {!editing.itemId && (
            <div className="two">
              <Field label="Title"><input type="text" value={editing.title} onChange={(e) => setEditing({ ...editing, title: e.target.value })} required /></Field>
              <Field label="Kind"><select value={editing.kind} onChange={(e) => setEditing({ ...editing, kind: e.target.value })}><option value="note">Note</option><option value="infographic">Infographic</option><option value="revision_sheet">Revision sheet</option></select></Field>
            </div>
          )}
          <p className="small muted">Content is stored as structured blocks (notes/v1), never raw HTML. Block types: heading, paragraph, list, table, callout (example, watch_out, formula, fun, note), infographic (waterfall).</p>
          <div className="two">
            <textarea className="code" value={editing.json} onChange={(e) => setEditing({ ...editing, json: e.target.value })} spellCheck={false} aria-label="Content JSON" />
            <div className="card" style={{ maxHeight: 520, overflow: "auto" }}>
              <div className="eyebrow">Preview</div>
              {preview?.ok ? <NotesRenderer blocks={preview.blocks} /> : <div className="err">JSON error: {preview?.msg}</div>}
            </div>
          </div>
          <div className="row" style={{ marginTop: 12 }}>
            <button className="btn ghost" disabled={!preview?.ok} onClick={() => save(false)}>Save draft</button>
            {canPublish && <button className="btn" disabled={!preview?.ok} onClick={() => save(true)}>Save and publish</button>}
            <button className="link-btn" onClick={() => setEditing(null)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}

function ResourcesSection({ lm, canPublish, act, reload }: { lm: L; canPublish: boolean; act: (fn: () => Promise<unknown>, msg: string) => Promise<void>; reload: () => void }) {
  const toast = useToast();
  const [f, setF] = useState({ kind: "video", title: "", mandatory: true, downloadable: false, provenance: "faculty_recording", licence_ref: "", duration: "", url: "" });
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<unknown>(null);

  async function upload(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    setBusy(true);
    const fd = new FormData();
    fd.set("lm_id", lm.id);
    fd.set("kind", f.kind);
    fd.set("title", f.title);
    fd.set("mandatory", String(f.mandatory));
    fd.set("downloadable", String(f.downloadable));
    fd.set("provenance", f.provenance);
    fd.set("sort_order", String(lm.resources.length));
    if (f.licence_ref) fd.set("licence_ref", f.licence_ref);
    if (f.duration) {
      const [m, s] = f.duration.split(":").map(Number);
      fd.set("duration_s", String(s === undefined ? m * 60 : m * 60 + s));
    }
    if (f.kind === "link") fd.set("url", f.url);
    else if (file) fd.set("file", file);
    try {
      await api("/admin/resources", { form: fd });
      toast("Uploaded as draft. Publish it to make it visible.");
      setF({ ...f, title: "", url: "", duration: "" });
      setFile(null);
      reload();
    } catch (e2) {
      setErr(e2);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card">
      <h3>Videos, PDFs and links</h3>
      <table className="data" style={{ marginTop: 8 }}>
        <thead><tr><th>Title</th><th>Kind</th><th>Details</th><th>Status</th><th /></tr></thead>
        <tbody>
          {lm.resources.map((r) => (
            <tr key={r.id}>
              <td><b>{r.title}</b><div className="small muted">{r.mandatory ? "mandatory" : "optional"} · {r.provenance.replaceAll("_", " ")}</div></td>
              <td>{r.kind}</td>
              <td className="small">{r.duration_s ? `${Math.floor(r.duration_s / 60)}:${String(r.duration_s % 60).padStart(2, "0")}` : ""} {r.size_bytes ? `${(r.size_bytes / 1048576).toFixed(1)} MB` : ""} {r.url ?? ""}</td>
              <td><StatusPill status={r.status} /></td>
              <td>
                {canPublish && (r.status === "published"
                  ? <button className="btn sm ghost" onClick={() => act(() => api(`/admin/resources/${r.id}/unpublish`, { method: "POST" }), "Unpublished")}>Unpublish</button>
                  : <button className="btn sm" onClick={() => act(() => api(`/admin/resources/${r.id}/publish`, { method: "POST" }), "Published")}>Publish</button>)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <form onSubmit={upload} style={{ marginTop: 14 }}>
        <div className="eyebrow">Add a resource</div>
        <ErrorBox error={err} />
        <div className="two">
          <Field label="Type"><select value={f.kind} onChange={(e) => setF({ ...f, kind: e.target.value, provenance: e.target.value === "video" ? "faculty_recording" : e.target.value === "link" ? "reference_only" : "original" })}>
            <option value="video">Class video (MP4/WebM)</option><option value="pdf">PDF notes</option><option value="class_note">Class handout (PDF)</option><option value="link">External link</option>
          </select></Field>
          <Field label="Title"><input type="text" value={f.title} onChange={(e) => setF({ ...f, title: e.target.value })} required /></Field>
          {f.kind === "link"
            ? <Field label="URL (https)"><input type="text" value={f.url} onChange={(e) => setF({ ...f, url: e.target.value })} required /></Field>
            : <Field label="File"><input type="file" accept={f.kind === "video" ? "video/mp4,video/webm" : "application/pdf"} onChange={(e) => setFile(e.target.files?.[0] ?? null)} required /></Field>}
          {f.kind === "video" && <Field label="Duration (mm:ss)" hint="Needed for the 90% watched rule"><input type="text" placeholder="12:05" value={f.duration} onChange={(e) => setF({ ...f, duration: e.target.value })} /></Field>}
          <Field label="Provenance (C-06)"><select value={f.provenance} onChange={(e) => setF({ ...f, provenance: e.target.value })}>
            <option value="original">Original (written by faculty)</option><option value="faculty_recording">Faculty recording</option><option value="reference_only">Reference link only</option><option value="licensed_third_party">Licensed third party</option>
          </select></Field>
          {f.provenance === "licensed_third_party" && <Field label="Licence reference"><input type="text" value={f.licence_ref} onChange={(e) => setF({ ...f, licence_ref: e.target.value })} required /></Field>}
        </div>
        <label className="check"><input type="checkbox" checked={f.mandatory} onChange={(e) => setF({ ...f, mandatory: e.target.checked })} /><span>Counts towards LM completion</span></label>
        {f.kind !== "video" && f.kind !== "link" && <label className="check"><input type="checkbox" checked={f.downloadable} onChange={(e) => setF({ ...f, downloadable: e.target.checked })} /><span>Students may download</span></label>}
        <button className="btn" disabled={busy}>{busy ? "Uploading…" : "Upload"}</button>
      </form>
    </div>
  );
}

function TopicsLos({ lm, act }: { lm: L; act: (fn: () => Promise<unknown>, msg: string) => Promise<void> }) {
  const [topic, setTopic] = useState("");
  const [los, setLos] = useState({ code: "", statement: "", command_word: "describe" });
  return (
    <div className="two">
      <div className="card">
        <h3>Topics</h3>
        <ul>{lm.topics.map((t) => <li key={t.id}>{t.title} <button className="link-btn small" onClick={() => act(() => api(`/admin/topics/${t.id}`, { method: "DELETE" }), "Removed")}>remove</button></li>)}</ul>
        <form className="row" onSubmit={(e) => { e.preventDefault(); void act(() => api("/admin/topics", { body: { lm_id: lm.id, title: topic, sort_order: lm.topics.length } }).then(() => setTopic("")), "Topic added"); }}>
          <input type="text" placeholder="New topic" value={topic} onChange={(e) => setTopic(e.target.value)} required style={{ flex: 1 }} />
          <button className="btn sm">Add</button>
        </form>
      </div>
      <div className="card">
        <h3>Learning Outcome Statements</h3>
        <ul className="small">{lm.los.map((l) => <li key={l.id}><b>{l.code}</b> ({l.command_word}) {l.statement} <button className="link-btn" onClick={() => act(() => api(`/admin/los/${l.id}`, { method: "DELETE" }), "Removed")}>remove</button></li>)}</ul>
        <form onSubmit={(e) => { e.preventDefault(); void act(() => api("/admin/los", { body: { lm_id: lm.id, ...los } }).then(() => setLos({ code: "", statement: "", command_word: "describe" })), "LOS added"); }}>
          <div className="row">
            <input type="text" placeholder="Code e.g. EQ-1-a" value={los.code} onChange={(e) => setLos({ ...los, code: e.target.value })} required style={{ width: 150 }} />
            <select value={los.command_word} onChange={(e) => setLos({ ...los, command_word: e.target.value })} style={{ width: 150 }}>{COMMAND_WORDS.map((w) => <option key={w}>{w}</option>)}</select>
          </div>
          <textarea placeholder="Statement (paraphrased; do not paste curriculum text)" value={los.statement} onChange={(e) => setLos({ ...los, statement: e.target.value })} required style={{ marginTop: 8, minHeight: 60 }} />
          <button className="btn sm" style={{ marginTop: 8 }}>Add LOS</button>
        </form>
      </div>
    </div>
  );
}
