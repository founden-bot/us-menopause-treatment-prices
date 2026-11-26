# US online menopause treatment prices

What US online menopause services charge for menopause hormone therapy and non-hormonal hot flash prescriptions,
and what US pharmacies pay for the same medicines. Every service price is read on the service's own page, in its own
words, with the day it was read and the page it was read on.

This repository is a daily copy of the open dataset published at **[menocost.com/data](https://menocost.com/data)**, where the
same prices are shown service by service and treatment by treatment, with each one's check date.

## What is in it

| File | What it holds | Rows |
|---|---|---|
| `data/menopause-treatment-prices.csv` (and `.json` with the column guide) | Self-pay prices at 75 online services | 275 |
| `data/menopause-pharmacy-costs.csv` | What US pharmacies pay per unit (CMS NADAC), week by week, 2026-01-07 to 2026-11-18 | 4,609 |
| `data/menopause-label-status.csv` | FDA labels of menopause hormone products (DailyMed) | 271 |
| `data/menopause-prescriptions-by-state.csv` | What Medicaid and Medicare drug plans paid for menopause medicines, by state (CMS) | 3,218 |
| `data/menopause-insurer-drug-lists.csv` | Menopause medicines on insurers' own drug lists (Aetna, Anthem, UnitedHealthcare, Kaiser, FEP Blue, Oscar, Cigna) and TRICARE's rules | 165 |

Prices last read: **2026-11-24**.

## Lowest 30-day cost by treatment

Lowest and middle price for 30 days of each treatment, with any membership the service charges on top, across the
services that publish one. Starting prices ("from") count as published.

| Treatment | Services with a price | Lowest | Middle |
|---|---|---|---|
| [Progesterone](https://menocost.com/treatments/progesterone) | 32 | $11 | $74 |
| [Vaginal estrogen](https://menocost.com/treatments/vaginal-estrogen) | 30 | $20 | $89 |
| [Low-dose paroxetine](https://menocost.com/treatments/paroxetine) | 6 | $20 | $69 |
| [Estradiol pill](https://menocost.com/treatments/estradiol-pill) | 32 | $29 | $79 |
| [Testosterone for women](https://menocost.com/treatments/testosterone-women) | 15 | $33 | $85 |
| [Compounded hormones](https://menocost.com/treatments/compounded-hormones) | 83 | $36 | $103 |
| [Estradiol patch](https://menocost.com/treatments/estradiol-patch) | 31 | $63 | $129 |
| [Estrogen and progesterone together](https://menocost.com/treatments/combined-hrt) | 19 | $69 | $124 |
| [Estradiol gel or spray](https://menocost.com/treatments/estradiol-gel) | 10 | $70 | $86 |

The cheapest option for each treatment, with the service and its terms, is on
[menocost.com](https://menocost.com/cheapest-hrt-online). What HRT costs per month, with and without insurance, is
answered on [How much does HRT cost?](https://menocost.com/costs/how-much-does-hrt-cost) and
[The cheapest way to get HRT without insurance](https://menocost.com/costs/cheapest-way-to-get-hrt).

## Columns of the price file

| Column | Meaning |
|---|---|
| `price_id` | Stable identifier of the price: service, treatment and product. |
| `service` | The online service that sells the treatment, by its own name. |
| `service_type` | Menopause clinic online, online clinic with a menopause program, compounded hormones online, or clinic network. |
| `treatment` | The treatment the product is, e.g. "Estradiol patch" or "Veozah (fezolinetant)". |
| `product` | The product as the service's page names it. |
| `compounded` | yes for a compounded product (not FDA-approved), no for an FDA-approved one, empty when the page does not say. |
| `advertised_price` | The price in the service's own words, e.g. "$100.00 1-month supply ... Shipped and billed every 3 months." |
| `price_usd_30_days` | The price for 30 days of the product, in US dollars. Empty when the page gives no price that converts to 30 days. |
| `price_is_calculated` | yes when the 30-day price is this site's division of a supply price (e.g. a 90-day price divided by 3), no when the page states a monthly price. |
| `supply_price_usd` | The price of a supply when the page prices one (e.g. 90 days), in US dollars. |
| `supply_days` | Days the supply price buys. |
| `plan_months` | Months a plan bills or ships at once, when more than one. |
| `starting_from` | yes when the page gives the price as a starting point ("from", "starting at"). |
| `membership_added_usd` | A membership the service charges every patient on top of this price, per month, when its page says so. |
| `cost_per_30_days_with_membership_usd` | The 30-day price plus that membership: the figure the site's lists compare. |
| `start_fee_usd` | What starting costs once before the first medication (a consult, a first visit, labs), as the page states it. Never added to the 30-day figure. |
| `includes` | What the price includes, in the page's terms. |
| `bills_insurance` | yes or no as the service's pages state whether it bills insurance; empty when they do not say. |
| `hsa_fsa` | yes or no as the service's pages state whether an HSA or FSA card pays; empty when they do not say. |
| `all_50_states` | yes when the service's pages say it serves all 50 states, no when they name states it does not serve; empty when they do not say. |
| `checked_on` | The date (UTC) the price was last read on its source page (YYYY-MM-DD). |
| `still_on_page_on` | The last date (UTC) the daily check found every amount of this price still on its source page, when that is later than checked_on; blank when no later check found it. |
| `review_status` | current within 30 days of checked_on; overdue after that, when the price is kept only as a dated reference. |
| `source_url` | The service's own page the price was read on. |
| `referral_program` | yes when this site may earn a referral fee from the service. It lifts the service in the site's default order (disclosed beside every list); every lowest-price list ignores it. |
| `page` | This site's page for the service, with every price in context. |

## How the prices are read

- Each price is read on the selling service's own page, never from a review site or a search snippet. A fact the page
  does not state is left empty.
- A daily check re-reads every cited page and flags a price that left its page; flagged prices are read again, and
  every price is read again within 30 days. `checked_on` is the day a person read the price, `still_on_page_on` the
  day the check last found it on the page.
- `price_usd_30_days` is the page's own monthly price, or a supply price divided to 30 days when
  `price_is_calculated` is `yes`.

## Ask an AI assistant: the price server (MCP)

The same records answer AI assistants through a public, read-only [Model Context Protocol](https://modelcontextprotocol.io)
server. No key, no sign-up. Add it to any MCP client that takes a remote server:

```json
{ "mcpServers": { "menocost": { "type": "http", "url": "https://menocost.com/api/mcp" } } }
```

It is listed in the Official MCP Registry as `com.menocost/menopause-prices`. Its tools:

- `find_menopause_treatment_prices`: US online services' prices for one menopause treatment, lowest 30-day cost first (a membership charged on top included).
- `find_menopause_service_prices`: Every published menopause treatment price of one US online service (Midi Health, Alloy, Winona, Evernow, Hone Health and others), lowest first, with its fees, insurance and the page each was read on.
- `find_menopause_pharmacy_cash_prices`: What a menopause medicine costs at a cash pharmacy without insurance, with a prescription: Mark Cuban Cost Plus Drugs' own published prices for the brand and its generic (estradiol tablets, patches, gel, vaginal cream, inserts and ring, progesterone, Prempro, Activella, Premarin, paroxetine 7.5 mg), a pharmacy membership's flat monthly price where its own page names the medicine (Amazon Pharmacy RxPass for estradiol tablets), and for brands Cost Plus does not sell, what US pharmacies pay (CMS NADAC) and the maker's savings program.
- `menopause_boxed_warning_status`: Where the current FDA labels of menopause hormone therapy stand on the boxed warning FDA asked makers to change on 10 Nov 2025, as FDA's label database (openFDA) reads today: per treatment, how many makers' labels carry the updated (endometrial-only) warning, none, or the full warning with cardiovascular and dementia language, and each label's brand, maker, route and date.
- `menopause_fda_actions`: FDA's approvals, generic approvals, label changes and safety notices for menopause treatments (estradiol, conjugated estrogens, progesterone, Veozah, Lynkuet, paroxetine 7.5 mg), newest first, each dated with its source, read from FDA's records each day.
- `menopause_pharmacy_cost_nadac`: What US retail pharmacies pay per unit for a menopause medicine and each of its strengths and brands, from CMS's weekly NADAC survey (newest week, and the week before when it moved).
- `menopause_public_payers`: What Medicaid paid per prescription (CMS State Drug Utilization Data, newest four quarters) and what Medicare drug plans paid per claim (CMS Part D Prescribers by Geography and Drug, newest year) for a menopause treatment, nationally or in one US state, with each drug's Medicare spending per unit over five years.
- `list_menopause_treatments`: Every menopause treatment this site keeps a price list for, with its lowest 30-day cost, how many prices it has and its page.

## License and citation

Creative Commons Attribution 4.0 International (CC BY 4.0): free to share and adapt, with credit. Cite it as:

> MenoCost.com, US online menopause treatment prices, https://menocost.com/data

Archived versions with a DOI are on [Zenodo](https://zenodo.org/records/24295689); the same data is on
[Hugging Face](https://huggingface.co/datasets/menocost/us-menopause-treatment-prices).

Prices change: before acting on one, open the service's page in `source_url`. Nothing here is medical advice.
