"use client";

import Link from "next/link";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/auth";
import { date } from "@/lib/format";

type Bm = { id: string; title: string; context: string | null; href: string | null; created_at: string; note: string | null };

export default function Bookmarks() {
  const user = useRequireUser();
  const { data, error, reload } = useApi<Bm[]>(user ? "/me/bookmarks" : null);
  if (!user || (!data && !error)) return <Loading />;
  return (
    <section className="blk">
      <div className="wrap" style={{ maxWidth: 860 }}>
        <h1 className="h-md" style={{ marginBottom: 14 }}>Bookmarks</h1>
        <ErrorBox error={error} />
        {data?.length === 0 && <p className="muted">Use ☆ Bookmark on any LM to save it here.</p>}
        <div className="stack">
          {data?.map((b) => (
            <div className="card spread" key={b.id}>
              <div>
                <div className="small muted">{b.context} · saved {date(b.created_at)}</div>
                {b.href ? <Link href={b.href}><b>{b.title}</b></Link> : <b>{b.title}</b>}
              </div>
              <button className="btn sm ghost" onClick={() => api(`/me/bookmarks/${b.id}`, { method: "DELETE" }).then(reload)}>Remove</button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
