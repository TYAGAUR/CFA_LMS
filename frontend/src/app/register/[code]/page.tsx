"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { use, useEffect, useState, type FormEvent } from "react";
import { ErrorBox, Field, Loading, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";
import { rupees } from "@/lib/format";
import type { Course } from "@/lib/types";

type Checkout = {
  registration_id: string;
  order_id: string;
  order_number: string;
  amount_paise: number;
  provider: string;
  checkout: { mode: "redirect"; url: string } | { mode: "razorpay_checkout"; script: string; options: Record<string, unknown> };
};

declare global {
  interface Window {
    Razorpay?: new (opts: Record<string, unknown>) => { open: () => void; on: (ev: string, cb: (r: unknown) => void) => void };
  }
}

function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) return resolve();
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error("Could not load the payment window. Check your connection and try again."));
    document.body.appendChild(s);
  });
}

function nextExamWindows(): { value: string; label: string }[] {
  const out = [];
  const now = new Date();
  for (const y of [now.getFullYear(), now.getFullYear() + 1, now.getFullYear() + 2]) {
    for (const m of [2, 5, 8, 11]) {
      const d = new Date(y, m - 1, 1);
      if (d > now) out.push({ value: `${y}-${String(m).padStart(2, "0")}`, label: d.toLocaleDateString("en-IN", { month: "long", year: "numeric" }) });
    }
  }
  return out.slice(0, 6);
}

export default function Register({ params }: { params: Promise<{ code: string }> }) {
  const { code } = use(params);
  const user = useRequireUser();
  const router = useRouter();
  const { data: course, error: loadError } = useApi<Course>(user ? `/courses/${code}` : null);
  const [form, setForm] = useState({ full_name: "", email: "", city: "", qualification: "", target_exam: "", accept: false });
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (user) setForm((f) => ({ ...f, full_name: user.full_name, email: user.email ?? "", city: user.city ?? "", qualification: user.qualification ?? "", target_exam: user.target_exam ?? course?.exam_window ?? "" }));
  }, [user, course?.exam_window]);

  if (!user || (!course && !loadError)) return <Loading />;
  if (loadError || !course) return <div className="wrap"><ErrorBox error={loadError} /></div>;
  if (course.my_registration?.status === "active") {
    return (
      <div className="wrap auth-card card">
        <div className="ok">You are already registered for {course.title}.</div>
        <Link className="btn" href="/dashboard">Go to dashboard</Link>
      </div>
    );
  }

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const r = await api<Checkout>(`/courses/${code}/register`, {
        body: { full_name: form.full_name, email: form.email || null, city: form.city, qualification: form.qualification, target_exam: form.target_exam, accept_course_terms: form.accept },
      });
      if (r.checkout.mode === "redirect") {
        router.push(r.checkout.url);
        return;
      }
      await loadScript(r.checkout.script);
      const opts = r.checkout.options;
      const rzp = new window.Razorpay!({
        ...opts,
        handler: async (resp: Record<string, string>) => {
          try {
            await api(`/payments/orders/${r.order_id}/confirm`, { body: { payload: resp } });
          } finally {
            router.push(`/checkout/${r.order_id}`);
          }
        },
        modal: { ondismiss: () => setBusy(false) },
      });
      rzp.on("payment.failed", () => router.push(`/checkout/${r.order_id}`));
      rzp.open();
    } catch (err) {
      setError(err);
      setBusy(false);
    }
  }

  return (
    <section className="blk">
      <div className="wrap two">
        <form className="card" onSubmit={submit}>
          <div className="eyebrow">Step 1 of 2 · Your details</div>
          <h1 className="h-md" style={{ margin: "4px 0 6px" }}>Register for {course.title}</h1>
          <ErrorBox error={error} />
          <Field label="Full name (as it should appear on receipts)"><input type="text" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required /></Field>
          <Field label="Email for receipts"><input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></Field>
          <Field label="City"><input type="text" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} required /></Field>
          <Field label="Highest qualification"><input type="text" placeholder="e.g. B.Com, final year" value={form.qualification} onChange={(e) => setForm({ ...form, qualification: e.target.value })} required /></Field>
          <Field label="Target exam window">
            <select value={form.target_exam} onChange={(e) => setForm({ ...form, target_exam: e.target.value })} required>
              <option value="">Choose…</option>
              {nextExamWindows().map((w) => <option key={w.value} value={w.value}>{w.label}</option>)}
            </select>
          </Field>
          <label className="check"><input type="checkbox" checked={form.accept} onChange={(e) => setForm({ ...form, accept: e.target.checked })} required />
            <span>I agree to the course terms: the account is for my use only, content must not be shared or recorded, and refunds follow the institute's refund policy.</span></label>
          <button className="btn" style={{ width: "100%", marginTop: 8 }} disabled={busy || !form.accept}>
            {busy ? "Opening secure payment…" : `Continue to pay ${rupees(course.fee_paise)}`}
          </button>
        </form>
        <aside className="card stack">
          <div className="eyebrow">Order summary</div>
          <h3>{course.title}</h3>
          <div className="small muted">{course.subjects.map((s) => s.name).join(" · ")}</div>
          <div className="spread"><span>Course fee (incl. GST)</span><b>{rupees(course.fee_paise)}</b></div>
          <div className="spread" style={{ borderTop: "1px solid var(--line)", paddingTop: 10 }}><b>Total</b><span className="price" style={{ fontSize: 24 }}>{rupees(course.fee_paise)}</span></div>
          <p className="small muted" style={{ margin: 0 }}>Step 2: pay on the Razorpay secure page (UPI, cards, net banking, wallets). Access opens as soon as the payment is confirmed.</p>
        </aside>
      </div>
    </section>
  );
}
