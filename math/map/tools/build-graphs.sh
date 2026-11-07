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
