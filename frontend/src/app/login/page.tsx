"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState, type FormEvent } from "react";
import { ErrorBox, Field } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

type Notice = { version: string; title: string; sections: { heading: string; text: string }[] };

function safeNext(n: string | null): string {
  return n && n.startsWith("/") && !n.startsWith("//") ? n : "/dashboard";
}

function LoginInner() {
  const params = useSearchParams();
  const next = safeNext(params.get("next"));
  const router = useRouter();
  const { reload } = useAuth();
  const [step, setStep] = useState<"mobile" | "otp" | "signup">("mobile");
  const [mobile, setMobile] = useState("");
  const [challenge, setChallenge] = useState<{ challenge_id: string; debug_code?: string } | null>(null);
  const [code, setCode] = useState("");
  const [signupToken, setSignupToken] = useState("");
  const [notice, setNotice] = useState<Notice | null>(null);
  const [form, setForm] = useState({ full_name: "", dob: "", email: "", city: "", accept: false, analytics: false, marketing: false });
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (step === "signup" && !notice) api<Notice>("/privacy/notice/current").then(setNotice).catch(setError);
  }, [step, notice]);

  async function run(fn: () => Promise<void>) {
    setBusy(true);
    setError(null);
    try {
      await fn();
    } catch (e) {
      setError(e);
    } finally {
      setBusy(false);
    }
  }

  const requestOtp = (e?: FormEvent) => {
    e?.preventDefault();
    return run(async () => {
      setChallenge(await api("/auth/otp/request", { body: { channel: "sms", destination: mobile } }));
      setCode("");
      setStep("otp");
    });
  };

  const verify = (e: FormEvent) => {
    e.preventDefault();
    return run(async () => {
      const r = await api<{ status: string; signup_token?: string }>("/auth/otp/verify", {
        body: { challenge_id: challenge!.challenge_id, code, channel: "sms", destination: mobile },
      });
      if (r.status === "signup_required") {
        setSignupToken(r.signup_token!);
        setStep("signup");
      } else {
        const me = await reload();
        router.replace(me?.status === "pending_guardian_consent" ? "/pending-consent" : next);
      }
    });
  };

  const signup = (e: FormEvent) => {
    e.preventDefault();
    return run(async () => {
      const u = await api<{ status: string }>("/auth/signup", {
        body: {
          signup_token: signupToken, full_name: form.full_name, dob: form.dob, email: form.email || null, city: form.city || null,
          accept_terms: form.accept, notice_version: notice?.version, product_analytics: form.analytics, marketing_messages: form.marketing,
        },
      });
      await reload();
      router.replace(u.status === "pending_guardian_consent" ? "/pending-consent" : next);
    });
  };

  return (
    <div className="wrap">
      <div className="card auth-card">
        <div className="eyebrow">Students</div>
        <h1 className="h-md" style={{ margin: "4px 0 6px" }}>
          {step === "signup" ? "Create your account" : "Sign in with your mobile"}
        </h1>
        <p className="muted small">No password needed. We send a 6-digit code by SMS.</p>
        <ErrorBox error={error} />

        {step === "mobile" && (
          <form onSubmit={requestOtp}>
            <Field label="Mobile number">
              <input type="tel" inputMode="numeric" autoComplete="tel-national" placeholder="98765 43210" value={mobile}
                onChange={(e) => setMobile(e.target.value)} required autoFocus />
            </Field>
            <button className="btn" style={{ width: "100%", marginTop: 16 }} disabled={busy}>
              Send code
            </button>
          </form>
        )}

        {step === "otp" && (
          <form onSubmit={verify}>
            <p className="small">Code sent to +91 {mobile.replace(/\D/g, "").slice(-10)}. <button type="button" className="link-btn" onClick={() => setStep("mobile")}>Change</button></p>
            {challenge?.debug_code && <div className="note">Local development: your code is <b>{challenge.debug_code}</b></div>}
            <Field label="6-digit code">
              <input className="otp" inputMode="numeric" autoComplete="one-time-code" maxLength={6} value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))} required autoFocus />
            </Field>
            <button className="btn" style={{ width: "100%", marginTop: 16 }} disabled={busy || code.length !== 6}>
              Verify
            </button>
            <button type="button" className="link-btn small" style={{ marginTop: 12 }} onClick={() => requestOtp()} disabled={busy}>
              Resend code
            </button>
          </form>
        )}

        {step === "signup" && (
          <form onSubmit={signup}>
            <Field label="Full name"><input type="text" autoComplete="name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required /></Field>
            <Field label="Date of birth" hint="Only used to check whether you are under 18. Under-18 students need a parent's consent.">
              <input type="date" value={form.dob} onChange={(e) => setForm({ ...form, dob: e.target.value })} required />
            </Field>
            <Field label="Email (optional)"><input type="email" autoComplete="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></Field>
            <Field label="City"><input type="text" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} /></Field>
            {notice && (
              <details className="card" style={{ marginTop: 14, padding: 12 }}>
                <summary style={{ cursor: "pointer", fontWeight: 600 }}>{notice.title} (please read)</summary>
                {notice.sections.map((s) => (
                  <p key={s.heading} className="small"><b>{s.heading}.</b> {s.text}</p>
                ))}
              </details>
            )}
            <label className="check"><input type="checkbox" checked={form.accept} onChange={(e) => setForm({ ...form, accept: e.target.checked })} required />
              <span>I have read the privacy notice and agree to the terms of use. <span className="muted">(required)</span></span></label>
            <label className="check"><input type="checkbox" checked={form.analytics} onChange={(e) => setForm({ ...form, analytics: e.target.checked })} />
              <span>Help improve the product with usage analytics. <span className="muted">(optional, adults only)</span></span></label>
            <label className="check"><input type="checkbox" checked={form.marketing} onChange={(e) => setForm({ ...form, marketing: e.target.checked })} />
              <span>Send me updates about new batches and events. <span className="muted">(optional)</span></span></label>
            <button className="btn" style={{ width: "100%", marginTop: 10 }} disabled={busy || !form.accept}>
              Create account
            </button>
          </form>
        )}
        <p className="small muted" style={{ marginTop: 18 }}>Faculty and staff: <Link href="/staff/login">staff sign-in</Link></p>
      </div>
    </div>
  );
}

export default function Login() {
  return (
    <Suspense>
      <LoginInner />
    </Suspense>
  );
}
