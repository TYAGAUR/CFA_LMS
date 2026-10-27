"use client";

import Link from "next/link";
import { useState } from "react";
import { FlashcardStudy } from "@/components/FlashcardStudy";
import { ErrorBox, Loading, useApi } from "@/components/ui";
import { useRequireUser } from "@/lib/auth";

type Deck = { code: string; name: string; icon: string; entitled: boolean; total: number; new: number; due: number; learning: number; mastered: number };

export default function Flashcards() {
  const user = useRequireUser();
  const { data: decks, error, reload } = useApi<Deck[]>(user ? "/flashcards/decks" : null);
  const [deck, setDeck] = useState<Deck | null>(null);

  if (!user || (!decks && !error)) return <Loading />;
  if (error) return <div className="wrap"><ErrorBox error={error} /></div>;

  if (deck) {
    return (
      <section className="blk">
        <div className="wrap stack">
          <div className="spread">
            <h2 className="h-md">{deck.icon} {deck.name}</h2>
            <button className="btn sm ghost" onClick={() => { setDeck(null); reload(); }}>All decks</button>
          </div>
          <FlashcardStudy subject={deck.code} />
        </div>
      </section>
    );
  }

  return (
    <section className="blk">
      <div className="wrap stack">
        <div>
          <div className="eyebrow">Revise</div>
          <h1 className="h-lg" style={{ margin: "6px 0 4px" }}>Flash<b>cards</b></h1>
          <p className="muted" style={{ margin: 0 }}>Spaced repetition: cards you know come back after longer gaps; difficult ones come back tomorrow. You can also study a chapter&apos;s cards from the Flashcards tab on any LM.</p>
        </div>
        <div className="g3">
          {decks?.map((d) => (
            <div className="card stack" key={d.code}>
              <h3>{d.icon} {d.name}</h3>
              <div className="row small">
                <span className="pill w">{d.due} due</span><span className="pill">{d.new} new</span><span className="pill g">{d.mastered} mastered</span>
              </div>
              {d.entitled ? (
                <button className="btn sm" onClick={() => setDeck(d)}>{d.due + d.new > 0 ? `Study ${Math.min(d.due + d.new, 30)} cards` : "Review ahead"}</button>
              ) : (
                <Link className="btn sm ghost" href="/courses">Register to study</Link>
              )}
            </div>
          ))}
        </div>
        {decks?.length === 0 && <p className="muted">No flashcards have been published yet.</p>}
      </div>
    </section>
  );
}
