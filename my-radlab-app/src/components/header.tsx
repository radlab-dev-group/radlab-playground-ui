"use client";

import Image from "next/image";

import { LANGS, t, type Lang } from "@/lib/i18n";
import { cn } from "@/lib/utils";

interface HeaderProps {
  lang: Lang;
  onLangChange: (lang: Lang) => void;
  indexReady: boolean;
}

export function Header({ lang, onLangChange, indexReady }: HeaderProps) {
  return (
    <header className="relative z-20 border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-4 px-4 py-5 sm:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <div className="relative h-10 w-10 shrink-0 overflow-hidden rounded-full ring-1 ring-slate-200">
            <Image
              src="/logo-circle.png"
              alt="RadLab"
              fill
              sizes="40px"
              className="object-cover"
            />
          </div>
          <div className="leading-tight">
            <div className="flex items-center gap-2">
              <h1 className="text-base font-semibold tracking-tight text-slate-900 sm:text-lg">
                {t(lang, "app_title")}
              </h1>
            </div>
            <p className="mt-1 text-xs text-slate-500">
              {t(lang, "app_tagline")}
            </p>
          </div>
        </div>

        <div className="ml-auto flex items-center gap-3">
          <div
            className={cn(
              "hidden items-center gap-2 rounded-full border px-3 py-1.5 text-xs sm:flex",
              indexReady
                ? "border-teal-200 bg-teal-50 text-teal-800"
                : "border-amber-200 bg-amber-50 text-amber-800"
            )}
          >
            <span
              className={cn(
                "h-1.5 w-1.5 rounded-full",
                indexReady ? "bg-teal-600" : "bg-amber-600"
              )}
            />
            {t(lang, "live_badge")}
          </div>

          <div className="flex items-center rounded-xl border border-slate-200 bg-slate-50 p-1">
            {LANGS.map((item) => (
              <button
                key={item.code}
                onClick={() => onLangChange(item.code)}
                aria-pressed={lang === item.code}
                className={cn(
                  "rounded-lg px-3 py-2 text-xs font-medium transition",
                  lang === item.code
                    ? "bg-white text-teal-800 shadow-sm"
                    : "text-slate-600 hover:bg-white hover:text-slate-900"
                )}
                title={item.label}
              >
                {item.flag} {item.code.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
}
