"use client";

import { use, useState, type FormEvent } from "react";
import { ErrorBox, Field, Loading, useApi } from "@/components/ui";
import { api } from "@/lib/api";

type View = {
  student_first_name: string;
  guardian_name: string;
  relation: string;
  already_verified: boolean;
  notice: { title: string; sections: { heading: string; text: string }[] };
};

export default function GuardianConsent({ params }: { params: Promise<{ token: string }> }) {
  const { token } = use(params);
  const { data, error } = useApi<View>(`/guardian-consent/${token}`);
  const [challenge, setChallenge] = useState<{ challenge_id: string; debug_code?: string } | null>(null);
  const [code, setCode] = useState("");
  const [confirm, setConfirm] = useState(false);
  const [marketing, setMarketing] = useState(false);
  const [done, setDone] = useState(false);
  const [err, setErr] = useState<unknown>(null);

  if (!data && !error) return <Loading />;
  if (error || !data) return <div className="wrap"><ErrorBox error={error} /></div>;

  async function sendOtp() {
    setErr(null);
    try {
      setChallenge(await api(`/guardian-consent/${token}/otp`, { method: "POST" }));
    } catch (e) {
      setErr(e);
    }
  }

  async function submit(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      await api(`/guardian-consent/${token}`, { body: { challenge_id: challenge!.challenge_id, code, accept: true, marketing_messages: marketing } });
      setDone(true);
    } catch (e2) {
      setErr(e2);
    }
  }

  return (
    <div className="wrap">
      <div className="card auth-card stack" style={{ maxWidth: 620 }}>
        <div className="eyebrow">Parent / guardian consent</div>
        <h1 className="h-md">{data.student_first_name} has asked to join Karan Sir Classes</h1>
        {done || data.already_verified ? (
          <div className="ok">Thank you. Consent is recorded and {data.student_first_name}'s account is active. You can close this page.</div>
        ) : (
          <>
            <p className="small" style={{ margin: 0 }}>
              Hello {data.guardian_name}. Please read how we use {data.student_first_name}'s information. For students under 18,
              usage analytics and leaderboards are switched off.
            </p>
            <div className="card" style={{ background: "var(--bg)" }}>
              {data.notice.sections.map((s) => (
                <p key={s.heading} className="small"><b>{s.heading}.</b> {s.text}</p>
              ))}
            </div>
            <ErrorBox error={err} />
            {!challenge ? (
              <button className="btn" onClick={sendOtp}>Verify my mobile number</button>
            ) : (
              <form onSubmit={submit}>
                {challenge.debug_code && <div className="note">Local development: code <b>{challenge.debug_code}</b></div>}
                <Field label="Code sent to your mobile"><input className="otp" inputMode="numeric" maxLength={6} value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))} required /></Field>
                <label className="check"><input type="checkbox" checked={confirm} onChange={(e) => setConfirm(e.target.checked)} required />
                  <span>I am the parent or lawful guardian of {data.student_first_name} and I consent to the processing described above.</span></label>
                <label className="check"><input type="checkbox" checked={marketing} onChange={(e) => setMarketing(e.target.checked)} />
                  <span>Send updates about batches and events (optional).</span></label>
                <button className="btn" disabled={!confirm || code.length !== 6}>Give consent</button>
              </form>
            )}
          </>
        )}
      </div>
    </div>
  );
}
