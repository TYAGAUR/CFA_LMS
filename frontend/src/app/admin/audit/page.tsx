"use client";

import { useState } from "react";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { dateTime } from "@/lib/format";

type A = { id: number; occurred_at: string; actor: string; action: string; target_type: string | null; target_id: string | null; reason: string | null; changes: unknown; metadata: unknown };

export default function AdminAudit() {
  const [action, setAction] = useState("");
  const { data, error } = useApi<A[]>(`/admin/audit${action ? `?action=${encodeURIComponent(action)}` : ""}`);
  const { data: chain, reload: verify } = useApi<{ ok: boolean; rows_checked: number }>("/admin/audit/verify");
  return (
    <>
      <div className="spread">
        <h1 className="h-md">Audit log</h1>
        {chain && <span className={`pill ${chain.ok ? "g" : "b"}`}>Hash chain {chain.ok ? "intact" : "BROKEN"} · {chain.rows_checked} rows <button className="link-btn small" onClick={verify}>re-check</button></span>}
      </div>
      <input type="search" placeholder="Filter by action prefix, e.g. order. or user.role" value={action} onChange={(e) => setAction(e.target.value)} style={{ maxWidth: 380 }} />
      <ErrorBox error={error} />
      {!data ? <Loading /> : (
        <div className="card table-wrap">
          <table className="data">
            <thead><tr><th>#</th><th>When</th><th>Actor</th><th>Action</th><th>Target</th><th>Details</th></tr></thead>
            <tbody>
              {data.map((a) => (
                <tr key={a.id}>
                  <td className="small muted">{a.id}</td>
                  <td className="small">{dateTime(a.occurred_at)}</td>
                  <td className="small">{a.actor}</td>
                  <td><code>{a.action}</code></td>
                  <td className="small">{a.target_type} {a.target_id?.slice(0, 8)}</td>
                  <td className="small" style={{ maxWidth: 360, wordBreak: "break-word" }}>
                    {a.reason && <div><b>Reason:</b> {a.reason}</div>}
                    {a.metadata ? <code>{JSON.stringify(a.metadata)}</code> : null}
                    {a.changes ? <code>{JSON.stringify(a.changes)}</code> : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
