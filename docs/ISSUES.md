# Issues

## 2026-10-06: `tip up to 2 USDC` pinned quantity 2

- **What I saw:** first recorded run of `"tip up to 2 USDC"` printed `pin 2 x 'Tip'`. The case still refused on `price_raw` (2000000 vs 3000000), so 6/6 still matched.
- **What was actually wrong:** `_quantity_from_ask` treated any `2` in the sentence as a count. The `2` in "up to 2 USDC" is a budget cap, not a quantity.
- **How I found it:** the recorded case log line `pin 2 x 'Tip'`.
- **What I changed:** quantity is 2 only when the first word is `two` or `2`. `test_parse_pins_the_quantity_that_was_asked` stays green; the tip pin is now `1 x 'Tip'`.
- **What it cost:** nothing on chain. A live tip with that pin would have refused on quantity instead of price, still unsigned.
- **Would the checks have caught it?** Yes, `check_quantity` would have refused 2 vs 1. The pin was still a lie about the ask.

## 2026-10-06: live `prepare_purchase` for Espresso returned `receipt-failed`

- **What I saw:** Gecko `prepare_purchase` for buyer `FaYWqJXHgTVJuJJhworKDqgg1MR4TFC92MxrcwYgTtJd` on `dev3pack-cafe` / Espresso / devnet refused `receipt-failed`.
- **What was actually wrong:** that public address has no class token (and likely no SOL for fees). Gecko will not build unsigned bytes for a wallet that cannot pay.
- **How I found it:** `projects/01-read-the-menu/responses/prepare.json`.
- **What I changed:** nothing in the buyer. The recorded lane is 6/6. Live landing waits on `scripts/devnet_setup.py` plus instructor funding of that address.
- **What it cost:** no signature. No money moved.
- **Would the checks have caught it?** They never ran: there were no bytes. This is a Gecko refusal, not a field refusal.
