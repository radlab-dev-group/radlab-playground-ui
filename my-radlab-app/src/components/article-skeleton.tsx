"use client";

import { t, type Lang } from "@/lib/i18n";

/**
 * Placeholder shown in the (top) article slot while the model is working,
 * so the reader keeps the final deliverable in place instead of waiting on
 * an empty page.
 */
export function ArticleSkeleton({ lang, label }: { lang: Lang; label: string }) {
  return (
    <section aria-busy="true" className="panel rounded-2xl px-5 py-6 sm:px-8">
      <div>
        <div className="mb-5 flex items-center gap-2 text-sm font-medium text-teal-800">
          <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-teal-600" />
          {t(lang, "article_onair")}
        </div>

        <div aria-hidden="true" className="mb-3 h-8 w-3/4 rounded-lg bg-slate-200 motion-safe:animate-pulse" />
        <div aria-hidden="true" className="mb-7 h-8 w-1/2 rounded-lg bg-slate-100 motion-safe:animate-pulse" />

        <div aria-hidden="true" className="mb-7 h-px w-full bg-slate-200" />

        <div aria-hidden="true" className="max-w-[70ch] space-y-3">
          {[100, 96, 88, 92, 72].map((width, idx) => (
            <div
              key={idx}
              className="h-3 rounded bg-slate-100 motion-safe:animate-pulse"
              style={{
                width: `${width}%`,
                animationDelay: `${idx * 120}ms`,
              }}
            />
          ))}
        </div>

        <div role="status" className="mt-7 flex items-start gap-2 text-sm text-teal-700">
          <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600" />
          <span className="min-w-0 break-words">{label}</span>
        </div>
      </div>
    </section>
  );
}
