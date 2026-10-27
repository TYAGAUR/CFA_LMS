"use client";

import Link from "next/link";
import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";

type S = { id: string; code: string; name: string; icon: string; status: string; exam_weight: string | null;
  lms: { id: string; lm_no: number; title: string; status: string; source_ref: string | null; resources: number; notes: number }[] };

export default function AdminCatalog() {
  const { data, error, reload } = useApi<S[]>("/admin/catalog");
  const toast = useToast();
  const [adding, setAdding] = useState<string | null>(null);
  const [lm, setLm] = useState({ lm_no: "", title: "", source_ref: "" });
  const [err, setErr] = useState<unknown>(null);

  async function addLm(e: FormEvent, subject: S) {
    e.preventDefault();
    setErr(null);
    try {
      await api("/admin/lms", { body: { subject_id: subject.id, lm_no: Number(lm.lm_no), title: lm.title, source_ref: lm.source_ref || null, status: "published" } });
      toast("LM added");
      setAdding(null);
      setLm({ lm_no: "", title: "", source_ref: "" });
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  if (error) return <ErrorBox error={error} />;
  if (!data) return <Loading />;
  return (
    <>
      <h1 className="h-md">Catalogue & content</h1>
      <p className="muted small" style={{ margin: 0 }}>Open an LM to add notes, videos, PDFs, topics and LOS. The internal source reference is never shown to students.</p>
      {data.map((s) => (
        <div className="card" key={s.id}>
          <div className="spread">
            <h3>{s.icon} {s.name} <span className="muted small">· {s.code} · {s.exam_weight}</span></h3>
            <button className="btn sm ghost" onClick={() => setAdding(adding === s.id ? null : s.id)}>Add LM</button>
          </div>
          {adding === s.id && (
            <form className="row" onSubmit={(e) => addLm(e, s)} style={{ marginTop: 10 }}>
              <ErrorBox error={err} />
              <div style={{ width: 90 }}><Field label="LM no."><input type="number" min={1} value={lm.lm_no} onChange={(e) => setLm({ ...lm, lm_no: e.target.value })} required /></Field></div>
              <div style={{ flex: 1 }}><Field label="Title"><input type="text" value={lm.title} onChange={(e) => setLm({ ...lm, title: e.target.value })} required /></Field></div>
              <div style={{ width: 170 }}><Field label="Source ref (internal)"><input type="text" value={lm.source_ref} onChange={(e) => setLm({ ...lm, source_ref: e.target.value })} /></Field></div>
              <button className="btn sm" style={{ alignSelf: "flex-end" }}>Save</button>
            </form>
          )}
          <table className="data" style={{ marginTop: 8 }}>
            <thead><tr><th>LM</th><th>Title</th><th>Notes</th><th>Resources</th><th>Status</th></tr></thead>
            <tbody>
              {s.lms.map((m) => (
                <tr key={m.id}>
                  <td>LM{m.lm_no}</td>
                  <td><Link href={`/admin/lms/${m.id}`}>{m.title}</Link>{m.source_ref && <div className="small muted">ref {m.source_ref}</div>}</td>
                  <td>{m.notes}</td>
                  <td>{m.resources}</td>
                  <td><StatusPill status={m.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </>
  );
}
