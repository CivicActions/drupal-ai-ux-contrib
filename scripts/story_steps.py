#!/usr/bin/env python3
"""Print an AI demo story page (or any HTML page) as markdown: headings, numbered steps, image alt text, links.

  python3 scripts/story_steps.py <url-or-file> [--main-only]

Stdlib only. --main-only keeps content after the first <h1> and inside <main>/<article> when present.
"""
import html
import re
import sys
import urllib.request
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "svg", "nav", "header", "footer"}


class Story(HTMLParser):
    def __init__(self, main_only):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.buf = []
        self.skip = 0
        self.list_stack = []  # 'ol' or 'ul'
        self.counters = []
        self.in_main = not main_only
        self.main_only = main_only
        self.href = None
        self.heading = None

    def flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        return text

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if self.main_only and tag in ("main", "article"):
            self.in_main = True
        if tag in ("h1", "h2", "h3", "h4"):
            if tag == "h1" and self.main_only:
                self.in_main = True
            self.heading = tag
            self.buf = []
        elif tag in ("ol", "ul"):
            self.list_stack.append(tag)
            self.counters.append(0)
        elif tag == "li":
            if self.counters:
                self.counters[-1] += 1
            self.buf = []
        elif tag == "p":
            self.buf = []
        elif tag == "a":
            self.href = a.get("href")
        elif tag == "img" and self.in_main:
            alt = a.get("alt", "").strip()
            if alt:
                self.out.append(f"  (image: {alt})")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("code", "kbd"):
            self.buf.append("`")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4") and self.heading:
            text = self.flush()
            if text and self.in_main:
                self.out.append("\n" + "#" * int(tag[1]) + " " + text)
            self.heading = None
        elif tag == "li":
            text = self.flush()
            if text and self.in_main:
                indent = "  " * (len(self.list_stack) - 1)
                marker = f"{self.counters[-1]}." if self.list_stack and self.list_stack[-1] == "ol" else "-"
                self.out.append(f"{indent}{marker} {text}")
        elif tag in ("ol", "ul"):
            if self.list_stack:
                self.list_stack.pop()
                self.counters.pop()
        elif tag == "p":
            text = self.flush()
            if text and self.in_main and not self.list_stack:
                self.out.append(text)
        elif tag == "a":
            if self.href and self.buf and self.in_main:
                label = "".join(self.buf[-1:]).strip()
                if label and not self.href.startswith("#"):
                    self.buf.append(f" ({self.href})")
            self.href = None
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("code", "kbd"):
            self.buf.append("`")

    def handle_data(self, data):
        if self.skip:
            return
        self.buf.append(data)


def load(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "drupal-ai-ux-contrib/story_steps"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
    with open(src, encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    main_only = "--main-only" in sys.argv
    p = Story(main_only)
    p.feed(load(args[0]))
    print(f"<!-- source: {args[0]} -->")
    print("\n".join(html.unescape(l) for l in p.out).strip())


if __name__ == "__main__":
    main()
