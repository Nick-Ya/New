#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$ROOT_DIR/build"

mkdir -p "$BUILD_DIR"

# Исправляем путь к исходникам
if [ -d "$ROOT_DIR/cpp-application" ]; then
    SOURCE_DIR="$ROOT_DIR/cpp-application"
else
    SOURCE_DIR="$ROOT_DIR"
fi

cd "$BUILD_DIR"
cmake -S "$SOURCE_DIR" -B "$BUILD_DIR"
cmake --build "$BUILD_DIR"

echo "[INFO] Build completed successfully"
echo "[INFO] Executable: $BUILD_DIR/grpc_udp_monitor"