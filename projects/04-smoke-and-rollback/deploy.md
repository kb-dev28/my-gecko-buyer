# Deploy (not public yet)

No public https URL is up. The check server runs locally:

```bash
uv run python server/check_server.py
```

`check_purchase` rebuilds `IntentRecord` + `Prepared.from_answer`, runs `check_all`, and
returns `{passed, field, asked, found}`. If `rpc_url` is set, `is_public_url` must pass
first.

Example, recorded case 5 (must refuse on `quantity`):

```bash
uv run python server/check_server.py --once <<'JSON'
{
  "intent": {
    "ask": "two bags of beans",
    "store": "dev3pack-cafe",
    "product": "Beans",
    "quantity": 2,
    "budget_raw": 2000000,
    "mint": "Eoqdd43nFQ9HzGq8HjBRVLCV6aTqCFRiwHy1ZVQheYSi",
    "buyer": "E4S9vud2r3uTXKuMra7MSAe4Admop8eewMYEPLSDK5pg",
    "network": "devnet",
    "store_authority": "Dt8quRFWgTMrrDgVa4GGFRJWksncskbs1tpYAQHkEPwJ",
    "menu_price_raw": 1500000
  },
  "prepared_answer": {}
}
JSON
```

Feed `fixtures/cases/5-beans.json` `calls.prepare_purchase` as `prepared_answer`. Expected
field: `quantity`, asked 2, found 1.

Rollback: take the process down. Nothing on chain depends on this server; the buyer runs
the same `check_all` in-process. Until there is a public URL, Friday uses stdio.
