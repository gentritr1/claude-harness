#!/bin/bash
# launchd entry point: run both checks; one failing must not skip the other.
d="$(cd "$(dirname "$0")" && pwd)"
"$d/check.sh"; a=$?
"$d/upstream.sh"; b=$?
exit $(( a | b ))
