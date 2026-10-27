"use client";

import Link from "next/link";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { date, examWindow, rupees } from "@/lib/format";
import type { Course } from "@/lib/types";

export default function Courses() {
  const { data, error, loading } = useApi<Course[]>("/courses");
  return (
    <section className="blk">
      <div className="wrap">
        <div className="eyebrow">Courses</div>
        <h1 className="h-lg" style={{ margin: "6px 0 22px" }}>
          Register for a <b>course</b>
        </h1>
        <ErrorBox error={error} />
        {loading && <Loading />}
        <div className="g3">
          {data?.map((c) => (
            <div className="card stack" key={c.code}>
              <div className="spread">
                <span className="pill">{c.subjects.length === 10 ? "Complete course" : `${c.subjects.length} subjects`}</span>
                {c.status !== "open" && <span className="pill b">Closed</span>}
              </div>
              <h3 style={{ fontSize: 20 }}>{c.title}</h3>
              <p className="muted" style={{ margin: 0 }}>{c.tagline}</p>
              <div>
                <div className="price">{rupees(c.fee_paise)}</div>
                <div className="small muted">
                  incl. GST ·{" "}
                  {c.access_ends_on ? `access until ${date(c.access_ends_on)}` : `${c.validity_days} days of access`}
                  {c.exam_window ? ` · ${examWindow(c.exam_window)} window` : ""}
                </div>
              </div>
              <div className="small">{c.subjects.map((s) => s.name).join(" · ")}</div>
              <Link className="btn" href={`/courses/${c.code}`}>
                View details
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
