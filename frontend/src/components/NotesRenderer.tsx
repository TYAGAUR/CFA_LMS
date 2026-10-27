// Renders notes/v1 JSON blocks (ADR-012). All text is rendered as React text nodes:
// no HTML from content is ever injected into the page.
import type { Block, Inline } from "@/lib/types";

const COLORS = ["#211C84", "#4A6CF7", "#1B9BB8", "#2F2AA0", "#0E7490"];
const CALLOUT_CLASS = { example: "ex", watch_out: "wo", formula: "fx", fun: "fun", note: "" } as const;

function Inlines({ items }: { items: Inline[] }) {
  return (
    <>
      {items.map((it, i) => {
        let node: React.ReactNode = it.t;
        if (it.b) node = <b>{node}</b>;
        if (it.i) node = <i>{node}</i>;
        if (it.sub) node = <sub>{node}</sub>;
        if (it.sup) node = <sup>{node}</sup>;
        if (it.link && it.link.startsWith("https://"))
          node = (
            <a href={it.link} target="_blank" rel="noopener noreferrer">
              {node}
            </a>
          );
        return <span key={i}>{node}</span>;
      })}
    </>
  );
}

export function NotesRenderer({ blocks }: { blocks: Block[] }) {
  return (
    <div className="notes">
      {blocks.map((b, i) => {
        switch (b.type) {
          case "heading":
            return <h3 key={i}>{b.text}</h3>;
          case "paragraph":
            return (
              <p key={i}>
                <Inlines items={b.inline} />
              </p>
            );
          case "list": {
            const items = b.items.map((it, j) => (
              <li key={j}>
                <Inlines items={it} />
              </li>
            ));
            return b.ordered ? <ol key={i}>{items}</ol> : <ul key={i}>{items}</ul>;
          }
          case "table":
            return (
              <div className="table-wrap" key={i}>
                <table>
                  <thead>
                    <tr>{b.header.map((h, j) => <th key={j}>{h}</th>)}</tr>
                  </thead>
                  <tbody>
                    {b.rows.map((r, j) => (
                      <tr key={j}>{r.map((c, k) => <td key={k}>{c}</td>)}</tr>
                    ))}
                  </tbody>
                </table>
              </div>
            );
          case "callout":
            return (
              <div key={i} className={`box ${CALLOUT_CLASS[b.variant]}`}>
                <div className="lb">{b.title}</div>
                <Inlines items={b.inline} />
              </div>
            );
          case "infographic":
            return (
              <figure key={i} className="wf" style={{ margin: "14px 0" }}>
                {b.data.map((d, j) => (
                  <div className="r" key={j}>
                    <span>{d.label}</span>
                    <div className="b" style={{ width: `${d.pct}%`, background: COLORS[j % COLORS.length] }}>
                      {d.text}
                    </div>
                  </div>
                ))}
                <figcaption className="sr-only">{b.alt}</figcaption>
              </figure>
            );
          case "image":
            return (
              <p key={i} className="muted small">
                [Image: {b.alt}]
              </p>
            );
          default:
            return null;
        }
      })}
    </div>
  );
}
