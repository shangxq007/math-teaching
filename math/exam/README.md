# 试卷

测评用卷。A3 横版双栏（两页 A4 拼一张 A3），自带密封线、卷头、页脚页码。

## 定位与分工

| 文档 | 性质 | 依据 |
| --- | --- | --- |
| 题库 `../bank/` | 按考点堆题 | 考点 |
| **试卷（本目录）** | **按细目表组卷** | **考点 × 题型 × 分值 × 难度** |
| 讲义 `../handout/` | 课后练手 | 课时 |

**先写细目表，再填题。** 细目表定了考点、题型、题号、分值、难度、预估用时，
题目只是往格子里填。没有细目表的试卷无法保证覆盖面，也无法复核。

## 版式

- `exam-zh` 类，`page/size = a3paper` → A3 横版双栏，左栏第 1 页、右栏第 2 页；
- 密封线 `sealline/show = true`，`scope = everypage`；
- 字体用 `font = termes, math-font = termes`（本机最省事，避免 newcm/asana 缺字体）。

改 A4：把 `size = a3paper` 改成 `size = a4paper` 重新编译。

## 编译

```bash
cd exam
latexmk -xelatex -g main
```

**必须 XeLaTeX**，`exam-zh` 仅支持 XeLaTeX。若报 `The font "NewCM10-Book" cannot be found`，
说明 `font` 没设成 termes；若报 `Asana-Math.otf ... not loadable`，装一下：
`sudo tlmgr install asana-math`。

## 文件

```
main.tex             学生卷：卷头 + 样卷（A3 横版双栏）
blueprint.tex        命题细目表（教师用，A4 竖版，单独编译）
chapters/README.md   题型写法细节
```

## 两份文件的关系

`blueprint.tex` 是**组卷的前置表**，先填它，再照它往 `main.tex` 填题。
改表之后题号会动，所以顺序永远是「先改表，再改卷」，不要反过来。

```bash
cd exam
latexmk -xelatex -g main        # 学生卷
latexmk -xelatex -g blueprint   # 细目表
```

## 题型写法

```latex
% 选择题：question 里写题干，choices 里写选项
\begin{question}
题干 \paren
\begin{choices}
\item 选项 A
\item 选项 B
\end{choices}
\end{question}

% 填空题：答案是方括号，不是花括号
\begin{question}
题干 \fillin[答案]
\end{question}

% 解答题与解答
\begin{problem}（20 分）题干 \end{problem}
\begin{solution} 解答 \end{solution}
```

注意：`choices` 必须写在 `question` **里面**；`\notice` 是环境（`\begin{notice}\item...\end{notice}`），
不是命令。
