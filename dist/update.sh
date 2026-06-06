#!/bin/bash
# youaudio — update logic
# Called by the `youaudio` CLI. Not meant to be run directly.
# Usage: source update.sh && youaudio_update [target-dir]

set -euo pipefail

youaudio_update() {
  local TARGET="${1:-.}"
  local SCRIPT_DIR
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  TARGET="$(cd "$TARGET" 2>/dev/null && pwd)" || {
    echo "youaudio: directory '$1' not found" >&2
    return 1
  }

  local DIST_DIR="$TARGET/dist"
  local COMPOSE_FILE="$DIST_DIR/docker-compose.yml"

  if [ ! -f "$COMPOSE_FILE" ]; then
    echo "youaudio: no project found at $TARGET" >&2
    echo "  (expected $COMPOSE_FILE)" >&2
    return 1
  fi

  for cmd in curl unzip rsync docker; do
    if ! command -v "$cmd" &>/dev/null; then
      echo "youaudio: '$cmd' is required but not installed" >&2
      return 1
    fi
  done

  local TMP_DIR
  TMP_DIR="$(mktemp -d)"
  trap 'rm -rf "$TMP_DIR"' EXIT

  # ---- Download with progress dots ----
  echo -n "  Downloading latest version from GitHub"
  curl -sfL -o "$TMP_DIR/repo.zip" \
    "https://github.com/lr-dbz/youaudio/archive/refs/heads/main/dist.zip" &
  local CURL_PID=$!
  while kill -0 $CURL_PID 2>/dev/null; do
    echo -n "."
    sleep 0.4
  done
  wait $CURL_PID || { echo " failed!"; return 1; }
  echo " done!"

  # ---- Verify zip integrity ----
  echo "  Verifying package..."
  if ! unzip -t "$TMP_DIR/repo.zip" &>/dev/null; then
    echo "youaudio: corrupted download" >&2
    return 1
  fi

  # ---- Extract ----
  echo "  Extracting..."
  unzip -q "$TMP_DIR/repo.zip" -d "$TMP_DIR/extracted"

  local REPO_DIR="$TMP_DIR/extracted/youaudio-main"
  if [ ! -d "$REPO_DIR" ]; then
    echo "youaudio: unexpected zip structure — expected 'youaudio-main/'" >&2
    return 1
  fi

  # ---- Preserve user config ----
  if [ -f "$DIST_DIR/module/config.json" ]; then
    cp "$DIST_DIR/module/config.json" "$TMP_DIR/config.json.bak"
    echo "  Preserved module/config.json"
  fi

  # ---- Backup current dist ----
  echo "  Backing up current version..."
  local BACKUP_DIR="$TMP_DIR/backup"
  rsync -a --delete "$DIST_DIR/" "$BACKUP_DIR/"

  # ---- Critical section: copy + docker restart (disable errexit for rollback) ----
  local RC=0
  set +e
  (
    set -e

    rsync -a --delete \
      --exclude='/download/' \
      --exclude='/music/' \
      --exclude='/update.sh' \
      --exclude='/youaudio' \
      "$REPO_DIR/dist/" "$DIST_DIR/"

    if [ -f "$TMP_DIR/config.json.bak" ]; then
      mkdir -p "$DIST_DIR/module"
      cp "$TMP_DIR/config.json.bak" "$DIST_DIR/module/config.json"
    fi

    mkdir -p "$DIST_DIR/download" "$DIST_DIR/music"

    cd "$DIST_DIR"
    docker compose -p youaudio down --remove-orphans
    docker compose -p youaudio up --build -d
  )
  RC=$?
  set -e

  if [ $RC -ne 0 ]; then
    echo "  Update failed. Rolling back..." >&2
    rsync -a --delete "$BACKUP_DIR/" "$DIST_DIR/"
    cd "$DIST_DIR"
    docker compose -p youaudio up --build -d || true
    echo "  Rolled back to previous version." >&2
    return $RC
  fi

  echo "  Done! youAudio is running the latest version."
}
