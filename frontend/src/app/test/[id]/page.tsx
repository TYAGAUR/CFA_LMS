"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { use, useCallback, useEffect, useRef, useState } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Loading } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";
import { type Attempt, type AttemptItem, DIFFICULTY_LABEL } from "@/lib/types";

const L = "ABC";
const fmt = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

export default function TestRunner({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const user = useRequireUser();
  const router = useRouter();
  const toast = useToast();
  const [a, setA] = useState<Attempt | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [i, setI] = useState(0);
  const [left, setLeft] = useState<number | null>(null);
  const shownAt = useRef(Date.now());
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    try {
      const d = await api<Attempt>(`/attempts/${id}`);
      setA(d);
      setLeft(d.seconds_left);
      if (d.status === "in_progress" && d.items) {
        const firstOpen = d.items.findIndex((x) => x.answer_index === null);
        setI((cur) => (cur === 0 && firstOpen > 0 ? firstOpen : cur));
      }
    } catch (e) {
      setError(e);
    }
  }, [id]);

  useEffect(() => {
    if (user) void load();
  }, [user, load]);

  // Countdown; the server is the authority and auto-submits at the deadline (BR-TST-07).
  useEffect(() => {
    if (a?.status !== "in_progress" || left === null) return;
    if (left <= 0) {
      void load();
      return;
    }
    const t = setTimeout(() => setLeft((s) => (s === null ? s : s - 1)), 1000);
    return () => clearTimeout(t);
  }, [left, a?.status, load]);

  useEffect(() => {
    shownAt.current = Date.now();
  }, [i]);

  if (!user || (!a && !error)) return <Loading />;
  if (error || !a || !a.items) return <div className="wrap"><ErrorBox error={error} /></div>;
  const items = a.items;
  const it = items[i];
  const done = a.status === "submitted";
  const elapsed = () => Math.round((Date.now() - shownAt.current) / 1000);

  function patchItem(pos: number, upd: Partial<AttemptItem>) {
    setA((cur) => cur && { ...cur, items: cur.items!.map((x) => (x.position === pos ? { ...x, ...upd } : x)) });
  }

  async function choose(k: number) {
    if (done || (a!.mode === "practice" && it.answer_index !== null)) return;
    patchItem(it.position, { answer_index: k });
    try {
      const r = await api<AttemptItem>(`/attempts/${a!.id}/items/${it.position}`, { method: "PUT", body: { answer_index: k, time_spent_s: elapsed() } });
      shownAt.current = Date.now();
      patchItem(it.position, r);
    } catch (e) {
      toast(errorText(e));
      void load();
    }
  }

  async function flag() {
    const f = !it.flagged;
    patchItem(it.position, { flagged: f });
    await api(`/attempts/${a!.id}/items/${it.position}`, { method: "PUT", body: { flagged: f, time_spent_s: elapsed() } }).catch(() => {});
  }

  async function submit() {
    const open = items.filter((x) => x.answer_index === null).length;
    if (open && !confirm(`${open} question(s) are unanswered and will be marked wrong. Submit anyway?`)) return;
    setSubmitting(true);
    try {
      setA(await api<Attempt>(`/attempts/${a!.id}/submit`, { method: "POST" }));
      setI(0);
      scrollTo({ top: 0 });
    } catch (e) {
      toast(errorText(e));
    } finally {
      setSubmitting(false);
    }
  }

  if (done) {
    const pct = Math.round(a.score_pct ?? 0);
    const color = a.passed === null ? "var(--accent)" : a.passed ? "var(--good)" : "var(--bad)";
    return (
      <section className="blk">
        <div className="wrap stack" style={{ maxWidth: 860 }}>
          <div className="card" style={{ textAlign: "center" }}>
            <div className="eyebrow">{a.title}</div>
            <div className="bigring" style={{ background: `conic-gradient(${color} ${pct}%, var(--line) 0)`, marginTop: 14 }}>
              <div><span>{pct}%<small>{a.correct} of {a.total}</small></span></div>
            </div>
            <h2 className="h-md">
              {a.submit_reason === "timeout" ? "Time's up: your test was submitted." : a.passed === null ? "Test complete" : a.passed ? "Above the pass mark. Well done!" : `Below the ${a.pass_mark}% guide. Review and try again.`}
            </h2>
            <p className="small muted">Pass marks are a guide only. Nothing is locked, so revise the notes and retake with fresh questions whenever you like.</p>
            <div className="row" style={{ justifyContent: "center" }}>
              <Link className="btn" href="/practice">Build a custom quiz</Link>
              {a.lm_id && <button className="btn ghost" onClick={async () => { try { const n = await api<Attempt>(`/lms/${a.lm_id}/quiz`, { method: "POST" }); router.push(`/test/${n.id}`); } catch (e) { toast(errorText(e)); } }}>Retake chapter quiz</button>}
            </div>
          </div>
          <h3>Review</h3>
          {items.map((x, k) => (
            <div key={x.position} className={`rv ${x.is_correct ? "ok" : "no"}`}>
              <b>{k + 1}. {x.stem}</b> <span className="pill small">{DIFFICULTY_LABEL[x.difficulty]}</span>
              <div style={{ marginTop: 6 }}>
                {x.is_correct ? "Correct: " : `Your answer: ${x.answer_index === null ? "none" : `${L[x.answer_index]}. ${x.options[x.answer_index]}`} · Correct: `}
                {x.correct_index !== undefined && `${L[x.correct_index]}. ${x.options[x.correct_index]}`}
              </div>
              <div className="ex">{x.explanation}</div>
            </div>
          ))}
        </div>
      </section>
    );
  }

  const answered = items.filter((x) => x.answer_index !== null).length;
  const reveal = a.mode === "practice" && it.correct_index !== undefined;
  return (
    <section className="blk">
      <div className="wrap layout-test">
        <div className="card" style={{ padding: 0 }}>
          <div className="qhead">
            <div><b>{a.title}</b><div className="small" style={{ opacity: 0.8 }}>{a.mode === "practice" ? "Practice: the answer shows after each question" : "Assessment: results after you submit"}</div></div>
            <div className="row">
              {left !== null && <span className={`timer ${left < 60 ? "low" : ""}`} aria-label="Time left">⏱ {fmt(left)}</span>}
              <button className="btn sm ghost" style={{ color: "#fff", borderColor: "#fff" }} onClick={() => router.push("/practice")}>Save & exit</button>
            </div>
          </div>
          <div className="qprog"><b style={{ width: `${(answered / a.total) * 100}%` }} /></div>
          <div className="qbody">
            <div className="row" style={{ marginBottom: 10 }}>
              <span className="pill">Question {i + 1} of {a.total}</span>
              <span className={`pill ${it.difficulty === "E" ? "g" : it.difficulty === "H" ? "b" : "w"}`}>{DIFFICULTY_LABEL[it.difficulty]}</span>
              <button className="link-btn small" onClick={flag}>{it.flagged ? "★ Flagged" : "☆ Flag for review"}</button>
            </div>
            <h3>{it.stem}</h3>
            <div role="radiogroup" aria-label="Answer options">
              {it.options.map((o, k) => {
                const cls = reveal ? (k === it.correct_index ? "ok" : k === it.answer_index ? "no" : "") : "";
                return (
                  <button key={k} type="button" role="radio" aria-checked={it.answer_index === k} className={`opt ${cls}`}
                    disabled={reveal} onClick={() => choose(k)}>
                    <span className="l">{L[k]}</span><span>{o}</span>
                  </button>
                );
              })}
            </div>
            {reveal && <div className={it.is_correct ? "ok" : "err"}><b>{it.is_correct ? "Correct." : "Not quite."}</b> {it.explanation}</div>}
          </div>
          <div className="spread" style={{ padding: "0 24px 20px" }}>
            <button className="btn ghost" disabled={i === 0} onClick={() => setI(i - 1)}>Previous</button>
            {i < a.total - 1 ? <button className="btn" onClick={() => setI(i + 1)}>Next question</button> :
              <button className="btn good" disabled={submitting} onClick={submit}>Submit test</button>}
          </div>
        </div>
        <aside className="card stack">
          <div className="small muted">{answered} of {a.total} answered · saved automatically</div>
          <div className="qnav">
            {items.map((x, k) => {
              const st = a.mode === "practice" && x.is_correct !== undefined ? (x.is_correct ? "ok" : "no") : x.answer_index !== null ? "ans" : "";
              return <button key={x.position} className={`${st} ${k === i ? "cur" : ""} ${x.flagged ? "flag" : ""}`} onClick={() => setI(k)} aria-label={`Question ${k + 1}`}>{k + 1}</button>;
            })}
          </div>
          <button className="btn good" disabled={submitting} onClick={submit}>Submit test</button>
        </aside>
      </div>
    </section>
  );
}
