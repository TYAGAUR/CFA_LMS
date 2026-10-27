"use client";

import Link from "next/link";
import { useState, type FormEvent } from "react";
import { ErrorBox, Loading } from "@/components/ui";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";

type Results = {
  lms: { id: string; title: string; subject: string; subject_code: string; entitled: boolean }[];
  content: { id: string; lm_id: string; title: string; lm: string; subject: string; subject_code: string; entitled: boolean; snippet: string | null }[];
};

/** ts_headline marks matches with <b>…</b>; render them safely as React nodes. */
function Snippet({ text }: { text: string }) {
  return <>{text.split(/(<b>.*?<\/b>)/g).map((p, i) => (p.startsWith("<b>") ? <b key={i}>{p.slice(3, -4)}</b> : <span key={i}>{p}</span>))}</>;
}

export default function Search() {
  const user = useRequireUser();
  const [q, setQ] = useState("");
  const [res, setRes] = useState<Results | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);
  if (!user) return <Loading />;

  async function run(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      setRes(await api<Results>(`/search?q=${encodeURIComponent(q)}`));
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="blk">
      <div className="wrap" style={{ maxWidth: 860 }}>
        <h1 className="h-md" style={{ marginBottom: 14 }}>Search notes and modules</h1>
        <form onSubmit={run} className="row">
          <input type="search" placeholder="e.g. preferred shares, duration, put-call parity" value={q} onChange={(e) => setQ(e.target.value)} style={{ flex: 1 }} minLength={2} required autoFocus />
          <button className="btn" disabled={busy}>Search</button>
        </form>
        <ErrorBox error={error} />
        {res && (
          <div className="stack" style={{ marginTop: 20 }}>
            {res.lms.length + res.content.length === 0 && <p className="muted">No results.</p>}
            {res.content.map((c) => (
              <div className="card" key={c.id}>
                <div className="small muted">{c.subject} · {c.lm}</div>
                {c.entitled ? <Link href={`/learn/${c.subject_code}?lm=${c.lm_id}&tab=notes&item=${c.id}`}><b>{c.title}</b></Link> : <b>{c.title} 🔒</b>}
                {c.snippet && <p className="small" style={{ margin: "6px 0 0" }}><Snippet text={c.snippet} /></p>}
              </div>
            ))}
            {res.lms.map((m) => (
              <div className="card" key={m.id}>
                <div className="small muted">{m.subject}</div>
                {m.entitled ? <Link href={`/learn/${m.subject_code}?lm=${m.id}`}><b>{m.title}</b></Link> : <b>{m.title} 🔒</b>}
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
