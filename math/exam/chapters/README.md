# 试卷章节写法

## 文件命名

`01.tex`、`02.tex`……每份卷一个文件，与 `../lesson/chapters/` 的课次号无关。
新增后在 `../main.tex` 里加 `\input{chapters/02}`。

## 骨架

一份卷子三段，顺序固定：

1. **细目表**——考点 / 题型 / 题号 / 分值 / 难度 / 预估用时，末尾合计行；
2. **卷头**——`\maketitle` + `notice` 环境（注意事项）+ `\information`（填写线）；
3. **试题**——按「选择 → 填空 → 解答」三节。

## 三条原则

- **题号连续**，全卷一个序列（选择 1–8、填空 9–12、解答 13–15），不要分节重排；
- **分值写进节标题**，如「选择题（每题 5 分，共 40 分）」，并在细目表里能核出来；
- **难度比例**按学段定：平时 5:3:2（易中难），月考 4:4:2，期中期末 3:4:3。

## 常见报错

| 报错 | 原因 |
| --- | --- |
| `Environment choices* undefined` | `choices` 里写成了 `choices*`；选项直接写多个 `\item` |
| `Key 'exam-zh/sealline/scope' accepts only ...` | `scope` 的取值是 `everypage` / `oddpage` / `firstpage` 等，没有 `all` |
| `Improper \prevdepth` / `missing \item` | `\notice{...}` 当命令用了；它是环境 |
| `Font "NewCM10-Book" cannot be found` | 导言区没设 `font = termes` |
