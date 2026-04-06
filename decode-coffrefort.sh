#!/bin/bash
# Decode le coffre-fort pour lire les credentials
# Usage: bash decode-coffrefort.sh > COFFREFORT.md
base64 -d COFFREFORT.md.b64
