"use client";

import { usePathname, useRouter } from "next/navigation";
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { api, ApiError } from "./api";
import type { Me } from "./types";

type AuthState = { user: Me | null; loading: boolean; reload: () => Promise<Me | null>; logout: () => Promise<void> };

const Ctx = createContext<AuthState>({ user: null, loading: true, reload: async () => null, logout: async () => {} });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);

  const reload = useCallback(async () => {
    try {
      const me = await api<Me>("/me");
      setUser(me);
      return me;
    } catch (e) {
      if (!(e instanceof ApiError) || e.status !== 401) console.error(e);
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await api("/auth/logout", { method: "POST" });
    } catch {
      /* already signed out */
    }
    setUser(null);
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  return <Ctx.Provider value={{ user, loading, reload, logout }}>{children}</Ctx.Provider>;
}

export const useAuth = () => useContext(Ctx);

/** Redirects to sign-in (or the guardian-consent screen) when needed. Returns the ready user or null. */
export function useRequireUser(opts: { staff?: boolean; perm?: string } = {}): Me | null {
  const { user, loading } = useAuth();
  const router = useRouter();
  const path = usePathname();
  useEffect(() => {
    if (loading) return;
    if (!user) {
      router.replace(`${opts.staff ? "/staff/login" : "/login"}?next=${encodeURIComponent(path)}`);
    } else if (user.status === "pending_guardian_consent" && path !== "/pending-consent") {
      router.replace("/pending-consent");
    } else if (opts.staff && !user.is_staff) {
      router.replace("/dashboard");
    }
  }, [user, loading, router, path, opts.staff]);
  if (loading || !user) return null;
  if (opts.staff && !user.is_staff) return null;
  if (opts.perm && !user.permissions.includes(opts.perm)) return null;
  return user;
}
