#!/bin/sh
# 由 .dot 生成 PDF 图，供 main.tex 引用。
# 用法：sh tools/build-graphs.sh
set -e
cd "$(dirname "$0")/.."
mkdir -p figures
for f in knowledge three-quadratics flow-inequality flow-condition flow-extreme flow-sign-chart; do
  dot -Tpdf "figures-src/$f.dot" -o "figures/$f.pdf"
  echo "wrote figures/$f.pdf"
done

# TikZ 图（standalone，需 xelatex）
for f in set-conditions ineq-on-axis parabola interval-extreme; do
  (cd figures-src && xelatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null 2>&1)
  cp "figures-src/$f.pdf" "figures/$f.pdf"
  echo "wrote figures/$f.pdf"
done
