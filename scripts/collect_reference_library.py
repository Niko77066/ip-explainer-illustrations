#!/usr/bin/env python3
"""Collect provenance-preserving IP references declared in a JSON manifest."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 (compatible; Codex-IP-Reference-Collector/1.0)"


def fetch(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=40) as response:
        return response.read(), response.headers.get_content_type()


def extension(url: str, content_type: str) -> str:
    by_type = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/svg+xml": "svg"}
    if content_type in by_type:
        return by_type[content_type]
    suffix = Path(urlparse(url).path).suffix.lower().lstrip(".")
    return suffix if suffix in {"jpg", "jpeg", "png", "webp", "svg"} else "bin"


def resolve_image(item: dict) -> str:
    if "image_url" in item:
        return item["image_url"]
    page, _ = fetch(item["source_page"])
    html = page.decode("utf-8", "replace")
    if item["resolver"] == "og-image":
        match = re.search(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I)
        if not match:
            match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']og:image["\']', html, re.I)
    elif item["resolver"] == "regex":
        match = re.search(item["pattern"], html, re.I)
    else:
        raise ValueError(f"unknown resolver: {item['resolver']}")
    if not match:
        raise ValueError("no source image found in official page")
    return match.group(1).replace("&amp;", "&")


def source_note(item: dict, image_url: str) -> str:
    return "\n".join((
        f"# {item['display_name']} reference",
        "",
        f"- family: {item['family']}",
        f"- version: {item['version']}",
        f"- source page: {item.get('source_page', image_url)}",
        f"- resolved asset: {image_url}",
        f"- fetched: {dt.date.today().isoformat()}",
        f"- rights holder: {item['rights_holder']}",
        "- local use: authorized by asset-library owner",
        "- redistribution: authorized by asset-library owner",
        "- provenance: first-party official web property",
        "",
    ))


def collect(manifest: dict, library_root: Path, family: str | None) -> tuple[int, list[str], int]:
    successful, failures = 0, []
    items = [item for item in manifest["items"] if family is None or item["family"] == family]
    for item in items:
        target = library_root / item["family"] / item["slug"] / item["version"]
        try:
            image_url = resolve_image(item)
            image, content_type = fetch(image_url)
            target.mkdir(parents=True, exist_ok=True)
            (target / f"front.{extension(image_url, content_type)}").write_bytes(image)
            (target / "source.md").write_text(source_note(item, image_url), encoding="utf-8")
            print(f"OK   {item['family']}/{item['slug']}")
            successful += 1
        except Exception as error:  # keep a single unavailable asset from aborting the library refresh
            failures.append(f"{item['family']}/{item['slug']}: {error}")
            print(f"FAIL {failures[-1]}", file=sys.stderr)
    return successful, failures, len(items)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--library-root", type=Path, required=True)
    parser.add_argument("--family", help="collect only one manifest family")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    successful, failures, attempted = collect(manifest, args.library_root, args.family)
    print(f"Collected {successful}/{attempted} references.")
    return 1 if failures and args.fail_on_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
