#!/bin/bash

set -euo pipefail

command -v auto-doc >/dev/null 2>&1 || { echo "auto-doc is not installed" >&2; exit 1; }

auto-doc -f action.yml
