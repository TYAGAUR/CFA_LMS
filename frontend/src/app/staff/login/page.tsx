"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState, type FormEvent } from "react";
import { ErrorBox, Field } from "@/components/ui";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

function StaffLoginInner() {
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next")?.startsWith("/") ? params.get("next")! : "/admin";
  const { reload } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mfa, setMfa] = useState<{ token: string; setup: boolean } | null>(null);
  const [secret, setSecret] = useState<{ secret: string; otpauth_uri: string } | null>(null);
  const [code, setCode] = useState("");
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);

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

  const login = (e: FormEvent) => {
    e.preventDefault();
    return run(async () => {
      const r = await api<{ status: string; mfa_token: string | null }>("/auth/staff/login", { body: { email, password } });
      if (r.status === "signed_in") {
        await reload();
        router.replace(next);
      } else {
        setMfa({ token: r.mfa_token!, setup: r.status === "mfa_setup_required" });
        if (r.status === "mfa_setup_required") setSecret(await api("/auth/staff/mfa/setup", { body: { mfa_token: r.mfa_token } }));
      }
    });
  };

  const verify = (e: FormEvent) => {
    e.preventDefault();
    return run(async () => {
      await api("/auth/staff/mfa", { body: { mfa_token: mfa!.token, code } });
      await reload();
      router.replace(next);
    });
  };

  return (
    <div className="wrap">
      <div className="card auth-card">
        <div className="eyebrow">Faculty and staff</div>
        <h1 className="h-md" style={{ margin: "4px 0 12px" }}>Staff sign-in</h1>
        <ErrorBox error={error} />
        {!mfa ? (
          <form onSubmit={login}>
            <Field label="Email"><input type="text" autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} required autoFocus /></Field>
            <Field label="Password"><input type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} required /></Field>
            <button className="btn" style={{ width: "100%", marginTop: 16 }} disabled={busy}>Sign in</button>
          </form>
        ) : (
          <form onSubmit={verify}>
            {secret && (
              <div className="note">
                Set up two-step verification: add this key to Google Authenticator, Microsoft Authenticator or similar, then
                enter the 6-digit code. <br />
                <code style={{ wordBreak: "break-all" }}>{secret.secret}</code>
              </div>
            )}
            <Field label="Authenticator code"><input className="otp" inputMode="numeric" maxLength={6} value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))} autoFocus required /></Field>
            <button className="btn" style={{ width: "100%", marginTop: 16 }} disabled={busy || code.length !== 6}>Verify</button>
          </form>
        )}
      </div>
    </div>
  );
}

export default function StaffLogin() {
  return (
    <Suspense>
      <StaffLoginInner />
    </Suspense>
  );
}
