"use client";

import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from "react";
import { AuthProvider } from "@/lib/auth";

const ToastCtx = createContext<(msg: string) => void>(() => {});
export const useToast = () => useContext(ToastCtx);

export function Providers({ children }: { children: ReactNode }) {
  const [msg, setMsg] = useState<string | null>(null);
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);
  const toast = useCallback((m: string) => {
    setMsg(m);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => setMsg(null), 3200);
  }, []);
  return (
    <AuthProvider>
      <ToastCtx.Provider value={toast}>
        {children}
        {msg && (
          <div className="toast" role="status">
            {msg}
          </div>
        )}
      </ToastCtx.Provider>
    </AuthProvider>
  );
}
