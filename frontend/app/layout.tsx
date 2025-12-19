import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import ReactQueryProvider from "@/components/providers/ReactQueryProvider";
import ParticleBackground from "@/components/ui/ParticleBackground";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Movie RAG Search",
  description: "Corrective RAG system for movie and TV show recommendations",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ParticleBackground />
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </body>
    </html>
  );
}
