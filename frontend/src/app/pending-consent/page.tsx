"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState, type FormEvent } from "react";
import { ErrorBox, Field, Loading, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function PendingConsent() {
  const { user, loading, reload } = useAuth();
  const router = useRouter();
  const { data: guardian, reload: reloadGuardian } = useApi<{ full_name: string; mobile: string; verified_at: string | null } | null>(
    user ? "/me/guardian" : null);
  const [form, setForm] = useState({ full_name: "", mobile: "", relation: "parent" });
  const [sent, setSent] = useState<{ guardian_mobile: string; debug_link?: string } | null>(null);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
    if (user && user.status === "active") router.replace("/dashboard");
  }, [user, loading, router]);

  useEffect(() => {
    if (!sent) return;
    const t = setInterval(async () => {
      const me = await reload();
      if (me?.status === "active") router.replace("/courses");
    }, 4000);
    return () => clearInterval(t);
  }, [sent, reload, router]);

  if (!user) return <Loading />;

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      setSent(await api("/me/guardian", { body: form }));
      reloadGuardian();
    } catch (err) {
      setError(err);
    }
  }

  return (
    <div className="wrap">
      <div className="card auth-card stack">
        <div className="eyebrow">One more step</div>
        <h1 className="h-md">A parent or guardian needs to approve your account</h1>
        <p className="muted small" style={{ margin: 0 }}>
          Because you are under 18, Indian data protection law requires consent from a parent or legal guardian before we can
          set up your learning account. We will send them a link by SMS.
        </p>
        <ErrorBox error={error} />
        {sent || guardian ? (
          <>
            <div className="ok">Consent request sent to {sent?.guardian_mobile ?? guardian?.mobile}. This page updates once they approve.</div>
            {sent?.debug_link && <div className="note">Local development: open the guardian link <a href={sent.debug_link}>here</a> (in a private window to act as the parent).</div>}
            <button className="link-btn small" onClick={() => setSent(null)}>Send to a different number</button>
          </>
        ) : null}
        {!sent && (
          <form onSubmit={submit}>
            <Field label="Parent or guardian's full name"><input type="text" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required /></Field>
            <Field label="Their mobile number"><input type="tel" value={form.mobile} onChange={(e) => setForm({ ...form, mobile: e.target.value })} required /></Field>
            <Field label="Relationship">
              <select value={form.relation} onChange={(e) => setForm({ ...form, relation: e.target.value })}>
                <option value="parent">Parent</option>
                <option value="legal_guardian">Legal guardian</option>
              </select>
            </Field>
            <button className="btn" style={{ width: "100%", marginTop: 14 }}>Send consent request</button>
          </form>
        )}
      </div>
    </div>
  );
}
