#!/usr/bin/env bash
set -euo pipefail

WORKSPACE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace|-w)
      WORKSPACE=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$WORKSPACE" = true ]; then
  TARGET_DIR="$(pwd)/.agents/skills/zero-context-journaling"
  echo "Installing zero-context-journaling skill to workspace .agents..."
else
  TARGET_DIR="${HOME}/.gemini/config/skills/zero-context-journaling"
  echo "Installing zero-context-journaling skill to global Antigravity config..."
fi

echo "Source: ${SCRIPT_DIR}"
echo "Target: ${TARGET_DIR}"

mkdir -p "${TARGET_DIR}"
cp -R "${SCRIPT_DIR}/"* "${TARGET_DIR}/"

echo ""
echo "Skill successfully installed! Antigravity will automatically discover zero-context-journaling."
