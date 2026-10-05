"""Keyless MCP server: one tool, `check_purchase`, that runs the buyer's seven checks."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer

from buyer.check import check_all
from buyer.intent import IntentRecord
from buyer.prepared import Prepared
from server.guard import is_public_url


def check_purchase(
    intent: dict[str, Any],
    prepared_answer: dict[str, Any],
    rpc_url: str | None = None,
) -> dict[str, Any]:
    """Rebuild the pin and the prepared bytes, then return the verdict.

    If `rpc_url` is given and `is_public_url` says no, refuse before fetching anything.
    """
    if rpc_url and not is_public_url(rpc_url):
        return {
            "passed": False,
            "field": "rpc_url",
            "asked": "a public https URL",
            "found": rpc_url,
        }
    record = IntentRecord(
        ask=intent["ask"],
        store=intent["store"],
        product=intent["product"],
        quantity=int(intent["quantity"]),
        budget_raw=int(intent["budget_raw"]),
        mint=intent["mint"],
        buyer=intent["buyer"],
        network=intent["network"],
        store_authority=intent["store_authority"],
        menu_price_raw=intent.get("menu_price_raw"),
        pinned_at=intent.get("pinned_at", ""),
    )
    prepared = Prepared.from_answer(prepared_answer)
    verdict = check_all(record, prepared)
    if verdict.unwritten is not None:
        return {
            "passed": False,
            "field": "unwritten",
            "asked": str(verdict.unwritten.what),
            "found": str(verdict.unwritten.hint),
        }
    if verdict.refusal is not None:
        refused = verdict.refusal
        return {
            "passed": False,
            "field": refused.field,
            "asked": refused.asked,
            "found": refused.found,
        }
    return {"passed": True, "field": None, "asked": None, "found": None}


def main() -> None:
    mcp = MCPServer("gecko-check")
    mcp.tool()(check_purchase)
    mcp.run()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--once":
        payload = json.loads(sys.stdin.read())
        print(json.dumps(check_purchase(**payload)))
    else:
        main()
