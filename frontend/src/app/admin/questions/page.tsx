"use client";

import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { DIFFICULTY_LABEL } from "@/lib/types";

type Q = { id: string; subject_id: string; lm_id: string | null; stem: string; options: string[]; correct_index: number; explanation: string; difficulty: "E" | "M" | "H"; qtype: string; lock_option_order: boolean; status: string; version: number; author_id: string | null };
type Cat = { id: string; code: string; name: string; lms: { id: string; lm_no: number; title: string }[] };
type Validation = { questions: number; answer_distribution: Record<string, number>; issues: string[]; ok: boolean };

const EMPTY = { subject_code: "", lm_id: "", stem: "", options: ["", "", ""], correct_index: 0, explanation: "", difficulty: "M", qtype: "conceptual", lock_option_order: false };

export default function QuestionBank() {
  const { user } = useAuth();
  const toast = useToast();
  const { data: cat } = useApi<Cat[]>("/admin/catalog");
  const [subject, setSubject] = useState("");
  const [lm, setLm] = useState("");
  const [status, setStatus] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [q, setQ] = useState("");
  const params = new URLSearchParams({ ...(subject ? { subject } : {}), ...(lm ? { lm_id: lm } : {}), ...(status ? { status } : {}), ...(difficulty ? { difficulty } : {}), ...(q ? { q } : {}) });
  const { data, error, reload } = useApi<{ total: number; items: Q[] }>(`/admin/questions?${params}`);
  const [edit, setEdit] = useState<{ id: string | null; f: typeof EMPTY } | null>(null);
  const [err, setErr] = useState<unknown>(null);
  const [val, setVal] = useState<Validation | null>(null);
  const can = (p: string) => !!user?.permissions.includes(p);
  const subjById = Object.fromEntries((cat ?? []).map((s) => [s.id, s]));
  const lmById = Object.fromEntries((cat ?? []).flatMap((s) => s.lms.map((l) => [l.id, { ...l, code: s.code }])));
  const lmsFor = cat?.find((s) => s.code === (edit?.f.subject_code || subject))?.lms ?? [];

  function open(x?: Q) {
    setErr(null);
    setEdit({ id: x?.id ?? null, f: x ? { subject_code: subjById[x.subject_id]?.code ?? "", lm_id: x.lm_id ?? "", stem: x.stem, options: [...x.options], correct_index: x.correct_index, explanation: x.explanation, difficulty: x.difficulty, qtype: x.qtype, lock_option_order: x.lock_option_order } : { ...EMPTY, subject_code: subject, lm_id: lm } });
    scrollTo({ top: 0, behavior: "smooth" });
  }

  async function save(e: FormEvent) {
    e.preventDefault();
    if (!edit) return;
    setErr(null);
    try {
      await api(edit.id ? `/admin/questions/${edit.id}` : "/admin/questions", { method: edit.id ? "PATCH" : "POST", body: { ...edit.f, lm_id: edit.f.lm_id || null } });
      toast(edit.id ? "Saved. Edited questions go back to draft until published again." : "Question saved as draft");
      setEdit(null);
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  async function setQStatus(id: string, action: string) {
    try {
      await api(`/admin/questions/${id}/${action}`, { method: "POST" });
      reload();
    } catch (e) {
      toast(errorText(e));
    }
  }

  const set = (k: keyof typeof EMPTY, v: unknown) => setEdit((s) => s && { ...s, f: { ...s.f, [k]: v } });

  return (
    <>
      <div className="spread">
        <h1 className="h-md">Question bank</h1>
        {can("qbank:write") && <button className="btn sm" onClick={() => open()}>New question</button>}
      </div>
      {edit && (
        <form className="card" onSubmit={save}>
          <h3>{edit.id ? "Edit question" : "New question"}</h3>
          <ErrorBox error={err} />
          <div className="two">
            <Field label="Subject"><select value={edit.f.subject_code} onChange={(e) => { set("subject_code", e.target.value); set("lm_id", ""); }} required><option value="">Choose…</option>{cat?.map((s) => <option key={s.code} value={s.code}>{s.name}</option>)}</select></Field>
            <Field label="Learning Module"><select value={edit.f.lm_id} onChange={(e) => set("lm_id", e.target.value)}><option value="">(Subject-level)</option>{lmsFor.map((l) => <option key={l.id} value={l.id}>LM{l.lm_no} · {l.title}</option>)}</select></Field>
          </div>
          <Field label="Question stem"><textarea value={edit.f.stem} onChange={(e) => set("stem", e.target.value)} required minLength={10} /></Field>
          {[0, 1, 2].map((k) => (
            <div key={k} className="row" style={{ marginTop: 8 }}>
              <label className="check" style={{ margin: 0 }}><input type="radio" name="correct" checked={edit.f.correct_index === k} onChange={() => set("correct_index", k)} /><span><b>{"ABC"[k]}</b></span></label>
              <input type="text" style={{ flex: 1 }} value={edit.f.options[k]} onChange={(e) => set("options", edit.f.options.map((o, j) => (j === k ? e.target.value : o)))} required placeholder={`Option ${"ABC"[k]}`} />
            </div>
          ))}
          <p className="small muted">Select the radio button next to the correct answer.</p>
          <Field label="Worked solution / explanation"><textarea value={edit.f.explanation} onChange={(e) => set("explanation", e.target.value)} required /></Field>
          <div className="two">
            <Field label="Difficulty"><select value={edit.f.difficulty} onChange={(e) => set("difficulty", e.target.value)}><option value="E">Easy</option><option value="M">Medium</option><option value="H">Hard</option></select></Field>
            <Field label="Type"><select value={edit.f.qtype} onChange={(e) => set("qtype", e.target.value)}><option value="conceptual">Conceptual</option><option value="numerical">Numerical</option></select></Field>
          </div>
          <label className="check"><input type="checkbox" checked={edit.f.lock_option_order} onChange={(e) => set("lock_option_order", e.target.checked)} /><span>Keep option order fixed (e.g. &quot;Both A and B&quot;)</span></label>
          <div className="row"><button className="btn">Save</button><button type="button" className="btn ghost" onClick={() => setEdit(null)}>Cancel</button></div>
        </form>
      )}
      <div className="row">
        <select value={subject} onChange={(e) => { setSubject(e.target.value); setLm(""); setVal(null); }} style={{ maxWidth: 220 }}><option value="">All subjects</option>{cat?.map((s) => <option key={s.code} value={s.code}>{s.name}</option>)}</select>
        <select value={lm} onChange={(e) => { setLm(e.target.value); setVal(null); }} style={{ maxWidth: 240 }} disabled={!subject}><option value="">All LMs</option>{cat?.find((s) => s.code === subject)?.lms.map((l) => <option key={l.id} value={l.id}>LM{l.lm_no} · {l.title}</option>)}</select>
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} style={{ maxWidth: 150 }}><option value="">Any difficulty</option><option value="E">Easy</option><option value="M">Medium</option><option value="H">Hard</option></select>
        <select value={status} onChange={(e) => setStatus(e.target.value)} style={{ maxWidth: 150 }}><option value="">Any status</option><option value="draft">Draft</option><option value="published">Published</option><option value="retired">Retired</option></select>
        <input type="search" placeholder="Search text" value={q} onChange={(e) => setQ(e.target.value)} style={{ maxWidth: 220 }} />
        {lm && <button className="btn sm ghost" onClick={() => api<Validation>(`/admin/questions/validate?lm_id=${lm}`).then(setVal)}>Run release checks</button>}
      </div>
      {val && (
        <div className={val.ok ? "ok" : "note"}>
          <b>{val.questions} questions · answers A {val.answer_distribution.A} / B {val.answer_distribution.B} / C {val.answer_distribution.C}.</b>
          {val.issues.length ? <ul style={{ margin: "6px 0 0" }}>{val.issues.map((i) => <li key={i}>{i}</li>)}</ul> : " All checks passed."}
        </div>
      )}
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <div className="small muted" style={{ marginBottom: 8 }}>{data.total} questions</div>
          <table className="data">
            <thead><tr><th>Question</th><th>Where</th><th>Level</th><th>Status</th><th /></tr></thead>
            <tbody>
              {data.items.map((x) => (
                <tr key={x.id}>
                  <td style={{ maxWidth: 480 }}><b>{x.stem}</b><div className="small muted">✓ {"ABC"[x.correct_index]}. {x.options[x.correct_index]}</div></td>
                  <td className="small">{subjById[x.subject_id]?.code.toUpperCase()}{x.lm_id && lmById[x.lm_id] ? ` LM${lmById[x.lm_id].lm_no}` : ""}</td>
                  <td className="small">{DIFFICULTY_LABEL[x.difficulty]}<div className="muted">{x.qtype}</div></td>
                  <td><StatusPill status={x.status} /><div className="small muted">v{x.version}</div></td>
                  <td className="small">
                    {can("qbank:write") && <button className="link-btn" onClick={() => open(x)}>Edit</button>}
                    {can("qbank:publish") && x.status !== "published" && <button className="link-btn" style={{ marginLeft: 8 }} onClick={() => setQStatus(x.id, "publish")}>Publish</button>}
                    {can("qbank:publish") && x.status === "published" && <button className="link-btn" style={{ marginLeft: 8 }} onClick={() => setQStatus(x.id, "retire")}>Retire</button>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
