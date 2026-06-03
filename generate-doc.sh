#!/bin/bash

set -euo pipefail

exec uv run "$(dirname "$0")/generate-doc.py"
