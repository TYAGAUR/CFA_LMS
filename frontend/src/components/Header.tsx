"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";

export function Header() {
  const { user, logout } = useAuth();
  const path = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  useEffect(() => setOpen(false), [path]);
  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (!(e.target as HTMLElement).closest(".menu, .avatar")) setOpen(false);
    };
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);

  const student = user && !user.is_staff;
  const links: [string, string][] = user
    ? [
        ...(student ? ([["/dashboard", "Home"], ["/learn", "Learn"], ["/practice", "Custom Quiz"], ["/courses", "Courses"], ["/bookmarks", "Bookmarks"]] as [string, string][]) : []),
        ...(user.is_staff ? ([["/admin", "Staff console"], ["/learn", "Preview content"]] as [string, string][]) : []),
      ]
    : [["/", "Home"], ["/courses", "Courses"]];

  const initials = user?.full_name.split(/\s+/).map((p) => p[0]).slice(0, 2).join("").toUpperCase();

  function toggleTheme() {
    const r = document.documentElement;
    const dark = r.dataset.theme ? r.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    r.dataset.theme = dark ? "light" : "dark";
  }

  return (
    <>
      <div className="util">
        <div className="wrap">
          <span>CFA Level I · Students · Faculty</span>
          <span>{user?.student_code ? `Student code ${user.student_code}` : "Learn a chapter. Revise. Repeat."}</span>
        </div>
      </div>
      <header className="top">
        <div className="wrap">
          <Link className="logo" href={user ? (user.is_staff ? "/admin" : "/dashboard") : "/"}>
            <i aria-hidden />
            Karan Sir Classes
          </Link>
          <nav className="main" aria-label="Main">
            {links.map(([href, label]) => (
              <Link key={href} href={href} className={path === href || (href !== "/" && path.startsWith(href)) ? "on" : ""}>
                {label}
              </Link>
            ))}
          </nav>
          <div className="row">
            {user && (
              <Link href="/search" className="ibtn" aria-label="Search" title="Search">
                ⌕
              </Link>
            )}
            <button className="ibtn" type="button" onClick={toggleTheme} aria-label="Toggle dark mode" title="Theme">
              ◐
            </button>
            {user ? (
              <button className="avatar" type="button" aria-label="Account menu" aria-expanded={open} onClick={() => setOpen((v) => !v)}>
                {initials}
              </button>
            ) : (
              <>
                <Link className="btn sm ghost" href="/staff/login">
                  Staff
                </Link>
                <Link className="btn sm" href="/login">
                  Sign in
                </Link>
              </>
            )}
          </div>
        </div>
        {open && user && (
          <div className="menu" role="menu">
            <h4>{user.full_name}</h4>
            <small>{user.is_staff ? user.role_names.join(", ") : user.mobile_e164}</small>
            <Link href="/profile">Profile, devices and privacy</Link>
            {!user.is_staff && <Link href="/orders">My orders and receipts</Link>}
            <button
              type="button"
              onClick={async () => {
                await logout();
                router.push("/");
              }}
            >
              Sign out
            </button>
          </div>
        )}
      </header>
    </>
  );
}
