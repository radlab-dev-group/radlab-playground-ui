"use client";

import { useMemo, useState } from "react";

import { t, type Lang } from "@/lib/i18n";
import { renderMarkdown, splitHeadline } from "@/lib/markdown";
import { formatWhen, readingMinutes, wordCount } from "@/lib/utils";
import type { ArticleResponse } from "@/lib/types";

interface ArticleResultProps {
  lang: Lang;
  article: ArticleResponse;
  numberOfNewsUsed: number;
  query: string;
}

/**
 * The generated article, presented as the hero of the page (editorial sheet).
 * Port of call_generate_article_api_and_show_response +
 * add_technical_info_for_gen_full_article, with the Markdown title promoted to
 * a real headline.
 */
export function ArticleResult({
  lang,
  article,
  numberOfNewsUsed,
  query,
}: ArticleResultProps) {
  const [copied, setCopied] = useState(false);

  const text = article.article_str ?? article.article ?? article.new_article ?? "";

  const parsed = useMemo(() => splitHeadline(text), [text]);
  const blocks = useMemo(() => renderMarkdown(parsed.body), [parsed.body]);

  const stats = useMemo(
    () => ({
      words: wordCount(text),
      minutes: readingMinutes(text),
      when: formatWhen(article.when_generated),
      time:
        article.generation_time !== undefined
          ? String(article.generation_time)
          : "—",
      model: article.model_used_to_generate ?? "—",
    }),
    [article, text]
  );

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      /* clipboard unavailable */
    }
  }

  function handleDownload() {
    const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `radlab-article-${Date.now()}.md`;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="panel panel-glow animate-fade-up relative overflow-hidden rounded-2xl">
      <div className="relative flex flex-col gap-3 border-b border-slate-200 bg-slate-50/60 px-5 py-4 sm:flex-row sm:items-center sm:px-8">
        <span className="inline-flex h-7 w-fit items-center rounded-md bg-teal-50 px-2 text-xs font-medium text-teal-700">
          02
        </span>
        <h3 className="text-base font-semibold text-slate-900">
          {t(lang, "article_title")}
        </h3>
        <div className="flex flex-wrap items-center gap-2 sm:ml-auto">
          <button
            onClick={handleCopy}
            className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-teal-800 transition hover:border-teal-300 hover:bg-teal-50"
          >
            {copied ? `✓ ${t(lang, "copied")}` : `⧉ ${t(lang, "copy")}`}
          </button>
          <button
            onClick={handleDownload}
            className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-teal-800 transition hover:border-teal-300 hover:bg-teal-50"
          >
            ↓ {t(lang, "download")}
          </button>
        </div>
      </div>

      <div className="relative mx-auto max-w-[78ch] px-5 py-8 sm:px-10 sm:py-10">
        <div className="mb-5 flex flex-wrap items-center gap-x-3 gap-y-2 text-xs">
          <span className="inline-flex items-center gap-2 rounded-full bg-teal-50 px-3 py-1.5 text-teal-800">
            <span className="h-1.5 w-1.5 rounded-full bg-teal-600" />
            {t(lang, "article_onair")}
          </span>
        </div>

        {parsed.headline ? (
          <h2 className="mb-6 break-words font-editorial text-3xl leading-[1.2] tracking-tight text-slate-900 sm:text-[42px]">
            {parsed.headline}
          </h2>
        ) : null}

        <div className="mb-8 flex flex-wrap items-center gap-x-3 gap-y-2 border-y border-slate-200 py-4 text-xs leading-relaxed text-slate-600">
          <span>
            <span>{stats.when}</span>
          </span>
          <span className="text-slate-300">·</span>
          <span>
            {t(lang, "based_on")}{" "}
            <span className="font-medium text-teal-800">{numberOfNewsUsed}</span>{" "}
            {t(lang, "sources_used")}
          </span>
          <span className="text-slate-300">·</span>
          <span>
            <span>{stats.words}</span>{" "}
            {t(lang, "word_count")}
          </span>
          <span className="text-slate-300">·</span>
          <span>
            <span>{stats.minutes}</span>{" "}
            {t(lang, "reading_time")}
          </span>
        </div>

        <article className="article-body max-w-[65ch] text-slate-700">
          {blocks.length > 0 ? (
            blocks
          ) : (
            <p className="text-[15px] text-slate-500">
              {text || t(lang, "article_empty")}
            </p>
          )}
        </article>

        <div className="mt-10 flex flex-wrap gap-x-5 gap-y-2 border-t border-slate-200 pt-4 text-xs leading-relaxed text-slate-500">
          <span>{t(lang, "gen_model")}: {stats.model}</span>
          <span>{t(lang, "gen_time")}: {stats.time}</span>
        </div>
        <p className="mt-3 break-words text-xs leading-relaxed text-slate-500">
          RAG · {query.slice(0, 110)}
          {query.length > 110 && "…"}
        </p>
      </div>
    </section>
  );
}
