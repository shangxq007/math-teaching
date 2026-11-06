# 知识图谱与解题流程

把一元二次函数的知识按层次结构画成图，并给出常见题型的解题流程图。
供基础较弱的同学使用：先过事实层与操作层，再碰结论层。

## 编译

```bash
cd map
latexmk -xelatex main
```

## 结构

- `main.tex` — 入口
- `figures-src/*.dot` — Graphviz 源文件（知识图谱与三张流程图）
- `figures/*.pdf` — 由 `.dot` 生成的矢量图
- `chapters/` — 知识图谱、二级结论卡片、解题流程
- `tools/build-graphs.sh` — 重新生成图片

改了 `.dot` 之后跑一次：

```bash
sh tools/build-graphs.sh
```

## 图与正文的关系

- 图只负责「结构」：层次、依赖、流程；
- 文字负责「为什么」：每条结论的推导与适用条件。

两者不要重复，否则学生会只看图不看字，或者只看字不看图。
