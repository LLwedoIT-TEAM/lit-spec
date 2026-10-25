#!/usr/bin/env bash
# Runs lit-core CLI (default and --strict-references) against every derived fixture.
cd /workspace/lit-core-prototype/packages/lit-core
for d in test/fixtures/upstream/* test/fixtures/day-one/* test/fixtures/derived/*; do
  [ -d "$d" ] || continue
  for mode in default strict; do
    flag=""; [ $mode = strict ] && flag="--strict-references"
    echo "### $(basename "$(dirname "$d")")/$(basename "$d") [$mode]"
    timeout 60 npx --no-install tsx scripts/validate-bundle.ts "$d" $flag 2>&1 | sed 's/^/    /'
    echo "    exit=${PIPESTATUS[0]}"
  done
done
