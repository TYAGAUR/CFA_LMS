"use client";

import Link from "next/link";
import { useToast } from "@/components/Providers";
import { ErrorBox, Loading, StatusPill, useApi } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { date } from "@/lib/format";

type R = { id: string; type: string; status: string; note: string | null; details: Record<string, string> | null; due_at: string; created_at: string; resolution_note: string | null; student: string; user_id: string };

export default function DataRequests() {
  const { data, error, reload } = useApi<R[]>("/admin/data-requests");
  const toast = useToast();

  async function update(r: R, status: string) {
    const note = prompt(`Resolution note for this ${r.type} request:`);
    if (!note) return;
    try {
      await api(`/admin/data-requests/${r.id}`, { body: { status, resolution_note: note } });
      reload();
    } catch (e) {
      toast(errorText(e));
    }
  }

  async function erase(r: R) {
    if (!confirm(`Permanently erase ${r.student}'s personal data? Payment records are kept without contact details. This cannot be undone.`)) return;
    try {
      await api(`/admin/data-requests/${r.id}/erase`, { method: "POST" });
      toast("Erasure completed");
      reload();
    } catch (e) {
      toast(errorText(e));
    }
  }

  if (error) return <ErrorBox error={error} />;
  if (!data) return <Loading />;
  return (
    <>
      <h1 className="h-md">Data requests</h1>
      <p className="muted small" style={{ margin: 0 }}>Requests under the DPDP Act. Respond before the due date (C-05 §6).</p>
      <div className="card table-wrap">
        <table className="data">
          <thead><tr><th>Student</th><th>Type</th><th>Details</th><th>Raised</th><th>Due</th><th>Status</th><th /></tr></thead>
          <tbody>
            {data.map((r) => (
              <tr key={r.id}>
                <td><Link href={`/admin/users/${r.user_id}`}>{r.student}</Link></td>
                <td>{r.type}</td>
                <td className="small">{r.note}{r.details && <code>{JSON.stringify(r.details)}</code>}{r.resolution_note && <div className="muted">→ {r.resolution_note}</div>}</td>
                <td className="small">{date(r.created_at)}</td>
                <td className="small">{date(r.due_at)}</td>
                <td><StatusPill status={r.status} /></td>
                <td className="small">
                  {!["completed", "rejected"].includes(r.status) && (
                    <>
                      {r.type === "erasure" ? <button className="btn sm bad" onClick={() => erase(r)}>Erase</button> : <button className="link-btn" onClick={() => update(r, "completed")}>Complete</button>}
                      <button className="link-btn" style={{ marginLeft: 8 }} onClick={() => update(r, "rejected")}>Reject</button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {data.length === 0 && <p className="muted">No requests.</p>}
      </div>
    </>
  );
}
