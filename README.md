# fitness-coach

健身统一入口 Skill：**知识答疑（带文件出处）+ 个人碳蛋脂配额计算 + 课程笔记检索** 三合一。一个入口接住所有健身需求，内部按意图路由到对应引擎。

## 安装

```bash
npx -y skills add hou-152/fitness-coach -g --all
```

## 三个子命令

```bash
# 知识检索（自动展开错字变体，命中带文件与行号）
python3 scripts/fc.py ask 蛋白质 分餐

# 碳蛋脂配额（已验证矩阵，展示匹配档位）
python3 scripts/fc.py quota --gender male --weight 70 --height 175 --goal fat-loss --training strength

# 研究层笔记检索
python3 scripts/fc.py notes 练后餐
```

作为 Agent Skill 使用时，无需手选——意图路由表自动分发：知识类 → 检索引擎；数字类 → 配额引擎；检索类 → 笔记引擎。

## 数据来源与授权

- 配额矩阵：B站UP主「好人松松」**【可任意分享】健身Excel超级套表**（25年9月版，SHA-256 `dc3ff002…`）
- 知识检索覆盖：UP 主直播课/图文的个人学习笔记与研究重述（公开传播需原作者授权）

## 依赖链（重要）

本 Skill 是**编排层**，按以下依赖工作：

| 引擎 | 作用 | 依赖 |
|---|---|---|
| `ask` | 需要 [fitness-kb](https://github.com/hou-152/fitness-kb)（如已发布）或本地知识库 | 58 万字文本层 + 概念变体表（自建） |
| `quota` | 需要 [diet-plan](https://github.com/hou-152/diet-plan)（已发布，矩阵内置） | 无外部依赖 |
| `notes` | 需要本地研究层目录（`研究工程/02-内容单元库/`，自建） | 无 |

没有本地知识库时，`ask` 与 `notes` 不可用（脚本会明确提示），`quota` 独立可用。

## 运行依赖

- 支持 Agent Skills 的客户端
- Python 3

## 已知边界

- 不回答伤病/疾病/疼痛类问题（建议就医）
- 输出为个人参考，非医疗建议
- 转写文本含 ASR 错字，检索靠概念变体表容错（内置）

## 内容

本仓库只发布运行 Skill 所需文件。评测样本、运行记录、私有知识库内容不包含在公开包中。
