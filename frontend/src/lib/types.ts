export type Me = {
  id: string;
  full_name: string;
  mobile_e164: string | null;
  email: string | null;
  student_code: string | null;
  status: "active" | "pending_guardian_consent" | string;
  is_minor: boolean;
  role_names: string[];
  is_staff: boolean;
  city: string | null;
  qualification: string | null;
  target_exam: string | null;
  permissions: string[];
};

export type CourseSubject = { id: string; code: string; name: string; icon: string; lm_count: number; lms?: { lm_no: number; title: string }[] };

export type Course = {
  id: string;
  code: string;
  title: string;
  tagline: string | null;
  description: string | null;
  fee_paise: number;
  currency: string;
  validity_days: number | null;
  access_ends_on: string | null;
  exam_window: string | null;
  status: string;
  seats_left: number | null;
  subjects: CourseSubject[];
  my_registration?: { id: string; status: string; order_id: string | null } | null;
};

export type Inline = { t: string; b?: boolean; i?: boolean; sub?: boolean; sup?: boolean; link?: string };
export type Block =
  | { type: "heading"; level: number; text: string }
  | { type: "paragraph"; inline: Inline[] }
  | { type: "list"; ordered: boolean; items: Inline[][] }
  | { type: "table"; header: string[]; rows: string[][] }
  | { type: "callout"; variant: "example" | "watch_out" | "formula" | "fun" | "note"; title: string; inline: Inline[] }
  | { type: "infographic"; kind: "waterfall"; data: { label: string; text: string; pct: number }[]; alt: string }
  | { type: "image"; resource_id: string; alt: string; caption?: string };

export type LmStats = {
  resources_total: number;
  resources_done: number;
  completion_pct: number;
  learned: boolean;
  learned_at: string | null;
  learned_undo_until: string | null;
  eoc_completed: boolean;
  revision_count: number;
};

export type LmSummary = { id: string; lm_no: number; title: string; summary: string | null } & Partial<LmStats>;

export type SubjectDetail = {
  id: string;
  code: string;
  name: string;
  icon: string;
  entitled: boolean;
  courses: { code: string; title: string; fee_paise: number }[];
  lms: LmSummary[];
};

export type ResourceRow = {
  id: string;
  kind: "video" | "pdf" | "class_note" | "link";
  title: string;
  mandatory: boolean;
  duration_s: number | null;
  downloadable: boolean;
  topic_id: string | null;
  completed: boolean;
  last_position_s: number;
};

export type LmDetail = {
  id: string;
  lm_no: number;
  title: string;
  summary: string | null;
  subject: { id: string; code: string; name: string };
  prev_lm_id: string | null;
  next_lm_id: string | null;
  topics: { id: string; title: string }[];
  content: { id: string; title: string; kind: string; topic_id: string | null }[];
  resources: ResourceRow[];
  los: { code: string; statement: string; command_word: string }[];
  eoc: { attempted: boolean; q_attempted: number; q_correct: number; completed_on: string | null; weak_topics: string | null } | null;
  progress: LmStats;
  quiz: { questions: number; available: boolean; size: number; pass_mark: number; best_pct: number | null; attempts: number };
};

export type Order = {
  id: string;
  number: string;
  purpose: string;
  description: string;
  amount_paise: number;
  currency: string;
  status: string;
  provider: string;
  created_at: string;
  paid_at: string | null;
  refunded_paise: number;
  offline_reference: string | null;
  payments: { provider_payment_id: string; status: string; method: string | null; amount_paise: number; captured_at: string | null; error_description: string | null }[];
};

export type AttemptItem = {
  position: number;
  stem: string;
  options: string[];
  difficulty: "E" | "M" | "H";
  answer_index: number | null;
  flagged: boolean;
  correct_index?: number;
  explanation?: string;
  is_correct?: boolean;
};

export type Attempt = {
  id: string;
  kind: "chapter" | "master" | "custom";
  title: string;
  mode: "practice" | "assessment";
  timed: boolean;
  time_limit_s: number | null;
  seconds_left: number | null;
  status: "in_progress" | "submitted";
  started_at: string;
  submitted_at: string | null;
  submit_reason: string | null;
  total: number;
  correct: number | null;
  score_pct: number | null;
  pass_mark: number | null;
  passed: boolean | null;
  lm_id: string | null;
  items?: AttemptItem[];
  answered?: number;
};

export const DIFFICULTY_LABEL = { E: "Easy", M: "Medium", H: "Hard" } as const;
