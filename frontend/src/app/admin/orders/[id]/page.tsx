"use client";

import Link from "next/link";
import { use, useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { dateTime, rupees } from "@/lib/format";

type D = {
  id: string; number: string; description: string; purpose: string; amount_paise: number; refunded_paise: number; status: string;
  provider: string; provider_order_id: string | null; offline_reference: string | null; created_at: string; paid_at: string | null;
  student: { id: string; name: string; code: string | null; mobile: string | null };
  payments: { id: string; provider_payment_id: string; status: string; amount_paise: number; method: string | null; error: string | null; captured_at: string | null; created_at: string }[];
  refunds: { id: string; amount_paise: number; status: string; reason: string; provider_refund_id: string | null; created_at: string }[];
};

export default function AdminOrder({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { user } = useAuth();
  const toast = useToast();
  const { data: o, error, reload } = useApi<D>(`/admin/orders/${id}`);
  const [rf, setRf] = useState({ amount: "", reason: "" });
  const [err, setErr] = useState<unknown>(null);
  if (error) return <ErrorBox error={error} />;
  if (!o) return <Loading />;
  const refundable = ["paid", "partially_refunded"].includes(o.status) && user?.permissions.includes("order:refund");

  async function refund(e: FormEvent) {
    e.preventDefault();
    if (!o) return;
    const amount = rf.amount ? Math.round(Number(rf.amount) * 100) : null;
    const full = !amount || amount >= o.amount_paise - o.refunded_paise;
    if (!confirm(`Refund ${rupees(amount ?? o.amount_paise - o.refunded_paise)}? ${full ? "This is a full refund and ends the student's access." : "Partial refund: access continues."}`)) return;
    setErr(null);
    try {
      await api(`/admin/orders/${o.id}/refund`, { body: { amount_paise: amount, reason: rf.reason } });
      toast("Refund recorded");
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  return (
    <>
      <div className="spread">
        <h1 className="h-md">Order {o.number}</h1>
        <StatusPill status={o.status} />
      </div>
      {o.status === "amount_mismatch" && <div className="err">The captured amount does not match the order. No access was granted. Check the payment in the gateway dashboard and refund or record it manually.</div>}
      <div className="card">
        <dl className="kv">
          <dt>Description</dt><dd>{o.description}</dd>
          <dt>Student</dt><dd><Link href={`/admin/users/${o.student.id}`}>{o.student.name}</Link> · {o.student.code} · {o.student.mobile}</dd>
          <dt>Amount</dt><dd>{rupees(o.amount_paise)}{o.refunded_paise ? ` (refunded ${rupees(o.refunded_paise)})` : ""}</dd>
          <dt>Gateway</dt><dd>{o.provider}{o.provider_order_id ? ` · ${o.provider_order_id}` : ""}</dd>
          {o.offline_reference && (<><dt>Offline reference</dt><dd>{o.offline_reference}</dd></>)}
          <dt>Created</dt><dd>{dateTime(o.created_at)}</dd>
          <dt>Paid</dt><dd>{dateTime(o.paid_at)}</dd>
        </dl>
      </div>
      <div className="card table-wrap">
        <h3>Payment attempts</h3>
        <table className="data">
          <thead><tr><th>Payment id</th><th>Status</th><th>Method</th><th>Amount</th><th>When</th></tr></thead>
          <tbody>{o.payments.map((p) => <tr key={p.id}><td>{p.provider_payment_id}</td><td><StatusPill status={p.status} />{p.error && <div className="small muted">{p.error}</div>}</td><td>{p.method}</td><td>{rupees(p.amount_paise)}</td><td className="small">{dateTime(p.captured_at ?? p.created_at)}</td></tr>)}</tbody>
        </table>
      </div>
      {o.refunds.length > 0 && (
        <div className="card table-wrap">
          <h3>Refunds</h3>
          <table className="data">
            <thead><tr><th>Amount</th><th>Status</th><th>Reason</th><th>Gateway ref</th><th>When</th></tr></thead>
            <tbody>{o.refunds.map((r) => <tr key={r.id}><td>{rupees(r.amount_paise)}</td><td><StatusPill status={r.status} /></td><td>{r.reason}</td><td>{r.provider_refund_id}</td><td className="small">{dateTime(r.created_at)}</td></tr>)}</tbody>
          </table>
        </div>
      )}
      {refundable && (
        <form className="card" onSubmit={refund}>
          <h3>Issue a refund</h3>
          <ErrorBox error={err} />
          <div className="two">
            <Field label={`Amount in ₹ (blank = full ${rupees(o.amount_paise - o.refunded_paise)})`}><input type="number" step="0.01" min="0.01" value={rf.amount} onChange={(e) => setRf({ ...rf, amount: e.target.value })} /></Field>
            <Field label="Reason (recorded in the audit log)"><input type="text" value={rf.reason} onChange={(e) => setRf({ ...rf, reason: e.target.value })} required minLength={3} /></Field>
          </div>
          <button className="btn bad" style={{ marginTop: 12 }}>Refund</button>
        </form>
      )}
    </>
  );
}
