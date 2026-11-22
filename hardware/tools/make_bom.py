#!/usr/bin/env python3
"""Generate hardware/transmitter/BOM.md from the KiCad root schematic via kicad-cli."""
import csv, os, re, subprocess, sys, tempfile
from datetime import date

HW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "transmitter")
SCH = os.path.join(HW, "transmitter.kicad_sch")
OUT = os.path.join(HW, "BOM.md")

# ---- Classification rules (edit here). First matching rule wins. ----
# (section, reference-prefix regex or None, keyword regex on Value+Description or None)
# If both are given, both must match; otherwise the one given must match.
RULES = [
    ("Modules", r"U\d", r"module|black ?pill|charger board|battery board|TP4056|IP2312|tft"),
    ("MCU", r"U\d", r"\bSTM32|ATmega|ESP32|RP2040"),
    ("ICs", r"U\d", None),
    ("Resistors", r"R\d", None),
    ("Capacitors", r"C\d", None),
    ("Inductors and ferrites", r"(L|FB)\d", None),
    ("Diodes and transistors", r"[DQ]\d", None),
    ("Connectors", r"[JP]\d", None),
    ("Switches", r"(SW|S)\d", None),
    ("Buzzer/audio", r"(LS|BZ)\d", None),
]
MISC = "Miscellaneous"
ORDER = [r[0] for r in RULES] + [MISC]
SKIP_REF = re.compile(r"^#|PWR_FLAG")

def classify(ref, text):
    for sec, pre, kw in RULES:
        if pre and not re.match(pre, ref):
            continue
        if kw and not re.search(kw, text, re.I):
            continue
        return sec
    return MISC

SI = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "R": 1, "r": 1,
      "k": 1e3, "K": 1e3, "M": 1e6, "G": 1e9}

def magnitude(v):
    m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*([pnuµmRrkKMG]?)(\d*)", v)
    if not m:
        return None
    num, suf, frac = m.groups()
    val = float(num + ("." + frac if suf and frac else ""))
    return val * SI.get(suf, 1)

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def ref_key(r):
    m = re.match(r"([A-Za-z]+)(\d+)", r)
    return (m.group(1), int(m.group(2))) if m else (r, 0)

def compress(refs):
    refs = sorted(refs, key=ref_key)
    out, i = [], 0
    while i < len(refs):
        j = i
        while (j + 1 < len(refs) and ref_key(refs[j + 1])[0] == ref_key(refs[i])[0]
               and ref_key(refs[j + 1])[1] == ref_key(refs[j])[1] + 1):
            j += 1
        out.append(refs[i] if j == i else
                   f"{refs[i]}, {refs[j]}" if j == i + 1 else f"{refs[i]}-{refs[j]}")
        i = j + 1
    return ", ".join(out)

def esc(s):
    return (s.strip() or "-").replace("|", "\\|").replace("\n", " ")

def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = os.path.join(td, "bom.csv")
        cmd = ["kicad-cli", "sch", "export", "bom", SCH, "-o", tmp,
               "--fields", "Reference,Value,Footprint,Description,${DNP}",
               "--labels", "Reference,Value,Footprint,Description,DNP",
               "--group-by", ""]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError:
            sys.exit("make_bom: kicad-cli not found")
        if r.returncode != 0 or not os.path.exists(tmp):
            sys.exit(f"make_bom: kicad-cli failed ({r.returncode}): {r.stderr or r.stdout}")
        with open(tmp, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    groups = {}
    for row in rows:
        ref = row["Reference"].strip()
        if not ref or SKIP_REF.search(ref):
            continue
        sec = classify(ref, row["Value"] + " " + row["Description"])
        key = (sec, row["Value"], row["Footprint"], row["Description"], row["DNP"])
        groups.setdefault(key, []).append(ref)

    sections = {}
    for (sec, val, fp, desc, dnp), refs in groups.items():
        sections.setdefault(sec, []).append((val, desc + (" (DNP)" if dnp else ""), fp, refs))

    def sortkey(item):
        val, _, _, refs = item
        mag = magnitude(val) if refs[0][0] in "RC" else None
        return (0, mag, natkey(val)) if mag is not None else (1, 0, natkey(val))

    lines = ["# Bill of Materials", "",
             f"- Generated: {date.today().isoformat()}",
             "- Source: `hardware/transmitter/transmitter.kicad_sch` (all sheets)",
             "- Regenerate: `python3 hardware/tools/make_bom.py`", "",
             "## Summary", "", "| Section | Lines | Parts |", "|---|---|---|"]
    tl = tp = 0
    for sec in ORDER:
        if sec in sections:
            n = sum(len(i[3]) for i in sections[sec])
            lines.append(f"| {sec} | {len(sections[sec])} | {n} |")
            tl += len(sections[sec]); tp += n
    lines.append(f"| **Total** | **{tl}** | **{tp}** |")
    summary = ", ".join(f"{s} {sum(len(i[3]) for i in sections[s])}" for s in ORDER if s in sections)
    for sec in ORDER:
        if sec not in sections:
            continue
        lines += ["", f"## {sec}", "", "| Qty | Value | Description | References | Footprint |",
                  "|---|---|---|---|---|"]
        for val, desc, fp, refs in sorted(sections[sec], key=sortkey):
            lines.append(f"| {len(refs)} | {esc(val)} | {esc(desc)} | {compress(refs)} | {esc(fp)} |")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"BOM.md written: {tl} lines, {tp} parts ({summary})")

if __name__ == "__main__":
    main()
