"use client";

import Link from "next/link";
import { useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { date } from "@/lib/format";

type U = { id: string; full_name: string; mobile_e164: string | null; email: string | null; student_code: string | null; status: string; is_minor: boolean; roles: string[]; created_at: string; last_login_at: string | null };

export default function AdminUsers() {
  const { user } = useAuth();
  const toast = useToast();
  const [q, setQ] = useState("");
  const [role, setRole] = useState("");
  const { data, error, reload } = useApi<{ total: number; items: U[] }>(`/admin/users?${new URLSearchParams({ ...(q ? { q } : {}), ...(role ? { role } : {}) })}`);
  const [staff, setStaff] = useState({ full_name: "", email: "", role: "author", temporary_password: "" });
  const [err, setErr] = useState<unknown>(null);

  async function create(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      await api("/admin/users", { body: { full_name: staff.full_name, email: staff.email, roles: [staff.role], temporary_password: staff.temporary_password } });
      toast("Staff account created");
      setStaff({ full_name: "", email: "", role: "author", temporary_password: "" });
      reload();
    } catch (e2) {
      setErr(e2);
    }
  }

  return (
    <>
      <h1 className="h-md">Users & staff</h1>
      {user?.permissions.includes("user:write") && (
        <details className="card">
          <summary style={{ cursor: "pointer", fontWeight: 700 }}>Add a staff member</summary>
          <form onSubmit={create}>
            <ErrorBox error={err} />
            <div className="two">
              <Field label="Full name"><input type="text" value={staff.full_name} onChange={(e) => setStaff({ ...staff, full_name: e.target.value })} required /></Field>
              <Field label="Email"><input type="email" value={staff.email} onChange={(e) => setStaff({ ...staff, email: e.target.value })} required /></Field>
              <Field label="Role">
                <select value={staff.role} onChange={(e) => setStaff({ ...staff, role: e.target.value })}>
                  <option value="author">Instructor / author</option><option value="reviewer">Academic reviewer</option>
                  {user.permissions.includes("role:assign_admin") && <><option value="admin">Administrator</option><option value="super_admin">Super administrator</option></>}
                </select>
              </Field>
              <Field label="Temporary password (min 12 characters)"><input type="text" value={staff.temporary_password} onChange={(e) => setStaff({ ...staff, temporary_password: e.target.value })} minLength={12} required /></Field>
            </div>
            <button className="btn" style={{ marginTop: 12 }}>Create</button>
          </form>
        </details>
      )}
      <div className="row">
        <input type="search" placeholder="Name, mobile, email or student code" value={q} onChange={(e) => setQ(e.target.value)} style={{ maxWidth: 340 }} />
        <select value={role} onChange={(e) => setRole(e.target.value)} style={{ maxWidth: 200 }}>
          <option value="">All roles</option>{["student", "author", "reviewer", "admin", "super_admin"].map((r) => <option key={r} value={r}>{r}</option>)}
        </select>
        {data && <span className="muted small">{data.total} users</span>}
      </div>
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>Name</th><th>Contact</th><th>Roles</th><th>Status</th><th>Joined</th></tr></thead>
            <tbody>
              {data.items.map((u) => (
                <tr key={u.id}>
                  <td><Link href={`/admin/users/${u.id}`}>{u.full_name}</Link><div className="small muted">{u.student_code}{u.is_minor ? " · under 18" : ""}</div></td>
                  <td className="small">{u.mobile_e164 ?? ""}<div>{u.email}</div></td>
                  <td className="small">{u.roles.join(", ")}</td>
                  <td><StatusPill status={u.status} /></td>
                  <td className="small">{date(u.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
