#!/usr/bin/env bash
# Runs unmodified lit-spec validate.py (isolated copy) and lit-core CLI against each probe fixture.
PY=/workspace/.pyv-litspec/bin/python
VENDOR=/workspace/lit-core-prototype/vendor/lit-spec
LC=/workspace/lit-core-prototype/packages/lit-core
for d in /workspace/lit-spec-clarifications/probe-fixtures/*; do
  n=$(basename "$d")
  T=$(mktemp -d); mkdir -p "$T/scripts" "$T/examples"
  cp -r "$VENDOR/schema" "$T/"; cp "$VENDOR/scripts/validate.py" "$T/scripts/"; cp -r "$d" "$T/examples/$n"
  echo "### probe/$n validate.py"
  OUT=$(timeout 60 "$PY" "$T/scripts/validate.py" 2>&1); RC=$?
  echo "$OUT" | tail -8 | sed 's/^/    /'; echo "    exit=$RC"; rm -rf "$T"
  for flag in "" "--strict-references" "--proposed"; do
    echo "### probe/$n lit-core ${flag:-[default]}"
    (cd "$LC" && timeout 60 npx --no-install tsx scripts/validate-bundle.ts "$d" $flag 2>&1) | sed 's/^/    /'
    echo "    exit=${PIPESTATUS[0]}"
  done
done
