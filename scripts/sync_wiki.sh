#!/usr/bin/env bash
set -e

# ==============================================================================
# Script de sincronização automática da Wiki do GitHub
# ==============================================================================

WIKI_DIR="/tmp/prompts_wiki"

if [ ! -d "$WIKI_DIR" ]; then
  echo "❌ Diretório da wiki não encontrado em $WIKI_DIR."
  exit 1
fi

echo "🚀 Sincronizando páginas da Wiki com o GitHub..."

cd "$WIKI_DIR"
git add .
git commit -m "docs(wiki): sync wiki documentation" || true

GH_TOKEN=$(gh auth token 2>/dev/null || true)

if [ -n "$GH_TOKEN" ]; then
  git remote set-url origin "https://${GH_TOKEN}@github.com/brunoez/prompts.wiki.git"
else
  git remote set-url origin "git@github.com:brunoez/prompts.wiki.git"
fi

git push -u origin master || git push -u origin main

echo "✅ Wiki sincronizada com sucesso!"
