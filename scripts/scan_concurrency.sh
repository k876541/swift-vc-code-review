#!/bin/sh
set -eu

root="${1:-.}"

if ! command -v rg >/dev/null 2>&1; then
  echo "rg is required" >&2
  exit 2
fi

scan() {
  label="$1"
  pattern="$2"
  echo "## $label"
  rg -n --glob '*.swift' "$pattern" "$root" || true
  echo
}

scan "Detached tasks" 'Task\.detached'
scan "Dispatch to main queue" 'DispatchQueue\.main\.(async|sync)'
scan "Unchecked sendability" '@unchecked[[:space:]]+Sendable'
scan "Unsafe isolation escapes" 'nonisolated\(unsafe\)|@preconcurrency'
scan "Continuation creation" 'withChecked(Throwing)?Continuation|withUnsafe(Throwing)?Continuation'
scan "Unstructured tasks" '(^|[^A-Za-z0-9_])Task[[:space:]]*\{'
scan "Timers and observers" 'Timer\.(scheduledTimer|publish)|NotificationCenter\.default\.(addObserver|publisher)'
scan "Subscriptions" '\.sink[[:space:]]*\{|\.subscribe[[:space:]]*\('

