# 章节文件

- `01-knowledge.tex` — 六层知识结构与知识图谱
- `02-conclusions.tex` — 二级结论卡片
- `03-flows.tex` — 解题流程图（补充说明）
- `04-tools.tex` — 三个二次、数轴穿根法、幂指对、三角工具

新增一篇时，文件名以序号开头，并在 `../main.tex` 中 `\input`。
图源放在 `figures-src/`（Graphviz `.dot` 或 TikZ standalone），用
`tools/build-graphs.sh` 生成到 `figures/`。
