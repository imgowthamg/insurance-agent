#!/bin/bash
set -e

echo "=> Building and starting containers..."
docker compose up -d --build

echo "=> Waiting for Ollama to be healthy..."
until docker compose exec ollama curl -sf http://localhost:11434/api/tags > /dev/null; do
  printf '.'
  sleep 2
done
echo ""

echo "=> Pulling gemma3:1b model (this may take a few minutes)..."
docker compose exec ollama ollama pull gemma3:1b

echo ""
echo "✓ All done!"
echo "  API:    http://localhost:8000"
echo "  Docs:   http://localhost:8000/docs"
echo "  Ollama: http://localhost:11434"
