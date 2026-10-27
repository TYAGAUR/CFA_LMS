"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, use } from "react";
import { NotesRenderer } from "@/components/NotesRenderer";
import { useToast } from "@/components/Providers";
import { FlashcardStudy } from "@/components/FlashcardStudy";
import { ResourceViewer } from "@/components/ResourceViewer";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";
import { duration, rupees } from "@/lib/format";
import type { Attempt, Block, LmDetail, SubjectDetail } from "@/lib/types";

type Tab = "notes" | "resources" | "quiz" | "flashcards" | "revision" | "los";

function LearnInner({ subject }: { subject: string }) {
  const user = useRequireUser();
  const router = useRouter();
  const params = useSearchParams();
  const toast = useToast();
  const { data: subjects } = useApi<{ code: string; name: string; entitled: boolean }[]>(user ? "/subjects" : null);
  const { data: subj, error, reload: reloadSubject } = useApi<SubjectDetail>(user ? `/subjects/${subject}` : null);
  const lmId = params.get("lm") ?? subj?.lms[0]?.id ?? null;
  const tab = (params.get("tab") as Tab) ?? "resources";
  const { data: lm, error: lmError, reload: reloadLm } = useApi<LmDetail>(user && subj?.entitled && lmId ? `/lms/${lmId}` : null);
  const itemId = params.get("item");
  const resId = params.get("res");

  function go(next: Record<string, string | null>) {
    const q = new URLSearchParams(params.toString());
    for (const [k, v] of Object.entries(next)) (v === null ? q.delete(k) : q.set(k, v));
    router.push(`/learn/${subject}?${q.toString()}`, { scroll: false });
  }

  if (!user || (!subj && !error)) return <Loading />;
  if (error || !subj) return <div className="wrap"><ErrorBox error={error} /></div>;

  const tabs = (
    <div className="subtabs">
      <div className="wrap">
        {subjects?.map((s) => (
          <Link key={s.code} href={`/learn/${s.code}`} className={s.code === subject ? "on" : ""}>
            {s.name}
            {!s.entitled && " 🔒"}
          </Link>
        ))}
      </div>
    </div>
  );

  if (!subj.entitled) {
    return (
      <>
        {tabs}
        <div className="wrap learn">
          <aside className="rail">
            {subj.lms.map((m) => (
              <div className="mod" key={m.id}><button type="button" disabled><span className="ic">{m.lm_no}</span>LM{m.lm_no} · {m.title}</button></div>
            ))}
          </aside>
          <article className="pane">
            <div className="pbody stack">
              <div className="eyebrow">{subj.name}</div>
              <h2 className="h-md">You haven't registered for this subject yet</h2>
              <p className="muted">Register for a course that includes {subj.name} and every LM opens immediately.</p>
              {subj.courses.map((c) => (
                <div className="spread card" key={c.code}>
                  <div><b>{c.title}</b><div className="small muted">{rupees(c.fee_paise)}</div></div>
                  <Link className="btn sm" href={`/courses/${c.code}`}>View course</Link>
                </div>
              ))}
            </div>
          </article>
        </div>
      </>
    );
  }

  const notes = lm?.content.filter((c) => c.kind === "note" || c.kind === "infographic") ?? [];
  const revision = lm?.content.filter((c) => c.kind === "revision_sheet") ?? [];
  const activeItem = itemId ?? (tab === "revision" ? revision[0]?.id : notes[0]?.id) ?? null;

  async function toggleLearned() {
    if (!lm) return;
    try {
      await api(`/lms/${lm.id}/learned`, { method: lm.progress.learned ? "DELETE" : "POST" });
      toast(lm.progress.learned ? "Marked as not learned" : "Marked as learned. Log a revision whenever you revisit it.");
      reloadLm();
      reloadSubject();
    } catch (e) {
      toast(errorText(e));
    }
  }

  async function logRevision() {
    if (!lm) return;
    try {
      const r = await api<{ counted: boolean; revision_count: number }>(`/lms/${lm.id}/revisions`, { body: { activity: tab === "revision" ? "revision_sheet" : "notes" } });
      toast(r.counted ? `Revision logged. ${r.revision_count} so far.` : "Already counted a revision today. Logged anyway.");
      reloadLm();
    } catch (e) {
      toast(errorText(e));
    }
  }

  return (
    <>
      {tabs}
      <div className="wrap learn">
        <aside className="rail" aria-label="Learning modules">
          <div className="spread" style={{ padding: "2px 4px 6px" }}>
            <b>{subj.name}</b>
            <small className="muted">{subj.lms.filter((m) => m.learned).length} of {subj.lms.length} learned</small>
          </div>
          {subj.lms.map((m) => {
            const open = m.id === lmId;
            return (
              <div key={m.id} className={`mod ${m.learned ? "done" : ""} ${open ? "cur" : ""}`}>
                <button type="button" aria-expanded={open} onClick={() => go({ lm: m.id, item: null, res: null, tab: "resources" })}>
                  <span className="ic">{m.learned ? "✓" : m.lm_no}</span>
                  <span>LM{m.lm_no} · {m.title}</span>
                  <span className="sc">{m.completion_pct ?? 0}%</span>
                </button>
                {open && lm && (
                  <ul>
                    {notes.map((c) => (
                      <li key={c.id}>
                        <button type="button" className={tab === "notes" && activeItem === c.id ? "on" : ""} onClick={() => go({ tab: "notes", item: c.id })}>
                          ▸ {c.title}
                        </button>
                      </li>
                    ))}
                    {lm.resources.map((r) => (
                      <li key={r.id}>
                        <button type="button" className={tab === "resources" && resId === r.id ? "on" : ""} onClick={() => go({ tab: "resources", res: r.id })}>
                          {r.kind === "video" ? "🎥" : r.kind === "link" ? "↗" : "📄"} {r.title}
                          {r.completed && <span className="tick">✓</span>}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            );
          })}
        </aside>

        <article className="pane">
          <ErrorBox error={lmError} />
          {!lm ? (
            <Loading />
          ) : (
            <>
              <div className="ph">
                <div className="crumb">{subj.name} › LM{lm.lm_no}</div>
                <h2>{lm.title}</h2>
                <div className="ptabs" role="tablist">
                  {([["resources", `Videos & resources (${lm.resources.length})`], ["flashcards", "Flashcards"], ["notes", `Notes (${notes.length})`], ["quiz", "Chapter quiz"], ["revision", "Revision sheet"], ["los", "LOS"]] as [Tab, string][]).map(([k, label]) => (
                    <button key={k} role="tab" aria-selected={tab === k} type="button" onClick={() => go({ tab: k, item: null })}>
                      {label}
                    </button>
                  ))}
                </div>
              </div>
              <div className="pbody">
                {tab === "notes" && (notes.length ? <ContentView id={activeItem!} /> : <Empty text="Notes for this LM are being prepared by the faculty." />)}
                {tab === "revision" && (revision.length ? <ContentView id={revision[0].id} /> : <Empty text="The revision sheet for this LM will appear here." />)}
                {tab === "resources" && <Resources lm={lm} resId={resId} onPick={(id) => go({ res: id })} onProgress={reloadLm} />}
                {tab === "flashcards" && <FlashcardStudy subject={subject} lmId={lm.id} compact />}
                {tab === "quiz" && <QuizPanel lm={lm} />}
                {tab === "los" && (lm.los.length ? (
                  <ul>{lm.los.map((l) => <li key={l.code}><b>{l.code}</b> ({l.command_word}) {l.statement}</li>)}</ul>
                ) : <Empty text="LOS statements for this LM have not been mapped yet." />)}
              </div>
              <div className="pbar">
                <div className="txt">
                  <b>{lm.progress.learned ? "You marked this LM as learned" : `${lm.progress.resources_done} of ${lm.progress.resources_total} mandatory resources done`}</b>
                  <small className="muted">Revisions logged: {lm.progress.revision_count}{lm.quiz.best_pct !== null ? ` · Best quiz score ${Math.round(lm.quiz.best_pct)}%` : ""}</small>
                </div>
                <button className="btn ghost sm" type="button" onClick={() => api(`/me/bookmarks`, { body: { target_type: "lm", target_id: lm.id } }).then(() => toast("Bookmarked")).catch((e) => toast(errorText(e)))}>☆ Bookmark</button>
                <button className="btn ghost sm" type="button" onClick={logRevision}>Log revision</button>
                <button className={`btn sm ${lm.progress.learned ? "ghost" : "good"}`} type="button" onClick={toggleLearned}>
                  {lm.progress.learned ? "Undo learned" : "Mark as learned"}
                </button>
                {lm.quiz.available && <button className="btn sm ghost" type="button" onClick={() => go({ tab: "quiz" })}>✎ Chapter quiz{lm.quiz.best_pct !== null ? ` · best ${Math.round(lm.quiz.best_pct)}%` : ""}</button>}
                {lm.next_lm_id && <button className="btn sm" type="button" onClick={() => go({ lm: lm.next_lm_id, item: null, res: null, tab: "resources" })}>Next LM →</button>}
              </div>
            </>
          )}
        </article>
      </div>
    </>
  );
}

function QuizPanel({ lm }: { lm: LmDetail }) {
  const router = useRouter();
  const toast = useToast();
  const q = lm.quiz;
  const { data: history } = useApi<Attempt[]>("/me/attempts?kind=chapter&limit=50");
  const mine = history?.filter((a) => a.lm_id === lm.id) ?? [];
  async function start() {
    try {
      const a = await api<Attempt>(`/lms/${lm.id}/quiz`, { method: "POST" });
      router.push(`/test/${a.id}`);
    } catch (e) {
      toast(errorText(e));
    }
  }
  if (!q.available) return <Empty text={q.questions ? `Only ${q.questions} question(s) so far. The chapter quiz opens once the faculty adds a few more.` : "Questions for this LM are being written by the faculty."} />;
  return (
    <div className="stack" style={{ maxWidth: 620 }}>
      <p style={{ margin: 0 }}>
        {q.size} questions drawn at random from {q.questions} in the LM{lm.lm_no} question bank. Timed at 90 seconds per question,
        with results and explanations after you submit. Each retake brings questions you haven&apos;t seen first.
      </p>
      <div className="row">
        <span className="pill">Guide pass mark {q.pass_mark}%</span>
        <span className="pill">{q.attempts} attempt(s)</span>
        {q.best_pct !== null && <span className={`pill ${q.best_pct >= q.pass_mark ? "g" : "w"}`}>Best {Math.round(q.best_pct)}%</span>}
      </div>
      <div><button className="btn" onClick={start}>{q.attempts ? "Retake with new questions" : "Start chapter quiz"}</button></div>
      <p className="small muted" style={{ margin: 0 }}>Nothing is locked: every LM stays open whatever your score.</p>
      {mine.length > 0 && (
        <table className="data">
          <thead><tr><th>When</th><th>Score</th><th /></tr></thead>
          <tbody>{mine.map((a) => <tr key={a.id}><td className="small">{new Date(a.submitted_at ?? a.started_at).toLocaleString("en-IN")}</td><td>{a.score_pct !== null ? `${Math.round(a.score_pct)}% (${a.correct}/${a.total})` : "in progress"}</td><td><Link href={`/test/${a.id}`}>{a.status === "submitted" ? "Review" : "Resume"}</Link></td></tr>)}</tbody>
        </table>
      )}
    </div>
  );
}

function Empty({ text }: { text: string }) {
  return <p className="muted" style={{ padding: "30px 0" }}>{text}</p>;
}

function ContentView({ id }: { id: string }) {
  const { data, error } = useApi<{ title: string; body: { blocks: Block[] } }>(`/content/${id}`);
  if (error) return <ErrorBox error={error} />;
  if (!data) return <Loading />;
  return (
    <>
      <h3 style={{ fontSize: 20, marginBottom: 8 }}>{data.title}</h3>
      <NotesRenderer blocks={data.body.blocks} />
    </>
  );
}

function Resources({ lm, resId, onPick, onProgress }: { lm: LmDetail; resId: string | null; onPick: (id: string) => void; onProgress: () => void }) {
  const current = resId ?? lm.resources[0]?.id;
  if (!lm.resources.length) return <Empty text="Class videos and PDFs for this LM will appear here once uploaded." />;
  return (
    <div className="vid">
      <div>{current && <ResourceViewer key={current} resourceId={current} onProgress={(done) => done && onProgress()} />}</div>
      <div className="reslist">
        {lm.resources.map((r, i) => (
          <button key={r.id} type="button" className={r.id === current ? "on" : ""} onClick={() => onPick(r.id)}>
            <span className={`n ${r.completed ? "done" : ""}`}>{r.completed ? "✓" : i + 1}</span>
            <span>
              <b>{r.title}</b>
              <small className="muted" style={{ display: "block" }}>
                {r.kind === "video" ? `Video ${duration(r.duration_s)}` : r.kind === "link" ? "External link" : "PDF"}
                {r.mandatory ? "" : " · optional"}
              </small>
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default function LearnSubject({ params }: { params: Promise<{ subject: string }> }) {
  const { subject } = use(params);
  return (
    <Suspense fallback={<Loading />}>
      <LearnInner subject={subject} />
    </Suspense>
  );
}
