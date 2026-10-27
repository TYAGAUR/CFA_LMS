"use client";

import Link from "next/link";
import { use, useEffect } from "react";
import { ErrorBox, Loading, StatusPill, useApi } from "@/components/ui";
import { useAuth, useRequireUser } from "@/lib/auth";
import { dateTime, rupees } from "@/lib/format";
import type { Order } from "@/lib/types";

export default function CheckoutResult({ params }: { params: Promise<{ orderId: string }> }) {
  const { orderId } = use(params);
  const user = useRequireUser();
  const { reload: reloadMe } = useAuth();
  const { data: o, error, reload } = useApi<Order>(user ? `/payments/orders/${orderId}` : null);

  // The webhook may land a moment after the browser returns: poll briefly (BR-PAY-04).
  useEffect(() => {
    if (!o || o.status !== "created") return;
    const t = setTimeout(reload, 2500);
    return () => clearTimeout(t);
  }, [o, reload]);
  useEffect(() => {
    if (o?.status === "paid") void reloadMe();
  }, [o?.status, reloadMe]);

  if (!user || (!o && !error)) return <Loading />;
  if (error || !o) return <div className="wrap"><ErrorBox error={error} /></div>;
  const pay = o.payments.find((p) => p.status === "captured") ?? o.payments.at(-1);

  return (
    <div className="wrap">
      <div className="card receipt stack">
        {o.status === "paid" ? (
          <div className="ok"><b>Payment successful.</b> Your course is now active and every section is open.</div>
        ) : o.status === "created" ? (
          <div className="note">{pay?.status === "failed" ? `Your last payment attempt failed: ${pay.error_description ?? "declined"}. You have not been charged.` : "Waiting for the payment confirmation from the gateway…"}</div>
        ) : (
          <div className="err">This order is {o.status.replaceAll("_", " ")}. Contact support with the order number if you were charged.</div>
        )}
        <div className="spread">
          <div>
            <div className="eyebrow">Receipt</div>
            <h2 className="h-md">{o.description}</h2>
          </div>
          <StatusPill status={o.status} />
        </div>
        <dl className="kv">
          <dt>Order number</dt><dd>{o.number}</dd>
          <dt>Amount</dt><dd>{rupees(o.amount_paise)} (incl. GST)</dd>
          <dt>Ordered</dt><dd>{dateTime(o.created_at)}</dd>
          {o.paid_at && (<><dt>Paid</dt><dd>{dateTime(o.paid_at)}</dd></>)}
          {pay && (<><dt>Payment reference</dt><dd>{pay.provider_payment_id}{pay.method ? ` · ${pay.method.toUpperCase()}` : ""}</dd></>)}
          {o.offline_reference && (<><dt>Offline reference</dt><dd>{o.offline_reference}</dd></>)}
          <dt>Billed to</dt><dd>{user.full_name} · {user.mobile_e164}</dd>
          <dt>GSTIN</dt><dd className="muted">To be added (BR-PAY-10)</dd>
        </dl>
        <div className="row">
          {o.status === "paid" ? <Link className="btn" href="/dashboard">Start studying</Link> : <Link className="btn" href="/courses">Back to courses</Link>}
          <button className="btn ghost" onClick={() => window.print()}>Print receipt</button>
        </div>
      </div>
    </div>
  );
}
