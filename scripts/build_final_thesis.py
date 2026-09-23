"""Build one consolidated thesis source and render review DOCX/PDF outputs."""

from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT / "thesis"


def reference_key(reference: str) -> str:
    doi = re.search(r"https://doi\.org/([^\s.]+(?:\.[^\s.]+)*)", reference, re.I)
    if doi:
        return "doi:" + doi.group(1).rstrip(".").lower()
    title = re.search(r"[‘']([^’']+)[’']", reference)
    value = title.group(1) if title else reference
    return "title:" + re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def parse_chapter(path: Path) -> tuple[str, dict[int, str]]:
    source = path.read_text(encoding="utf-8")
    body, reference_block = source.split("\n## References\n", maxsplit=1)
    references: dict[int, str] = {}
    for match in re.finditer(r"(?ms)^\[(\d+)\]\s+(.+?)(?=\n\n\[\d+\]|\Z)", reference_block):
        references[int(match.group(1))] = " ".join(match.group(2).splitlines()).strip()
    heading = re.match(r"# Chapter (\d+)\s+\n\s*# ([^\n]+)\s*\n", body)
    if not heading:
        raise ValueError(f"Unexpected chapter heading structure: {path}")
    body = (
        f"# Chapter {heading.group(1)}: {heading.group(2)}\n"
        + body[heading.end() :].lstrip()
    )
    return body, references


def expand_numbers(value: str) -> list[int]:
    numbers: list[int] = []
    for part in value.split(","):
        part = part.strip()
        range_match = re.fullmatch(r"(\d+)\s*(?:–|--|-)\s*(\d+)", part)
        if range_match:
            start, end = map(int, range_match.groups())
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(part))
    return numbers


def consolidate(chapter_paths: Iterable[Path]) -> tuple[list[str], list[str]]:
    global_numbers: dict[str, int] = {}
    global_references: dict[str, str] = {}
    chapter_bodies: list[str] = []
    citation_pattern = re.compile(r"\[([0-9]+(?:\s*(?:,|–|--|-)\s*[0-9]+)*)\]")

    for path in chapter_paths:
        body, local_references = parse_chapter(path)

        def replace(
            match: re.Match[str], references: dict[int, str] = local_references
        ) -> str:
            local_numbers = expand_numbers(match.group(1))
            if not local_numbers or any(number not in references for number in local_numbers):
                return match.group(0)
            mapped: list[int] = []
            for number in local_numbers:
                reference = references[number]
                key = reference_key(reference)
                if key not in global_numbers:
                    global_numbers[key] = len(global_numbers) + 1
                    global_references[key] = reference
                elif len(reference) > len(global_references[key]):
                    global_references[key] = reference
                mapped.append(global_numbers[key])
            return "[" + ",".join(str(number) for number in mapped) + "]"

        chapter_bodies.append(citation_pattern.sub(replace, body).rstrip())

    ordered = [""] * len(global_numbers)
    for key, number in global_numbers.items():
        ordered[number - 1] = global_references[key]
    return chapter_bodies, ordered


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    chapters = [THESIS / f"thesis_chapter_{number}.md" for number in range(1, 6)]
    bodies, references = consolidate(chapters)
    front = (THESIS / "front_matter.md").read_text(encoding="utf-8").rstrip()
    reference_text = "\n\n".join(
        f"[{number}] {reference}" for number, reference in enumerate(references, start=1)
    )
    complete = (
        front
        + "\n\n"
        + "\n\n\\newpage\n\n".join(bodies)
        + "\n\n\\newpage\n\n# References\n\n"
        + reference_text
        + "\n"
    )
    source_path = THESIS / "final_thesis.md"
    source_path.write_text(complete, encoding="utf-8", newline="\n")
    (THESIS / "references.md").write_text(
        "# Consolidated references\n\n" + reference_text + "\n",
        encoding="utf-8",
        newline="\n",
    )

    common = [
        "pandoc",
        str(source_path),
        "--from=markdown+raw_tex+tex_math_single_backslash",
        f"--resource-path={THESIS}:{ROOT}",
        "--toc",
        "--number-sections",
    ]
    run(common + ["--output", str(THESIS / "final_thesis.docx")])
    run(
        common
        + [
            "--pdf-engine=xelatex",
            "--output",
            str(THESIS / "final_thesis.pdf"),
        ]
    )
    print(f"Built {source_path}, final_thesis.docx, and final_thesis.pdf")
    print(f"Consolidated {len(references)} cited references")


if __name__ == "__main__":
    main()
