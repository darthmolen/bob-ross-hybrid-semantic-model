#!/usr/bin/env python3
"""
extract_prep.py — recover canvas preparation from what Bob says, not what the painting shows.

The finished image cannot distinguish "black gesso ground" from "very dark paint over
Liquid White", and the CSV's one-hot columns record the ground but never the transparent
tone laid over it. Both facts are, however, spoken aloud in the opening minute of nearly
every episode. This script pulls the captions, reads that opening window, and writes a
review sheet pairing what Bob said against what the dataset claims.

Nothing here overwrites your index. It produces prep_review.csv for you to read.

    pip install youtube-transcript-api

    python extract_prep.py                       # all 403
    python extract_prep.py --underpainting-only  # just the 65 tagged episodes
    python extract_prep.py --season 16 --episode 8
    python extract_prep.py --window 180          # widen the opening window

Transcripts are cached under .transcript_cache/, so reruns cost nothing and an
interrupted run resumes where it stopped. Only real answers are cached — a request
YouTube refuses is left uncached and retried on the next run, so a rate-limited run
degrades into "come back later" instead of into 400 false negatives.

YouTube blocks bulk transcript requests aggressively, usually after well under a
dozen. Expect to run this repeatedly over days, or through a residential proxy.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass, field, asdict

CSV_URL = ("https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/"
           "master/data/bob_ross_paintings.csv")
CACHE_DIR = ".transcript_cache"
OUT_PATH = "prep_review.csv"

# --------------------------------------------------------------------------
# Vocabulary
#
# Auto-generated captions mangle paint names constantly and drop nearly all
# punctuation, so every term carries its common mis-hearings. Add to these as
# you find new ones — that is the main maintenance cost of this script.
# --------------------------------------------------------------------------

COLORS = {
    "Phthalo Blue":      [r"f?th?a?lo\s+blue", r"halo\s+blue", r"salo\s+blue"],
    "Phthalo Green":     [r"f?th?a?lo\s+green", r"halo\s+green"],
    "Prussian Blue":     [r"prussian\s+blue", r"russian\s+blue"],
    "Alizarin Crimson":  [r"aliz+ari?n\s+crimson", r"lizard\s*in\s+crimson",
                          r"alizarin", r"as\s+the\s+crimson"],
    "Bright Red":        [r"bright\s+red"],
    "Cadmium Yellow":    [r"cadmium\s+yellow", r"cad\s+yellow", r"calcium\s+yellow"],
    "Indian Yellow":     [r"indian\s+yellow", r"indiana\s+yellow"],
    "Yellow Ochre":      [r"yellow\s+ocher", r"yellow\s+ochre", r"yellow\s+oaker"],
    "Sap Green":         [r"sap\s+green", r"sat\s+green"],
    "Van Dyke Brown":    [r"van\s*dyke\s+brown", r"van\s*dike\s+brown", r"vandyke"],
    "Dark Sienna":       [r"dark\s+si?enn?a", r"dark\s+sierra", r"dark\s+sena"],
    "Burnt Umber":       [r"burnt\s+umber", r"burnt\s+amber"],
    "Midnight Black":    [r"midnight\s+black"],
    "Titanium White":    [r"titanium\s+white"],
}

GROUNDS = {
    "Liquid Clear": [r"liquid\s+clear"],
    "Liquid White": [r"liquid\s+white"],
    "Liquid Black": [r"liquid\s+black"],
    # Bob almost never says "black gesso" twice; the second reference is nearly always
    # "these black canvases" or "a black canvas", so both count as the same statement.
    "Black Gesso":  [r"black\s+gesso", r"black\s+jesso", r"black\s+gessoed",
                     r"black\s+canvas(?:es)?", r"these\s+black\s+c\w*\s*es"],
    "White Gesso":  [r"white\s+gesso", r"white\s+jesso"],
    # Tape is the workshop reality behind the Contact Paper tag: duct tape, masking
    # tape, a taped circle. Distinguish a straight-edge from a shaped mask by hand.
    "Contact Paper": [r"contact\s+paper", r"masking\s+tape", r"duct\s+tape",
                      r"piece\s+of\s+tape", r"run\s+some\s+tape", r"made\s+a\s+circle",
                      r"masking", r"cut\s+the\s+shape"],
    # Not in the CSV schema at all — S07E03 lays Liquid Black over a dried opaque
    # acrylic yellow ground. Worth surfacing wherever else it happens.
    "Acrylic Ground": [r"acrylic\s+\w+\s+paint", r"painted\s+(?:it\s+)?yellow",
                       r"canvas.{0,20}painted\s+\w+.{0,10}acrylic"],
}

# Phrases that mark Bob describing preparation rather than painting. A colour
# name only counts as a tone if it lands near one of these.
PREP_CUES = [
    r"thin\s+coat", r"thin\s+layer", r"covered?\s+(?:the|this|that)\s+canvas",
    r"cover(?:ed)?\s+(?:it|this)\s+with", r"start(?:ed)?\s+(?:out\s+)?with",
    r"already\s+(?:got|have)", r"go(?:ne)?\s+over\s+(?:it|that|this)",
    r"put\s+(?:a|some)\s+.{0,20}on\s+(?:the|this)\s+canvas",
    r"pre[\s-]?(?:pared|paring)", r"under\s*paint", r"let\s+(?:it|that)\s+dry",
    r"dried?\s+(?:completely|overnight)", r"applied?\s+(?:a|some)",
    # phrasings that actually carry the tone in the transcripts recovered so far
    r"already\s+(?:done|covered)", r"let\s+me\s+tell\s+you\s+what",
    r"transparent\s+(?:color|colour|paint|yellow|red)", r"layers?\s+of\s+color",
    r"even\s+coat", r"on\s+top\s+of\s+that", r"onto\s+(?:that|this)",
    r"we'?ve\s+(?:just\s+)?used", r"mixture\s+of", r"still\s+wet",
]

CUE_RE = re.compile("|".join(PREP_CUES), re.I)
WORD_WINDOW = 140   # characters either side of a cue in which a colour counts


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

@dataclass
class Row:
    season: int
    episode: int
    title: str
    painting_index: str
    video_id: str
    csv_ground: str          # from the one-hot columns
    tagged_underpainting: bool
    palette: list = field(default_factory=list)


@dataclass
class Finding:
    said_grounds: list = field(default_factory=list)
    said_tones: list = field(default_factory=list)
    confidence: str = "none"     # high | low | none
    quote: str = ""
    status: str = "ok"           # ok | no-captions | blocked


def load_rows(path_or_url: str) -> list[Row]:
    if path_or_url.startswith("http"):
        text = urllib.request.urlopen(path_or_url, timeout=60).read().decode("utf-8")
        lines = text.splitlines()
    else:
        lines = open(path_or_url, encoding="utf-8").read().splitlines()

    out = []
    for r in csv.DictReader(lines):
        ground = []
        if r.get("Black_Gesso") == "1":
            ground.append("Black Gesso")
        if r.get("Liquid_Black") == "1":
            ground.append("Liquid Black")
        if r.get("Liquid_Clear") == "1":
            ground.append("Liquid Clear")
        try:
            tags = ast.literal_eval(r["tags"]) if r.get("tags") else []
            palette = ast.literal_eval(r["colors"]) if r.get("colors") else []
        except (ValueError, SyntaxError):
            tags, palette = [], []
        if "Contact Paper" in tags:
            ground.append("Contact Paper")

        vid = (r.get("youtube_src") or "").rstrip("/").split("/")[-1].split("?")[0]

        out.append(Row(
            season=int(r["season"]),
            episode=int(r["episode"]),
            title=r["painting_title"],
            painting_index=r["painting_index"],
            video_id=vid,
            csv_ground=" + ".join(ground) if ground else "Liquid White (unflagged)",
            tagged_underpainting="Underpainting" in tags,
            palette=palette,
        ))
    return out


# --------------------------------------------------------------------------
# Captions
# --------------------------------------------------------------------------

class Blocked(Exception):
    """YouTube refused the request. Transient — never cached, never counted as
    'this video has no captions'."""


# Failures that mean "ask again later", not "there is nothing here". Caching one of
# these as an empty transcript poisons the cache permanently: the 65-episode run that
# first exposed this came back 60/65 'no-captions' purely because the IP was blocked
# after the sixth request, and every one of those 60 would have been skipped forever
# on the next run.
TRANSIENT = ("ipblocked", "requestblocked", "toomanyrequests", "youtubereques",
             "failedtocreateconsentcookie", "connection", "timeout", "temporar")


def _is_transient(exc: Exception) -> bool:
    name = type(exc).__name__.lower()
    return any(t in name for t in TRANSIENT) or "blocking requests from your ip" in str(exc).lower()


def fetch_transcript(video_id: str) -> list | None:
    """Return a list of caption cues, or None if the video genuinely has no captions.

    Raises Blocked when YouTube refuses the request, so the caller can back off
    instead of writing a false negative to the cache.

    Cached on disk. A cached empty list means 'checked, this video really has no
    captions' and is not retried.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.join(CACHE_DIR, f"{video_id}.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as fh:
            return json.load(fh) or None

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        sys.exit("Missing dependency. Run: pip install youtube-transcript-api")

    try:
        # The library's API changed across major versions; support both.
        if hasattr(YouTubeTranscriptApi, "get_transcript"):
            raw = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "en-US"])
        else:
            raw = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US"])
            raw = [c if isinstance(c, dict) else
                   {"text": c.text, "start": c.start, "duration": c.duration}
                   for c in raw]
        cues = [{"text": c["text"], "start": float(c["start"])} for c in raw]
    except Exception as exc:
        if _is_transient(exc):
            raise Blocked(str(exc)[:200]) from exc
        cues = []      # genuinely no transcript for this video — safe to remember

    with open(cache, "w", encoding="utf-8") as fh:
        json.dump(cues, fh)
    return cues or None


def opening_text(cues: list, window_s: float) -> str:
    """Flatten the first `window_s` seconds into one lowercase string."""
    words = [c["text"] for c in cues if c["start"] <= window_s]
    text = " ".join(words)
    text = re.sub(r"\[.*?\]", " ", text)        # [Music], [Applause]
    text = re.sub(r"\s+", " ", text)
    return text.lower()


# --------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------

def find_terms(text: str, table: dict) -> list[tuple[str, int]]:
    """Return (canonical_name, position) for every term matched in the text."""
    hits = []
    for name, patterns in table.items():
        for pat in patterns:
            m = re.search(pat, text, re.I)
            if m:
                hits.append((name, m.start()))
                break
    return sorted(hits, key=lambda h: h[1])


def analyse(text: str) -> Finding:
    f = Finding()
    if not text.strip():
        f.status = "no-captions"
        return f

    f.said_grounds = [name for name, _ in find_terms(text, GROUNDS)]

    cue_spans = [m.span() for m in CUE_RE.finditer(text)]
    colour_hits = find_terms(text, COLORS)

    for name, pos in colour_hits:
        near = any(abs(pos - s) <= WORD_WINDOW or abs(pos - e) <= WORD_WINDOW
                   for s, e in cue_spans)
        if near:
            f.said_tones.append(name)

    if f.said_tones and f.said_grounds:
        f.confidence = "high"
    elif f.said_tones or f.said_grounds:
        f.confidence = "low"

    # Keep the sentence around the first prep cue so a human can adjudicate fast.
    if cue_spans:
        s = max(0, cue_spans[0][0] - 90)
        e = min(len(text), cue_spans[0][1] + 190)
        f.quote = text[s:e].strip()

    return f


def disagreement(row: Row, f: Finding) -> str:
    """Flag where the captions and the dataset tell different stories."""
    flags = []
    csv_set = {g.strip() for g in row.csv_ground.replace("(unflagged)", "").split("+")}
    csv_set = {g for g in csv_set if g and g != "Liquid White"}
    said = set(f.said_grounds)

    if "Black Gesso" in csv_set and "Black Gesso" not in said and f.status == "ok":
        flags.append("gesso-not-heard")
    if "Black Gesso" in said and "Black Gesso" not in csv_set:
        flags.append("gesso-not-in-csv")
    if "Liquid Clear" in said and "Liquid Clear" not in csv_set:
        flags.append("clear-not-in-csv")
    if row.tagged_underpainting and not f.said_tones and f.status == "ok":
        flags.append("tone-unrecovered")
    if f.said_tones and not row.tagged_underpainting:
        flags.append("tone-not-tagged")

    off = [t for t in f.said_tones if row.palette and t not in row.palette]
    if off:
        flags.append("tone-off-palette:" + "/".join(off))

    return ";".join(flags)


# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=CSV_URL, help="path or URL to bob_ross_paintings.csv")
    ap.add_argument("--out", default=OUT_PATH)
    ap.add_argument("--window", type=float, default=150.0,
                    help="seconds of opening narration to read (default 150)")
    ap.add_argument("--underpainting-only", action="store_true",
                    help="only the episodes tagged Underpainting")
    ap.add_argument("--season", type=int)
    ap.add_argument("--episode", type=int)
    ap.add_argument("--sleep", type=float, default=2.0,
                    help="pause between uncached fetches")
    ap.add_argument("--retries", type=int, default=4,
                    help="retries per episode when YouTube blocks the request")
    ap.add_argument("--max-backoff", type=float, default=300.0,
                    help="ceiling on the block backoff, in seconds")
    args = ap.parse_args()

    rows = load_rows(args.csv)
    if args.underpainting_only:
        rows = [r for r in rows if r.tagged_underpainting]
    if args.season:
        rows = [r for r in rows if r.season == args.season]
    if args.episode:
        rows = [r for r in rows if r.episode == args.episode]

    print(f"{len(rows)} episodes queued. Cache: {CACHE_DIR}/", file=sys.stderr)

    results = []
    backoff = args.sleep
    for i, row in enumerate(rows, 1):
        cached = os.path.exists(os.path.join(CACHE_DIR, f"{row.video_id}.json"))

        cues, blocked = None, False
        if row.video_id:
            for attempt in range(args.retries + 1):
                try:
                    cues = fetch_transcript(row.video_id)
                    backoff = max(args.sleep, backoff / 2)
                    break
                except Blocked as exc:
                    if attempt == args.retries:
                        blocked = True
                        print(f"   blocked on {row.video_id}: {exc}", file=sys.stderr)
                        break
                    backoff = min(args.max_backoff, max(backoff * 3, 15.0))
                    print(f"   blocked, waiting {backoff:.0f}s "
                          f"(attempt {attempt + 1}/{args.retries})", file=sys.stderr)
                    time.sleep(backoff)

        if blocked:
            f = Finding(status="blocked")
        elif cues is None:
            f = Finding(status="no-captions")
        else:
            f = analyse(opening_text(cues, args.window))

        results.append((row, f))
        mark = {"high": "++", "low": " +", "none": "  "}.get(f.confidence, "  ")
        print(f"{mark} [{i:>3}/{len(rows)}] S{row.season:02d}E{row.episode:02d} "
              f"{row.title[:34]:<34} "
              f"ground={'/'.join(f.said_grounds) or '-':<28} "
              f"tone={'/'.join(f.said_tones) or '-'}", file=sys.stderr)

        if not cached and cues is not None:
            time.sleep(backoff)

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["season", "episode", "title", "painting_index",
                    "csv_ground", "tagged_underpainting",
                    "said_ground", "said_tone", "confidence",
                    "disagreement", "status", "quote"])
        for row, f in results:
            w.writerow([row.season, row.episode, row.title, row.painting_index,
                        row.csv_ground, int(row.tagged_underpainting),
                        " + ".join(f.said_grounds), " + ".join(f.said_tones),
                        f.confidence, disagreement(row, f), f.status, f.quote])

    n = len(results)
    high = sum(1 for _, f in results if f.confidence == "high")
    tones = sum(1 for _, f in results if f.said_tones)
    nocap = sum(1 for _, f in results if f.status == "no-captions")
    blocked_n = sum(1 for _, f in results if f.status == "blocked")
    flagged = sum(1 for r, f in results if disagreement(r, f))

    print(f"\nWrote {args.out}", file=sys.stderr)
    print(f"  {high}/{n} high confidence   {tones}/{n} with a tone recovered", file=sys.stderr)
    print(f"  {nocap} without captions     {flagged} with a dataset disagreement", file=sys.stderr)
    if blocked_n:
        say = lambda t: print(t, file=sys.stderr)
        say(f"  {blocked_n} BLOCKED by YouTube - not cached, rerun to pick them up.")
        say("  A blocked run is not a result. If most of a run comes back blocked,")
        say("  the IP is rate-limited: wait, raise --sleep, or route through a proxy")
        say("  (see the youtube-transcript-api README on IP bans).")
    print("\nSort by `confidence` descending and read the `quote` column — "
          "adjudicating a row takes about five seconds.", file=sys.stderr)


if __name__ == "__main__":
    main()
