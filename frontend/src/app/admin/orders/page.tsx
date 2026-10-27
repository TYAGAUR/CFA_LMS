"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { ErrorBox, Loading, StatusPill, useApi } from "@/components/ui";
import { dateTime, rupees } from "@/lib/format";

type O = { id: string; number: string; description: string; amount_paise: number; refunded_paise: number; status: string; provider: string; created_at: string; paid_at: string | null; student: string; user_id: string; student_code: string | null };

function OrdersInner() {
  const params = useSearchParams();
  const [q, setQ] = useState("");
  const [status, setStatus] = useState(params.get("status") ?? "");
  const { data, error } = useApi<O[]>(`/admin/orders?${new URLSearchParams({ ...(q ? { q } : {}), ...(status ? { status } : {}) })}`);
  const { data: rev } = useApi<{ by_status: { status: string; count: number; amount_paise: number; refunded_paise: number }[] }>("/admin/revenue");
  return (
    <>
      <h1 className="h-md">Payments & refunds</h1>
      {rev && (
        <div className="row">
          {rev.by_status.map((s) => (
            <div className="card" key={s.status} style={{ padding: "10px 14px" }}>
              <StatusPill status={s.status} /> <b>{s.count}</b> <span className="small muted">· {rupees(s.amount_paise)}</span>
            </div>
          ))}
        </div>
      )}
      <div className="row">
        <input type="search" placeholder="Order number, name, mobile" value={q} onChange={(e) => setQ(e.target.value)} style={{ maxWidth: 320 }} />
        <select value={status} onChange={(e) => setStatus(e.target.value)} style={{ maxWidth: 220 }}>
          <option value="">All statuses</option>
          {["created", "paid", "partially_refunded", "refunded", "amount_mismatch", "expired"].map((s) => <option key={s} value={s}>{s.replaceAll("_", " ")}</option>)}
        </select>
      </div>
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>Order</th><th>Student</th><th>Amount</th><th>Gateway</th><th>Status</th><th>Date</th></tr></thead>
            <tbody>
              {data.map((o) => (
                <tr key={o.id}>
                  <td><Link href={`/admin/orders/${o.id}`}>{o.number}</Link><div className="small muted">{o.description}</div></td>
                  <td><Link href={`/admin/users/${o.user_id}`}>{o.student}</Link><div className="small muted">{o.student_code}</div></td>
                  <td>{rupees(o.amount_paise)}{o.refunded_paise ? <div className="small muted">−{rupees(o.refunded_paise)}</div> : null}</td>
                  <td>{o.provider}</td>
                  <td><StatusPill status={o.status} /></td>
                  <td className="small">{dateTime(o.paid_at ?? o.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}

export default function AdminOrders() {
  return <Suspense><OrdersInner /></Suspense>;
}
