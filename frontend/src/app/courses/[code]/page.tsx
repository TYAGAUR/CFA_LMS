"use client";

import Link from "next/link";
import { use } from "react";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { useAuth } from "@/lib/auth";
import { date, examWindow, rupees } from "@/lib/format";
import type { Course } from "@/lib/types";

export default function CoursePage({ params }: { params: Promise<{ code: string }> }) {
  const { code } = use(params);
  const { user } = useAuth();
  const { data: c, error, loading } = useApi<Course>(`/courses/${code}`, [user?.id]);
  if (loading) return <Loading />;
  if (error || !c) return <div className="wrap"><ErrorBox error={error} /></div>;
  const reg = c.my_registration;
  const active = reg?.status === "active";

  return (
    <section className="blk">
      <div className="wrap two">
        <div className="stack">
          <div>
            <div className="eyebrow">Course</div>
            <h1 className="h-lg" style={{ margin: "6px 0 10px" }}>{c.title}</h1>
            <p className="muted" style={{ fontSize: 17, margin: 0 }}>{c.tagline}</p>
          </div>
          {c.description && <p>{c.description}</p>}
          <div className="card">
            <h3>What's included</h3>
            <p className="small muted">Every Learning Module below opens as soon as your payment is confirmed. There are no chapter locks.</p>
            {c.subjects.map((s) => (
              <details key={s.code} style={{ borderTop: "1px solid var(--line)", padding: "10px 0" }}>
                <summary style={{ cursor: "pointer", fontWeight: 600 }}>
                  {s.icon} {s.name} <span className="muted small">· {s.lms?.length ?? s.lm_count} LMs</span>
                </summary>
                <ol style={{ margin: "8px 0 0", paddingLeft: 22 }} className="small">
                  {s.lms?.map((lm) => <li key={lm.lm_no}>{lm.title}</li>)}
                </ol>
              </details>
            ))}
          </div>
        </div>
        <aside className="card stack" style={{ position: "sticky", top: 80 }}>
          <div className="price">{rupees(c.fee_paise)}</div>
          <div className="small muted">Fee including GST</div>
          <dl className="kv">
            <dt>Access</dt>
            <dd>{c.access_ends_on ? `Until ${date(c.access_ends_on)}` : `${c.validity_days} days from payment`}</dd>
            {c.exam_window && (<><dt>Exam window</dt><dd>{examWindow(c.exam_window)}</dd></>)}
            <dt>Subjects</dt>
            <dd>{c.subjects.length}</dd>
            {c.seats_left !== null && (<><dt>Seats left</dt><dd>{c.seats_left}</dd></>)}
          </dl>
          {active ? (
            <>
              <div className="ok">You are registered for this course.</div>
              <Link className="btn" href="/dashboard">Go to my dashboard</Link>
            </>
          ) : c.status !== "open" ? (
            <div className="note">Registrations for this course are closed.</div>
          ) : (
            <Link className="btn" href={user ? `/register/${c.code}` : `/login?next=${encodeURIComponent(`/register/${c.code}`)}`}>
              {reg?.status === "pending_payment" ? "Complete payment" : "Register and pay"}
            </Link>
          )}
          <p className="small muted" style={{ margin: 0 }}>
            Secure payment via Razorpay: UPI, cards, net banking and wallets. We never see your card or bank details.
          </p>
        </aside>
      </div>
    </section>
  );
}
