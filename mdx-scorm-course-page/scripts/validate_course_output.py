#!/usr/bin/env python3
"""Check course-output conventions, not the complete mdx-scorm runtime grammar.

Read-only. Code fences (including HTML Apps), inline code, frontmatter, raw
script/style/pre/code bodies, and text-exercise literal content are excluded
from prose checks. Source fidelity and runtime semantics still need review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Issue:
    severity: str
    code: str
    line: int
    message: str
    path: str = ""


@dataclass
class Block:
    name: str
    start: int
    body_start: int
    end: int
    fence: int
    opening: str


@dataclass
class Exceptions:
    title: set[str] = field(default_factory=set)
    feedback: set[str] = field(default_factory=set)
    numbering: set[str] = field(default_factory=set)
    choicecloze_semantic_conflict: set[str] = field(default_factory=set)


OPEN = re.compile(r"^ {0,3}(:{3,})([\w-]+)(?=$|[\s{\[]).*$")
CLOSE = re.compile(r"^ {0,3}(:{3,})[ \t]*$")
CODE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
SECTION = re.compile(r"^ {0,3}\[([A-Za-z][\w-]*)\][ \t]*$", re.M)
TEXT_TYPES = {"textselect", "textedit"}


def blank(value: str) -> str:
    return re.sub(r"[^\r\n]", " ", value)


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def header_span(text: str) -> tuple[int, int] | None:
    match = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    return match.span() if match else None


def mask_code(text: str) -> str:
    """Keep offsets stable; literal text-exercise content is not Markdown code."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    fence: tuple[str, int] | None = None
    literal_type: str | None = None
    literal_section = ""
    span = header_span(text)
    offset = 0
    for line in lines:
        value = line.rstrip("\r\n")
        if span and offset < span[1]:
            out.append(blank(line)); offset += len(line); continue
        marker = CODE.match(value)
        if fence:
            out.append(blank(line))
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
        elif literal_type and literal_section == "content":
            out.append(line)
            if CLOSE.match(value):
                literal_type = None; literal_section = ""
            elif (section := SECTION.fullmatch(value)):
                literal_section = section[1]
        elif marker:
            fence = (marker[1][0], len(marker[1]))
            out.append(blank(line))
        else:
            out.append(line)
            opening = OPEN.match(value)
            if opening and opening[2] in TEXT_TYPES:
                literal_type = opening[2]; literal_section = ""
            elif literal_type and (section := SECTION.fullmatch(value)):
                literal_section = section[1]
            elif literal_type and CLOSE.match(value):
                literal_type = None; literal_section = ""
        offset += len(line)
    return "".join(out)


def mask_inline_code(text: str) -> str:
    return re.sub(r"(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)", lambda m: blank(m[0]), text)


def masked_source(text: str) -> str:
    value = mask_code(text)
    # Mask comments and raw code/style containers before finding directives.
    value = re.sub(r"<!--.*?-->", lambda m: blank(m[0]), value, flags=re.S)
    value = re.sub(r"<(script|style|pre|code)\b[^>]*>.*?</\1\s*>", lambda m: blank(m[0]), value, flags=re.S | re.I)
    return value


def scan_blocks(text: str, masked: str) -> tuple[list[Block], list[Issue]]:
    stack: list[tuple[str, int, int, int, str]] = []
    blocks: list[Block] = []
    issues: list[Issue] = []
    offset = 0
    for line in masked.splitlines(keepends=True):
        value = line.rstrip("\r\n")
        if (close := CLOSE.match(value)):
            if stack and len(close[1]) >= stack[-1][3]:
                name, start, body_start, length, opening = stack.pop()
                blocks.append(Block(name, start, body_start, offset, length, opening))
            elif not stack:
                issues.append(Issue("warning", "unmatched-fence", line_at(text, offset), "Closing directive fence has no matching opener; inspect source."))
        elif (opening := OPEN.match(value)):
            # Inside a text-exercise content field, apparent nested directives
            # are literal content for this checker, not separate exercises.
            if stack and stack[-1][0] in TEXT_TYPES:
                offset += len(line); continue
            stack.append((opening[2], offset, offset + len(line), len(opening[1]), text[offset:offset + len(value)]))
        offset += len(line)
    for name, start, _, _, _ in stack:
        issues.append(Issue("warning", "unclosed-fence", line_at(text, start), f"{name} has no explicit closing fence; generated pages should balance fences."))
    return sorted(blocks, key=lambda b: b.start), issues


def sections(body: str) -> dict[str, list[tuple[int, int]]]:
    markers = list(SECTION.finditer(body))
    result: dict[str, list[tuple[int, int]]] = {}
    for i, marker in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(body)
        result.setdefault(marker[1], []).append((marker.end(), end))
    return result


def section(body: str, name: str) -> str | None:
    spans = sections(body).get(name)
    return body[slice(*spans[0])].strip() if spans else None


def attr(opening: str, name: str) -> str | None:
    found = re.search(r"(?<![\w-])" + re.escape(name) + r"\s*=\s*(?:\"((?:\\.|[^\"\\])*)\"|'((?:\\.|[^'\\])*)'|([^\s}]+))", opening)
    if found:
        return next(v for v in found.groups() if v is not None)
    if re.search(r"(?<=[{\s])" + re.escape(name) + r"(?=[}\s])", opening):
        return "true"
    return None


def cloze_options(value: str) -> list[tuple[str | None, str]]:
    result: list[tuple[str | None, str]] = []
    for raw in value.splitlines():
        # Mirrors the important delimiter boundary: pipes take precedence.
        chunks = re.split(r"\|+" if "|" in raw else r"[,，;；、]+", raw)
        for chunk in chunks:
            item = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", chunk).strip()
            if not item:
                continue
            label = re.match(r"^([A-Z])[.)、:]\s*(.*)$", item)
            result.append((label[1], label[2]) if label else (item if re.fullmatch(r"[A-Z]", item) else None, item))
    return result


def inspect_text(text: str, relative: str = "page.mdx", exceptions: Exceptions | None = None) -> list[Issue]:
    exceptions = exceptions or Exceptions()
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    masked = masked_source(text)
    blocks, issues = scan_blocks(text, masked)

    def add(severity: str, code: str, offset: int, message: str) -> None:
        issues.append(Issue(severity, code, line_at(text, offset), message))

    if span := header_span(text):
        for match in re.finditer(r"^([A-Za-z][\w-]*):", text[span[0]:span[1]], re.M):
            key = match[1]
            allow = exceptions.title if key == "title" else exceptions.feedback if key in {"feedback", "feedbackMode"} else exceptions.numbering
            if key in {"title", "feedback", "feedbackMode", "numbering", "numberType", "numberingType", "type"} and relative not in allow:
                add("warning", "explicit-frontmatter", match.start(), f"{key} is valid only if supported and deliberately requested, inherited from a reference, or preserved during editing; omit redundant defaults. Use the page exception flag for a known decision.")

    # Exclude literal answer-bearing content from prose convention rules.
    prose = list(masked)
    for block in blocks:
        if block.name in TEXT_TYPES:
            body = masked[block.body_start:block.end]
            for start, end in sections(body).get("content", []):
                a, b = block.body_start + start, block.body_start + end
                prose[a:b] = blank(masked[a:b])
    prose_text = mask_inline_code("".join(prose))

    for match in re.finditer(r"<https?://[^>\n]+>", prose_text):
        add("warning", "web-link-form", match.start(), "Use [display text](URL) for a course webpage link; preserve the exact URL.")
    for match in re.finditer(r"<!--\s*(?:TODO\b|待确认|待核实)[\s\S]*?-->", mask_code(text), re.I):
        add("warning", "editorial-note", match.start(), "Move an editorial note outside MDX; preserve this text if it is intentionally quoted source content.")
    for match in re.finditer(r"(?<!\\)(\*{1,3}|_{1,3}|~~)(?=\S)[^\n]*?:pop\[[^\n]+?\][^\n]*?\1", prose_text):
        add("warning", "pop-emphasis", match.start(), "Inspect Pop inside Markdown emphasis; preserve the complete formatting span with b/i/del tags for renderer compatibility.")

    definitions: list[tuple[str, Block]] = []
    for block in blocks:
        if block.name == "pop" and (key := attr(block.opening, "def")):
            definitions.append((key, block))
    refs = [(m[1] or m[2] or m[3], m.start()) for m in re.finditer(r":pop\[(?:\\.|[^\]\\])*\]\{[^}\n]*\bref\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^}\s]+))", prose_text)]
    ids = Counter(key for key, _ in definitions)
    for key, offset in refs:
        if key not in ids:
            add("error", "missing-pop-definition", offset, f"Pop ref {key!r} has no definition.")
    for key, block in definitions:
        if ids[key] > 1:
            add("error", "duplicate-pop-definition", block.start, f"Pop definition {key!r} is duplicated; later content would replace earlier content.")
        if key not in {name for name, _ in refs}:
            add("warning", "unreachable-pop", block.start, f"Pop definition {key!r} is not reachable. Preserve the note in a visible glossary instead of hiding it in an unreferenced definition.")
        body = prose_text[block.body_start:block.end]
        body = re.sub(r"\*[^*\n]+\*|<i>.*?</i>|<em>.*?</em>", "", body)
        if re.search(r"(?<![\w*])(?:adj|adv|n|v|prep|pron|conj|num|art|aux)\.(?![\w*])", body):
            add("warning", "pos-style", block.start, "Inspect grammatical labels in this Pop; italicize part-of-speech labels, without changing ordinary source abbreviations.")

    for block in blocks:
        body = masked[block.body_start:block.end]
        clean = mask_inline_code(body)
        fields = sections(body)
        name = block.name
        if name.lower() in TEXT_TYPES and name not in TEXT_TYPES:
            add("error", "text-directive-case", block.start, "Text exercise directive names must be exactly lowercase textselect/textedit.")
        if name == "fillblank" and attr(block.opening, "aiscore") is not None:
            add("error", "ai-score-case", block.start, "Use the case-sensitive attribute aiScore, not aiscore.")
        if name in TEXT_TYPES:
            # HTML-looking strings and backticks in this field are literal
            # text, so inspect original section data rather than prose masks.
            body = text[block.body_start:block.end]
            fields = sections(body)
            allowed = {"prompt", "content", "explanation"}
            for label, ranges in fields.items():
                if label not in allowed:
                    add("error", "text-section", block.body_start + ranges[0][0], f"{name} does not support [{label}]; answers belong in content markers.")
                if len(ranges) > 1:
                    add("error", "duplicate-text-section", block.start, f"{name} repeats [{label}].")
            if not section(body, "content"):
                add("error", "missing-text-content", block.start, f"{name} requires nonempty [content].")
            attr_header = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', lambda m: blank(m[0]), block.opening)
            attributes = set(re.findall(r"(?<=[{\s])([A-Za-z][\w-]*)(?=\s*=|[}\s])", attr_header))
            permitted = {"id", "open", "weight", "scorm", "showExplanation"} | ({"mode"} if name == "textselect" else set())
            for key in sorted(attributes - permitted):
                add("error", "text-attribute", block.start, f"Unsupported {name} attribute {key!r}.")
            if name == "textselect" and attr(block.opening, "mode") not in {None, "word", "span"}:
                add("error", "text-mode", block.start, "textselect mode must be word or span.")
            if attr(block.opening, "showExplanation") not in {None, "instant", "onSubmit", "none"}:
                add("error", "text-explanation-mode", block.start, "showExplanation must be onSubmit, instant, or none.")
            continue  # Full marker grammar, token boundaries and scoring belong to the engine.
        if name in {"fillblank", "choicecloze"}:
            for match in re.finditer(r"@blank@", clean, re.I):
                add("warning", "blank-token", block.body_start + match.start(), "Use @--@ for a blank; @blank@ is only acceptable as intentional literal source text.")
        if name == "choicecloze":
            groups = [cloze_options(line) for line in (section(body, "options") or "").splitlines() if line.strip()]
            answers = [line.strip() for line in (section(body, "answer") or "").splitlines() if line.strip()]
            for index, value in enumerate(answers):
                # One option line is shared; several lines correspond to
                # consecutive blanks. Do not flatten separate option groups.
                opts = groups[0] if len(groups) == 1 else groups[index] if index < len(groups) else []
                labels = {label for label, _ in opts if label}
                displays = {value for _, value in opts}
                if re.fullmatch(r"[1-9]\d*", value):
                    if opts and int(value) > len(opts):
                        add("error", "cloze-index", block.start, f"Answer {value} exceeds {len(opts)} parsed options.")
                elif value in labels:
                    pass
                elif value in displays and not re.search(r"[,，;；、]", value):
                    pass  # Existing full-text answers are runtime-supported.
                elif re.fullmatch(r"[ivxlcdmIVXLCDMⅠ-Ⅻⅰ-ⅻ]+", value):
                    add("warning", "cloze-roman", block.start, "Encode a Roman-numeral display label as a 1-based decimal answer position.")
                else:
                    add("warning", "cloze-answer", block.start, f"Check answer {value!r}; prefer a 1-based index for punctuation-bearing or ambiguous options. Text answers are not categorically invalid.")
            if relative not in exceptions.choicecloze_semantic_conflict:
                # Limit the heuristic to the actual task, not a preceding unrelated page section.
                content = mask_inline_code(section(body, "content") or "")
                if re.search(r"wrong order|correct order|reconstruct.{0,40}(?:flow|sequence)|排序题|逻辑顺序", content, re.I):
                    add("warning", "cloze-semantics", block.start, "This task may be ordering; inspect whether sorting preserves the learner action better.")
                elif re.search(r"match each|matching (?:task|exercise)|匹配题|配对题", content, re.I):
                    add("warning", "cloze-semantics", block.start, "This task may be independent pairing; inspect whether matching is appropriate.")
        if name in {"choice", "game-choice"}:
            items = re.split(r"^\[item\](?:\{[^\n]*\})?[ \t]*$", body, flags=re.M) if name == "game-choice" else [body]
            for item in items:
                options = (section(item, "options") or "").splitlines()
                options = [re.sub(r"^\s*[-*+]\s+", "", v).strip() for v in options if v.strip()]
                labels = {chr(65 + i) for i in range(len(options))} | {str(i + 1) for i in range(len(options))}
                displays = {re.sub(r"^[A-Za-z][.)]\s*", "", v) for v in options}
                for answer in (section(item, "answer") or "").splitlines():
                    value = answer.strip()
                    if value in displays or value in labels:
                        continue
                    values = [v for v in re.split(r"[\s,，;；、|]+", value) if v]
                    if len(values) == 1 and len(value) > 1 and all(ch in labels for ch in value):
                        values = list(value)
                    if len(values) > 1 and all(v in labels for v in values):
                        add("warning", "multiselect-lines", block.start, "Write one correct option label per answer line; same-line lists may parse but are not the authoring convention.")
        if name == "sorting":
            items = section(clean, "items")
            if items is not None:
                for raw in items.splitlines():
                    if raw.strip() and not raw[:1].isspace() and not re.match(r"(?:\d+[.)]|-)\s+", raw):
                        add("warning", "sorting-marker", block.start, "Use decimal-number or '-' item markers; preserve source A/B labels after a supported marker. Inspect rich continuation lines manually.")
                        break
        if name in {"translate", "fillblank"}:
            cue = section(clean, "content") if name == "fillblank" else section(clean, "prompt")
            if re.search(r"translate.{0,160}(?:into|to)\s+Chinese|English[- ]to[- ]Chinese|英译中|译成汉语|翻译成中文", cue or "", re.I | re.S):
                explicit_alternative = attr(block.opening, "open") == "true" or attr(block.opening, "useManualMarking") == "true"
                if not explicit_alternative and (name != "fillblank" or attr(block.opening, "aiScore") != "true"):
                    add("warning", "translation-route", block.start, "Project default for English-to-Chinese AI grading is fillblank{aiScore=true}; respect an explicit non-AI/manual/open choice. This is not a parser language restriction.")
                elif not explicit_alternative and name == "fillblank":
                    if (section(clean, "content") or "").count("@--@") != 1 or not section(clean, "answer") or not section(clean, "ai"):
                        add("warning", "translation-pattern", block.start, "For scored AI translation, check one standalone blank, the supplied reference answer, and a task-specific [ai] instruction; never invent missing source answers.")

    for issue in issues:
        issue.path = relative
    return sorted(issues, key=lambda i: (i.line, i.code))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="An MDX page or directory; read-only")
    for flag in ("title", "feedback", "numbering", "choicecloze-semantic-conflict"):
        parser.add_argument("--allow-" + flag, action="append", default=[], metavar="RELATIVE_MDX_PATH", help="Suppress this convention warning for an already-established page decision")
    parser.add_argument("--strict-conventions", action="store_true", help="Exit nonzero on warnings too; do not use to override source/user decisions")
    parser.add_argument("--json", action="store_true", help="Print machine-readable issues and coverage limits")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.exists():
        parser.error(f"Path does not exist: {root}")
    pages = [root] if root.is_file() and root.suffix.lower() == ".mdx" else sorted(root.rglob("*.mdx")) if root.is_dir() else []
    if not pages:
        parser.error("No .mdx files found")
    base = root.parent if root.is_file() else root
    exceptions = Exceptions(set(args.allow_title), set(args.allow_feedback), set(args.allow_numbering), set(args.allow_choicecloze_semantic_conflict))
    issues: list[Issue] = []
    for page in pages:
        issues.extend(inspect_text(page.read_text(encoding="utf-8-sig"), page.relative_to(base).as_posix(), exceptions))
    errors = sum(i.severity == "error" for i in issues)
    warnings = len(issues) - errors
    limitation = "Convention/structural checks only; not full engine grammar, source-fidelity, HTML safety, preview, or Print validation."
    if args.json:
        print(json.dumps({"pages": len(pages), "errors": errors, "warnings": warnings, "issues": [asdict(i) for i in issues], "coverage": limitation}, ensure_ascii=False, indent=2))
    else:
        for issue in issues:
            print(f"{issue.severity.upper()}: {issue.path}:{issue.line} [{issue.code}] {issue.message}")
        print(f"Checked {len(pages)} MDX page(s): {errors} error(s), {warnings} warning(s). {limitation}")
    return 1 if errors or (args.strict_conventions and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
