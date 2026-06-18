[🇨🇳 中文](CONTRIBUTING.md) | [🇬🇧 English](CONTRIBUTING_EN.md)

---

# 🤝 贡献指南

感谢你愿意帮助 SourceGuide 变得更好！

> **目标：** 把任意 GitHub 仓库或本地项目转换成清晰、可信、适合中文开发者阅读的源码学习路线。

欢迎提交 Issue、Pull Request、真实仓库生成示例、文档改进和新的技术栈识别规则。

---

## 📋 目录

- [🐣 适合贡献的方向](#-适合贡献的方向)
- [🛠️ 开发环境](#️-开发环境)
- [📝 Pull Request Checklist](#-pull-request-checklist)
- [🎯 Issue 类型](#-issue-类型)
- [🧭 设计原则](#-设计原则)
- [📦 发布与维护](#-发布与维护)

---

## 🐣 适合贡献的方向

| 方向 | 说明 |
| --- | --- |
| 🧩 **新技术栈识别** | PHP、C#、Ruby、移动端、Monorepo 等 |
| 🎯 **改进运行方式推断** | 更准确识别安装/启动/测试/lint/Docker 命令 |
| 📝 **改进文档生成质量** | 让中文输出更自然、更少模板味 |
| 📸 **真实仓库示例** | 帮助用户理解 SourceGuide 的效果 |
| 🧪 **测试 fixture** | 覆盖更多项目结构和边界情况 |
| 📖 **文档改进** | README、示例、错误提示、贡献流程 |

---

## 🛠️ 开发环境

推荐 Python 3.10+。

```bash
# 克隆 & 进入项目
git clone https://github.com/liduanchen/SourceGuide.git
cd SourceGuide

# 创建虚拟环境
python -m venv .venv
```

**Windows PowerShell：**
```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

**macOS / Linux：**
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**常用命令：**

```bash
# 运行测试
pytest

# 离线生成演示文档（不需要 API Key）
sourceguide generate . --route quick --offline --output demo/sourceguide --overwrite

# 查看 CLI 帮助
sourceguide --help
sourceguide generate --help
```

---

## 📝 Pull Request Checklist

提交 PR 前请逐项确认：

```markdown
- [ ] 已为行为变化**新增或更新测试**
- [ ] 已运行 `pytest` **全部通过**
- [ ] 没有提交 API Key、`.env`、临时 clone 目录、缓存或生成产物
- [ ] CLI 参数、环境变量名、输出文件名**保持兼容**
- [ ] 修改了对外行为 → 已更新 `CHANGELOG.md`
- [ ] 文档引用的文件**来自真实扫描结果**
- [ ] 不确定的信息标注了**"不确定"**
```

---

## 🎯 Issue 类型

| 类型 | 标签 | 说明 |
| --- | --- | --- |
| 🐛 **Bug** | `bug` | 扫描错误、生成错误、CLI 异常、校验器误判 |
| ✨ **Feature** | `enhancement` | 新技术栈识别、输出格式、AI Provider、工作流 |
| 📖 **Docs** | `documentation` | README、示例、生成文档清晰度、贡献说明 |
| ❓ **Question** | `question` | 使用方式、配置、路线图或设计讨论 |

---

## 🧭 设计原则

1. **不是 README 总结器**——而是源码学习路线生成器
2. **所有路线都必须包含"如何运行这个项目"**
3. **所有引用文件必须来自真实扫描结果**
4. **不确定的内容必须标注"不确定"**
5. **Markdown 输出能直接放进 GitHub 仓库**
6. **对外接口谨慎变更**——CLI 参数、环境变量、输出文件名

---

## 📦 发布与维护

项目遵循[语义化版本](https://semver.org/)：

```
MAJOR.MINOR.PATCH
```

- `MAJOR`：破坏性变更
- `MINOR`：新增向后兼容的功能
- `PATCH`：修复问题、优化文档或小幅改进

公开行为发生变化时，请更新 `CHANGELOG.md`。破坏性变更需要在 PR 中说明原因、影响范围和迁移方式。

---

<div align="center">

**再次感谢你的贡献！** 🎉

</div>
