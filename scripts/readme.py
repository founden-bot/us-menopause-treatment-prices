"""Writes README.md from the dataset files in data/ (run by the daily refresh workflow).

Every figure in the README is counted from the files themselves, so the README never says more than the data holds.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def rows_of(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


prices = json.loads((DATA / "menopause-treatment-prices.json").read_text(encoding="utf-8"))
rows = prices["prices"]
services = sorted({r["service"] for r in rows})
treatments = {}
for r in rows:
    v = r.get("cost_per_30_days_with_membership_usd")
    if v is None:
        continue
    t = treatments.setdefault(r["treatment"], [])
    t.append(v)
pharmacy = rows_of("menopause-pharmacy-costs.csv")
labels = rows_of("menopause-label-status.csv")
payers = rows_of("menopause-prescriptions-by-state.csv")
insurers = rows_of("menopause-insurer-drug-lists.csv") if (DATA / "menopause-insurer-drug-lists.csv").exists() else []
tools_file = DATA / "mcp-tools.json"
TOOLS = json.loads(tools_file.read_text(encoding="utf-8")) if tools_file.exists() else []
weeks = sorted({r["week_as_of"] for r in pharmacy if r.get("week_as_of")})


def usd(v):
    return f"${v:,.0f}" if v >= 10 else f"${v:,.2f}"


lines = [
    "# US online menopause treatment prices",
    "",
    "What US online menopause services charge for menopause hormone therapy and non-hormonal hot flash prescriptions,",
    "and what US pharmacies pay for the same medicines. Every service price is read on the service's own page, in its own",
    "words, with the day it was read and the page it was read on.",
    "",
    f"This repository is a daily copy of the open dataset published at **[menocost.com/data]({prices['url']})**, where the",
    "same prices are shown service by service and treatment by treatment, with each one's check date.",
    "",
    "## What is in it",
    "",
    "| File | What it holds | Rows |",
    "|---|---|---|",
    f"| `data/menopause-treatment-prices.csv` (and `.json` with the column guide) | Self-pay prices at {len(services)} online services | {len(rows):,} |",
    f"| `data/menopause-pharmacy-costs.csv` | What US pharmacies pay per unit (CMS NADAC), week by week{f', {weeks[0]} to {weeks[-1]}' if weeks else ''} | {len(pharmacy):,} |",
    f"| `data/menopause-label-status.csv` | FDA labels of menopause hormone products (DailyMed) | {len(labels):,} |",
    f"| `data/menopause-prescriptions-by-state.csv` | What Medicaid and Medicare drug plans paid for menopause medicines, by state (CMS) | {len(payers):,} |",
] + ([f"| `data/menopause-insurer-drug-lists.csv` | Menopause medicines on insurers' own drug lists (Aetna, Anthem, UnitedHealthcare, Kaiser, FEP Blue, Oscar, Cigna) and TRICARE's rules | {len(insurers):,} |"] if insurers else []) + [
    "",
    f"Prices last read: **{prices.get('date_modified', 'see the file')}**.",
    "",
    "## Lowest 30-day cost by treatment",
    "",
    "Lowest and middle price for 30 days of each treatment, with any membership the service charges on top, across the",
    "services that publish one. Starting prices (\"from\") count as published.",
    "",
    "| Treatment | Services with a price | Lowest | Middle |",
    "|---|---|---|---|",
]
# Each treatment's page on menocost.com, where every price is listed with its check date and terms.
PAGES = {
    "Estradiol patch": "estradiol-patch", "Estradiol gel or spray": "estradiol-gel", "Estradiol pill": "estradiol-pill",
    "Vaginal estrogen": "vaginal-estrogen", "Progesterone": "progesterone", "Estrogen and progesterone together": "combined-hrt",
    "Compounded hormones": "compounded-hormones", "Testosterone for women": "testosterone-women",
    "Veozah (fezolinetant)": "fezolinetant", "Lynkuet (elinzanetant)": "elinzanetant", "Low-dose paroxetine": "paroxetine",
}
for name, vals in sorted(treatments.items(), key=lambda kv: min(kv[1])):
    vals = sorted(vals)
    mid = vals[len(vals) // 2] if len(vals) % 2 else (vals[len(vals) // 2 - 1] + vals[len(vals) // 2]) / 2
    label = f"[{name}](https://menocost.com/treatments/{PAGES[name]})" if name in PAGES else name
    lines.append(f"| {label} | {len(vals)} | {usd(vals[0])} | {usd(mid)} |")
lines += [
    "",
    "The cheapest option for each treatment, with the service and its terms, is on",
    "[menocost.com](https://menocost.com/cheapest-hrt-online). What HRT costs per month, with and without insurance, is",
    "answered on [How much does HRT cost?](https://menocost.com/costs/how-much-does-hrt-cost) and",
    "[The cheapest way to get HRT without insurance](https://menocost.com/costs/cheapest-way-to-get-hrt).",
    "",
    "## Columns of the price file",
    "",
    "| Column | Meaning |",
    "|---|---|",
]
for c in prices["columns"]:
    lines.append(f"| `{c['name']}` | {c['description'].replace('|', '/')} |")
lines += [
    "",
    "## How the prices are read",
    "",
    "- Each price is read on the selling service's own page, never from a review site or a search snippet. A fact the page",
    "  does not state is left empty.",
    "- A daily check re-reads every cited page and flags a price that left its page; flagged prices are read again, and",
    "  every price is read again within 30 days. `checked_on` is the day a person read the price, `still_on_page_on` the",
    "  day the check last found it on the page.",
    "- `price_usd_30_days` is the page's own monthly price, or a supply price divided to 30 days when",
    "  `price_is_calculated` is `yes`.",
    "",
    "## Ask an AI assistant: the price server (MCP)",
    "",
    "The same records answer AI assistants through a public, read-only [Model Context Protocol](https://modelcontextprotocol.io)",
    "server. No key, no sign-up. Add it to any MCP client that takes a remote server:",
    "",
    "```json",
    '{ "mcpServers": { "menocost": { "type": "http", "url": "https://menocost.com/api/mcp" } } }',
    "```",
    "",
    "It is listed in the Official MCP Registry as `com.menocost/menopause-prices`. Its tools:",
    "",
] + [f"- `{t['name']}`: {t['description'].split('. ')[0].rstrip('.')}." for t in TOOLS] + [
    "",
    "## License and citation",
    "",
    f"{prices['license']['name']}: free to share and adapt, with credit. Cite it as:",
    "",
    f"> {prices['attribution']}",
    "",
    "Archived versions with a DOI are on [Zenodo](https://doi.org/10.5281/zenodo.24293626); the same data is on",
    "[Hugging Face](https://huggingface.co/datasets/menocost/us-menopause-treatment-prices). A report on these prices,",
    "*What US online menopause services charge for hormone therapy* (November 2026), is",
    "[doi:10.5281/zenodo.24558133](https://doi.org/10.5281/zenodo.24558133).",
    "",
    "Prices change: before acting on one, open the service's page in `source_url`. Nothing here is medical advice.",
    "",
]
(ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"README.md written: {len(rows)} prices, {len(services)} services")
