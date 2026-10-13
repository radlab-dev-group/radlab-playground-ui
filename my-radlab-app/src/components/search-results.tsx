"use client";

import { useMemo, useState } from "react";

import { t, type Lang } from "@/lib/i18n";
import { cn, formatCrawledDate, hostOf } from "@/lib/utils";
import type { NewsItem, SearchInCategory } from "@/lib/types";
import { PolarityBar, polarityMeta } from "./polarity-chart";

interface SearchResultsProps {
  lang: Lang;
  searchInCategory: SearchInCategory;
  categoriesSorted: string[];
}

type ViewMode = "wire" | "list";

interface SourceRow {
  citation: number;
  category: string;
  item: NewsItem;
}

/**
 * "Materiał źródłowy" — the evidence the article was built from.
 * Port of add_search_results_to_container / show_result_urls, restyled as a
 * numbered citation wire (horizontal scroll) with a compact list alternative.
 */
export function SearchResults({
  lang,
  searchInCategory,
  categoriesSorted,
}: SearchResultsProps) {
  const [view, setView] = useState<ViewMode>("wire");
  const [category, setCategory] = useState<string>("__all__");

  const orderedCategories = useMemo(() => {
    const present = Object.keys(searchInCategory).filter(
      (cat) => (searchInCategory[cat]?.length ?? 0) > 0
    );
    const known = categoriesSorted.filter((cat) => present.includes(cat));
    const extra = present.filter((cat) => !categoriesSorted.includes(cat));
    return [...known, ...extra.sort((a, b) => a.localeCompare(b))];
  }, [searchInCategory, categoriesSorted]);

  // Flat, citation-numbered list across every category.
  const allRows = useMemo<SourceRow[]>(() => {
    const rows: SourceRow[] = [];
    let citation = 1;
    for (const cat of orderedCategories) {
      for (const item of searchInCategory[cat] ?? []) {
        rows.push({ citation: citation++, category: cat, item });
      }
    }
    return rows.sort((a, b) =>
      (b.item.news_sub_page?.when_crawled ?? "").localeCompare(
        a.item.news_sub_page?.when_crawled ?? ""
      )
    );
  }, [orderedCategories, searchInCategory]);

  const rows = useMemo(
    () =>
      category === "__all__"
        ? allRows
        : allRows.filter((row) => row.category === category),
    [allRows, category]
  );

  if (!orderedCategories.length) return null;

  return (
    <section className="panel animate-fade-up rounded-2xl px-5 py-5 sm:px-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex h-6 items-center rounded-md bg-teal-50 px-2 text-xs font-medium text-teal-800">
              03
            </span>
            <h3 className="text-base font-semibold text-slate-900">
              {t(lang, "material_title")}
            </h3>
            <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
              {allRows.length}
            </span>
          </div>
          <p className="mt-1.5 text-sm leading-relaxed text-slate-600">
            {t(lang, "material_hint")}
          </p>
        </div>

        <div className="flex self-start items-center gap-1 rounded-lg border border-slate-200 bg-slate-50 p-1">
          {(["wire", "list"] as ViewMode[]).map((mode) => (
            <button
              key={mode}
              onClick={() => setView(mode)}
              aria-pressed={view === mode}
              className={cn(
                "rounded-md px-3 py-1.5 text-sm transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700",
                view === mode
                  ? "bg-teal-50 font-medium text-teal-800"
                  : "text-slate-600 hover:bg-white hover:text-slate-900"
              )}
            >
              {mode === "wire" ? `⇢ ${t(lang, "view_wire")}` : `≡ ${t(lang, "view_list")}`}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-5 flex flex-col gap-5 lg:flex-row lg:items-start">
        <PolarityBar lang={lang} items={allRows.map((row) => row.item)} />

        <div className="flex flex-wrap gap-1.5 lg:ml-auto lg:max-w-[60%] lg:justify-end">
          <FilterChip
            label={t(lang, "all_categories")}
            count={allRows.length}
            active={category === "__all__"}
            onClick={() => setCategory("__all__")}
          />
          {orderedCategories.map((cat) => (
            <FilterChip
              key={cat}
              label={cat}
              count={searchInCategory[cat].length}
              active={category === cat}
              onClick={() => setCategory(cat)}
            />
          ))}
        </div>
      </div>

      {view === "wire" ? (
        <div className="-mx-2 mt-5 flex snap-x snap-mandatory gap-3 overflow-x-auto px-2 pb-3">
          {rows.map((row) => (
            <WireCard key={row.citation} lang={lang} row={row} />
          ))}
        </div>
      ) : (
        <div className="mt-5 divide-y divide-slate-200 overflow-hidden rounded-xl border border-slate-200">
          {rows.map((row) => (
            <ListRow key={row.citation} lang={lang} row={row} />
          ))}
        </div>
      )}
    </section>
  );
}

function FilterChip({
  label,
  count,
  active,
  onClick,
}: {
  label: string;
  count: number;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={cn(
        "rounded-full border px-3 py-1.5 text-[13px] transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-700",
        active
          ? "border-teal-200 bg-teal-50 text-teal-800"
          : "border-slate-200 bg-white text-slate-600 hover:border-teal-200 hover:text-teal-800"
      )}
    >
      {label}
      <span className="ml-1.5 text-xs">{count}</span>
    </button>
  );
}

function WireCard({ lang, row }: { lang: Lang; row: SourceRow }) {
  const url = row.item.news_sub_page?.news_url ?? "";
  const date = formatCrawledDate(row.item.news_sub_page?.when_crawled ?? "");
  const meta = polarityMeta(row.item.polarity_3c);
  const excerpt = (row.item.generated_text ?? "").replace(/\s+/g, " ");

  return (
    <article className="group flex w-[290px] shrink-0 snap-start flex-col rounded-xl border border-slate-200 bg-white p-4 transition hover:border-teal-200">
      <div className="mb-2.5 flex items-center gap-2">
        <span className="inline-flex h-6 w-6 items-center justify-center rounded-md bg-teal-50 text-xs font-semibold text-teal-800">
          {String(row.citation).padStart(2, "0")}
        </span>
        <span className="truncate text-xs text-slate-600">
          {hostOf(url)}
        </span>
        <span
          className={cn("ml-auto h-2 w-2 shrink-0 rounded-full", meta.dot)}
          title={t(lang, meta.key)}
          role="img"
          aria-label={t(lang, meta.key)}
        />
      </div>

      <p className="line-clamp-4 text-sm leading-relaxed text-slate-600">
        {excerpt}
      </p>

      <div className="mt-auto flex items-center justify-between gap-2 pt-3">
        <span className="text-xs text-slate-600">{date}</span>
        <a
          href={url}
          target="_blank"
          rel="noreferrer noopener"
          className="shrink-0 text-xs font-medium text-teal-700 transition hover:text-teal-800 hover:underline"
        >
          {t(lang, "open_source")} ↗
        </a>
      </div>
    </article>
  );
}

function ListRow({ lang, row }: { lang: Lang; row: SourceRow }) {
  const url = row.item.news_sub_page?.news_url ?? "";
  const date = formatCrawledDate(row.item.news_sub_page?.when_crawled ?? "");
  const meta = polarityMeta(row.item.polarity_3c);
  const excerpt = (row.item.generated_text ?? "").replace(/\s+/g, " ");

  return (
    <article className="group flex items-start gap-3 bg-white px-4 py-4 transition hover:bg-slate-50">
      <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-teal-50 text-xs font-semibold text-teal-800">
        {String(row.citation).padStart(2, "0")}
      </span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600">
          <span>{date}</span>
          <span className="text-slate-400">·</span>
          <span className="truncate">
            {hostOf(url)}
          </span>
          <span className="text-slate-400">·</span>
          <span className={meta.color}>{t(lang, meta.key)}</span>
        </div>
        <p className="mt-1 line-clamp-2 text-sm leading-relaxed text-slate-600">
          {excerpt}
        </p>
      </div>
      <a
        href={url}
        target="_blank"
        rel="noreferrer noopener"
        aria-label={`${t(lang, "open_source")}: ${hostOf(url)}`}
        className="shrink-0 rounded-lg border border-slate-200 px-2.5 py-1 text-sm text-teal-700 transition hover:border-teal-200 hover:bg-teal-50 hover:text-teal-800"
      >
        ↗
      </a>
    </article>
  );
}
