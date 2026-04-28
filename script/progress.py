#!/usr/bin/env python3
"""Generate a PDF submission listing and exercise completion report."""

import os
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Chapter order as listed in src/aata.xml
CHAPTER_FILES = [
    'sets.xml', 'integers.xml', 'groups.xml', 'cyclic.xml', 'permute.xml',
    'cosets.xml', 'crypt.xml', 'algcodes.xml', 'isomorph.xml', 'normal.xml',
    'homomorph.xml', 'matrix.xml', 'struct.xml', 'actions.xml', 'sylow.xml',
    'rings.xml', 'poly.xml', 'domains.xml', 'boolean.xml', 'vect.xml',
    'fields.xml', 'finite.xml', 'galois.xml',
]

CHAPTER_TITLES = {
    'sets.xml':      'Sets and Equivalences',
    'integers.xml':  'The Integers',
    'groups.xml':    'Groups',
    'cyclic.xml':    'Cyclic Groups',
    'permute.xml':   'Permutation Groups',
    'cosets.xml':    'Cosets and Lagrange\'s Theorem',
    'crypt.xml':     'Cryptography',
    'algcodes.xml':  'Algebraic Coding Theory',
    'isomorph.xml':  'Isomorphisms',
    'normal.xml':    'Normal Subgroups',
    'homomorph.xml': 'Homomorphisms',
    'matrix.xml':    'Groups of Symmetries',
    'struct.xml':    'Abelian and Solvable Groups',
    'actions.xml':   'Group Actions',
    'sylow.xml':     'Sylow Theorems',
    'rings.xml':     'Introduction to Rings',
    'poly.xml':      'Polynomial Rings',
    'domains.xml':   'Integral Domains',
    'boolean.xml':   'Lattices and Boolean Algebras',
    'vect.xml':      'Vector Spaces',
    'fields.xml':    'Extension Fields',
    'finite.xml':    'Finite Fields',
    'galois.xml':    'Galois Theory',
}


def parse_exercise_counts():
    """Parse exercise-counts.md, return {xml_stem: divisional_count}."""
    counts = {}
    md_path = REPO_ROOT / 'exercise-counts.md'
    with open(md_path) as f:
        for line in f:
            m = re.match(r'\|\s*(\w+\.xml)\s*\|\s*(\d+)', line)
            if m:
                counts[m.group(1)] = int(m.group(2))
    return counts


def parse_exercise_spec(spec: str) -> set[int]:
    """Parse an exercise specification string into a set of exercise numbers.

    Handles comma- and underscore-separated ranges and singles:
      '01-22'              -> {1..22}
      '01-06,09-12,15-17'  -> {1..6, 9..12, 15..17}
      '01-10_15'           -> {1..10, 15}
    """
    spec = spec.replace('_', ',')
    exercises: set[int] = set()
    for segment in spec.split(','):
        segment = segment.strip()
        if not segment:
            continue
        if '-' in segment:
            parts = segment.split('-')
            start, end = int(parts[0]), int(parts[1])
            exercises.update(range(start, end + 1))
        else:
            exercises.add(int(segment))
    return exercises


def scan_pdfs():
    """Return {chapter_num: [(version, filename, covered_set), ...]}."""
    answers_dir = REPO_ROOT / 'answers'
    pdf_re = re.compile(r'^ch(\d+)-ex(.+)-v(\d+)\.pdf$')
    chapters: dict[int, list[tuple[int, str, set[int]]]] = {}

    for ch_dir in sorted(answers_dir.iterdir()):
        if not ch_dir.is_dir() or not ch_dir.name.startswith('chapter-'):
            continue
        for pdf in sorted(ch_dir.glob('*.pdf')):
            m = pdf_re.match(pdf.name)
            if not m:
                continue
            ch_num = int(m.group(1))
            spec = m.group(2)
            version = int(m.group(3))
            covered = parse_exercise_spec(spec)
            chapters.setdefault(ch_num, []).append((version, pdf.name, covered))

    return chapters


def build_report():
    exercise_counts = parse_exercise_counts()
    pdf_data = scan_pdfs()

    rows = []
    total_covered = 0
    total_divisional = 0

    for idx, xml_file in enumerate(CHAPTER_FILES):
        ch_num = idx + 1
        divisional = exercise_counts.get(xml_file, 0)
        title = CHAPTER_TITLES.get(xml_file, xml_file.replace('.xml', ''))

        entries = pdf_data.get(ch_num, [])
        if entries:
            max_version = max(v for v, _, _ in entries)
            latest = [(v, name, covered) for v, name, covered in entries if v == max_version]
            # Combine covered sets from all PDFs at the latest version
            covered_union: set[int] = set()
            for _, _, covered in latest:
                covered_union |= covered
            # Cap at divisional total (don't count reading-q numbers)
            covered_count = len({x for x in covered_union if x <= divisional})
            pdf_names = [name for _, name, _ in latest]
        else:
            covered_count = 0
            pdf_names = []

        pct = (covered_count / divisional * 100) if divisional else 0
        total_covered += covered_count
        total_divisional += divisional

        rows.append({
            'ch': ch_num,
            'title': title,
            'pdfs': pdf_names,
            'covered': covered_count,
            'total': divisional,
            'pct': pct,
        })

    overall_pct = (total_covered / total_divisional * 100) if total_divisional else 0
    return rows, total_covered, total_divisional, overall_pct


def print_terminal(rows, total_covered, total_divisional, overall_pct):
    print(f"\n{'Ch':>3}  {'Title':<35}  {'PDFs':<45}  {'Done':>9}  {'%':>6}")
    print('-' * 105)
    for r in rows:
        pdf_str = ', '.join(r['pdfs']) if r['pdfs'] else '—'
        frac = f"{r['covered']}/{r['total']}"
        print(f"{r['ch']:>3}  {r['title']:<35}  {pdf_str:<45}  {frac:>9}  {r['pct']:>5.1f}%")
    print('-' * 105)
    print(f"{'':>3}  {'TOTAL':<35}  {'':45}  {f'{total_covered}/{total_divisional}':>9}  {overall_pct:>5.1f}%")
    print()


def write_markdown(rows, total_covered, total_divisional, overall_pct):
    today = date.today().isoformat()
    lines = [
        '# Exercise Completion Progress',
        '',
        f'Generated: {today}  ',
        f'Counts divisional exercises only. Latest PDF version per chapter.',
        '',
        '| Ch | Title | Latest PDF(s) | Covered | Total | % |',
        '|---:|---|---|---:|---:|---:|',
    ]
    for r in rows:
        pdf_str = ', '.join(f'`{p}`' for p in r['pdfs']) if r['pdfs'] else '—'
        lines.append(
            f"| {r['ch']} | {r['title']} | {pdf_str} | {r['covered']} | {r['total']} | {r['pct']:.1f}% |"
        )
    lines += [
        f'| | **Total** | | **{total_covered}** | **{total_divisional}** | **{overall_pct:.1f}%** |',
        '',
    ]

    out_path = REPO_ROOT / 'answers' / 'PROGRESS.md'
    out_path.write_text('\n'.join(lines))
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == '__main__':
    rows, total_covered, total_divisional, overall_pct = build_report()
    print_terminal(rows, total_covered, total_divisional, overall_pct)
    write_markdown(rows, total_covered, total_divisional, overall_pct)
