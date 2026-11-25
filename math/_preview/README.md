# 版式打样（_preview）

正文之外的**版式试验场**：A3 试卷、A4 讲义、一页纸速查表三种成品的 demo。

- `demo-a3.tex` / `demo-a4.tex` / `demo-sheet.tex`：可直接编译的样例源文件。
- `preview-*.png`：对应的效果截图，供挑选版式时对照（PDF 按 .gitignore 不入库）。

改版心、行距、字号等全局参数后，先在这里编译打样，再回 `common/preamble.tex` 落地。
