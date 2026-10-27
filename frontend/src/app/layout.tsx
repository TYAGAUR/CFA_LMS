import type { Metadata } from "next";
import { Figtree } from "next/font/google";
import type { ReactNode } from "react";
import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";
import { Providers } from "@/components/Providers";
import "./globals.css";

const figtree = Figtree({ subsets: ["latin"], weight: ["300", "400", "500", "600", "700", "800"], variable: "--font-figtree" });

export const metadata: Metadata = {
  title: { default: "Karan Sir Classes · CFA Level I", template: "%s · Karan Sir Classes" },
  description: "Structured CFA Level I preparation: class videos, notes, revision and progress in one place.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={figtree.variable}>
      <body>
        <Providers>
          <Header />
          <main>{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
