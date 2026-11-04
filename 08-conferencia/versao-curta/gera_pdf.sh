#!/bin/zsh
# gera_pdf.sh: renderiza as duas versões para a AIM 2027 (versão curta de cerca de 9 mil palavras, extended abstract de 3 mil e prévia Elsevier da versão curta)
# em PDF com o Chrome headless e deixa uma cópia autocontida no Desktop (HTML + figuras + PDFs).
# Uso: ./gera_pdf.sh            (no Mac; no desktop Windows trocar o caminho do navegador)
set -e
AQUI="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$AQUI/../.." && pwd)"
DESK="$HOME/Desktop/AIM 2027 - Versao Curta"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DATA="$(date +%F)"

mkdir -p "$DESK/figuras"
for f in fig7_armados.jpg fig8_nadir_obliquo.jpg fig9_desenho_experimental.png fig10_ajuste_fino.png fig12_limiar_armado.png; do
  cp "$REPO/06-resultados/figuras/$f" "$DESK/figuras/"
done
for par in "versao-curta-aim2027.html:AIM2027_versao-curta-9k-palavras_$DATA.pdf" "esqueleto-aim2027.html:AIM2027_extended-abstract-3k-palavras_$DATA.pdf" "versao-curta-elsevier.html:AIM2027_versao-curta_previa-elsevier_$DATA.pdf"; do
  html="${par%%:*}"; pdf="${par##*:}"
  # a cópia do Desktop aponta para ./figuras em vez de ../../06-resultados/figuras
  sed 's#\.\./\.\./06-resultados/figuras/#figuras/#g' "$AQUI/$html" > "$DESK/$html"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$DESK/$pdf" "file://$DESK/$html" 2>/dev/null
  echo "PDF: $DESK/$pdf"
  command -v pdfinfo >/dev/null && pdfinfo "$DESK/$pdf" | grep Pages
done
