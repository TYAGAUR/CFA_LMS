"use client";

import Link from "next/link";
import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { dateTime } from "@/lib/format";

type R = { id: string; status: string; created_at: string; activated_at: string | null; course_code: string; course: string; user_id: string; student: string; student_code: string | null; mobile: string | null; form: Record<string, string>; order_id: string | null };

export default function AdminRegistrations() {
  const { user } = useAuth();
  const toast = useToast();
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const path = `/admin/registrations?${new URLSearchParams({ ...(q ? { q } : {}), ...(status ? { status } : {}) })}`;
  const { data, error, reload } = useApi<R[]>(path);
  const { data: courses } = useApi<{ code: string; title: string; fee_paise: number }[]>("/admin/courses");
  const [off, setOff] = useState({ mobile: "", course_code: "", reference: "", amount: "" });
  const [err, setErr] = useState<unknown>(null);

  async function offline(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      await api("/admin/registrations/offline", { body: { mobile: off.mobile, course_code: off.course_code, reference: off.reference, amount_paise: off.amount ? Math.round(Number(off.amount) * 100) : null } });
      toast("Offline payment recorded and access granted");
      setOff({ mobile: "", course_code: "", reference: "", amount: "" });
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  return (
    <>
      <h1 className="h-md">Registrations</h1>
      {user?.permissions.includes("order:offline") && (
        <details className="card">
          <summary style={{ cursor: "pointer", fontWeight: 700 }}>Record an offline payment (cash / bank transfer)</summary>
          <form onSubmit={offline}>
            <ErrorBox error={err} />
            <p className="small muted">The student must have signed up first. Access is granted immediately and the action is audit-logged.</p>
            <div className="two">
              <Field label="Student mobile"><input type="tel" value={off.mobile} onChange={(e) => setOff({ ...off, mobile: e.target.value })} required /></Field>
              <Field label="Course">
                <select value={off.course_code} onChange={(e) => setOff({ ...off, course_code: e.target.value })} required>
                  <option value="">Choose…</option>{courses?.map((c) => <option key={c.code} value={c.code}>{c.title}</option>)}
                </select>
              </Field>
              <Field label="Payment reference (UTR, receipt no.)"><input type="text" value={off.reference} onChange={(e) => setOff({ ...off, reference: e.target.value })} required /></Field>
              <Field label="Amount received in ₹ (blank = course fee)"><input type="number" step="0.01" value={off.amount} onChange={(e) => setOff({ ...off, amount: e.target.value })} /></Field>
            </div>
            <button className="btn" style={{ marginTop: 12 }}>Record payment</button>
          </form>
        </details>
      )}
      <div className="row">
        <input type="search" placeholder="Search name, mobile, code" value={q} onChange={(e) => setQ(e.target.value)} style={{ maxWidth: 320 }} />
        <select value={status} onChange={(e) => setStatus(e.target.value)} style={{ maxWidth: 220 }}>
          <option value="">All statuses</option><option value="active">Active</option><option value="pending_payment">Pending payment</option><option value="cancelled">Cancelled</option>
        </select>
      </div>
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>Student</th><th>Course</th><th>City / target</th><th>Status</th><th>Created</th><th /></tr></thead>
            <tbody>
              {data.map((r) => (
                <tr key={r.id}>
                  <td><Link href={`/admin/users/${r.user_id}`}>{r.student}</Link><div className="small muted">{r.student_code} · {r.mobile}</div></td>
                  <td>{r.course}</td>
                  <td className="small">{r.form.city ?? "—"} · {r.form.target_exam ?? "—"}</td>
                  <td><StatusPill status={r.status} /></td>
                  <td className="small">{dateTime(r.created_at)}</td>
                  <td>
                    {r.order_id && <Link className="small" href={`/admin/orders/${r.order_id}`}>Order</Link>}
                    {r.status === "active" && user?.permissions.includes("order:refund") && (
                      <button className="link-btn small" style={{ marginLeft: 10 }} onClick={async () => {
                        const reason = prompt("Reason for cancelling access (no refund is issued from here):");
                        if (!reason) return;
                        await api(`/admin/registrations/${r.id}/cancel`, { body: { reason } });
                        reload();
                      }}>Cancel access</button>
                    )}
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
