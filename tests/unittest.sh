#!/bin/bash
set -e
cd "${BASH_SOURCE%/*}/.." || exit


PYTHONPATH=client/pygameui python -m unittest Text
