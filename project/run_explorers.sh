#!/bin/bash
# Fast rebuild: preprocessing (as needed), both models and both explorers, without the seed tests,
# convergence check or topic-count test (those are for a full run).
#
# Usage: ./run_explorers.sh [start]
#   03         boilerplate list or lemma corrections changed: 03 -> 04 -> 05 -> models -> explorers (~8 min)
#   05         stopwords changed: 05 -> models -> explorers (~5 min)
#   models     data unchanged, model settings changed: models -> explorers (~4 min)
#   explorers  only names or page design changed: explorers (~1 min)
# Default: 03. Stops at the first failing step. Runs under caffeinate (macOS) so the machine stays awake.

set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-../venv/bin/python}"
START="${1:-03}"

case "$START" in
  03|05|models|explorers) ;;
  *) echo "Usage: $0 [03|05|models|explorers]"; exit 2 ;;
esac

# Keep the machine awake for the whole run
if [ -z "${RUN_EXPLORERS_AWAKE:-}" ] && command -v caffeinate > /dev/null; then
  RUN_EXPLORERS_AWAKE=1 exec caffeinate -i "$0" "$@"
fi

step() { echo; echo "===== $(date '+%H:%M:%S') $*"; "$PY" "$@"; }
T0=$(date +%s)

if [ "$START" = 03 ]; then
  step preprocessing/03_remove_boilerplate.py
  step preprocessing/04_normalize_text.py
fi
if [ "$START" = 03 ] || [ "$START" = 05 ]; then
  step preprocessing/05_remove_stopwords.py
  step analysis/check_pipeline_output.py
fi

if [ "$START" != explorers ]; then
  # The whole-corpus and the period models are independent: fit them at the same time
  echo; echo "===== $(date '+%H:%M:%S') models: 07 and 15 in parallel"
  LOG=$(mktemp -d)
  "$PY" modeling/07_fit_baseline_lda.py > "$LOG/07.log" 2>&1 & P07=$!
  "$PY" modeling/15_fit_period_lda.py > "$LOG/15.log" 2>&1 & P15=$!
  FAIL=0
  wait $P07 || FAIL=1
  wait $P15 || FAIL=1
  cat "$LOG/07.log" "$LOG/15.log"
  rm -rf "$LOG"
  if [ $FAIL -ne 0 ]; then echo "A model fit failed (see above)"; exit 1; fi
fi

step modeling/14_generate_topic_explorer.py
step modeling/17_generate_period_explorer.py
step analysis/18_alignment_null.py

echo
echo "===== $(date '+%H:%M:%S') done in $(( ($(date +%s) - T0) / 60 )) min"
if [ "$START" != explorers ]; then
  echo "Models refitted: topic and chain names match only where the 'Topic names' and 'Chain names' lines"
  echo "above say so; the seed tests, convergence check, topic-count test and"
  echo "the numbers in docs/PIPELINE_DOCUMENTATION.md are from the last full run."
fi
