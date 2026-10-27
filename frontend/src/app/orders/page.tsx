"use client";

import Link from "next/link";
import { ErrorBox, Loading, StatusPill, useApi } from "@/components/ui";
import { useRequireUser } from "@/lib/auth";
import { dateTime, rupees } from "@/lib/format";
import type { Order } from "@/lib/types";

export default function Orders() {
  const user = useRequireUser();
  const { data, error } = useApi<Order[]>(user ? "/me/orders" : null);
  if (!user || (!data && !error)) return <Loading />;
  return (
    <section className="blk">
      <div className="wrap" style={{ maxWidth: 900 }}>
        <h1 className="h-md" style={{ marginBottom: 14 }}>My orders and receipts</h1>
        <ErrorBox error={error} />
        {data?.length === 0 && <p className="muted">No orders yet. <Link href="/courses">Browse courses</Link></p>}
        {!!data?.length && (
          <div className="card table-wrap">
            <table className="data">
              <thead><tr><th>Order</th><th>Course</th><th>Amount</th><th>Status</th><th>Date</th><th /></tr></thead>
              <tbody>
                {data.map((o) => (
                  <tr key={o.id}>
                    <td>{o.number}</td>
                    <td>{o.description}</td>
                    <td>{rupees(o.amount_paise)}{o.refunded_paise ? <div className="small muted">refunded {rupees(o.refunded_paise)}</div> : null}</td>
                    <td><StatusPill status={o.status} /></td>
                    <td>{dateTime(o.paid_at ?? o.created_at)}</td>
                    <td><Link href={`/checkout/${o.id}`}>Receipt</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}
