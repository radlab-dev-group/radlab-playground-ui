"use client";

import { t, type Lang } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export type PipelinePhase = "idle" | "searching" | "generating" | "done" | "error";

interface PipelineProps {
  lang: Lang;
  phase: PipelinePhase;
  stepLabel: string | null;
}

const STEP_KEYS = ["step_query", "step_search", "step_index", "step_gen"];

/**
 * A horizontal "broadcast pipeline" that visualises the RAG flow:
 * query -> search -> match -> generate.
 */
export function Pipeline({ lang, phase, stepLabel }: PipelineProps) {
  const activeIndex =
    phase === "idle" ? -1
    : phase === "searching" ? 1
    : phase === "generating" ? 3
    : phase === "done" ? 4
    : 0;

  return (
    <div className="panel rounded-2xl px-5 py-4">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {STEP_KEYS.map((key, idx) => {
          const reached = activeIndex >= idx;
          const current =
            (idx === 1 && phase === "searching") ||
            (idx === 3 && phase === "generating") ||
            (idx === 2 && phase === "generating");
          return (
            <div key={key} className="flex min-w-0 items-center gap-2">
              <div
                className={cn(
                  "flex h-7 w-7 shrink-0 items-center justify-center rounded-full border text-xs font-medium transition-colors",
                  reached
                    ? "border-teal-200 bg-teal-50 text-teal-800"
                    : "border-slate-200 bg-slate-50 text-slate-600"
                )}
              >
                {phase === "done" && reached ? "✓" : idx + 1}
              </div>
              <div className="min-w-0 flex-1">
                <div
                  className={cn(
                    "text-xs font-medium leading-relaxed transition-colors sm:text-sm",
                    reached ? "text-teal-800" : "text-slate-600"
                  )}
                >
                  {t(lang, key)}
                </div>
                <div aria-hidden="true" className="mt-1 h-0.5 w-full overflow-hidden rounded bg-slate-200">
                  <div
                    className={cn(
                      "h-full rounded bg-teal-600 transition-all duration-700",
                      current ? "w-full motion-safe:animate-pulse" : reached ? "w-full" : "w-0"
                    )}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
      {stepLabel && (
        <div role="status" className="mt-3 flex items-start gap-2 text-sm text-teal-700">
          <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600" />
          <span className="min-w-0 break-words">{stepLabel}</span>
        </div>
      )}
    </div>
  );
}
