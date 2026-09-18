# 上游 PR 计划（方法论第④步「贡献」）

> 目标：往 TheAlgorithms/Python 提 1 个被合并的 PR —— 这是简历上最强的一类背书。
>
> **官方规则（读 CONTRIBUTING.md 得出）**：
> - **不要**开 issue 说"我要实现某个算法"，直接提 PR
> - 修文档、补注释、加测试类 PR 同样受欢迎
> - 文件名严格 snake_case；同行注释不超过 88 字符
> - 注释要解释 **why** 而不是复述 **what**；注释放在被描述代码的**前面**
> - `ruff check` 必须通过（提交前本地跑一遍）
> - 不要更新 `README.md` / `DIRECTORY.md`（由 CI 自动生成）

---

## 已发现的候选（按落地难度排序）

### ★ 候选 1：修正 CONTRIBUTING.md 的拼写错误（**建议从这个起步**）

**位置**：`CONTRIBUTING.md` 第 199 行

**现状**：

```
[Install ty](https://docs.astral.sh/ty/installation/) and then pslease use the command
`ty check` to test all files or `ty check path/to/file.py` to test a specific file.
```

**问题**：`pslease` 是 `please` 的拼写错误。

**改动**：

```diff
-[Install ty](https://docs.astral.sh/ty/installation/) and then pslease use the command `ty check` to test all files or `ty check path/to/file.py` to test a specific file.
+[Install ty](https://docs.astral.sh/ty/installation/) and then please use the command `ty check` to test all files or `ty check path/to/file.py` to test a specific file.
```

**为什么适合做第一个 PR**：

- 改动只有 1 个字符，零争议、零风险，维护者几乎没有拒绝的理由
- 是**客观错误**，不是我主观觉得"应该改"
- 通常几小时到几天内就能合并，能快速拿到第一个 contribution 记录

**PR 标题**

```
docs: fix typo "pslease" -> "please" in CONTRIBUTING.md
```

**PR 描述**（英文，照官方模板，简洁）

```markdown
### Describe your change:

- [x] Fix a typo in documentation

Fixes a typo in `CONTRIBUTING.md`: `pslease` -> `please`.

### Checklist:

- [x] I have read [CONTRIBUTING.md](https://github.com/TheAlgorithms/Python/blob/master/CONTRIBUTING.md)
- [x] This pull request is all my own work -- I have not plagiarized it.
- [x] All filenames are in snake_case.
- [x] All functions and variable names follow Python naming conventions.
- [x] All new and existing tests passed.
```

---

### ☆ 候选 2：删掉 CONTRIBUTING.md 里重复粘贴的段落

**位置**：`CONTRIBUTING.md` 第 70-82 行

**现状**：`#### Pre-Commit Plugin` 这个标题下面，内容是前面
`#### What is an Algorithm?` 章节（第 56-68 行）的**逐字重复** ——
同一个 "have intuitive class and function names…" 列表被粘贴了第二遍。
真正的 pre-commit 章节在第 84 行的 `#### Pre-commit`。

**改动**：删除第 70-82 行整段（含那个名不副实的小标题）。

**建议**：和候选 1 放进**同一个 PR**，因为都是同一文件里的文档修正，
一次贡献解决两处问题。标题改为：

```
docs: fix typo and remove duplicated section in CONTRIBUTING.md
```

> 如果担心"一次 PR 只做一件事"的评审习惯，就只提交候选 1 —— 它更保险。

---

### △ 候选 3：`graphs/dijkstra.py` 的模块级副作用（**暂缓，争议较大**）

**位置**：`graphs/dijkstra.py` 第 107-114 行

**现状**：模块顶层直接执行了三条 `print(short_distance)`，
导致 **import 这个文件就会打印 3 行结果**。

**与官方规范冲突**：CONTRIBUTING 明确要求算法应
"have minimal side effects (e.g., `print()`, `plot()`, `read()`, `write()`)"、
"return all calculation results instead of printing or plotting them"。

**为什么暂缓**：

- 该文件的 doctest 依赖模块级变量 `G` / `G2` / `G3`，一改就得连带重构；
- 全仓可能不止这一处同类写法，单独改一个容易被认为"风格不统一"；
- 这类改动需要讨论，等候选 1/2 建立起可信度后再动更稳妥。

---

## 操作流程（等 M1 全部完成后执行）

1. 在 GitHub 网页上 fork `TheAlgorithms/Python` 到自己的账号（`jiangnan0541`）
2. 克隆自己的 fork 并建分支：

   ```bash
   git clone git@github.com:jiangnan0541/Python.git ta-python
   cd ta-python
   git checkout -b docs/fix-typo-contributing
   ```

3. 改文件 —— **只改这一处，不要顺手改别的**
4. 提交：

   ```bash
   git commit -am 'docs: fix typo "pslease" -> "please" in CONTRIBUTING.md'
   ```

5. 推送并开 PR：

   ```bash
   git push origin docs/fix-typo-contributing
   ```

   然后在网页上提 PR，标题 / 描述照上面写。

6. 等 CI 跑完（绿了就等 review），期间**不要**反复 push 催促

## 注意事项

- 官方**不认领 issue**，直接提 PR 即可
- 一个 PR 只解决一件事（候选 1 和 2 是否合并，按当时判断）
- PR 描述用英文，客气、简短、不寒暄
- 提交信息遵循他们的习惯：`docs: ...` / `fix: ...`（仓库大量使用 Conventional Commits）
- 别动 `README.md` 和 `DIRECTORY.md`

---

## ✅ 状态（2026-09-18 已执行）

**候选 1（CONTRIBUTING.md 拼写 `pslease`→`please`）已提交 PR：**

- **PR 链接**：https://github.com/TheAlgorithms/Python/pull/15375 （状态 OPEN）
- **fork**：`jiangnan0541/Python`（GitHub 给 fork 沿用上游仓库名 "Python"；父仓库已核实 = `TheAlgorithms/Python`）
- **分支**：`fix/contributing-typo`（基于 fork 的 `master` HEAD `a3815789` 创建）
- **commit**：`64ddc75a70c62061d91dab63eec81363d2cea173`
- **提交信息**：`docs: fix typo pslease to please in CONTRIBUTING.md`

**操作方式（无需克隆大仓库）**：用 `gh api` 直接走 API ——

1. `gh api -X POST repos/TheAlgorithms/Python/forks`（创建 fork，幂等）
2. `gh api repos/jiangnan0541/Python/git/refs/heads/master --jq .object.sha` 取 master HEAD
3. `gh api -X POST repos/jiangnan0541/Python/git/refs -f ref=refs/heads/fix/contributing-typo -f sha=<master>` 建分支
   （⚠️ contents API 的 `branch` 参数**不会**自动建分支，必须先建好，否则 404）
4. `gh api repos/jiangnan0541/Python/contents/CONTRIBUTING.md?ref=master` 取 `sha` + base64 内容
5. 本地把 `pslease`→`please`、重新 base64，再 `gh api -X PUT .../contents/CONTRIBUTING.md -f branch=... -f content=<b64> -f sha=<原sha>`
6. `gh pr create --repo TheAlgorithms/Python --head jiangnan0541:fix/contributing-typo --base master --title ... --body ...`

> 参考克隆里未搜到 DCO / sign-off 要求，上游大概率不强制 DCO；PR 已正常 OPEN，等 CI 与 review。
> 若后续要补第二个候选（删重复段落），建议另开一个 PR，保持"一个 PR 一件事"。
