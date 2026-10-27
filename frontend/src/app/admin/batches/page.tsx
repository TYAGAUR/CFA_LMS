"use client";

import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { date } from "@/lib/format";

type B = { id: string; code: string; name: string; exam_window: string | null; starts_on: string; ends_on: string; status: string; students: number };

export default function AdminBatches() {
  const { data, error, reload } = useApi<B[]>("/admin/batches");
  const toast = useToast();
  const [f, setF] = useState({ code: "", name: "", exam_window: "", starts_on: "", ends_on: "", status: "active" });
  const [err, setErr] = useState<unknown>(null);
  async function create(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      await api("/admin/batches", { body: { ...f, exam_window: f.exam_window || null } });
      toast("Batch created");
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }
  return (
    <>
      <h1 className="h-md">Batches</h1>
      <p className="muted small" style={{ margin: 0 }}>A course can be linked to a batch, so students who pay for it join that batch automatically.</p>
      <details className="card">
        <summary style={{ cursor: "pointer", fontWeight: 700 }}>New batch</summary>
        <form onSubmit={create}>
          <ErrorBox error={err} />
          <div className="two">
            <Field label="Code"><input type="text" value={f.code} onChange={(e) => setF({ ...f, code: e.target.value.toUpperCase() })} required /></Field>
            <Field label="Name"><input type="text" value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} required /></Field>
            <Field label="Exam window (YYYY-MM)"><input type="text" value={f.exam_window} onChange={(e) => setF({ ...f, exam_window: e.target.value })} /></Field>
            <Field label="Status"><select value={f.status} onChange={(e) => setF({ ...f, status: e.target.value })}><option value="planned">Planned</option><option value="active">Active</option><option value="closed">Closed</option></select></Field>
            <Field label="Starts on"><input type="date" value={f.starts_on} onChange={(e) => setF({ ...f, starts_on: e.target.value })} required /></Field>
            <Field label="Ends on"><input type="date" value={f.ends_on} onChange={(e) => setF({ ...f, ends_on: e.target.value })} required /></Field>
          </div>
          <button className="btn" style={{ marginTop: 12 }}>Create</button>
        </form>
      </details>
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>Batch</th><th>Exam window</th><th>Dates</th><th>Students</th><th>Status</th></tr></thead>
            <tbody>{data.map((b) => <tr key={b.id}><td><b>{b.code}</b><div className="small muted">{b.name}</div></td><td>{b.exam_window}</td><td className="small">{date(b.starts_on)} – {date(b.ends_on)}</td><td>{b.students}</td><td><StatusPill status={b.status} /></td></tr>)}</tbody>
          </table>
        </div>
      )}
    </>
  );
}
