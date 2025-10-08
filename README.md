# radlab-playground-ui

radlab‑playground‑ui is a Streamlit‑based interactive playground that lets users explore information,
browse generated summaries, interact with generative chat models, and monitor system status.

The interface is fully localisation‑aware, supporting multiple languages out‑of‑the‑box, 
and is publicly available at https://playground.radlab.dev.


All interactions are performed through a set of thin wrapper APIs (`src/api_public.py`)
that communicate with the backend services. The interface is fully configurable
via JSON and Excel files, making it easy to adapt to new languages, logos, or data sources.

---  

## Pages Overview

The **`streamlit_ui/pages/`** directory contains the individual Streamlit pages that make up the UI. Below is a short
description of each page:

| File                 | Description                                                                                                                    |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `administration.py`  | Administrative tools for system settings, and monitoring backend health.                                                       |
| `creator_actual.py`  | Interface for creating article from indexed summaries based on the user query (RAG)                                            |
| `home.py`            | The landing page that introduces the playground, provides quick links to all other sections, and displays general information. |
| `info_explorator.py` | Explores informational graphs, showing examples, explanations, and how the explorer works.                                     |
| `news_browser.py`    | Browse generated items, filter by topics or dates, and view full articles.                                                     |
| `news_stream.py`     | Real‑time news indexing mechanism, showing the latest generated headlines and summaries.                                       |
| `public_chat.py`     | Public chat interface that connects to the generative chat model for interactive conversations.                                |
| `statistics.py`      | Displays statistics, metrics.                                                                                                  |

---  

## Running the Interface

The UI is deployed and can be accessed publicly at:

**https://playground.radlab.dev**

Visit the URL above to explore the playground without any local setup.

---

## Installation

1. **Prerequisites**
    * Python >= 3.9
    * `git` (to clone the repo)

2. **Clone the repository**

```shell script
git clone https://github.com/your-org/radlab-playground-ui.git
   cd radlab-playground-ui
```

3. **Create a virtual environment (optional but recommended)**

```shell script
python -m venv .venv
source .venv/bin/activate\
```

4. **Install dependencies**

```shell script
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Verify the resources**

    * `resources/configs/ui-configuration.json` – UI defaults.
    * `resources/language/ui_lang_def.xlsx` – translation strings.
    * `resources/images/` – logos and graphics used throughout the UI.

If you need to customise any of these files, edit them directly; the UI reads them at start‑up.

---  

## Running the app

The repository ships a tiny wrapper script that launches Streamlit with the correct entry point:

```shell script
./run.sh
```

`run.sh` simply executes:

```shell script
streamlit run streamlit_ui/app.py
```

You can also start the app manually:

```shell script
streamlit run streamlit_ui/app.py
```
