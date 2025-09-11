# radlab-playground-ui

radlab‑playground‑ui is a Streamlit‑based interactive playground that lets users explore graphs,
browse generated news, interact with generative chat models, and monitor system status.

All UI elements are localisation‑aware, so the interface can be presented
in multiple languages with a single configuration step.

All interactions are performed through a set of thin wrapper APIs (`src/api_public.py`)
that communicate with the backend services. The interface is fully configurable
via JSON and Excel files, making it easy to adapt to new languages, logos, or data sources.

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
