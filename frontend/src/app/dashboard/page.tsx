"use client";

import Link from "next/link";
import { ErrorBox, Loading, Meter, Ring, useApi } from "@/components/ui";
import { useRequireUser } from "@/lib/auth";
import { dateTime, examWindow } from "@/lib/format";

type Dash = {
  user: { full_name: string; student_code: string | null; target_exam: string | null };
  next_action: { type: string; title: string; subtitle?: string; completion_pct?: number; href: string };
  subjects: { code: string; name: string; icon: string; lm_count: number; learned_count: number; completion_pct: number }[];
  pending: { title: string; reason: string; href: string }[];
  recent: { title: string; at: string; href: string }[];
};

export default function Dashboard() {
  const user = useRequireUser();
  const { data, error } = useApi<Dash>(user && !user.is_staff ? "/me/dashboard" : null);
  const { data: regs } = useApi<{ id: string; status: string; access_until: string | null; course: { code: string; title: string } }[]>(
    user && !user.is_staff ? "/me/registrations" : null);

  if (!user) return <Loading />;
  if (user.is_staff) {
    return (
      <div className="wrap card auth-card">
        <p>You are signed in as staff.</p>
        <Link className="btn" href="/admin">Open the staff console</Link>
      </div>
    );
  }
  if (error) return <div className="wrap"><ErrorBox error={error} /></div>;
  if (!data) return <Loading />;
  const na = data.next_action;
  const pending = regs?.filter((r) => r.status === "pending_payment") ?? [];

  return (
    <>
      <div className="hero">
        <div className="wrap">
          <div>
            <div className="eyebrow" style={{ color: "var(--cy)" }}>
              Welcome back{data.user.target_exam ? ` · targeting ${examWindow(data.user.target_exam)}` : ""}
            </div>
            <h1 style={{ marginTop: 10 }}>
              Hello, <b>{data.user.full_name.split(" ")[0]}</b>.
            </h1>
            <p>Every section of your registered subjects is open. Pick up where you left off, or jump to any LM.</p>
          </div>
          <div className="cont">
            <div className="top">
              <div className="eyebrow">{na.type === "register" ? "Get started" : na.type === "revise" ? "Revision time" : "Continue where you left off"}</div>
              <h3 style={{ fontSize: 20, margin: "6px 0 10px" }}>{na.title}</h3>
              {na.completion_pct !== undefined && <Meter pct={na.completion_pct} label="LM progress" />}
              {na.subtitle && <p className="small muted" style={{ margin: "8px 0 0" }}>{na.subtitle}</p>}
              <Link className="btn" style={{ marginTop: 14 }} href={na.href}>
                {na.type === "register" ? "Browse courses" : na.type === "mark_learned" ? "Review and mark learned" : "Continue"}
              </Link>
            </div>
          </div>
        </div>
      </div>

      <section className="blk">
        <div className="wrap stack">
          {pending.map((r) => (
            <div className="note" key={r.id}>
              Your registration for <b>{r.course.title}</b> is waiting for payment. <Link href={`/register/${r.course.code}`}>Complete payment</Link>
            </div>
          ))}
          {data.subjects.length > 0 && (
            <>
              <div>
                <div className="eyebrow">Your subjects</div>
                <h2 className="h-md" style={{ margin: "4px 0 12px" }}>Progress by subject</h2>
              </div>
              <div className="g3">
                {data.subjects.map((s) => (
                  <Link key={s.code} className="card subj" href={`/learn/${s.code}`}>
                    <Ring pct={s.completion_pct} />
                    <div>
                      <b>{s.icon} {s.name}</b>
                      <small>{s.learned_count} of {s.lm_count} LMs learned</small>
                    </div>
                  </Link>
                ))}
              </div>
            </>
          )}
          <div className="g3">
            <Link className="card subj" href="/practice"><div className="ring" style={{ background: "var(--soft)" }}><span>✎</span></div><div><b>Custom Quiz</b><small>Pick subjects, chapters and difficulty</small></div></Link>
            <Link className="card subj" href="/flashcards"><div className="ring" style={{ background: "var(--soft)" }}><span>⟲</span></div><div><b>Flashcards</b><small>Spaced repetition: review what&apos;s due today</small></div></Link>
            <Link className="card subj" href="/learn"><div className="ring" style={{ background: "var(--soft)" }}><span>▤</span></div><div><b>Chapter quizzes</b><small>On every LM, under the Chapter quiz tab</small></div></Link>
          </div>
          <div className="two">
            <div className="card">
              <h3>Pending</h3>
              {data.pending.length === 0 ? (
                <p className="muted small">Nothing pending. Take the chapter quiz after you mark an LM as learned.</p>
              ) : (
                <ul className="small" style={{ paddingLeft: 18 }}>
                  {data.pending.map((p) => (
                    <li key={p.href}><Link href={p.href}>{p.title}</Link> · <span className="muted">{p.reason}</span></li>
                  ))}
                </ul>
              )}
            </div>
            <div className="card">
              <h3>Recently opened</h3>
              {data.recent.length === 0 ? <p className="muted small">Open any LM to get started.</p> : (
                <ul className="small" style={{ paddingLeft: 18 }}>
                  {data.recent.map((r) => (
                    <li key={r.href + r.at}><Link href={r.href}>{r.title}</Link> <span className="muted">· {dateTime(r.at)}</span></li>
                  ))}
                </ul>
              )}
              {regs && regs.filter((r) => r.status === "active").map((r) => (
                <p key={r.id} className="small muted" style={{ marginBottom: 0 }}>{r.course.title}: access until {dateTime(r.access_until)}</p>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
