# Women in U.S. Politics: 2024–2026

🚧 **Work in progress**

An exploratory project on women's representation in U.S. politics, focusing on Congress and comparisons across states and political parties in 2024 and 2026.

The analysis uses Python, pandas, and Plotly. Data cleaning, comparisons, and maps are still being developed, so results are preliminary and the notebook may not yet run from start to finish.

## Project files

- [`notebooks/EDA.ipynb`](notebooks/EDA.ipynb): main analysis notebook.
- [`index.html`](index.html): browser dashboard with view, party, and state filters.
- [`app.py`](app.py): generates the HTML from the local datasets.
- [`dashboard.html`](dashboard.html): dashboard template, including layout, filters, and map interactions.
- [`assets/data4women_logo_dark.png`](assets/data4women_logo_dark.png): Data4Women logo, displayed at the top right and embedded in the generated HTML.
- `data/`: local datasets and exports.
- `data/metadata.json`: shared data update date (`last_update`) displayed in the app and EDA notebook. Update this value when refreshing the data.
- `notebooks/*.png`: exploratory maps.

## Getting started

Open [`index.html`](index.html) directly in your browser. No Python server or Streamlit is required to use the dashboard. The filters, summary, and table work offline; the map requires internet access to load geographic boundaries. Plotly and the aggregated state data are embedded in the generated HTML.

On macOS, you can also open it from the project directory:

```bash
open index.html
```

The header displays the Data4Women logo, the author credit **By: Loreto**, and the last update from `data/metadata.json`.

The view selector switches between the share of all House seats held by women in the 2026 dataset and the change in the number of women between 2024 and 2026. Party and state filters update the summary, map, and table together. The percentage denominator includes all seats in the selected states, regardless of party.

The map supports zoom from **1× to 3×**. Its center is constrained around the U.S. region, with more movement allowed as you zoom in. At 1×, the center stays fixed. Use **Reset map** to return to the initial view. These interaction limits have been checked programmatically; browser interaction still needs visual verification.

## Updating the dashboard

Generation requires Python 3.14+ and [uv](https://docs.astral.sh/uv/). The dashboard reads these local files:

- `data/1976-2024-house.tab`: 2024 House districts, used for state seat totals; Washington, D.C. is excluded.
- `data/women_candidates_2024.xlsx`, sheet `Data`: women with office `U.S. Rep.` and general election result `W`.
- `data/2026 Women congress.xlsx`, sheet `Data`: women with office `U.S. Representative`.
- `data/metadata.json`: update date shown in the header.

The 2026 seat totals use the 2024 apportionment. Women are deduplicated by state, first name, last name, and party before counting.

After changing the source data, update `last_update` in `data/metadata.json` and regenerate the HTML:

```bash
uv run python app.py
```

Regenerate after editing `dashboard.html` or replacing the logo as well. Reopen or reload `index.html` to see the changes. The generated file embeds Plotly, aggregated state data, and the logo, so it can be shared on its own; map boundaries still require internet access.

## Analysis notebook

To open the notebook:

```bash
uv sync --dev
uv run jupyter lab
```

Open `notebooks/EDA.ipynb` using the project environment. The notebook expects `notebooks/` as its working directory to load data from `../data`.

## Data sources

Women's representation and candidate data come from the **Center for American Women and Politics (CAWP), Eagleton Institute of Politics, Rutgers University**:

- CAWP. [*Women in the 120th Congress*](https://cawp.rutgers.edu/candidates-2026-election-results-tracker/women-120th-congress).
- CAWP. [*Women Elected Officials Database — By Party*](https://cawp.rutgers.edu/data/women-elected-officials-database?tab=ByParty).
- CAWP. [*Women Candidates in 2026 — Candidate List*](https://cawp.rutgers.edu/data/candidates-women-candidates-2026?tab=CandidateList).
- CAWP. [*Women Candidates in 2026 — Rebound Candidates*](https://cawp.rutgers.edu/data/candidates-women-candidates-2026?tab=ReboundCandidates).
- CAWP. [*2024 Summary of Women Candidates*](https://cawp.rutgers.edu/data/candidates-election-results-and-analysis-0/2024-summary-women-candidates).

Election returns are hosted on **Harvard Dataverse**:

- MIT Election Data and Science Lab. 2017. *U.S. House 1976–2024*. Harvard Dataverse, V15. [doi:10.7910/DVN/IG0UN2](https://doi.org/10.7910/DVN/IG0UN2). The local file is `1976-2024-house.tab`; its download version has not been confirmed.
- Senate data (`senate_2022.csv`): [Harvard Dataverse, file ID 7412054, version 3.0](https://dataverse.harvard.edu/file.xhtml?fileId=7412054&version=3.0). Full dataset citation and coverage are still to be verified.

References reviewed on November 5, 2026. CAWP's live data may change as election results and officeholder records are updated. Candidate lists and elected-member counts need to be distinguished when making comparisons.

## Website synchronization

After a PR is merged into `main`, `.github/workflows/sync-dashboard.yml` copies the generated `index.html` to `data4women-org/data4women-org.github.io` and commits it only if changed. Include the regenerated HTML in the PR. Direct pushes and unmerged PR closures do not synchronize the website; no scheduled job runs.

Set the Actions secret `WEBSITE_SYNC_TOKEN` to a fine-grained token limited to the website repository with Contents read/write permission. Its owner must be allowed to push to the website's `main`. The website deployment workflow must already be on `main` and GitHub Pages must use GitHub Actions. See the website README for activation steps. The workflow handles only the committed HTML; it does not execute source Python code.
