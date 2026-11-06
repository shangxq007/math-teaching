# Teaching

通用教学文档仓库。每个学科一个子目录，学科内按文档类型再分子目录。

## 目录结构

```
Teaching/
├── README.md
└── math/                 数学学科
│   ├── common/           共享导言区与宏
│   │   ├── preamble.tex
│   │   └── macros.tex
│   ├── lesson/           教案
│   ├── bank/             题库
│   ├── guide/            导学案
│   ├── extension/        拓展阅读（ElegantPaper）
│   ├── map/              知识图谱与解题流程
│   ├── slides/           课件（Beamer）
│   ├── figures/          封面与图片素材
│   └── .vscode/          VS Code + LaTeX Workshop 配置
└── <其他学科>/           后续新增
```

## 学科目录命名

新增学科时在 `Teaching/` 下建目录，建议用英文小写（如 `physics`、`chemistry`），
并在本文件末尾登记一行。

## 编译

每个文档类型目录（`lesson/`、`bank/`、`guide/`）都是独立的 LaTeX 工程，
进入目录后执行：

```bash
latexmk -xelatex main          # 首次 / 完整编译
latexmk -xelatex -pvc main     # 持续预览（保存即重编）
```

或在 VS Code 中打开该目录，保存即自动编译（见各目录的 `.vscode/settings.json`）。

## 登记

| 学科 | 目录 | 说明 |
| --- | --- | --- |
| 数学 | `math/` | 教案 / 题库 / 导学案 |
