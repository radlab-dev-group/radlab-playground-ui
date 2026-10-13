"use client";

import { t, type Lang } from "@/lib/i18n";
import { hostOf } from "@/lib/utils";
import type { CategoriesWithPages } from "@/lib/types";

interface SourcesPanelProps {
  lang: Lang;
  categories?: CategoriesWithPages;
  loading: boolean;
  error: string | null;
}

/**
 * Shows the indexed categories + pages (the creator activates all of them,
 * mirroring prepare_info_creator_public).
 */
export function SourcesPanel({ lang, categories, loading, error }: SourcesPanelProps) {
  const entries = categories ? Object.entries(categories) : [];
  const totalPages = new Set(
    entries.flatMap(([, info]) =>
      (info.category_pages ?? []).map((page) => page.main_url)
    )
  ).size;

  return (
    <aside aria-label={t(lang, "sources_title")} className="px-1 text-sm text-slate-600">
      {loading && (
        <div role="status" className="flex items-center gap-2 text-sm text-slate-600">
          <span aria-hidden="true" className="h-2 w-2 rounded-full bg-teal-600" />
          {t(lang, "loading_categories")}
        </div>
      )}

      {error && !loading && (
        <div role="alert" className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
          {error}
        </div>
      )}

      {!loading && !error && (
        <details className="group/sources">
          <summary className="cursor-pointer rounded-lg py-1 leading-relaxed marker:text-teal-700 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-teal-700">
            <span>{t(lang, "sources_scope_count").replace("{count}", String(totalPages))}</span>
            <span aria-hidden="true" className="mx-2 text-slate-400">·</span>
            <span className="font-medium text-teal-700 underline-offset-4 group-hover/sources:underline">
              <span className="group-open/sources:hidden">{t(lang, "sources_show")}</span>
              <span className="hidden group-open/sources:inline">{t(lang, "sources_hide")}</span>
            </span>
          </summary>

          <div className="panel mt-3 rounded-xl p-4 sm:p-5">
            <p className="mb-4 text-sm leading-relaxed text-slate-600">
              {t(lang, "sources_hint")}
            </p>
            <div className="max-h-72 space-y-4 overflow-y-auto pr-1">
              {entries.map(([name, info]) => {
                const seen = new Set<string>();
                const uniquePages = (info.category_pages ?? []).filter((page) => {
                  if (seen.has(page.main_url)) return false;
                  seen.add(page.main_url);
                  return true;
                });
                return (
                  <div key={name} className="group">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-slate-900">
                        {info.category_info?.display_name || name}
                      </span>
                      <span className="text-xs text-slate-600">
                        {uniquePages.length}
                      </span>
                    </div>
                    <div className="mt-1.5 flex flex-wrap gap-1.5">
                      {uniquePages.map((page) => (
                        <span
                          key={page.main_url}
                          className="inline-flex max-w-full items-center gap-1.5 rounded-md border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600 [overflow-wrap:anywhere]"
                        >
                          <span aria-hidden="true" className="h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-600" />
                          {hostOf(page.main_url)}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="mt-4 flex items-center gap-2 border-t border-slate-200 pt-3 text-xs text-emerald-700">
              <span aria-hidden="true" className="h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-600" />
              {t(lang, "all_sources_active")}
            </div>
          </div>
        </details>
      )}
    </aside>
  );
}
