"use client";

import { useEffect, useMemo, useState } from "react";

import { Header } from "@/components/header";
import { QueryPanel, type ArticleStyle } from "@/components/query-panel";
import { SourcesPanel } from "@/components/sources-panel";
import { Pipeline, type PipelinePhase } from "@/components/pipeline";
import { SearchResults } from "@/components/search-results";
import { ArticleResult } from "@/components/article-result";
import { ArticleSkeleton } from "@/components/article-skeleton";

import {
  buildFilterPages,
  collectNewsIds,
  deriveNumOfResults,
  fetchCategoriesWithPages,
  generateArticle,
  searchNews,
} from "@/lib/api";
import { t, type Lang } from "@/lib/i18n";
import type {
  ArticleResponse,
  CategoriesWithPages,
  SearchInCategory,
} from "@/lib/types";

export default function CreatorPage() {
  const [lang, setLang] = useState<Lang>("pl");
  const [categories, setCategories] = useState<CategoriesWithPages | null>(null);
  const [categoriesLoading, setCategoriesLoading] = useState(true);
  const [categoriesError, setCategoriesError] = useState<string | null>(null);

  const [query, setQuery] = useState("");
  const [style, setStyle] = useState<ArticleStyle>("simple");
  const [lastDays, setLastDays] = useState(1);

  const [suggestions, setSuggestions] = useState<string[]>([]);

  const [phase, setPhase] = useState<PipelinePhase>("idle");
  const [stepLabel, setStepLabel] = useState<string | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [categoriesFailed, setCategoriesFailed] = useState(false);

  const [searchResult, setSearchResult] = useState<SearchInCategory | null>(null);
  const [article, setArticle] = useState<ArticleResponse | null>(null);
  const [numberOfNewsUsed, setNumberOfNewsUsed] = useState(0);

  const hasRun = searchResult !== null || article !== null;

  const categoriesErrorMessage = categoriesFailed
    ? categoriesError ?? t(lang, "categories_error")
    : null;

  const categoriesSorted = useMemo(
    () => (categories ? Object.keys(categories) : []),
    [categories]
  );

  const hasMatches = useMemo(
    () =>
      !!searchResult &&
      Object.values(searchResult).some((list) => list.length > 0),
    [searchResult]
  );

  // 1) Load the indexed categories + pages on mount
  //    (PublicNewsStreamAPI.list_available_categories_with_pages).
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const result = await fetchCategoriesWithPages();
      if (cancelled) return;
      if (result.ok && result.data) {
        setCategories(result.data);
      } else {
        setCategoriesError(result.error ?? null);
        setCategoriesFailed(true);
      }
      setCategoriesLoading(false);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // 2) Keep the document language in sync with the UI language switch.
  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  // 3) Draw the predefined queries (kreator-pytania.txt) server-side: a fresh
  //    random subset on every entry / refresh of the page.
  useEffect(() => {
    let cancelled = false;
    loadPredefinedQueries().then((queries) => {
      if (!cancelled && queries) setSuggestions(queries);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleShuffleSuggestions() {
    const queries = await loadPredefinedQueries();
    if (queries) setSuggestions(queries);
  }

  // 4) Run the full creator pipeline
  //    (show_creator_search_window -> search -> generate).
  async function handleCreate() {
    setApiError(null);
    setNotice(null);
    setSearchResult(null);
    setArticle(null);

    if (!categories) {
      setApiError(t(lang, "categories_error"));
      return;
    }

    const filterPages = buildFilterPages(categories);
    const numOfResults = deriveNumOfResults(0, lastDays);

    // --- search phase ---
    setPhase("searching");
    setStepLabel(t(lang, "progress_search"));

    const searchRes = await searchNews({
      query,
      filterPages,
      numOfResults,
      lastDays,
    });

    if (!searchRes.ok || !searchRes.data?.search_result) {
      setPhase("error");
      setStepLabel(null);
      setApiError(searchRes.error ?? t(lang, "api_error"));
      return;
    }

    const searchInCategory = searchRes.data.search_result;
    const queryResponseId = searchRes.data.query_response_id;
    setSearchResult(searchInCategory);

    const totalMatches = Object.values(searchInCategory).reduce(
      (sum, list) => sum + list.length,
      0
    );
    if (totalMatches === 0) {
      setPhase("idle");
      setStepLabel(null);
      setNotice(t(lang, "no_data_found"));
      return;
    }

    // --- generation phase ---
    setPhase("generating");
    setStepLabel(t(lang, "progress_gen"));

    const newsIds = collectNewsIds(searchInCategory);
    const articleType = buildArticlePrompt(lang, style);

    const genRes = await generateArticle({
      userQuery: query,
      newsIds,
      articleType,
      queryResponseId,
    });

    if (!genRes.ok || !genRes.data) {
      setPhase("error");
      setStepLabel(null);
      setApiError(genRes.error ?? t(lang, "api_error"));
      return;
    }

    setNumberOfNewsUsed(newsIds.length);
    setArticle(genRes.data);
    setPhase("done");
    setStepLabel(t(lang, "progress_ready"));
  }

  return (
    <div className="bg-controlroom min-h-screen">
      <Header lang={lang} onLangChange={setLang} indexReady={!!categories} />

      <main className="mx-auto max-w-4xl space-y-8 px-4 py-8 sm:px-6 sm:py-12">
        {!article && (
          <div className="max-w-2xl">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-teal-700">
              {t(lang, "intro_eyebrow")}
            </p>
            <h2 className="font-editorial text-4xl leading-tight tracking-tight text-slate-900 sm:text-5xl">
              {t(lang, "intro_title")}
            </h2>
            <p className="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg">
              {t(lang, "intro_description")}
            </p>
          </div>
        )}

        <div className="space-y-6">
          <div className="min-w-0 space-y-6">
            <QueryPanel
              lang={lang}
              query={query}
              onQueryChange={setQuery}
              style={style}
              onStyleChange={setStyle}
              lastDays={lastDays}
              onLastDaysChange={setLastDays}
              onSubmit={handleCreate}
              busy={phase === "searching" || phase === "generating"}
              error={apiError}
              hasRun={hasRun}
              suggestions={suggestions}
              onUseSuggestion={(value) => setQuery(value)}
              onShuffleSuggestions={handleShuffleSuggestions}
              collapsed={!!article}
            />

            <SourcesPanel
              lang={lang}
              categories={categories ?? undefined}
              loading={categoriesLoading}
              error={categoriesErrorMessage}
            />

            {notice && phase !== "error" && (
              <div className="animate-fade-up rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm text-amber-900">
                <div className="mb-1 font-semibold">
                  {t(lang, "notice_title")}
                </div>
                {notice}
              </div>
            )}

            {phase !== "idle" && !article && (
              <Pipeline lang={lang} phase={phase} stepLabel={stepLabel} />
            )}

            {/* 02 — the article is the hero: it renders first (top) */}
            {article ? (
              <ArticleResult
                lang={lang}
                article={article}
                numberOfNewsUsed={numberOfNewsUsed}
                query={query}
              />
            ) : phase === "generating" ? (
              <ArticleSkeleton lang={lang} label={stepLabel ?? t(lang, "progress_gen")} />
            ) : null}

            {/* 03 — supporting evidence sits below the article */}
            {hasMatches && searchResult && (
              <SearchResults
                lang={lang}
                searchInCategory={searchResult}
                categoriesSorted={categoriesSorted}
              />
            )}
          </div>
        </div>

        <footer className="border-t border-slate-200 pt-6">
          <div className="flex flex-col items-start justify-between gap-3 text-xs leading-relaxed text-slate-500 sm:flex-row sm:items-center">
            <span>{t(lang, "footer_note")}</span>
            <span className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600" />
              {t(lang, "index_note")}
            </span>
          </div>
        </footer>
      </main>
    </div>
  );
}

/**
 * Fetches the random predefined queries served by /api/predefined-queries.
 * Suggestions are a convenience, so any failure degrades to "no suggestions".
 */
async function loadPredefinedQueries(): Promise<string[] | null> {
  try {
    const response = await fetch("/api/predefined-queries", { cache: "no-store" });
    if (!response.ok) return null;
    const payload = (await response.json()) as { queries?: unknown };
    if (!Array.isArray(payload.queries)) return null;
    return payload.queries.filter((item): item is string => typeof item === "string");
  } catch {
    return null;
  }
}

/**
 * Builds the article_type prompt (port of the prompt assembly in
 * show_creator_search_window):
 *   p1 + ("formal..." | "simple...")
 */
function buildArticlePrompt(lang: Lang, style: ArticleStyle): string {
  const base = t(lang, "model_prompt_p1");
  const suffix =
    style === "formal" ? t(lang, "model_prompt_formal") : t(lang, "model_prompt_simple");
  return `${base} ${suffix}`;
}
