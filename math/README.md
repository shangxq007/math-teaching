# 数学教学文档

使用 ElegantLaTeX 系列模板（ElegantBook / ElegantNote）+ XeLaTeX。

## 子目录

| 目录 | 类型 | 模板 | 说明 |
| --- | --- | --- | --- |
| `lesson/` | 教案 | ElegantBook | 每章一课时，含教学目标/重难点/教学过程/板书/作业 |
| `bank/` | 题库 | ElegantBook | 题目用 `problem` 环境，解答用 `solution` 环境 |
| `guide/` | 导学案 | ElegantNote | 每课含学习目标/预习导学/课堂探究/当堂检测/课后作业 |
| `extension/` | 拓展阅读 | ElegantPaper | 课后延伸与深入，含摘要、关键词、参考文献 |
| `map/` | 知识图谱与流程 | ElegantNote | 知识层次图、二级结论卡片、解题流程图 |
| `slides/` | 课件 | Beamer + Metropolis | 16:9 演示文稿，保存即编译 |
| `common/` | — | — | 共享导言区 `preamble.tex` 与教学宏 `macros.tex` |
| `figures/` | — | — | 封面与图片素材 |

每个子目录都有自己的 `README.md`，说明该类型的写法与约定。

## 快速开始

```bash
cd lesson        # 或 bank / guide
latexmk -xelatex main
```

## 约定

- 每个 `chapters/` 目录存放按课时/章节拆分的 `.tex`，文件名以序号开头（`01.tex`、`02.tex`）。
- 新课时：在 `chapters/` 新增文件，并在 `main.tex` 中 `\input` 一行。
- 图片统一放 `figures/`，在 `main.tex` 中用 `\graphicspath{{../figures/}}` 引入。
- 中文字体与数学字体已在 `common/preamble.tex` 中统一配置，不要在单个文件里重复设置。
- `extension/` 的编号与 `lesson/` 的课次号对应；教案与导学案的作业环节用 `\reading{编号}{篇名}` 指向对应篇目。
