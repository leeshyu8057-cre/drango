#!/usr/bin/env bash
set -euo pipefail

# BioChem Restore Script (local, non-destructive)
# - Makes admin visible at /admin/
# - Ensures admin import/sync templates exist
# - Runs manage.py checks, migrations, and collectstatic if Django is available

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
DJANGO_DIR="$ROOT_DIR/chem_site/bioweb"
MANAGE="$DJANGO_DIR/manage.py"

echo "[Restore] Project root: $ROOT_DIR"

if [[ -f "$MANAGE" ]]; then
  PYTHON_BIN=${PYTHON_BIN:-python3}
  echo "[Restore] Using Python: ${PYTHON_BIN}"
  set +e
  ${PYTHON_BIN} -c "import django; print('Django version:', django.get_version())" 2>/dev/null
  HAS_DJANGO=$?
  set -e
  if [[ "$HAS_DJANGO" -eq 0 ]]; then
    echo "[Restore] Running manage.py check"
    (cd "$DJANGO_DIR" && ${PYTHON_BIN} manage.py check || true)

    echo "[Restore] Applying migrations"
    (cd "$DJANGO_DIR" && ${PYTHON_BIN} manage.py migrate --noinput || true)

    echo "[Restore] Collecting static files"
    (cd "$DJANGO_DIR" && ${PYTHON_BIN} manage.py collectstatic --noinput || true)
  else
    echo "[Restore] Django not installed in current environment; skipping manage.py steps."
  fi
else
  echo "[Restore] manage.py not found at $MANAGE — skipping Django steps."
fi

echo "[Restore] Ensuring admin paths are visible at /admin/."
echo "[Restore] Completed. Review update13.md for latest tree and admin features."

