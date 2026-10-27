"use client";

import { useCallback, useEffect, useState } from "react";
import { useToast } from "@/components/Providers";
import { Loading } from "@/components/ui";
import { api, errorText } from "@/lib/api";

type Card = { id: string; front: string; back: string };
export type FlashSession = { subject: { code: string; name: string }; counts: { due: number; new: number; later: number }; cards: Card[] };
type Rating = "known" | "needs_revision" | "difficult";

/** Flip-and-rate study session with spaced repetition (BR-FC). Used on /flashcards and in the LM tab. */
export function FlashcardStudy({ subject, lmId, compact = false }: { subject: string; lmId?: string; compact?: boolean }) {
  const toast = useToast();
  const [sess, setSess] = useState<FlashSession | null>(null);
  const [scope, setScope] = useState<"lm" | "subject">(lmId ? "lm" : "subject");
  const [queue, setQueue] = useState<Card[]>([]);
  const [flipped, setFlipped] = useState(false);
  const [tally, setTally] = useState({ known: 0, needs_revision: 0, difficult: 0 });

  const load = useCallback(async (cram = false, forceScope?: "lm" | "subject") => {
    try {
      let useScope = forceScope ?? scope;
      const url = (sc: "lm" | "subject") =>
        `/flashcards/session?subject=${subject}&limit=30${sc === "lm" && lmId ? `&lm_id=${lmId}` : ""}${cram ? "&include_future=true" : ""}`;
      let s = await api<FlashSession>(url(useScope));
      const empty = s.counts.due + s.counts.new + s.counts.later === 0;
      if (useScope === "lm" && empty) {
        useScope = "subject"; // no cards for this LM yet: fall back to the subject deck
        s = await api<FlashSession>(url(useScope));
      }
      setScope(useScope);
      setSess(s);
      setQueue(s.cards);
      setFlipped(false);
      setTally({ known: 0, needs_revision: 0, difficult: 0 });
    } catch (e) {
      toast(errorText(e));
    }
  }, [subject, lmId, scope, toast]);

  useEffect(() => {
    void load(false, lmId ? "lm" : "subject");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [subject, lmId]);

  const rate = useCallback(async (r: Rating) => {
    const card = queue[0];
    if (!card) return;
    setFlipped(false);
    setTally((t) => ({ ...t, [r]: t[r] + 1 }));
    // Difficult cards come back later in this session.
    setQueue((q) => (r === "difficult" && q.length > 1 ? [...q.slice(1, 4), card, ...q.slice(4)] : q.slice(1)));
    try {
      await api(`/flashcards/${card.id}/review`, { body: { rating: r } });
    } catch (e) {
      toast(errorText(e));
    }
  }, [queue, toast]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.key === " ") { e.preventDefault(); setFlipped((f) => !f); }
      if (flipped && e.key === "1") void rate("known");
      if (flipped && e.key === "2") void rate("needs_revision");
      if (flipped && e.key === "3") void rate("difficult");
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [flipped, rate]);

  if (!sess) return <Loading />;
  const card = queue[0];
  const reviewed = tally.known + tally.needs_revision + tally.difficult;
  const total = sess.counts.due + sess.counts.new + sess.counts.later;

  if (total === 0) return <p className="muted" style={{ padding: "30px 0" }}>No flashcards for {sess.subject.name} yet. The faculty adds them in the staff console.</p>;

  const study = (
    <div className="stack">
      {lmId && (
        <p className="small muted" style={{ margin: 0 }}>
          {scope === "lm" ? "Cards for this LM." : `No cards specific to this LM yet, so here is the ${sess.subject.name} deck.`}
          {" "}{sess.counts.due} due · {sess.counts.new} new
        </p>
      )}
      {card ? (
        <>
          <div className={`flip ${flipped ? "on" : ""}`} onClick={() => setFlipped(!flipped)} role="button" tabIndex={0} aria-label="Flip card"
            style={compact ? { height: 240 } : undefined}>
            <div className="in">
              <div className="face front"><small>Question · {queue.length} left</small><span>{card.front}</span></div>
              <div className="face back"><small>Answer</small><span>{card.back}</span></div>
            </div>
          </div>
          {!flipped ? (
            <div><button className="btn" onClick={() => setFlipped(true)}>Show answer (Space)</button></div>
          ) : (
            <div className="row">
              <button className="btn good" onClick={() => rate("known")}>1 · I know this</button>
              <button className="btn ghost" onClick={() => rate("needs_revision")}>2 · Needs revision</button>
              <button className="btn" style={{ background: "var(--coral)", borderColor: "var(--coral)" }} onClick={() => rate("difficult")}>3 · Difficult</button>
            </div>
          )}
        </>
      ) : (
        <div className="card stack" style={{ textAlign: "center" }}>
          <h3>{reviewed ? "Session complete 🎉" : "Nothing due right now"}</h3>
          {reviewed > 0 && <p className="muted" style={{ margin: 0 }}>{reviewed} reviews: {tally.known} known, {tally.needs_revision} need revision, {tally.difficult} difficult.</p>}
          <div className="row" style={{ justifyContent: "center" }}>
            <button className="btn" onClick={() => load()}>Check for due cards</button>
            <button className="btn ghost" onClick={() => load(true)}>Review ahead anyway</button>
          </div>
        </div>
      )}
      <p className="small muted" style={{ margin: 0 }}>Keyboard: Space flips · 1 / 2 / 3 rate. Known cards return after 1, 3, then 7+ days; difficult ones tomorrow.</p>
    </div>
  );

  if (compact) return <div style={{ maxWidth: 640 }}>{study}</div>;
  return (
    <div className="fc">
      {study}
      <aside className="card stack">
        <div className="eyebrow">This session</div>
        <div style={{ fontSize: 40, fontWeight: 300 }}>{reviewed}</div>
        <div className="small muted">cards reviewed · {sess.counts.due} were due, {sess.counts.new} new</div>
      </aside>
    </div>
  );
}
