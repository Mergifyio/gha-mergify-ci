#!/bin/bash

set -euo pipefail

command -v uv >/dev/null 2>&1 || { echo "uv is not installed: https://docs.astral.sh/uv/" >&2; exit 1; }

exec uv run "$(dirname "$0")/generate-doc.py"
