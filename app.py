import base64
import json
from pathlib import Path

import pandas as pd
from plotly.offline import get_plotlyjs

DATA = Path(__file__).resolve().parent / "data"
STATE = "State"
STATE_NAME = "State Name"
WOMEN_2024 = "Women in 2024"
WOMEN_2026 = "Women in 2026"
SEATS = "Seats in 2026"
PERCENT = "Women in 2026 (%)"
CHANGE = "Difference (2026 − 2024)"
PARTIES = {"All": None, "Democratic": "D", "Republican": "R"}


def load_data(party=None, seats_column=SEATS):
    results = pd.read_csv(
        DATA / "1976-2024-house.tab",
        usecols=["year", "state", "state_po", "district"],
    )
    seats = (
        # DC has a representative, but a special one, not a state representative, so we exclude it from the count of seats.
        results.loc[(results["year"] == 2024) & (results["state_po"] != "DC")]
        .drop_duplicates(["state_po", "district"])
        .groupby("state_po")
        .agg(**{seats_column: ("district", "size"), STATE_NAME: ("state", "first")})
    )

    candidates = pd.read_excel(DATA / "women_candidates_2024.xlsx", sheet_name="Data")
    women_2024 = candidates.loc[
        candidates["Office"].eq("U.S. Rep.")
        & candidates["General Election Result"].eq("W")
    ]

    congress = pd.read_excel(DATA / "2026 Women congress.xlsx", sheet_name="Data")

    women_2026 = congress.loc[congress["Office"].eq("U.S. Representative")]

    keys = ["State", "First Name", "Last Name", "Party"]

    states = seats.copy()
    for label, rows in [(WOMEN_2024, women_2024), (WOMEN_2026, women_2026)]:
        if party is not None:
            rows = rows.loc[rows["Party"].eq(party)]
        counts = rows.drop_duplicates(keys).groupby("State").size()
        states[label] = counts.reindex(states.index, fill_value=0)

    # Note: The number of seats by state in 2026 is the same as the 2024.
    states[PERCENT] = 100 * states[WOMEN_2026] / states[seats_column]
    states[CHANGE] = states[WOMEN_2026] - states[WOMEN_2024]
    return states.rename_axis(STATE).reset_index()


def main():
    """Build a browser-only dashboard with embedded data and Plotly."""
    payload = {
        party: load_data(code).to_dict(orient="records")
        for party, code in PARTIES.items()
    }
    metadata = json.loads((DATA / "metadata.json").read_text(encoding="utf-8"))
    template = (Path(__file__).parent / "dashboard.html").read_text(encoding="utf-8")
    html = template.replace("/* PLOTLY_LIBRARY */", get_plotlyjs())
    html = html.replace("/* DASHBOARD_DATA */", json.dumps(payload).replace("<", "\\u003c"))
    html = html.replace("/* METADATA */", json.dumps(metadata).replace("<", "\\u003c"))
    logo = Path(__file__).parent / "assets" / "data4women_logo_dark.png"
    logo_uri = "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode("ascii")
    html = html.replace("assets/data4women_logo_dark.png", logo_uri)
    output = Path(__file__).parent / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"Created {output}")


if __name__ == "__main__":
    main()
