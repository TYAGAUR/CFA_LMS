"use client";

import { useEffect, useState, type FormEvent } from "react";
import { useToast } from "@/components/Providers";
import { ErrorBox, Field, Loading, StatusPill, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { useAuth, useRequireUser } from "@/lib/auth";
import { date, dateTime } from "@/lib/format";

type Consents = { is_minor: boolean; consents: Record<string, { granted: boolean; updated_at: string | null }> };
type Sess = { id: string; device_label: string | null; created_at: string; last_seen_at: string; current: boolean };
type Dr = { id: string; type: string; status: string; created_at: string; due_at: string; resolution_note: string | null };

const OPTIONAL = [
  ["product_analytics", "Usage analytics to improve the product", true],
  ["marketing_messages", "Updates about batches and events", false],
] as const;

export default function Profile() {
  const user = useRequireUser();
  const { reload } = useAuth();
  const toast = useToast();
  const { data: consents, reload: reloadConsents } = useApi<Consents>(user ? "/me/consents" : null);
  const { data: sessions, reload: reloadSessions } = useApi<Sess[]>(user ? "/me/sessions" : null);
  const { data: requests, reload: reloadRequests } = useApi<Dr[]>(user ? "/me/data-requests" : null);
  const [form, setForm] = useState({ full_name: "", email: "", city: "", qualification: "" });
  const [dr, setDr] = useState({ type: "access", note: "", nominee_name: "", nominee_contact: "" });
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    if (user) setForm({ full_name: user.full_name, email: user.email ?? "", city: user.city ?? "", qualification: user.qualification ?? "" });
  }, [user]);
  if (!user) return <Loading />;

  async function save(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await api("/me", { method: "PATCH", body: { ...form, email: form.email || null } });
      await reload();
      toast("Profile saved");
    } catch (err) {
      setError(err);
    }
  }

  async function setConsent(purpose: string, granted: boolean) {
    try {
      await api("/me/consents", { body: { purpose, granted } });
      reloadConsents();
      toast(granted ? "Consent given" : "Consent withdrawn");
    } catch (e) {
      toast(errorText(e));
    }
  }

  async function submitRequest(e: FormEvent) {
    e.preventDefault();
    try {
      await api("/me/data-requests", { body: { type: dr.type, note: dr.note || null, nominee_name: dr.nominee_name || null, nominee_contact: dr.nominee_contact || null } });
      toast("Request submitted");
      setDr({ type: "access", note: "", nominee_name: "", nominee_contact: "" });
      reloadRequests();
    } catch (err) {
      toast(errorText(err));
    }
  }

  async function download() {
    const data = await api("/me/data-export");
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `my-data-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
  }

  return (
    <section className="blk">
      <div className="wrap two">
        <div className="stack">
          <form className="card" onSubmit={save}>
            <h3>Profile</h3>
            <ErrorBox error={error} />
            <dl className="kv" style={{ marginTop: 10 }}>
              <dt>Mobile</dt><dd>{user.mobile_e164 ?? "—"}</dd>
              <dt>Student code</dt><dd>{user.student_code ?? "—"}</dd>
              <dt>Roles</dt><dd>{user.role_names.join(", ")}</dd>
            </dl>
            <Field label="Full name"><input type="text" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} /></Field>
            <Field label="Email"><input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></Field>
            <Field label="City"><input type="text" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} /></Field>
            <Field label="Qualification"><input type="text" value={form.qualification} onChange={(e) => setForm({ ...form, qualification: e.target.value })} /></Field>
            <button className="btn" style={{ marginTop: 14 }}>Save</button>
          </form>

          <div className="card">
            <h3>Signed-in devices</h3>
            <p className="small muted">Students can be signed in on up to 2 devices. Signing in on a third ends the oldest session.</p>
            {sessions?.map((s) => (
              <div className="spread" key={s.id} style={{ borderTop: "1px solid var(--line)", padding: "8px 0" }}>
                <div><b>{s.device_label}</b> {s.current && <span className="pill g">this device</span>}<div className="small muted">Last active {dateTime(s.last_seen_at)}</div></div>
                {!s.current && <button className="btn sm ghost" onClick={() => api(`/me/sessions/${s.id}`, { method: "DELETE" }).then(reloadSessions)}>Sign out</button>}
              </div>
            ))}
          </div>
        </div>

        <div className="stack">
          <div className="card">
            <h3>Privacy choices</h3>
            <p className="small muted">The service itself needs your account data. These extras are optional and you can change them any time.</p>
            {OPTIONAL.map(([purpose, label, adultsOnly]) => {
              const c = consents?.consents[purpose];
              const blocked = adultsOnly && consents?.is_minor;
              return (
                <label className="check" key={purpose}>
                  <input type="checkbox" checked={!!c?.granted} disabled={blocked || !consents} onChange={(e) => setConsent(purpose, e.target.checked)} />
                  <span>{label}{blocked ? " (not available under 18)" : ""}<br /><small className="muted">{c?.updated_at ? `Last changed ${dateTime(c.updated_at)}` : "Not given"}</small></span>
                </label>
              );
            })}
          </div>

          <form className="card" onSubmit={submitRequest}>
            <h3>Your data rights</h3>
            <p className="small muted">Download a copy of your data now, or send a request to our Grievance Officer.</p>
            <button type="button" className="btn sm ghost" onClick={download}>Download my data (JSON)</button>
            <Field label="Request type">
              <select value={dr.type} onChange={(e) => setDr({ ...dr, type: e.target.value })}>
                <option value="access">Summary of my data</option>
                <option value="correction">Correct my data</option>
                <option value="erasure">Delete my account and data</option>
                <option value="nomination">Nominate someone to act for me</option>
                <option value="grievance">Raise a grievance</option>
              </select>
            </Field>
            {dr.type === "nomination" ? (
              <>
                <Field label="Nominee name"><input type="text" value={dr.nominee_name} onChange={(e) => setDr({ ...dr, nominee_name: e.target.value })} required /></Field>
                <Field label="Nominee phone or email"><input type="text" value={dr.nominee_contact} onChange={(e) => setDr({ ...dr, nominee_contact: e.target.value })} required /></Field>
              </>
            ) : (
              <Field label="Details"><textarea value={dr.note} onChange={(e) => setDr({ ...dr, note: e.target.value })} /></Field>
            )}
            {dr.type === "erasure" && <div className="note">Deleting your account ends access to all courses. Payment records are kept as required by law, without your contact details.</div>}
            <button className="btn" style={{ marginTop: 12 }}>Submit request</button>
            {!!requests?.length && (
              <table className="data" style={{ marginTop: 14 }}>
                <thead><tr><th>Type</th><th>Status</th><th>Raised</th><th>Due</th></tr></thead>
                <tbody>{requests.map((r) => <tr key={r.id}><td>{r.type}</td><td><StatusPill status={r.status} /></td><td>{date(r.created_at)}</td><td>{date(r.due_at)}</td></tr>)}</tbody>
              </table>
            )}
          </form>
        </div>
      </div>
    </section>
  );
}
