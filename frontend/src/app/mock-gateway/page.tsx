"use client";

// Local-only stand-in for the Razorpay hosted checkout (PAYMENT_PROVIDER=mock).
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";
import { rupees } from "@/lib/format";

function MockGatewayInner() {
  const user = useRequireUser();
  const params = useSearchParams();
  const router = useRouter();
  const providerOrderId = params.get("order_id") ?? "";
  const { data, error } = useApi<{ order_id: string; number: string; description: string; amount_paise: number; status: string }>(
    user && providerOrderId ? `/payments/mock/orders/${providerOrderId}` : null,
  );
  const [busy, setBusy] = useState(false);
  const [failMsg, setFailMsg] = useState<string | null>(null);
  const [err, setErr] = useState<unknown>(null);

  async function pay(outcome: "success" | "failure") {
    setBusy(true);
    setErr(null);
    try {
      const r = await api<{ order_id: string; checkout_payload: Record<string, string> | null; error: string | null }>(
        "/payments/mock/complete", { body: { provider_order_id: providerOrderId, outcome } });
      if (r.checkout_payload) {
        await api(`/payments/orders/${r.order_id}/confirm`, { body: { payload: r.checkout_payload } });
        router.replace(`/checkout/${r.order_id}`);
      } else {
        setFailMsg(r.error ?? "Payment failed");
      }
    } catch (e) {
      setErr(e);
    } finally {
      setBusy(false);
    }
  }

  if (!user) return <Loading />;
  return (
    <div className="wrap">
      <div className="card auth-card stack">
        <div className="mock-banner">TEST GATEWAY · no real money moves (local development)</div>
        <ErrorBox error={error ?? err} />
        {data && (
          <>
            <div>
              <div className="eyebrow">Pay Karan Sir Classes</div>
              <h2 className="h-md">{data.description}</h2>
              <div className="small muted">Order {data.number}</div>
            </div>
            <div className="price">{rupees(data.amount_paise)}</div>
            {data.status === "paid" ? (
              <button className="btn" onClick={() => router.replace(`/checkout/${data.order_id}`)}>This order is already paid. View receipt</button>
            ) : (
              <>
                {failMsg && <div className="err">{failMsg}. You can try again.</div>}
                <button className="btn good" disabled={busy} onClick={() => pay("success")}>Pay with test UPI (success)</button>
                <button className="btn ghost" disabled={busy} onClick={() => pay("failure")}>Simulate a declined payment</button>
                <button className="link-btn small" onClick={() => router.back()}>Cancel and go back</button>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default function MockGateway() {
  return (
    <Suspense>
      <MockGatewayInner />
    </Suspense>
  );
}
