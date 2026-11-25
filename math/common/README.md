# 共享导言区与宏

全库共用，**不要在单个文档里重复设置**。

- `preamble.tex`：字体（Noto Serif/Sans CJK、Asana Math）、数学宏包、版式（A4、边距 18mm、行距 1.2）、`\complement` 补丁。
- `macros.tex`：教案／导学案的结构环境与常用命令（`\tk`、`\blank`、`\level`、`\key` 等）。
- `envs.tex`：讲义／笔记／卡片／错题本／速查表／反思的盒子环境（`derivation`、`summary`、`conccard`、`commonerror` 等）。

新增环境前先查这里有没有现成的；各册 `main.tex` 统一 `\input{../common/preamble}` 之类引入。
