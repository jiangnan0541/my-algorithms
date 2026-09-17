# my-algorithms — 经典算法手写实现

> 复刻自官方仓库：<https://github.com/TheAlgorithms/Python>
> 路线：读源码 → 写 mini 版 → 证对比 → 提 PR

手写实现经典算法，按 **排序 / 动态规划 / 图论** 三大类组织，全部配 pytest 单元测试。

## 我做了什么

- 从零手写 **100+** 经典算法（排序 30 / 动态规划 30 / 图论 40），统一风格、统一测试。
- 每个算法附：复杂度标注、docstring 说明、边界用例。

## 学到什么

- （持续补充）关键知识点、踩过的坑、设计取舍。

## 与官方对比

| 维度 | 官方 TheAlgorithms/Python | 我的 mini 版 |
|------|---------------------------|--------------|
| 功能覆盖 | 上千个算法，按学科分几十个目录 | 聚焦 3 类共 100+ 个，精选高频 |
| 代码量 | 庞大、贡献者众多、风格不一 | 精简、风格统一 |
| 性能 | 教学可读优先 | 同样教学优先，额外标注时间/空间复杂度 |
| 测试 | doctest 与 pytest 混用 | 统一 pytest，目标覆盖率 >80% |

## 目录结构

```
my-algorithms/
├── src/myalgo/
│   ├── sorting/               # 排序
│   ├── dynamic_programming/   # 动态规划
│   └── graph/                 # 图论
├── tests/                     # pytest 单元测试
├── docs/
│   ├── architecture.md        # 官方源码模块依赖图
│   └── source-notes/          # 读源码笔记
├── requirements.txt
└── pyproject.toml             # pytest 配置
```

## 环境

- Python 3.11（Anaconda3 环境：`conda activate py311`）
- 依赖：`pip install -r requirements.txt`（pytest 走清华镜像，秒装）

## 运行

```bash
conda activate py311
pytest -q                      # 跑全部测试
pytest -v tests/test_sorting.py  # 只跑排序类
```

## 进度

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M1 | 三类各手写 10 个，跑通 pytest | 🔄 进行中（每类已有 1 个样板） |
| M2 | 补 docstring + 边界用例，覆盖率 >80% | ⬜ |
| M3 | README 写分类索引 | 🔄 已完成索引骨架 |

### 分类索引

| 分类 | 目录 | 已完成 | 目标 |
|------|------|--------|------|
| 排序 | `src/myalgo/sorting/` | 1 | 10 |
| 动态规划 | `src/myalgo/dynamic_programming/` | 1 | 10 |
| 图论 | `src/myalgo/graph/` | 1 | 10 |

## 参考

- 官方仓库：<https://github.com/TheAlgorithms/Python>
- 模块依赖图：见 `docs/architecture.md`
- 复刻方法论：见 `METHODOLOGY.md`
