#!/bin/bash
# REBUILD CSS — OBLIGATOIRE après toute modification CSS
# Combine style.css + style-v12.css → style.min.css
# NE JAMAIS minifier style.css seul !

DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Combining style.css + style-v12.css..."
cat "$DIR/style.css" "$DIR/style-v12.css" > /tmp/mybotia-combined.css
echo "Minifying..."
npx --yes csso-cli /tmp/mybotia-combined.css -o "$DIR/style.min.css"
SIZE=$(wc -c < "$DIR/style.min.css")
echo "✅ style.min.css rebuilt ($SIZE bytes)"
echo "⚠️  N'oublie pas de bumper le cache-buster dans index.html !"
rm /tmp/mybotia-combined.css
