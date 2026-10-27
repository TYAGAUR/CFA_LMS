"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Loading, useApi } from "@/components/ui";
import { useRequireUser } from "@/lib/auth";

export default function LearnIndex() {
  const user = useRequireUser();
  const router = useRouter();
  const { data } = useApi<{ code: string; entitled: boolean }[]>(user ? "/subjects" : null);
  useEffect(() => {
    if (!data) return;
    const first = data.find((s) => s.entitled) ?? data[0];
    if (first) router.replace(`/learn/${first.code}`);
  }, [data, router]);
  return <Loading />;
}
