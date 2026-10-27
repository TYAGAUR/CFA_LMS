// Indian digit grouping for ₹ (P-07 §9) and IST dates.

const inr = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 });

export function rupees(paise: number): string {
  const v = paise / 100;
  return Number.isInteger(v) ? inr.format(v).replace(/\.00$/, "") : inr.format(v);
}

export function date(d: string | null | undefined): string {
  if (!d) return "—";
  return new Date(d).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric", timeZone: "Asia/Kolkata" });
}

export function dateTime(d: string | null | undefined): string {
  if (!d) return "—";
  return new Date(d).toLocaleString("en-IN", {
    day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", timeZone: "Asia/Kolkata",
  });
}

export function duration(s: number | null | undefined): string {
  if (!s) return "";
  const m = Math.floor(s / 60);
  return `${m}:${String(s % 60).padStart(2, "0")}`;
}

export function examWindow(w: string | null | undefined): string {
  if (!w) return "";
  const [y, m] = w.split("-");
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return m ? `${months[Number(m) - 1]} ${y}` : w;
}

export function todayIso(): string {
  return new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Kolkata" });
}
