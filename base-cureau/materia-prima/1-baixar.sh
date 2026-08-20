#!/usr/bin/env bash
# Baixa os reels da @lucureau listados em urls.txt.
#
# Pré-requisitos (uma vez só):
#   pip install -U yt-dlp
#   estar LOGADO no Instagram no navegador (o yt-dlp pega o cookie de lá)
#
# Uso:
#   ./1-baixar.sh              # baixa tudo de urls.txt
#   ./1-baixar.sh tier1.txt    # baixa só o arquivo que você passar
#
# Trocar 'chrome' pelo seu navegador se for outro: firefox, brave, edge, safari.

set -euo pipefail

LISTA="${1:-urls.txt}"
NAVEGADOR="${NAVEGADOR:-chrome}"
DESTINO="${DESTINO:-videos}"

mkdir -p "$DESTINO"

yt-dlp \
  --cookies-from-browser "$NAVEGADOR" \
  --batch-file "$LISTA" \
  --output "$DESTINO/%(id)s.%(ext)s" \
  --write-info-json \
  --no-overwrites \
  --ignore-errors \
  --sleep-requests 2 \
  --retries 5

echo
echo "Baixados em $DESTINO/:"
ls -1 "$DESTINO"/*.mp4 2>/dev/null | wc -l
echo
echo "A data de cada post está no .info.json (campo 'timestamp' / 'upload_date')."
echo "Não jogue os .info.json fora — a data é obrigatória na base de princípios."
