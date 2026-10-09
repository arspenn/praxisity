#!/usr/bin/env bash
# Check that a document generated from a Praxisity template kept the template's structure.
#
# Usage: check-template-structure.sh TEMPLATE OUTPUT [--repeat]
#
# Compares structural anchors (headings, bold labels, horizontal rules, table headers,
# italic footer lines) between the template and the output. Template placeholders
# (`[like this]`) become wildcards and element IDs (REQ-F1, COMP-3, SPEC-NNN) are
# normalized, so filled-in content does not count as drift.
#
#   default   fixed structure: anchors must match one-to-one, in order (charter, README).
#   --repeat  repeating blocks: every template anchor must match at least one output
#             anchor and every output anchor must match some template anchor
#             (spec, design, DIP).
#
# Also reports HTML comments left in the output and template placeholders left unfilled.
# Exit 0 when clean, 1 when anything is found. Needs only bash, awk, grep, sed.
# Identical copies live in each template skill; edit all of them together.
set -u
if [ $# -lt 2 ]; then sed -n '2,18p' "$0"; exit 2; fi
T=$1; O=$2; MODE=fixed; [ "${3:-}" = "--repeat" ] && MODE=repeat

# Structural anchors of a file, one per line. Bold labels keep only the label.
anchors() {
  awk '
    { line=$0; sub(/[ \t]+$/, "", line) }
    line ~ /^#+ / || line ~ /^---$/ || line ~ /^\*[^*].*[^*]\*$/ { print line; prev=line; next }
    line ~ /^\*\*[^*]+:\*\*/ { print substr(line, 1, index(line, ":**")+2); prev=line; next }
    line ~ /^\|[ \t:|-]+\|$/ && prev ~ /^\|/ { print prev; prev=line; next }
    { prev=line }
  ' "$1"
}

# Normalize IDs: REQ-F3, REQ-F12, SPEC-NNN, SPEC-012, COMP-1 all become <PREFIX>-n.
normalize() {
  sed -E -e 's/(^|[^A-Za-z0-9-])([A-Z]{2,6}-)(F|N)?([0-9]+|NNN|MMM|DDD)($|[^A-Za-z0-9-])/\1\2n\5/g' \
         -e 's/(^|[^A-Za-z0-9-])([A-Z]{2,6}-)(F|N)?([0-9]+|NNN|MMM|DDD)($|[^A-Za-z0-9-])/\1\2n\5/g'
}

TA=$(mktemp); OA=$(mktemp); trap 'rm -f "$TA" "$OA"' EXIT
anchors "$T" | normalize > "$TA"
anchors "$O" | normalize > "$OA"

problems=$(awk -v mode="$MODE" '
  # Turn a template anchor into an ERE: placeholders match anything, the rest is literal.
  function pattern(s,  r, i, c) {
    gsub(/\[[^]]*\]/, "\001", s)
    r = ""
    for (i = 1; i <= length(s); i++) {
      c = substr(s, i, 1)
      if (index("\\.^$|()[]{}*+?", c)) c = "\\" c
      r = r c
    }
    gsub(/\001/, ".*", r)
    return "^" r "$"
  }
  FNR == NR { src[++nt] = $0; pat[nt] = pattern($0); next }
  { out[++no] = $0 }
  END {
    if (mode == "repeat") {
      for (i = 1; i <= nt; i++) {
        hit = 0; for (j = 1; j <= no; j++) if (out[j] ~ pat[i]) { hit = 1; break }
        if (!hit) print "missing anchor: " src[i]
      }
      for (j = 1; j <= no; j++) {
        hit = 0; for (i = 1; i <= nt; i++) if (out[j] ~ pat[i]) { hit = 1; break }
        if (!hit) print "unexpected anchor: " out[j]
      }
    } else {
      if (nt != no) print "anchor count differs: template " nt ", output " no
      n = (nt < no) ? nt : no
      for (i = 1; i <= n; i++) if (out[i] !~ pat[i])
        print "anchor " i " differs: template \047" src[i] "\047 vs output \047" out[i] "\047"
    }
  }
' "$TA" "$OA")

comments=$(grep -n -E '<!--|-->' "$O" | sed -E 's/^([0-9]+):.*/line \1: HTML comment not stripped/')

leftovers=""
while IFS= read -r ph; do
  case "$ph" in *.md*|*http*|'[Unreleased]') continue ;; esac
  grep -qF -- "$ph" "$O" && leftovers="${leftovers}placeholder left unfilled: ${ph}
"
done < <(grep -oE '\[[^]]+\]' "$T" | sort -u)

all=$(printf '%s\n%s\n%s' "$problems" "$comments" "$leftovers" | sed '/^$/d')
if [ -n "$all" ]; then
  printf 'STRUCTURE CHECK FAILED (%s):\n' "$(printf '%s\n' "$all" | wc -l | tr -d ' ')"
  printf '%s\n' "$all" | sed 's/^/  - /'
  exit 1
fi
printf 'STRUCTURE CHECK OK: %s anchors match the template\n' "$(wc -l < "$OA" | tr -d ' ')"