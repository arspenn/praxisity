#!/usr/bin/env python3
"""Check that a document generated from a Praxisity template kept the template's structure.

Usage: check-template-structure.py TEMPLATE OUTPUT [--repeat]

Compares structural anchors (headings, bold labels, horizontal rules, table headers,
italic footer lines) between the template and the output. Template placeholders
(`[like this]`, `NNN`, `MMM`, `DDD`) become wildcards, and element IDs (REQ-F1, COMP-3,
SPEC-012) are normalized, so filled-in content does not count as drift.

  default   fixed structure: anchors must match one-to-one, in order (charter, README).
  --repeat  repeating blocks: every template anchor must match at least one output anchor
            and every output anchor must match some template anchor (spec, design, DIP).

Also reports HTML comments left in the output and template placeholders left unfilled.
Exit 0 when clean, 1 when anything is found. Identical copies live in each template skill.
"""
import re
import sys

ANCHOR = re.compile(
    r"^(#{1,6} .*|\*\*[^*]+:\*\*|---|\*[^*].*[^*]\*)\s*$"
)
TABLE_SEP = re.compile(r"^\|[\s:|-]+\|\s*$")
ID = re.compile(r"\b([A-Z]{2,6}-)(?:F|N)?(?:[0-9]+|[NMD]{3})\b")
PLACEHOLDER = re.compile(r"\[[^\]]+\]")


def anchors(lines):
    """Return the structural anchor lines, in order."""
    out = []
    for i, raw in enumerate(lines):
        line = raw.rstrip()
        if ANCHOR.match(line):
            if line.startswith("**"):
                line = line[: line.index(":**") + 3]  # keep only the bold label
            out.append(line)
        elif TABLE_SEP.match(line) and i > 0 and lines[i - 1].lstrip().startswith("|"):
            out.append(lines[i - 1].rstrip())  # table header row
    return out


def normalize(line):
    """Normalize IDs so REQ-F3 and REQ-F12, or SPEC-NNN and SPEC-012, compare equal."""
    return ID.sub(lambda m: m.group(1) + "n", line)


def pattern(template_line):
    """Turn a template anchor into a regex: placeholders match anything."""
    parts = PLACEHOLDER.split(normalize(template_line))
    return re.compile("^" + ".*".join(re.escape(p) for p in parts) + "$")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    template, output = read(argv[1]), read(argv[2])
    repeat = "--repeat" in argv[3:]
    problems = []

    t_anchors = anchors(template)
    o_anchors = [normalize(a) for a in anchors(output)]
    patterns = [(a, pattern(a)) for a in t_anchors]

    if repeat:
        for src, pat in patterns:
            if not any(pat.match(o) for o in o_anchors):
                problems.append(f"missing anchor: {src}")
        for o in o_anchors:
            if not any(pat.match(o) for _, pat in patterns):
                problems.append(f"unexpected anchor: {o}")
    else:
        if len(patterns) != len(o_anchors):
            problems.append(
                f"anchor count differs: template {len(patterns)}, output {len(o_anchors)}"
            )
        for idx, ((src, pat), o) in enumerate(zip(patterns, o_anchors)):
            if not pat.match(o):
                problems.append(f"anchor {idx + 1} differs: template '{src}' vs output '{o}'")

    for n, line in enumerate(output, 1):
        if "<!--" in line or "-->" in line:
            problems.append(f"line {n}: HTML comment not stripped")

    template_text = "\n".join(template)
    output_text = "\n".join(output)
    for ph in sorted(set(PLACEHOLDER.findall(template_text))):
        if ".md" in ph or "http" in ph or ph == "[Unreleased]":
            continue  # markdown link text, not a placeholder
        if ph in output_text:
            problems.append(f"placeholder left unfilled: {ph}")

    if problems:
        print(f"STRUCTURE CHECK FAILED ({len(problems)}):")
        for p in problems:
            print("  - " + p)
        return 1
    print(f"STRUCTURE CHECK OK: {len(o_anchors)} anchors match the template")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))