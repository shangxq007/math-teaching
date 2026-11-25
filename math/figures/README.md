# 封面与图片素材

- `figures-src/`：矢量源文件（SVG/AI/TikZ 导出）。
- 本目录下散放的 PDF/PNG 由源文件生成，用于各册 `\graphicspath{{../figures/}}`。
- 低多边形山峦封面（蓝／绿／青三套配色）由 `../tools/make_cover.py` 生成，不手改。

`.gitignore` 保留 `figures/**/*.pdf`，其余构建产物不入库。
