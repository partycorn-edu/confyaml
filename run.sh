#!/bin/sh
# Запуск транслятора: ./run.sh < input.conf > output.yaml
DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHONPATH="$DIR/src" exec python3 -m confyaml "$@"
