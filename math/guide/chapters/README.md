# 导学案章节目录

每个文件对应一个课时，文件名以两位序号开头，按顺序在 `../main.tex` 中 `\input`。

- `01.tex` — 集合的含义与表示

新增课时步骤：

1. 在此目录新建 `NN.tex`（如 `02.tex`）；
2. 在 `../main.tex` 中追加 `\input{chapters/02}`；
3. 保存即自动编译。

模板使用 ElegantNote（article 结构），章节用 `\section`。
