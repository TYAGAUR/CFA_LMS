"use client";

import Link from "next/link";
import { useState } from "react";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { dateTime } from "@/lib/format";

type Rep = { course: string; subjects: { code: string; name: string }[]; rows: { student: string; student_code: string | null; user_id: string; last_active: string | null; subjects: Record<string, { learned: number; total: number }> }[] };

export default function Reports() {
  const { data: courses } = useApi<{ code: string; title: string }[]>("/courses");
  const [course, setCourse] = useState("");
  const { data, error, loading } = useApi<Rep>(course ? `/admin/reports/progress?course=${course}` : null);

  function csv() {
    if (!data) return;
    const head = ["Student", "Code", "Last active", ...data.subjects.map((s) => s.name)];
    const lines = data.rows.map((r) => [r.student, r.student_code ?? "", r.last_active ?? "", ...data.subjects.map((s) => `${r.subjects[s.code].learned}/${r.subjects[s.code].total}`)]);
    const text = [head, ...lines].map((l) => l.map((c) => `"${String(c).replaceAll('"', '""')}"`).join(",")).join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: "text/csv" }));
    a.download = `progress-${course}.csv`;
    a.click();
  }

  return (
    <>
      <h1 className="h-md">Progress report</h1>
      <div className="row">
        <select value={course} onChange={(e) => setCourse(e.target.value)} style={{ maxWidth: 360 }}>
          <option value="">Choose a course…</option>{courses?.map((c) => <option key={c.code} value={c.code}>{c.title}</option>)}
        </select>
        {data && <button className="btn sm ghost" onClick={csv}>Export CSV</button>}
      </div>
      <ErrorBox error={error} />
      {loading && <Loading />}
      {data && (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>Student</th><th>Last active</th>{data.subjects.map((s) => <th key={s.code}>{s.code.toUpperCase()}</th>)}</tr></thead>
            <tbody>
              {data.rows.map((r) => (
                <tr key={r.user_id}>
                  <td><Link href={`/admin/users/${r.user_id}`}>{r.student}</Link><div className="small muted">{r.student_code}</div></td>
                  <td className="small">{dateTime(r.last_active)}</td>
                  {data.subjects.map((s) => <td key={s.code} className="small">{r.subjects[s.code].learned}/{r.subjects[s.code].total}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
          {data.rows.length === 0 && <p className="muted">No active students in this course yet.</p>}
        </div>
      )}
    </>
  );
}
