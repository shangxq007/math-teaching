# Teaching

通用教学文档仓库（git 管理）。每个学科一个子目录，学科内按文档类型再分子目录。
**构建产物不入库**：编译好的 PDF、LaTeX 中间文件、Manim 视频均忽略（见 `.gitignore`）。

## 目录结构

```
Teaching/
├── README.md            本文件：仓库说明与学科登记
└── math/                数学学科（子库自带 README.md，含完整文档体系）
    ├── common/          共享导言区与宏（preamble / macros / envs）
    ├── sources/         外部原始素材（raw/ 逐字拷贝 + 索引）
    ├── handout/         讲义（学生主材料，六段结构）
    ├── outline/         理论概要（骨架，无例题）
    ├── notes/           笔记（四段留白）
    ├── formula/         速查表（A4 横版三栏）
    ├── map/             知识图谱与解题流程
    ├── topic/           专题训练（12 个专题）
    ├── errorbook/       错题本（错解→正解→变式→反思）
    ├── guide/           导学案（与教材同步章节）
    ├── extension/       拓展阅读（ElegantPaper）
    ├── modeling/        建模活动单
    ├── exam/            试卷 + 命题细目表（exam-zh）
    ├── bank/            题库（与教材同步章节）
    ├── answer/          答案与解析
    ├── lesson/          教案
    ├── reflection/      教学反思
    ├── slides/          课件（Beamer + Metropolis，16:9）
    ├── hv-guide/        高观点系列导学案（独立成册，编号 0–9；架构见其 ARCHITECTURE.md）
    ├── hv-bank/         高观点系列题库（独立成册，编号 0–9）
    ├── manim/           Manim CE 动画工程（渲染走 manim-video skill 的 manim-run.sh）
    ├── figures/         封面与图片素材（仅此目录保留矢量图 PDF/PNG）
    ├── tools/           小工具（make_cover.py 生成封面）
    └── _preview/        版式打样（demo tex + preview png）
```

各子目录自带 `README.md`，说明该类型的写法与约定；数学库的完整分层说明见 `math/README.md`。

## 约定

- 学科目录用英文小写（如 `physics`、`chemistry`），并在下方「登记」表补一行。
- 每个文档类型目录都是独立 LaTeX 工程，进入目录执行：

  ```bash
  latexmk -xelatex main          # 首次 / 完整编译
  latexmk -xelatex -pvc main     # 持续预览（保存即重编）
  ```

  或在 VS Code 中打开该目录，保存即自动编译（见各目录 `.vscode/settings.json`）。
- 新增盒子环境前先查 `common/envs.tex`；字体与版式只在 `common/preamble.tex` 设置一次。
- 高观点系列单独成册（`hv-guide/`、`hv-bank/`），编号自成体系，不与 `guide/`、`bank/` 混排。

## 构建产物不入库

`.gitignore` 统一忽略 `*.pdf`（`figures/` 下的矢量源图除外）、LaTeX 中间文件、
`*_variant_*.tex`、`dist/`，以及 Manim 的媒体/视频产物。换机器后重新编译即可复现。

## 登记

| 学科 | 目录 | 说明 |
| --- | --- | --- |
| 数学 | `math/` | 教案 / 题库 / 导学案 / 高观点系列 / Manim 动画 |
