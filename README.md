<div align="center">

[🇨🇳 中文](README.md) | [🇬🇧 English](README_EN.md)

---

# 📖 SourceGuide

**把任意 GitHub 仓库变成源码学习路线**

<p>
  <a href="https://github.com/liduanchen/SourceGuide/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/liduanchen/SourceGuide/ci.yml?branch=master&style=flat-square" alt="CI Status">
  </a>
  <a href="https://github.com/liduanchen/SourceGuide/commits/master">
    <img src="https://img.shields.io/github/last-commit/liduanchen/SourceGuide?style=flat-square" alt="Last Commit">
  </a>
  <a href="https://github.com/liduanchen/SourceGuide">
    <img src="https://img.shields.io/github/languages/code-size/liduanchen/SourceGuide?style=flat-square" alt="Code Size">
  </a>
  <a href="https://github.com/liduanchen/SourceGuide">
    <img src="https://img.shields.io/github/languages/top/liduanchen/SourceGuide?style=flat-square" alt="Top Language">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/liduanchen/SourceGuide?style=flat-square" alt="License">
  </a>
</p>

<p>
  <b>中文</b> · <a href="#features">功能</a> · <a href="#quick-start">快速开始</a> · <a href="#usage">用法</a> · <a href="#how-it-works">原理</a> · <a href="#roadmap">路线图</a>
</p>

<br>

[✨ 在线体验](https://codespaces.new/liduanchen/SourceGuide) &nbsp;|&nbsp; [📖 查看输出示例](examples/README.md) &nbsp;|&nbsp; [🤝 贡献指南](CONTRIBUTING.md)

</div>

---

## 🎯 这是什么？

SourceGuide 是一个面向中文开发者的开源 CLI 工具。你**给它一个 GitHub 仓库地址或本地项目目录**，它会自动分析项目结构、识别技术栈、推断运行方式、找出核心文件，然后生成一组**适合阅读和分享的源码学习路线**。

> **它不是 README 总结器。** 同一个仓库，不同目的的人应该有不同读法。

<a id="features"></a>

## ✨ 功能

- 📦 支持**公开 GitHub 仓库 URL** 和**本地项目目录**
- 🧠 自动识别 **Python、Node.js、Go、Rust、Java、Docker** 等常见技术栈
- 🔍 自动推断**安装、启动、测试和 lint** 命令
- 🏆 自动生成**核心文件 Top 10** 和推荐阅读顺序
- 🔌 支持 **OpenAI 兼容 API**（可接入任意 LLM）
- 🌏 默认**中文输出**，支持单条/全部路线生成
- ⚙️ 环境变量配置，适合本地开发和 CI
- 📝 **Markdown-first**，方便放入 GitHub、掘金、知乎或文档站

<a id="quick-start"></a>

## 🚀 快速开始

### 前提条件

- Python 3.9+
- 一个 OpenAI 兼容 API Key

### 在线体验

点击 [✨ 在线体验](https://codespaces.new/liduanchen/SourceGuide) 会打开 GitHub Codespaces 云端开发环境。环境创建完成后可以直接运行：

```bash
sourceguide --help
sourceguide generate . --route quick --offline --output demo/sourceguide --overwrite
```

`--offline` 会使用规则生成器生成演示文档，不需要 API Key。真实 AI 生成仍然需要配置 `OPENAI_API_KEY`。

### 安装

```bash
git clone https://github.com/liduanchen/SourceGuide.git
cd SourceGuide
python -m venv .venv
```

**Windows PowerShell：**
```powershell
.\.venv\Scripts\Activate.ps1
pip install -e .
```

**macOS / Linux：**
```bash
source .venv/bin/activate
pip install -e .
```

验证安装：
```bash
sourceguide --help
```

### 配置 API Key

```bash
export OPENAI_API_KEY="sk-your-api-key"
```

Windows PowerShell 用户：
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key"
```

> 💡 也可参考 [`.env.example`](.env.example) 配置文件。**不要把真实 API Key 提交到 GitHub。**

### 生成文档

**分析本地项目：**
```bash
sourceguide generate .
```

**分析公开 GitHub 仓库：**
```bash
sourceguide generate https://github.com/pallets/flask
```

就是这么简单！输出会默认生成到 `docs/sourceguide/` 目录下。

## 📄 生成内容

SourceGuide 会为每个仓库生成 **4 条学习路线 + 若干参考文档**：

```
docs/sourceguide/
├── README.md                 ← 路线索引
├── 01-我是小白路线.md         ← 🟢 从零跑起来
├── 02-快速了解路线.md         ← 🔵 10 分钟判断价值
├── 03-贡献者路线.md           ← 🟣 参与开发入口
├── 04-项目面试路线.md         ← 🟠 简历/面试/分享
├── run-guide.md              ← 运行指南
├── source-map.md             ← 源码地图
├── architecture.md           ← 架构概览
├── glossary.md               ← 术语表
└── exercises.md              ← 练习题
```

每条路线都**必须包含"如何运行这个项目"**。如果运行方式无法自动确定，SourceGuide 会明确列出已发现的线索、可能的启动方式和排查建议。

<a id="usage"></a>

## 📖 用法

```text
sourceguide generate <repo-or-path> [options]
```

| 选项 | 默认值 | 作用 |
| --- | --- | --- |
| `--route` | `all` | `all` / `beginner` / `quick` / `contributor` / `interview` |
| `--output` | `docs/sourceguide` | 输出目录 |
| `--model` | `gpt-4.1-mini` | 模型名称 |
| `--base-url` | `https://api.openai.com/v1` | API 地址 |
| `--language` | `zh-CN` | 输出语言 |
| `--depth` | `normal` | 教程深度：`basic` / `normal` / `deep` |
| `--overwrite` | `false` | 覆盖已有输出 |
| `--offline` | `false` | 使用规则生成器离线生成演示文档，不调用 AI API |

> CLI 参数优先级高于环境变量。

### 示例

```bash
# 只生成"快速了解"路线
sourceguide generate . --route quick --overwrite

# 指定输出目录
sourceguide generate . --output docs/sourceguide --overwrite

# 临时覆盖模型和 API 地址
sourceguide generate . --model gpt-4.1 --base-url https://api.example.com/v1

# 不配置 API Key，先离线体验生成效果
sourceguide generate . --route quick --offline --output demo/sourceguide --overwrite
```

## ⚙️ 配置

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `OPENAI_API_KEY` | — | **必填**。API Key |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI 兼容 API 地址 |
| `SOURCEGUIDE_MODEL` | `gpt-4.1-mini` | 默认模型 |
| `SOURCEGUIDE_LANGUAGE` | `zh-CN` | 输出语言 |
| `SOURCEGUIDE_OUTPUT_DIR` | `docs/sourceguide` | 默认输出目录 |
| `SOURCEGUIDE_DEPTH` | `normal` | 教程深度：`basic` / `normal` / `deep` |
| `SOURCEGUIDE_TIMEOUT` | `60` | API 超时（秒） |
| `SOURCEGUIDE_DEBUG` | `false` | 是否输出调试信息 |

<a id="how-it-works"></a>

## 🧠 原理

SourceGuide 采用“先规则扫描，再分阶段生成，最后强校验”的流程。它不会把整个仓库一次性丢给模型，而是先把项目压缩成可信的结构化线索，再生成面向不同读者的路线文档。

```mermaid
flowchart TD
    A["输入<br/>GitHub URL / 本地路径"] --> B["准备源码<br/>clone 或读取本地目录"]

    subgraph S1["规则分析层"]
        C["扫描文件树<br/>过滤无关文件"]
        D["识别项目线索<br/>README / 依赖 / 配置 / 入口 / 测试"]
        E["识别技术栈<br/>Python / Node / Go / Rust / Java / Docker"]
        F["推断运行方式<br/>安装 / 启动 / 测试 / lint"]
        G["排序核心文件<br/>Top 10 + 阅读顺序"]
    end

    subgraph S2["生成与校验层"]
        H["构造分析上下文<br/>只使用真实扫描结果"]
        I["AI 分阶段生成<br/>四条源码学习路线"]
        J["质量校验<br/>运行说明 / 真实文件引用 / 不确定标注"]
    end

    subgraph S3["Markdown 输出"]
        K["docs/sourceguide/<br/>路线 / 运行指南 / 源码地图 / 架构 / 术语 / 练习"]
    end

    B --> C --> D --> E --> F --> G --> H --> I --> J --> K
```

| 阶段 | 做什么 | 产物 |
| --- | --- | --- |
| **准备源码** | 接收本地路径或 GitHub URL，必要时克隆公开仓库 | 可扫描的项目目录 |
| **规则分析** | 扫描文件树、识别技术栈、推断运行方式、排序核心文件 | 结构化项目上下文 |
| **分阶段生成** | 基于真实扫描结果生成 4 条学习路线和辅助文档 | Markdown 草稿 |
| **质量校验** | 检查运行说明、真实文件引用和“不确定”标注 | 可发布文档 |
| **写入输出** | 将结果写入 `docs/sourceguide/` | GitHub 友好的文档包 |

> 设计重点：所有被引用的源码文件必须来自真实扫描结果；无法确认的信息必须写成“不确定”，而不是生成看起来很自信的幻觉内容。

## 🧱 项目结构

```
src/sourceguide/
├── cli.py          # CLI 入口
├── config.py       # 环境变量配置
├── repository.py   # 本地目录和 GitHub 仓库准备
├── scanner.py      # 文件扫描
├── stack.py        # 技术栈识别
├── runtime.py      # 运行方式推断
├── core_files.py   # 核心文件识别
├── ai.py           # OpenAI 兼容 Provider
├── renderer.py     # 规则生成器和模板化输出
├── writer.py       # Markdown 写入
├── validators.py   # 输出校验
└── pipeline.py     # 主流程编排
```

## 🛠️ 开发

```bash
pip install -e ".[dev]"
pytest
```

当前测试覆盖：
- 环境变量读取
- GitHub URL 和本地路径识别
- 文件扫描忽略规则
- 技术栈识别
- 运行方式推断
- 核心文件排序
- Markdown 校验器
- Mock AI client 集成测试

<a id="roadmap"></a>

## 🗺️ 路线图

SourceGuide 会先把 CLI 和 Markdown 生成做扎实，再逐步扩展到自动化、协作和文档站。

```mermaid
timeline
    title SourceGuide Roadmap
    v0.1 MVP : CLI
             : 公开 GitHub 仓库
             : 本地目录
             : 中文 Markdown 输出
    v0.2 可配置 : sourceguide.toml
               : 自定义扫描规则
               : 自定义模板
    v0.3 增量更新 : 只重写变化文档
                 : 保留用户手写补充
                 : 扫描结果缓存
    v0.4 自动化 : GitHub Action
               : 仓库更新后自动生成
               : CI 产物检查
    v0.5 多场景 : 多语言输出
               : 私有仓库授权
               : HTML 文档站
    v1.0 稳定版 : 稳定 CLI / API
                : 插件化分析器
                : 完善示例和发布文档
```

| 阶段 | 状态 | 重点 | 说明 |
| :--- | :---: | :--- | :--- |
| **v0.1 MVP** | ✅ 已实现 | CLI + 公开仓库 + 本地目录 + 中文 Markdown 输出 | 先让核心生成链路跑通，并保证输出文件可信 |
| **v0.2 可配置** | 🔜 下一步 | `sourceguide.toml` + 自定义扫描规则 + 自定义模板 | 让不同项目能按自己的目录结构和写作风格生成 |
| **v0.3 增量更新** | 🔜 规划中 | 只重写变化部分，保留用户手写补充 | 让 SourceGuide 可以长期维护文档，而不是每次全量覆盖 |
| **v0.4 自动化** | 🔜 规划中 | GitHub Action + CI 文档检查 | 仓库更新后自动刷新学习路线，适合开源项目长期使用 |
| **v0.5 多场景** | 🔜 规划中 | 多语言输出 + 私有仓库授权 + HTML 文档站 | 从个人 CLI 扩展到团队、课程和文档站场景 |
| **v1.0 稳定版** | 🔮 目标 | 稳定 CLI/API + 插件化分析器 + 完整示例 | 固化公共接口，支持社区贡献更多语言和框架分析器 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！建议优先贡献：

- 🧩 新技术栈识别规则
- 🎯 更准确的运行方式推断
- 📝 更自然的中文文档模板
- 📸 真实仓库生成示例
- 🧪 测试用 fixture 项目

提交 PR 前请运行：
```bash
pytest
```

完整说明见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 📄 许可证

[MIT](LICENSE) © duanmuzichen

---

<div align="center">

**如果这个项目对你有帮助，欢迎 ⭐ Star 支持！**

</div>
