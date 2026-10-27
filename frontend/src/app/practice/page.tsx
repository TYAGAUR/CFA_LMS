"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Loading, StatusPill, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";
import { dateTime } from "@/lib/format";
import type { Attempt } from "@/lib/types";

type Opt = { code: string; name: string; icon: string; entitled: boolean; questions: number; lms: { id: string; lm_no: number; title: string; questions: number }[] };
type Preview = { available: number; by_difficulty: Record<"E" | "M" | "H", number>; numerical: number };
type Stats = { answered: number; by_subject: { code: string; name: string; answered: number; accuracy_pct: number | null }[]; by_difficulty: { difficulty: string; answered: number; accuracy_pct: number | null }[] };

const DIFF = [["all", "Mixed"], ["E", "Easy"], ["M", "Medium"], ["H", "Hard"]] as const;
const QTYPE = [["all", "All types"], ["conceptual", "Conceptual"], ["numerical", "Numerical"]] as const;

export default function Practice() {
  const user = useRequireUser();
  const router = useRouter();
  const toast = useToast();
  const { data: opts, error } = useApi<Opt[]>(user ? "/practice/options" : null);
  const { data: history } = useApi<Attempt[]>(user ? "/me/attempts?limit=15" : null);
  const { data: stats } = useApi<Stats>(user ? "/me/test-stats" : null);
  const entitled = useMemo(() => opts?.filter((o) => o.entitled && o.questions > 0) ?? [], [opts]);
  const [subjects, setSubjects] = useState<string[]>([]);
  const [lmIds, setLmIds] = useState<string[]>([]);
  const [difficulty, setDifficulty] = useState<"all" | "E" | "M" | "H">("all");
  const [qtype, setQtype] = useState<"all" | "conceptual" | "numerical">("all");
  const [count, setCount] = useState(10);
  const [mode, setMode] = useState<"practice" | "assessment">("practice");
  const [timed, setTimed] = useState(false);
  const [preview, setPreview] = useState<Preview | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (entitled.length && !subjects.length) setSubjects([entitled[0].code]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entitled]);

  useEffect(() => {
    if (!subjects.length) return setPreview(null);
    const t = setTimeout(() => {
      api<Preview>("/tests/preview", { body: { subject_codes: subjects, lm_ids: lmIds, difficulty, qtype } }).then(setPreview).catch(() => setPreview(null));
    }, 200);
    return () => clearTimeout(t);
  }, [subjects, lmIds, difficulty, qtype]);

  if (!user || (!opts && !error)) return <Loading />;
  if (error) return <div className="wrap"><ErrorBox error={error} /></div>;

  const lmChoices = entitled.filter((s) => subjects.includes(s.code)).flatMap((s) => s.lms.filter((l) => l.questions > 0).map((l) => ({ ...l, subject: s.code })));
  const available = preview?.available ?? 0;
  const n = Math.min(count, available);

  async function start() {
    setBusy(true);
    try {
      const a = await api<Attempt & { served: number; requested: number }>("/tests", {
        body: { subject_codes: subjects, lm_ids: lmIds, difficulty, qtype, count: n, mode, timed },
      });
      router.push(`/test/${a.id}`);
    } catch (e) {
      toast(errorText(e));
      setBusy(false);
    }
  }

  async function subjectTest(code: string) {
    try {
      const a = await api<Attempt>(`/subjects/${code}/test`, { method: "POST" });
      router.push(`/test/${a.id}`);
    } catch (e) {
      toast(errorText(e));
    }
  }

  const toggle = <T,>(list: T[], v: T) => (list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);

  return (
    <section className="blk">
      <div className="wrap stack">
        <div>
          <div className="eyebrow">Custom Quiz</div>
          <h1 className="h-lg" style={{ margin: "6px 0 4px" }}>Build your <b>own quiz</b></h1>
          <p className="muted" style={{ margin: 0 }}>Pick subjects, chapters and difficulty. Questions you haven't seen come first, then ones you got wrong.</p>
        </div>

        {entitled.length === 0 ? (
          <div className="note">Register for a course to unlock practice questions. <Link href="/courses">View courses</Link></div>
        ) : (
          <div className="two">
            <div className="card">
              <label className="f" style={{ marginTop: 0 }}>1 · Subjects</label>
              <div className="chipgrid">
                {entitled.map((s) => (
                  <button key={s.code} type="button" className="chip" aria-pressed={subjects.includes(s.code)}
                    onClick={() => { setSubjects(toggle(subjects, s.code)); setLmIds([]); }}>
                    {s.icon} {s.name} <span className="small">({s.questions})</span>
                  </button>
                ))}
              </div>
              <label className="f">2 · Chapters (optional; none selected = all)</label>
              <div className="chipgrid">
                {lmChoices.map((l) => (
                  <button key={l.id} type="button" className="chip" aria-pressed={lmIds.includes(l.id)} onClick={() => setLmIds(toggle(lmIds, l.id))} title={l.title}>
                    {l.subject.toUpperCase()} LM{l.lm_no} <span className="small">({l.questions})</span>
                  </button>
                ))}
                {lmChoices.length === 0 && <span className="small muted">Select a subject first.</span>}
              </div>
              <label className="f">3 · Difficulty</label>
              <div className="seg">
                {DIFF.map(([k, label]) => (
                  <button key={k} type="button" aria-pressed={difficulty === k} onClick={() => setDifficulty(k)}>
                    {label}{k !== "all" && preview ? ` (${preview.by_difficulty[k]})` : ""}
                  </button>
                ))}
              </div>
              <label className="f">4 · Question type</label>
              <div className="seg">
                {QTYPE.map(([k, label]) => <button key={k} type="button" aria-pressed={qtype === k} onClick={() => setQtype(k)}>{label}</button>)}
              </div>
              <label className="f" htmlFor="cnt">5 · Number of questions: {count}</label>
              <input id="cnt" type="range" min={1} max={100} value={count} onChange={(e) => setCount(Number(e.target.value))} />
              <label className="f">6 · Mode</label>
              <div className="seg">
                <button type="button" aria-pressed={mode === "practice"} onClick={() => setMode("practice")}>Practice (answer shown after each question)</button>
                <button type="button" aria-pressed={mode === "assessment"} onClick={() => setMode("assessment")}>Assessment (results at the end)</button>
              </div>
              <label className="check" style={{ marginTop: 14 }}>
                <input type="checkbox" checked={timed} onChange={(e) => setTimed(e.target.checked)} />
                <span>Timed: 90 seconds per question, like the real exam. The test submits itself when time runs out.</span>
              </label>
            </div>
            <aside className="sumry stack">
              <div className="eyebrow" style={{ color: "var(--cy)" }}>Your quiz</div>
              <div><span className="n">{n}</span> <span>questions</span></div>
              <ul className="small" style={{ margin: 0, paddingLeft: 18 }}>
                <li>{available} matching questions available</li>
                {count > available && available > 0 && <li>Only {available} match these choices, so the test will have {available}.</li>}
                <li>{DIFF.find(([k]) => k === difficulty)?.[1]} difficulty · {mode === "practice" ? "practice mode" : "assessment mode"}</li>
                <li>{timed ? `Time limit ${Math.ceil((n * 90) / 60)} min` : "Untimed (resume within 7 days)"}</li>
              </ul>
              <button className="btn" disabled={busy || !subjects.length || available === 0} onClick={start} style={{ background: "var(--cy)", borderColor: "var(--cy)", color: "#08143a" }}>
                {busy ? "Preparing…" : "Start quiz"}
              </button>
              {available === 0 && subjects.length > 0 && <div className="small">No questions match. Try Mixed difficulty or more subjects.</div>}
            </aside>
          </div>
        )}

        {entitled.length > 0 && (
          <div className="card">
            <h3>Subject tests</h3>
            <p className="small muted">Up to 50 timed questions across a whole subject. The pass mark of 75% is a guide only.</p>
            <div className="row">
              {entitled.map((s) => <button key={s.code} className="btn sm ghost" onClick={() => subjectTest(s.code)}>{s.icon} {s.name}</button>)}
            </div>
          </div>
        )}

        <div className="two">
          <div className="card table-wrap">
            <h3>Recent tests</h3>
            {!history?.length ? <p className="small muted">No tests yet.</p> : (
              <table className="data">
                <thead><tr><th>Test</th><th>Score</th><th>Status</th><th>When</th></tr></thead>
                <tbody>
                  {history.map((a) => (
                    <tr key={a.id}>
                      <td><Link href={`/test/${a.id}`}>{a.title}</Link><div className="small muted">{a.mode}{a.timed ? " · timed" : ""}</div></td>
                      <td>{a.score_pct !== null ? `${Math.round(a.score_pct)}% (${a.correct}/${a.total})` : `${a.total} Qs`}</td>
                      <td><StatusPill status={a.status === "in_progress" ? "in_progress" : a.passed === false ? "below pass mark" : "completed"} /></td>
                      <td className="small">{dateTime(a.submitted_at ?? a.started_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          <div className="card">
            <h3>Accuracy</h3>
            {!stats?.answered ? <p className="small muted">Your accuracy by subject and difficulty appears after your first submitted test.</p> : (
              <>
                <p className="small muted">{stats.answered} questions answered. Weakest subjects first.</p>
                {stats.by_subject.map((s) => (
                  <div key={s.code} style={{ marginBottom: 8 }}>
                    <div className="spread small"><span>{s.name}</span><b>{s.accuracy_pct}%</b></div>
                    <div className="meter"><b style={{ width: `${s.accuracy_pct ?? 0}%`, background: (s.accuracy_pct ?? 0) < 60 ? "var(--bad)" : undefined }} /></div>
                  </div>
                ))}
                <div className="row small" style={{ marginTop: 10 }}>
                  {stats.by_difficulty.filter((d) => d.answered).map((d) => <span key={d.difficulty} className="pill">{{ E: "Easy", M: "Medium", H: "Hard" }[d.difficulty]}: {d.accuracy_pct}%</span>)}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
