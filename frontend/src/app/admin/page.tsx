"use client";

import Link from "next/link";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { useAuth } from "@/lib/auth";
import { rupees } from "@/lib/format";

type Overview = {
  students: number; active_registrations: number; pending_payments: number; revenue_this_month_paise: number;
  active_students_7d: number; orders_needing_review: number; open_data_requests: number;
};

export default function AdminHome() {
  const { user } = useAuth();
  const canReport = user?.permissions.includes("report:read");
  const { data, error } = useApi<Overview>(canReport ? "/admin/overview" : null);
  if (!canReport) {
    return (
      <div className="card">
        <h3>Welcome, {user?.full_name}</h3>
        <p>Use <Link href="/admin/catalog">Catalogue & content</Link> to add notes, videos and PDFs to Learning Modules.</p>
      </div>
    );
  }
  if (error) return <ErrorBox error={error} />;
  if (!data) return <Loading />;
  const stats: [string, string | number, string?][] = [
    ["Students", data.students],
    ["Active registrations", data.active_registrations],
    ["Awaiting payment", data.pending_payments],
    ["Revenue this month (net)", rupees(data.revenue_this_month_paise)],
    ["Active students (7 days)", data.active_students_7d],
    ["Orders needing review", data.orders_needing_review, "/admin/orders?status=amount_mismatch"],
    ["Open data requests", data.open_data_requests, "/admin/data-requests"],
  ];
  return (
    <>
      <h1 className="h-md">Overview</h1>
      <div className="g3">
        {stats.map(([label, v, href]) => (
          <div className="card" key={label}>
            <div className="small muted">{label}</div>
            <div className="stat">{v}</div>
            {href && Number(v) > 0 && <Link className="small" href={href}>Review →</Link>}
          </div>
        ))}
      </div>
    </>
  );
}
