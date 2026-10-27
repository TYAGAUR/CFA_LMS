"use client";

import Link from "next/link";
import { use, useState } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Loading, StatusPill, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { date, dateTime, rupees } from "@/lib/format";

type D = {
  id: string; full_name: string; mobile_e164: string | null; email: string | null; student_code: string | null; status: string; is_minor: boolean;
  roles: string[]; city: string | null; qualification: string | null; target_exam: string | null; dob: string | null; created_at: string; last_login_at: string | null; active_sessions: number;
  registrations: { id: string; status: string; course: string; created_at: string; activated_at: string | null }[];
  orders: { id: string; number: string; amount_paise: number; status: string; provider: string; created_at: string }[];
  entitlements: { id: string; subject: string; source: string; starts_at: string; ends_at: string; revoked_at: string | null }[];
};

const ALL_ROLES = ["student", "author", "reviewer", "admin", "super_admin"];

export default function AdminUser({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { user: me } = useAuth();
  const toast = useToast();
  const { data: u, error, reload } = useApi<D>(`/admin/users/${id}`);
  const [roles, setRoles] = useState<string[] | null>(null);
  if (error) return <ErrorBox error={error} />;
  if (!u) return <Loading />;
  const can = (p: string) => me?.permissions.includes(p);

  async function act(fn: () => Promise<unknown>, msg: string) {
    try {
      await fn();
      toast(msg);
      reload();
    } catch (e) {
      toast(errorText(e));
    }
  }

  const r = roles ?? u.roles;
  return (
    <>
      <div className="spread">
        <h1 className="h-md">{u.full_name}</h1>
        <StatusPill status={u.status} />
      </div>
      <div className="two">
        <div className="card">
          <dl className="kv">
            <dt>Student code</dt><dd>{u.student_code ?? "—"}</dd>
            <dt>Mobile</dt><dd>{u.mobile_e164 ?? "—"}</dd>
            <dt>Email</dt><dd>{u.email ?? "—"}</dd>
            <dt>Age group</dt><dd>{u.is_minor ? "Under 18 (guardian consent)" : "Adult"}</dd>
            <dt>City / qualification</dt><dd>{u.city ?? "—"} · {u.qualification ?? "—"}</dd>
            <dt>Target exam</dt><dd>{u.target_exam ?? "—"}</dd>
            <dt>Joined / last login</dt><dd>{date(u.created_at)} · {dateTime(u.last_login_at)}</dd>
            <dt>Active sessions</dt><dd>{u.active_sessions}</dd>
          </dl>
          <div className="row" style={{ marginTop: 14 }}>
            {can("session:revoke") && <button className="btn sm ghost" onClick={() => act(() => api(`/admin/users/${u.id}/sessions`, { method: "DELETE" }), "Sessions revoked")}>Sign out everywhere</button>}
            {can("user:write") && u.status === "active" && (
              <button className="btn sm bad" onClick={() => { const reason = prompt("Reason for deactivating:"); if (reason) void act(() => api(`/admin/users/${u.id}/deactivate`, { body: { reason } }), "Deactivated"); }}>Deactivate</button>
            )}
            {can("user:write") && u.status === "deactivated" && (
              <button className="btn sm" onClick={() => { const reason = prompt("Reason for reactivating:"); if (reason) void act(() => api(`/admin/users/${u.id}/reactivate`, { body: { reason } }), "Reactivated"); }}>Reactivate</button>
            )}
          </div>
        </div>
        {can("user:write") && (
          <div className="card">
            <h3>Roles</h3>
            {ALL_ROLES.map((role) => (
              <label className="check" key={role}>
                <input type="checkbox" checked={r.includes(role)} disabled={(role === "admin" || role === "super_admin") && !can("role:assign_admin")}
                  onChange={(e) => setRoles(e.target.checked ? [...r, role] : r.filter((x) => x !== role))} />
                <span>{role}</span>
              </label>
            ))}
            <button className="btn sm" disabled={!roles} onClick={() => act(() => api(`/admin/users/${u.id}/roles`, { method: "PUT", body: { roles: r } }).then(() => setRoles(null)), "Roles updated")}>Save roles</button>
          </div>
        )}
      </div>
      <div className="card table-wrap">
        <h3>Registrations</h3>
        <table className="data"><thead><tr><th>Course</th><th>Status</th><th>Created</th><th>Activated</th></tr></thead>
          <tbody>{u.registrations.map((x) => <tr key={x.id}><td>{x.course}</td><td><StatusPill status={x.status} /></td><td>{dateTime(x.created_at)}</td><td>{dateTime(x.activated_at)}</td></tr>)}</tbody></table>
      </div>
      <div className="card table-wrap">
        <h3>Orders</h3>
        <table className="data"><thead><tr><th>Order</th><th>Amount</th><th>Status</th><th>Gateway</th><th>Date</th></tr></thead>
          <tbody>{u.orders.map((o) => <tr key={o.id}><td><Link href={`/admin/orders/${o.id}`}>{o.number}</Link></td><td>{rupees(o.amount_paise)}</td><td><StatusPill status={o.status} /></td><td>{o.provider}</td><td>{dateTime(o.created_at)}</td></tr>)}</tbody></table>
      </div>
      <div className="card table-wrap">
        <h3>Subject access</h3>
        <table className="data"><thead><tr><th>Subject</th><th>Source</th><th>From</th><th>Until</th><th /></tr></thead>
          <tbody>{u.entitlements.map((e) => (
            <tr key={e.id}><td>{e.subject}</td><td>{e.source}</td><td>{date(e.starts_at)}</td><td>{e.revoked_at ? <span className="pill b">revoked</span> : date(e.ends_at)}</td>
              <td>{!e.revoked_at && can("entitlement:grant") && <button className="link-btn small" onClick={() => { const reason = prompt("Reason for revoking:"); if (reason) void act(() => api(`/admin/entitlements/${e.id}/revoke`, { body: { reason } }), "Access revoked"); }}>Revoke</button>}</td></tr>
          ))}</tbody></table>
      </div>
    </>
  );
}
