// Same-origin API client. Cookies carry the session; the CSRF header is added to writes;
// an expired access token is refreshed once, transparently (ADR-003, A-04 §1.2).

export class ApiError extends Error {
  status: number;
  code: string;
  detail: string;
  meta?: Record<string, unknown>;
  errors?: { loc: string[]; msg: string }[];
  constructor(status: number, body: Record<string, unknown>) {
    super(String(body.detail ?? body.title ?? "Request failed"));
    this.status = status;
    this.code = String(body.code ?? "error");
    this.detail = String(body.detail ?? body.title ?? "Request failed");
    this.meta = body.meta as Record<string, unknown> | undefined;
    this.errors = body.errors as { loc: string[]; msg: string }[] | undefined;
  }
  /** First field error message, for forms. */
  get fieldMessage(): string {
    const e = this.errors?.[0];
    if (!e) return this.detail;
    const field = e.loc.filter((p) => p !== "body").join(".");
    return field ? `${field}: ${e.msg}` : e.msg;
  }
}

type Opts = { method?: string; body?: unknown; form?: FormData; signal?: AbortSignal };

function csrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  return document.cookie.match(/(?:^|; )csrf_token=([^;]+)/)?.[1];
}

let refreshing: Promise<boolean> | null = null;

async function refresh(): Promise<boolean> {
  refreshing ??= fetch("/api/v1/auth/refresh", { method: "POST", credentials: "same-origin" })
    .then((r) => r.ok)
    .catch(() => false)
    .finally(() => setTimeout(() => (refreshing = null), 0));
  return refreshing;
}

export async function api<T = unknown>(path: string, opts: Opts = {}, retry = true): Promise<T> {
  const method = opts.method ?? (opts.body || opts.form ? "POST" : "GET");
  const headers: Record<string, string> = { Accept: "application/json" };
  let body: BodyInit | undefined;
  if (opts.form) body = opts.form;
  else if (opts.body !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(opts.body);
  }
  if (method !== "GET") {
    const t = csrf();
    if (t) headers["X-CSRF-Token"] = t;
  }
  const res = await fetch(`/api/v1${path}`, { method, headers, body, credentials: "same-origin", signal: opts.signal });
  if (res.status === 401 && retry && !path.startsWith("/auth/")) {
    if (await refresh()) return api<T>(path, opts, false);
  }
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) throw new ApiError(res.status, data ?? {});
  return data as T;
}

export function errorText(e: unknown): string {
  if (e instanceof ApiError) return e.status === 422 ? e.fieldMessage : e.detail;
  if (e instanceof Error) return e.message;
  return "Something went wrong.";
}
