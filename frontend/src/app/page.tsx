"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Loading, useApi } from "@/components/ui";
import { useAuth } from "@/lib/auth";
import { examWindow, rupees } from "@/lib/format";
import type { Course } from "@/lib/types";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const { data: courses } = useApi<Course[]>("/courses");
  const { data: subjects } = useApi<{ code: string; name: string; icon: string; lm_count: number; exam_weight: string | null }[]>("/subjects");

  useEffect(() => {
    if (!loading && user) router.replace(user.is_staff ? "/admin" : "/dashboard");
  }, [user, loading, router]);

  if (loading || user) return <Loading />;
  const featured = courses?.find((c) => c.status === "open");

  return (
    <>
      <div className="hero">
        <div className="wrap">
          <div>
            <div className="eyebrow" style={{ color: "var(--cy)" }}>CFA® Level I · 10 subjects</div>
            <h1 style={{ marginTop: 10 }}>
              Learn a chapter.
              <br />
              Revise it often.
              <br />
              <b>Walk in ready.</b>
            </h1>
            <p style={{ marginTop: 16 }}>
              Structured study for the CFA Level I exam with Karan Singh, CFA. Class videos, notes, revision sheets and progress
              tracking in one place. Register for a course, pay securely online, and start studying straight away.
            </p>
            <div className="row" style={{ marginTop: 22 }}>
              <Link className="btn" href="/courses">
                View courses
              </Link>
              <Link className="btn ghost" href="/login">
                I already registered
              </Link>
            </div>
          </div>
          {featured && (
            <div className="cont">
              <div className="top">
                <div className="eyebrow">Now enrolling</div>
                <h3 style={{ fontSize: 22, margin: "6px 0 8px" }}>{featured.title}</h3>
                <p className="muted" style={{ margin: 0 }}>{featured.tagline}</p>
                <div className="price" style={{ marginTop: 12 }}>{rupees(featured.fee_paise)}</div>
                <div className="small muted">incl. GST{featured.exam_window ? ` · for the ${examWindow(featured.exam_window)} window` : ""}</div>
                <Link className="btn" style={{ marginTop: 14 }} href={`/courses/${featured.code}`}>
                  See what's included
                </Link>
              </div>
              <div className="facts">
                <div>All sections open from day one, no chapter locks</div>
                <div>Track videos, notes, EOC practice and revisions</div>
                <div>Pay by UPI, card or net banking through Razorpay</div>
              </div>
            </div>
          )}
        </div>
      </div>

      <section className="blk">
        <div className="wrap">
          <div className="eyebrow">The syllabus</div>
          <h2 className="h-md" style={{ margin: "4px 0 16px" }}>Ten subjects, one Learning Module at a time</h2>
          <div className="g3">
            {subjects?.map((s) => (
              <div className="card subj" key={s.code}>
                <div className="ring" style={{ background: "var(--soft)" }} aria-hidden>
                  <span style={{ fontSize: 20 }}>{s.icon}</span>
                </div>
                <div>
                  <b>{s.name}</b>
                  <small>
                    {s.lm_count} LMs{s.exam_weight ? ` · ${s.exam_weight} of the exam` : ""}
                  </small>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
