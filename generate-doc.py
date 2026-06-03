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


def collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


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
        description = collapse(str(spec.get("description", "")))
        rows.append(f"| `{name}` | string | {required} | {default_cell} | {description} |")
    return "\n".join(rows)


def main() -> None:
    action = yaml.safe_load(ACTION.read_text())
    table = render_table(action.get("inputs") or {})
    block = f"{START}\n\n{table}\n\n{END}"

    readme = README.read_text()
    pattern = re.escape(START) + r".*?" + re.escape(END)
    if not re.search(pattern, readme, flags=re.DOTALL):
        raise SystemExit("AUTO-DOC-INPUT markers not found in README.md")

    README.write_text(re.sub(pattern, lambda _: block, readme, flags=re.DOTALL))


if __name__ == "__main__":
    main()
