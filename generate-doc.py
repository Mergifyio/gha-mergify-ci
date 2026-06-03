# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Generate the README Inputs table from action.yml.

Replaces tj-actions/auto-doc: parses the action's inputs and rewrites the
GitHub-flavoured Markdown table between the AUTO-DOC-INPUT markers in README.md.
"""

import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).parent
ACTION = ROOT / "action.yml"
README = ROOT / "README.md"
START = "<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->"
END = "<!-- AUTO-DOC-INPUT:END -->"


def render_description(text: str) -> str:
    """Render an action.yml description as a single Markdown table cell.

    Wrapped prose lines are joined with spaces; `*`-prefixed lines (e.g. the
    list of actions) become `<br>`-separated bullets so they render as a list
    inside the cell rather than a run of literal asterisks.
    """
    parts: list[str] = []
    for raw in text.strip().splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("* "):
            parts.append("<br>• " + line[2:].strip())
        elif parts:
            parts[-1] += " " + line
        else:
            parts.append(line)
    return "".join(parts)


def render_table(inputs: dict) -> str:
    rows = [
        "| Input | Type | Required | Default | Description |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name in sorted(inputs):
        spec = inputs[name] or {}
        required = "true" if spec.get("required") else "false"
        default = spec.get("default")
        default_cell = f"`{default}`" if default not in (None, "") else ""
        description = render_description(str(spec.get("description", "")))
        rows.append(f"| `{name}` | string | {required} | {default_cell} | {description} |")
    return "\n".join(rows)


def main() -> None:
    action = yaml.safe_load(ACTION.read_text(encoding="utf-8"))
    table = render_table(action.get("inputs") or {})
    block = f"{START}\n\n{table}\n\n{END}"

    readme = README.read_text(encoding="utf-8")
    pattern = re.escape(START) + r".*?" + re.escape(END)
    if not re.search(pattern, readme, flags=re.DOTALL):
        raise SystemExit("AUTO-DOC-INPUT markers not found in README.md")

    new = re.sub(pattern, lambda _: block, readme, flags=re.DOTALL)
    README.write_text(new, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
