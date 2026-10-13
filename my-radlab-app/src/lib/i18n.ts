export type Lang = "pl" | "en";

export const LANGS: { code: Lang; label: string; flag: string }[] = [
  { code: "pl", label: "Polski", flag: "🇵🇱" },
  { code: "en", label: "English", flag: "🇬🇧" },
];

type Dict = Record<string, { pl: string; en: string }>;

/**
 * Strings ported from streamlit_ui/resources/language/ui_lang_def.xlsx
 * (keys act_creator_*, list_of_found_* and a few app-level labels).
 */
const DICT: Dict = {
  app_title: { pl: "Puls Informacji", en: "Puls Informacji" },
  app_tagline: {
    pl: "Co słychać teraz?",
    en: "What’s happening now?",
  },
  intro_eyebrow: { pl: "Mniej szukania, więcej wiedzy", en: "Less searching, more understanding" },
  intro_title: { pl: "Co chcesz dziś wiedzieć?", en: "What would you like to know today?" },
  intro_description: {
    pl: "Wybierz temat. Zbierz aktualne wiadomości z wielu źródeł w jeden czytelny artykuł. Źródła znajdziesz tuż pod tekstem.",
    en: "Choose a topic. Bring current news from multiple sources together in one easy-to-read article. You’ll find the sources just below the text.",
  },
  live_badge: { pl: "INDEKS AKTYWNY", en: "INDEX LIVE" },
  index_note: {
    pl: "News ze Strumienia Aktualności trafia do indeksu po ok. 10 minutach",
    en: "News from the stream lands in the index after ~10 minutes",
  },

  // What is (sidebar expander in streamlit)
  what_is_title: {
    pl: "Czym jest Puls Informacji?",
    en: "What is Puls Informacji?",
  },
  what_is_desc: {
    pl: "**Kreator Aktualności**, to pod spodem system oparty o **RAG**. Działa na zasadach wyszukiwarki, gdzie na zadane przez użytkownika pytanie generowana jest odpowiedź przez model generatywny. Odpowiedź kreowana jest w oparciu o **dostarczone** przez **wyszukiwarkę newsy**, ograniczając przy tym _halucynację_ modeli gen AI. W Kreatorze **nie korzystamy z zewnętrznych API** do przeszukiwania. Bazujemy na **własnym indeksie** przeszukiwaniowemu analizowanych przez nas stron.",
    en: "**News Creator** is a system based on **RAG**. It works like a search engine, where a generative model generates a response to a user's query. The response is created based on **news provided** by the **search engine**, thereby limiting the _hallucination_ of gen AI models. In the Creator, **we do not use external API** for searching. We rely on our **own search index** of the pages we analyze.",
  },

  // Query panel
  query_label: {
    pl: "O czym chcesz przeczytać?",
    en: "What would you like to read about?",
  },
  query_placeholder: {
    pl: "Na przykład: Co nowego w świecie technologii i sztucznej inteligencji?",
    en: "For example: What’s new in technology and artificial intelligence?",
  },
  style_label: {
    pl: "Styl generowanego artykułu",
    en: "Style of the generated article",
  },
  style_simple: {
    pl: "Zrozumiała dla każdego",
    en: "Understandable to everyone",
  },
  style_formal: {
    pl: "Formalny język",
    en: "Formal language",
  },
  last_days_label: { pl: "Ostatnie dni", en: "Recent days" },
  btn_run: { pl: "Przygotuj artykuł", en: "Create article" },
  btn_edit_query: { pl: "Edytuj zapytanie", en: "Edit query" },
  btn_close_editor: { pl: "Zwiń", en: "Collapse" },
  btn_run_again: { pl: "Wygeneruj ponownie", en: "Generate again" },
  suggestions_title: {
    pl: "Szukasz inspiracji?",
    en: "Need some inspiration?",
  },
  suggestions_hint: {
    pl: "Wybierz jeden z tematów",
    en: "Choose one of these topics",
  },
  suggestions_refresh: { pl: "Losuj kolejne", en: "Draw again" },
  no_query_error: {
    pl: "Brak pytania! Należy najpierw wpisać pytanie!",
    en: "No question! You must enter a question first!",
  },
  model_prompt_p1: {
    pl: "Tworzona przez Ciebie treść musi być napisana",
    en: "The content you create must be written",
  },
  model_prompt_formal: {
    pl: "formalnym/urzędowym tonem.",
    en: "in a formal/official tone.",
  },
  model_prompt_simple: {
    pl: "bardzo prostym językiem, aby była zrozumiała dla wszystkich.",
    en: "in very simple language so that it is understandable to everyone.",
  },

  // Progress
  progress_search: {
    pl: "Trwa wyszukiwanie newsów związanych z zapytaniem...",
    en: "Searching for news related to your query...",
  },
  progress_gen: {
    pl: "Trwa kreowanie aktualności... na naszym sprzęcie może to chwilę potrwać (nawet 1-2 min)... :)",
    en: "Creating the article... on our hardware this may take a while (even 1-2 min)... :)",
  },
  progress_ready: { pl: "Gotowe!", en: "Ready!" },
  notice_title: { pl: "Informacja", en: "Notice" },
  no_data_found: {
    pl: "Nie odnaleziono nic w bazie!",
    en: "Nothing found in the database!",
  },
  api_error: {
    pl: "Wystąpił błąd połączenia z API. Sprawdź konfigurację i spróbuj ponownie.",
    en: "Connection error to the API. Check configuration and try again.",
  },

  // Results
  found_news_title: {
    pl: "Wykaz znalezionych newsów",
    en: "List of found news",
  },
  sources_title: {
    pl: "Zasięg wyszukiwania",
    en: "Search scope",
  },
  sources_scope_count: {
    pl: "Przeszukiwane serwisy informacyjne: {count}",
    en: "News sites searched: {count}",
  },
  sources_show: { pl: "Zobacz źródła", en: "View sources" },
  sources_hide: { pl: "Ukryj źródła", en: "Hide sources" },
  sources_hint: {
    pl: "Kategorie i źródła dostępne w Pulsie Informacji (wszystkie aktywne)",
    en: "Categories and sources available in Puls Informacji (all active)",
  },
  pages: { pl: "stron", en: "sites" },
  polarity_title: {
    pl: "Polaryzacja w dopasowanych newsach",
    en: "Polarization in matched news",
  },
  polarity_subtitle: {
    pl: "Polaryzacja 3c w dopasowanych newsach [procent]",
    en: "Polarization 3c in matched news [percent]",
  },
  pos: { pl: "pozytywny", en: "positive" },
  neg: { pl: "negatywny", en: "negative" },
  amb: { pl: " ambiwalentny", en: "ambivalent" },

  // Article result (hero)
  article_title: { pl: "Twój artykuł", en: "Your article" },
  article_onair: { pl: "Na podstawie wiadomości z indeksu", en: "Based on indexed news" },
  article_empty: {
    pl: "Model nie zwrócił treści spróbuje ponownie za chwilę.",
    en: "The model returned no content — please try again in a moment.",
  },
  based_on: { pl: "Na podstawie", en: "Based on" },
  sources_used: { pl: "dopasowanych newsów", en: "matched news items" },

  // Source material (wire)
  material_title: { pl: "Źródła do artykułu", en: "Article sources" },
  material_hint: {
    pl: "Wiadomości dopasowane do Twojego tematu i przekazane do przygotowania artykułu — nie lista wszystkich przeszukiwanych serwisów.",
    en: "News matched to your topic and supplied to create the article — not the list of all sites searched.",
  },
  view_wire: { pl: "Przegląd", en: "Wire" },
  view_list: { pl: "Lista", en: "List" },
  no_polarity: { pl: "brak klasyfikacji", en: "unclassified" },
  all_categories: { pl: "Wszystkie", en: "All" },
  when_generated: {
    pl: "Wygenerowano w dniu",
    en: "Generated on",
  },
  gen_time: {
    pl: "Czas generowania (s)",
    en: "Generation time (s)",
  },
  gen_model: { pl: "Model generujący", en: "Generating model" },
  news_used: {
    pl: "Liczba dopasowanych newsów",
    en: "Number of matching news items",
  },
  word_count: { pl: "słów", en: "words" },
  reading_time: { pl: "min czytania", en: "min read" },
  copy: { pl: "Kopiuj", en: "Copy" },
  copied: { pl: "Skopiowano!", en: "Copied!" },
  download: { pl: "Pobierz .md", en: "Download .md" },
  open_source: { pl: "Otwórz źródło", en: "Open source" },

  // Pipeline steps
  step_query: { pl: "Zapytanie", en: "Query" },
  step_search: { pl: "Wyszukiwanie", en: "Search" },
  step_index: { pl: "Dopasowanie", en: "Matching" },
  step_gen: { pl: "Generowanie", en: "Generation" },

  // Footer
  footer_note: {
    pl: "Puls Informacji by RadLab — aktualne wiadomości na Twój temat",
    en: "Puls Informacji by RadLab — current news on your topic",
  },
  loading_categories: {
    pl: "Ładowanie indeksu źródeł...",
    en: "Loading source index...",
  },
  categories_error: {
    pl: "Nie udało się pobrać kategorii źródeł.",
    en: "Failed to load source categories.",
  },
  all_sources_active: {
    pl: "wszystkie źródła aktywne",
    en: "all sources active",
  },
};

export function t(lang: Lang, key: string): string {
  const entry = DICT[key];
  if (!entry) return key;
  return entry[lang] ?? entry.pl;
}
