"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { Loading } from "@/components/ui";
import { useRequireUser } from "@/lib/auth";

const NAV: [string, string, string][] = [
  ["/admin", "Overview", "report:read"],
  ["/admin/catalog", "Catalogue & content", "catalog:read_admin"],
  ["/admin/questions", "Question bank", "catalog:read_admin"],
  ["/admin/flashcards", "Flashcards", "catalog:read_admin"],
  ["/admin/courses", "Courses & fees", "course:manage"],
  ["/admin/registrations", "Registrations", "order:read"],
  ["/admin/orders", "Payments & refunds", "order:read"],
  ["/admin/users", "Users & staff", "user:read"],
  ["/admin/batches", "Batches", "batch:manage"],
  ["/admin/reports", "Progress report", "report:read"],
  ["/admin/data-requests", "Data requests", "data_request:process"],
  ["/admin/audit", "Audit log", "audit:read"],
];

export default function AdminLayout({ children }: { children: ReactNode }) {
  const user = useRequireUser({ staff: true });
  const path = usePathname();
  if (!user) return <Loading />;
  const items = NAV.filter(([, , perm]) => user.permissions.includes(perm));
  return (
    <div className="wrap admin">
      <nav aria-label="Staff console">
        <div className="eyebrow" style={{ padding: "4px 12px 8px" }}>Staff console</div>
        {items.map(([href, label]) => (
          <Link key={href} href={href} className={path === href || (href !== "/admin" && path.startsWith(href)) ? "on" : ""}>
            {label}
          </Link>
        ))}
      </nav>
      <div className="stack" style={{ minWidth: 0 }}>{children}</div>
    </div>
  );
}
