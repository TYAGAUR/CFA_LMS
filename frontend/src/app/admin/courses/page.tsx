"use client";

import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { date, rupees } from "@/lib/format";

type C = {
  id: string; code: string; title: string; tagline: string | null; description: string | null; fee_paise: number;
  validity_days: number | null; access_ends_on: string | null; seat_limit: number | null; batch_id: string | null;
  exam_window: string | null; status: string; sort_order: number; subject_codes: string[]; active_registrations: number;
};

const EMPTY = { code: "", title: "", tagline: "", description: "", fee: "", validity_days: "", access_ends_on: "", seat_limit: "", batch_id: "", exam_window: "", status: "draft", sort_order: "0", subject_codes: [] as string[] };

export default function AdminCourses() {
  const { data, error, reload } = useApi<C[]>("/admin/courses");
  const { data: subjects } = useApi<{ code: string; name: string }[]>("/admin/catalog");
  const { data: batches } = useApi<{ id: string; code: string; name: string }[]>("/admin/batches");
  const toast = useToast();
  const [edit, setEdit] = useState<{ id: string | null; f: typeof EMPTY } | null>(null);
  const [err, setErr] = useState<unknown>(null);

  function open(c?: C) {
    setErr(null);
    setEdit({
      id: c?.id ?? null,
      f: c ? {
        code: c.code, title: c.title, tagline: c.tagline ?? "", description: c.description ?? "", fee: String(c.fee_paise / 100),
        validity_days: c.validity_days ? String(c.validity_days) : "", access_ends_on: c.access_ends_on ?? "", seat_limit: c.seat_limit ? String(c.seat_limit) : "",
        batch_id: c.batch_id ?? "", exam_window: c.exam_window ?? "", status: c.status, sort_order: String(c.sort_order), subject_codes: c.subject_codes,
      } : EMPTY,
    });
  }

  async function save(e: FormEvent) {
    e.preventDefault();
    if (!edit) return;
    const f = edit.f;
    const body = {
      code: f.code, title: f.title, tagline: f.tagline || null, description: f.description || null, fee_paise: Math.round(Number(f.fee) * 100),
      validity_days: f.validity_days ? Number(f.validity_days) : null, access_ends_on: f.access_ends_on || null,
      seat_limit: f.seat_limit ? Number(f.seat_limit) : null, batch_id: f.batch_id || null, exam_window: f.exam_window || null,
      status: f.status, sort_order: Number(f.sort_order), subject_codes: f.subject_codes,
    };
    try {
      await api(edit.id ? `/admin/courses/${edit.id}` : "/admin/courses", { method: edit.id ? "PATCH" : "POST", body });
      toast("Course saved");
      setEdit(null);
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  if (error) return <ErrorBox error={error} />;
  if (!data) return <Loading />;
  const set = (k: keyof typeof EMPTY, v: string | string[]) => setEdit((s) => s && { ...s, f: { ...s.f, [k]: v } });

  return (
    <>
      <div className="spread">
        <h1 className="h-md">Courses & fees</h1>
        <button className="btn sm" onClick={() => open()}>New course</button>
      </div>
      {edit && (
        <form className="card" onSubmit={save}>
          <h3>{edit.id ? "Edit course" : "New course"}</h3>
          <ErrorBox error={err} />
          <div className="two">
            <Field label="Code (A–Z, 0–9, -)"><input type="text" value={edit.f.code} onChange={(e) => set("code", e.target.value.toUpperCase())} required /></Field>
            <Field label="Status">
              <select value={edit.f.status} onChange={(e) => set("status", e.target.value)}>
                <option value="draft">Draft (hidden)</option><option value="open">Open for registration</option><option value="closed">Closed</option>
              </select>
            </Field>
          </div>
          <Field label="Title"><input type="text" value={edit.f.title} onChange={(e) => set("title", e.target.value)} required /></Field>
          <Field label="Tagline"><input type="text" value={edit.f.tagline} onChange={(e) => set("tagline", e.target.value)} /></Field>
          <Field label="Description"><textarea value={edit.f.description} onChange={(e) => set("description", e.target.value)} /></Field>
          <div className="two">
            <Field label="Fee in ₹ (incl. GST)"><input type="number" min={1} step="0.01" value={edit.f.fee} onChange={(e) => set("fee", e.target.value)} required /></Field>
            <Field label="Seat limit (optional)"><input type="number" min={1} value={edit.f.seat_limit} onChange={(e) => set("seat_limit", e.target.value)} /></Field>
            <Field label="Validity in days" hint="Or set an access end date"><input type="number" min={1} value={edit.f.validity_days} onChange={(e) => set("validity_days", e.target.value)} /></Field>
            <Field label="Access ends on"><input type="date" value={edit.f.access_ends_on} onChange={(e) => set("access_ends_on", e.target.value)} /></Field>
            <Field label="Exam window (YYYY-MM)"><input type="text" placeholder="2027-05" value={edit.f.exam_window} onChange={(e) => set("exam_window", e.target.value)} /></Field>
            <Field label="Batch (optional)">
              <select value={edit.f.batch_id} onChange={(e) => set("batch_id", e.target.value)}>
                <option value="">None</option>{batches?.map((b) => <option key={b.id} value={b.id}>{b.code} · {b.name}</option>)}
              </select>
            </Field>
          </div>
          <Field label="Subjects included">
            <div className="row">
              {subjects?.map((s) => (
                <label key={s.code} className="check" style={{ margin: 0 }}>
                  <input type="checkbox" checked={edit.f.subject_codes.includes(s.code)}
                    onChange={(e) => set("subject_codes", e.target.checked ? [...edit.f.subject_codes, s.code] : edit.f.subject_codes.filter((x) => x !== s.code))} />
                  <span>{s.name}</span>
                </label>
              ))}
            </div>
          </Field>
          <div className="row" style={{ marginTop: 14 }}>
            <button className="btn">Save</button>
            <button type="button" className="btn ghost" onClick={() => setEdit(null)}>Cancel</button>
          </div>
        </form>
      )}
      <div className="card table-wrap">
        <table className="data">
          <thead><tr><th>Course</th><th>Fee</th><th>Access</th><th>Subjects</th><th>Active</th><th>Status</th><th /></tr></thead>
          <tbody>
            {data.map((c) => (
              <tr key={c.id}>
                <td><b>{c.title}</b><div className="small muted">{c.code}</div></td>
                <td>{rupees(c.fee_paise)}</td>
                <td className="small">{c.access_ends_on ? `until ${date(c.access_ends_on)}` : `${c.validity_days} days`}</td>
                <td className="small">{c.subject_codes.join(", ")}</td>
                <td>{c.active_registrations}{c.seat_limit ? ` / ${c.seat_limit}` : ""}</td>
                <td><StatusPill status={c.status} /></td>
                <td><button className="btn sm ghost" onClick={() => open(c)}>Edit</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
