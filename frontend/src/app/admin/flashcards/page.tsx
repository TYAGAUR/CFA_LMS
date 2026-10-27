"use client";

import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

type C = { id: string; subject_id: string; lm_id: string | null; front: string; back: string; status: string };
type Cat = { id: string; code: string; name: string; lms: { id: string; lm_no: number; title: string }[] };

export default function AdminFlashcards() {
  const { user } = useAuth();
  const toast = useToast();
  const { data: cat } = useApi<Cat[]>("/admin/catalog");
  const [subject, setSubject] = useState("");
  const { data, error, reload } = useApi<C[]>(`/admin/flashcards${subject ? `?subject=${subject}` : ""}`);
  const [edit, setEdit] = useState<{ id: string | null; subject_code: string; lm_id: string; front: string; back: string; status: string } | null>(null);
  const [err, setErr] = useState<unknown>(null);
  const canWrite = !!user?.permissions.includes("flashcard:write");
  const byId = Object.fromEntries((cat ?? []).map((s) => [s.id, s]));

  async function save(e: FormEvent) {
    e.preventDefault();
    if (!edit) return;
    setErr(null);
    try {
      const { id, ...body } = edit;
      await api(id ? `/admin/flashcards/${id}` : "/admin/flashcards", { method: id ? "PATCH" : "POST", body: { ...body, lm_id: body.lm_id || null } });
      toast("Card saved");
      setEdit(null);
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  return (
    <>
      <div className="spread">
        <h1 className="h-md">Flashcards</h1>
        {canWrite && <button className="btn sm" onClick={() => setEdit({ id: null, subject_code: subject, lm_id: "", front: "", back: "", status: "published" })}>New card</button>}
      </div>
      <p className="small muted" style={{ margin: 0 }}>Keep one clear prompt per card and a short answer. Longer numerical problems belong in the question bank.</p>
      {edit && (
        <form className="card" onSubmit={save}>
          <ErrorBox error={err} />
          <div className="two">
            <Field label="Subject"><select value={edit.subject_code} onChange={(e) => setEdit({ ...edit, subject_code: e.target.value, lm_id: "" })} required><option value="">Choose…</option>{cat?.map((s) => <option key={s.code} value={s.code}>{s.name}</option>)}</select></Field>
            <Field label="LM (optional)"><select value={edit.lm_id} onChange={(e) => setEdit({ ...edit, lm_id: e.target.value })}><option value="">Whole subject</option>{cat?.find((s) => s.code === edit.subject_code)?.lms.map((l) => <option key={l.id} value={l.id}>LM{l.lm_no} · {l.title}</option>)}</select></Field>
          </div>
          <Field label="Front (prompt)"><textarea value={edit.front} onChange={(e) => setEdit({ ...edit, front: e.target.value })} required style={{ minHeight: 60 }} /></Field>
          <Field label="Back (answer)"><textarea value={edit.back} onChange={(e) => setEdit({ ...edit, back: e.target.value })} required style={{ minHeight: 60 }} /></Field>
          <Field label="Status"><select value={edit.status} onChange={(e) => setEdit({ ...edit, status: e.target.value })}><option value="published">Published</option><option value="draft">Draft</option><option value="retired">Retired</option></select></Field>
          <div className="row" style={{ marginTop: 12 }}><button className="btn">Save</button><button type="button" className="btn ghost" onClick={() => setEdit(null)}>Cancel</button></div>
        </form>
      )}
      <select value={subject} onChange={(e) => setSubject(e.target.value)} style={{ maxWidth: 260 }}><option value="">All subjects</option>{cat?.map((s) => <option key={s.code} value={s.code}>{s.name}</option>)}</select>
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>Front</th><th>Back</th><th>Subject</th><th>Status</th><th /></tr></thead>
            <tbody>
              {data.map((c) => (
                <tr key={c.id}>
                  <td><b>{c.front}</b></td><td className="small">{c.back}</td><td className="small">{byId[c.subject_id]?.name}</td><td><StatusPill status={c.status} /></td>
                  <td>{canWrite && <button className="link-btn small" onClick={() => setEdit({ id: c.id, subject_code: byId[c.subject_id]?.code ?? "", lm_id: c.lm_id ?? "", front: c.front, back: c.back, status: c.status })}>Edit</button>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
