#!/usr/bin/env python3
"""Import the latest accepted Codeforces solution for each problem."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_KEY = os.environ["CODEFORCES_API_KEY"]
API_SECRET = os.environ["CODEFORCES_API_SECRET"]
HANDLE = os.environ["CODEFORCES_HANDLE"]
STATE_FILE = Path(".codeforces_sync_state.json")
SOLUTIONS_DIR = Path("solutions")
PAGE_SIZE = 1000
API_DELAY_SECONDS = 2.1


def signed_params(method: str, params: dict[str, str]) -> dict[str, str]:
    random_prefix = f"{random.getrandbits(24):06x}"
    query = urllib.parse.urlencode(sorted(params.items()))
    message = f"{random_prefix}/{method}?{query}#{API_SECRET}"
    signature = random_prefix + hashlib.sha512(message.encode("utf-8")).hexdigest()
    return {**params, "apiSig": signature}


def api_call(method: str, params: dict[str, str], authenticated: bool = False) -> list[dict[str, Any]]:
    request_params = dict(params)
    if authenticated:
        request_params["apiKey"] = API_KEY
        request_params["time"] = str(int(time.time()))
        request_params = signed_params(method, request_params)

    url = f"https://codeforces.com/api/{method}?{urllib.parse.urlencode(request_params)}"
    request = urllib.request.Request(url, headers={"User-Agent": "Codeforces-GitHub-Importer/1.0"})

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError("Codeforces API request failed; check the Actions log and try again.") from exc

    if payload.get("status") != "OK":
        # Do not print the request URL; it contains signed API parameters.
        raise RuntimeError(f"Codeforces API error: {payload.get('comment', 'unknown error')}")

    result = payload.get("result")
    if not isinstance(result, list):
        raise RuntimeError("Codeforces API returned an unexpected response.")
    return result


def current_contest_ids() -> set[int]:
    active_phases = {"CODING", "PENDING_SYSTEM_TEST", "SYSTEM_TEST"}
    active: set[int] = set()

    for gym in ("false", "true"):
        contests = api_call("contest.list", {"gym": gym})
        for contest in contests:
            if contest.get("phase") in active_phases:
                try:
                    active.add(int(contest["id"]))
                except (KeyError, TypeError, ValueError):
                    continue
        time.sleep(API_DELAY_SECONDS)

    return active


def get_source(submission: dict[str, Any]) -> str | None:
    for key in ("source", "sourceCode"):
        value = submission.get(key)
        if isinstance(value, str) and value:
            return value

    encoded = submission.get("sourceBase64")
    if isinstance(encoded, str) and encoded:
        try:
            padded = encoded + "=" * (-len(encoded) % 4)
            return base64.urlsafe_b64decode(padded).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return None
    return None


def extension_for(language: str) -> str:
    value = language.lower()
    if "c++" in value or "cpp" in value:
        return ".cpp"
    if "c#" in value or "csharp" in value:
        return ".cs"
    if value in {"c", "gnu c", "ms c", "gnu c11", "ms c11"} or value.startswith("gnu c ") or value.startswith("ms c "):
        return ".c"
    if "python" in value or "pypy" in value:
        return ".py"
    if "java" in value:
        return ".java"
    if "kotlin" in value:
        return ".kt"
    if "javascript" in value or "node.js" in value:
        return ".js"
    if "typescript" in value:
        return ".ts"
    if "rust" in value:
        return ".rs"
    if "golang" in value or value == "go":
        return ".go"
    if "ruby" in value:
        return ".rb"
    if "php" in value:
        return ".php"
    if "haskell" in value:
        return ".hs"
    if "scala" in value:
        return ".scala"
    if "swift" in value:
        return ".swift"
    return ".txt"


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._-")
    return cleaned[:70] or "problem"


def load_cursor() -> int:
    if not STATE_FILE.exists():
        return 0
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return max(0, int(data.get("last_submission_id", 0)))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def main() -> None:
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    old_cursor = load_cursor()
    active_contests = current_contest_ids()

    latest: dict[str, dict[str, Any]] = {}
    newest_seen = old_cursor
    deferred_ids: list[int] = []
    start = 1

    while True:
        page = api_call(
            "user.status",
            {
                "handle": HANDLE,
                "from": str(start),
                "count": str(PAGE_SIZE),
                "includeSources": "true",
            },
            authenticated=True,
        )
        if not page:
            break

        reached_old_cursor = False
        for submission in page:
            try:
                submission_id = int(submission["id"])
            except (KeyError, TypeError, ValueError):
                continue

            if submission_id <= old_cursor:
                reached_old_cursor = True
                continue

            newest_seen = max(newest_seen, submission_id)
            contest_id = submission.get("contestId")
            if contest_id is not None:
                try:
                    if int(contest_id) in active_contests:
                        deferred_ids.append(submission_id)
                        continue
                except (TypeError, ValueError):
                    pass

            if submission.get("verdict") != "OK":
                continue

            source = get_source(submission)
            if source is None:
                # Leave this submission above the saved cursor so a later run can retry it.
                deferred_ids.append(submission_id)
                continue

            problem = submission.get("problem") or {}
            index = str(problem.get("index") or "problem")
            title = str(problem.get("name") or index)
            contest_folder = str(contest_id or problem.get("problemsetName") or "other")
            key = f"{contest_folder}/{index}"
            # user.status is newest first, so the first accepted source is the latest one.
            latest.setdefault(key, {
                "contest_folder": contest_folder,
                "index": index,
                "title": title,
                "language": str(submission.get("programmingLanguage") or ""),
                "source": source,
            })

        if reached_old_cursor or len(page) < PAGE_SIZE:
            break

        start += len(page)
        time.sleep(API_DELAY_SECONDS)

    for item in latest.values():
        folder = SOLUTIONS_DIR / safe_name(item["contest_folder"])
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"{safe_name(item['index'])}_{safe_name(item['title'])}{extension_for(item['language'])}"
        (folder / filename).write_text(item["source"], encoding="utf-8")

    if deferred_ids:
        next_cursor = max(old_cursor, min(newest_seen, min(deferred_ids) - 1))
    else:
        next_cursor = newest_seen

    STATE_FILE.write_text(
        json.dumps({"handle": HANDLE, "last_submission_id": next_cursor}, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Imported or refreshed {len(latest)} accepted problem solution(s).")
    if deferred_ids:
        print(f"Deferred {len(deferred_ids)} submission(s) for a later run.")


if __name__ == "__main__":
    main()
