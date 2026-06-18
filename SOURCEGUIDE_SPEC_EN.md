[🇨🇳 中文](SOURCEGUIDE_SPEC.md) | [🇬🇧 English](SOURCEGUIDE_SPEC_EN.md)

---

# SourceGuide Product & Architecture Specification

## 1. Project Positioning

SourceGuide is an open-source tool for Chinese-speaking developers that converts any GitHub repository or local project into guided source-code learning paths.

It is not a README summarizer, nor just a documentation generator. Its core value:

**The same repository should be read differently by people with different goals.**

SourceGuide generates 4 learning paths based on user intent:

- Beginner path
- Quick overview path
- Contributor path
- Interview path

Every path must include "how to run this project" — the depth of explanation varies.

## 2. Core Goals

Given a GitHub repository URL or local project directory, SourceGuide automatically:

- Fetches the project source code
- Scans the project structure
- Identifies the tech stack
- Finds entry points, config files, core modules, and test directories
- Determines how to run the project
- Generates 4 Chinese source-code learning paths
- Generates architecture docs, glossaries, recommended reading order, and exercises

The final output is a set of Markdown documents suitable for reading, bookmarking, and publishing on GitHub, 掘金, 知乎, or project doc sites.

## 3. Target Users

### Beginner Developers

Want to understand an open-source project but don't know where to start.

### Quick Evaluators

Want to decide within 10 minutes whether a project is worth deeper exploration.

### Potential Contributors

Want to file issues, fix bugs, or submit their first PR.

### Job Seekers & Interviewees

Want to turn an open-source project into a portfolio piece, interview material, or learning case study.

## 4. User Interface

SourceGuide v1 is CLI-only.

Two input types are supported:

- GitHub repository URL
- Local project directory

Users can generate all paths or a single path.

Supported parameters:

- Output language (default: Chinese)
- Route: all, beginner, quick, contributor, interview
- Output directory
- Model configuration
- API base URL
- Tutorial depth
- Whether to overwrite existing docs
- Whether to generate architecture docs
- Whether to generate glossary

## 5. Output Directory Structure

Default output is written to `docs/sourceguide/` inside the target project.

Output files include:

- `README.md`: Entry point explaining how to learn this project
- `01-路径-名称.md`: Learning paths (4 files)
- `architecture.md`: Architecture diagram and module relationships
- `glossary.md`: Terminology explanations
- `exercises.md`: Practice tasks
- `run-guide.md`: Unified run instructions (referenced by all paths)
- `source-map.md`: Core file map

## 6. The Four Learning Paths

### Beginner Path

Goal: Let developers with basic skills run the project and understand the main flow.

Must include:

- What this project does
- Prerequisite knowledge
- How to run the project (extremely detailed)
- What each command means
- What each dependency does
- Windows, macOS, Linux considerations
- Which file to start reading from
- Which files to skip for now
- Common terminology
- Common error troubleshooting
- 3 practice tasks suitable for beginners

The beginner path must not assume users already understand frameworks, build tools, package managers, environment variables, or test commands.

### Quick Overview Path

Goal: Let users evaluate the project's value in 10 minutes.

Must include:

- One-sentence project description
- What problem it solves
- Core feature list
- Tech stack overview
- Shortest way to run it
- Project highlights
- Potential risks or shortcomings
- Whether it's worth deeper exploration
- Top 5 core files to read next

The quick overview path must be short, direct, and conclusive.

### Contributor Path

Goal: Help users make their first contribution.

Must include:

- How to run the project
- How to enter development mode
- How to run tests
- How to check code style
- Main module boundaries
- Which directories are good for newcomers
- Potential first PR tasks
- Pre-submission checklist
- How to locate bugs
- How to add a small feature
- Contribution risk points

The contributor path focuses on enabling users to modify code, not on teaching concepts.

### Interview Path

Goal: Help users explain the project clearly for resumes, interviews, or tech talks.

Must include:

- One-sentence project description
- Project background and business value
- How to run the project
- Where is the entry point
- What happens at startup
- How to explain the architecture
- How to explain core modules
- How to explain technical challenges
- Resume-ready phrasing
- Questions interviewers might ask
- Answer strategies for each question
- Possible optimization directions

The interview path must help users go from "I've read it" to "I can explain it clearly."

## 7. Global Generation Rules

All paths must include "how to run this project."

If SourceGuide cannot determine the run method, it must not omit this section. Instead, it must output:

- Clues found about how to run it
- Possible start methods
- Configuration the user needs to confirm
- Potentially missing dependencies
- Troubleshooting suggestions

All paths must answer:

- What is this project
- How to run it
- Where is the entry point
- Which files should I read first
- How to troubleshoot issues

Empty generalities are forbidden, such as:

- "The project has a clear structure"
- "High code quality"
- "Feature-rich"
- "Great for learning"

Unless supported by specific files, modules, or evidence.

## 8. System Architecture

SourceGuide consists of 8 core modules.

### CLI Entry Layer

Parses user input, arguments, output directory, and route selection.

Responsibilities:

- Accept GitHub URL or local path
- Validate input
- Create task context
- Call the main pipeline
- Show progress and results

### Repository Layer

Prepares the source code.

Responsibilities:

- Clone GitHub repositories
- Read local projects
- Manage temporary directories
- Identify repo name, default branch, project size
- Avoid redundant downloads

### Scanner Layer

Understands the project structure.

Responsibilities:

- Walk the file tree
- Filter irrelevant directories and files
- Identify README, dependency files, entry points, config files, test dirs, example dirs
- Generate a project file map
- Count languages and file types

Default ignore list:

- `.git`
- `node_modules`
- `.venv`
- `dist`
- `build`
- `coverage`
- `__pycache__`
- Images, videos, archives, large binaries
- Minified files
- Lock files (readable but not primary analysis targets)

### Tech Stack Layer

Determines the project type.

Detection signals:

- Python: `pyproject.toml`, `requirements.txt`, `setup.py`
- Node.js: `package.json`
- Go: `go.mod`
- Rust: `Cargo.toml`
- Java: `pom.xml`, `build.gradle`
- Docker: `Dockerfile`, `docker-compose`
- Frontend frameworks: Next.js, Vite, React, Vue, Svelte
- Backend frameworks: FastAPI, Flask, Django, Express, NestJS

### Runtime Inference Layer

This is SourceGuide's key module.

Responsibilities:

- Extract run steps from README
- Infer install method from dependency files
- Find start commands from script configs
- Infer container run method from Docker files
- Infer test commands from test configs
- Assign confidence levels to each run method

Outputs:

- Recommended run method
- Alternative run method
- Environment requirements
- Dependency installation method
- Test method
- Common issues

### Core File Identification Layer

Finds the most worthwhile files to read.

Judgment criteria:

- Entry points
- Heavily referenced files
- Routes, services, core classes, core functions
- Configuration hub
- Data models
- Modules with test coverage
- Modules used in examples
- Files mentioned in README

Outputs:

- Top 10 core files
- Role of each file
- Recommended reading order
- Relationships between files

### AI Analysis Layer

Converts scan results into structured understanding.

Analysis tasks include:

- Project goal summary
- Tech stack summary
- Module responsibility summary
- Run method explanation
- Architecture relationship inference
- Path content generation
- Glossary generation
- Interview Q&A generation
- Exercise generation

The AI layer must generate in stages, avoiding feeding the entire repository to the model at once.

### Document Generation Layer

Renders structured content into Markdown.

Responsibilities:

- Apply fixed templates
- Generate 4 learning paths
- Generate architecture docs
- Generate glossary
- Generate exercises
- Maintain consistent headings, ordering, and style
- Verify each path includes run instructions

## 9. Main Pipeline

The complete flow:

1. Accept input
2. Prepare repository
3. Scan file tree
4. Filter irrelevant files
5. Identify tech stack
6. Infer run method
7. Identify core files
8. Analyze README and config
9. Analyze core modules
10. Generate project knowledge summary
11. Generate 4 learning paths
12. Generate architecture diagram and glossary
13. Validate document completeness
14. Write output directory
15. Print completion result

## 10. MVP Scope

v1 must include:

- GitHub URL support
- Local directory support
- Chinese output
- Full 4-path generation
- Single-path generation
- Auto-detect major tech stacks
- Auto-infer run method
- Auto-generate core file map
- Auto-generate Markdown docs
- OpenAI-compatible API support
- Custom model support
- Clear README
- At least 2 real-world repo examples

v1 explicitly excludes:

- Web UI
- VS Code extension
- Browser extension
- GitHub Action
- Multi-user collaboration
- Private repo authorization
- PDF export
- Documentation site deployment

## 11. Phase 2 Features

Possible additions for phase 2:

- HTML doc site
- GitHub Action
- VS Code extension
- Multi-language output
- Incremental updates
- Private repo support
- Interactive architecture diagrams
- Call chain analysis
- Course-style chapter splitting
- Project scoring
- Learning progress checklist

## 12. Quality Standards

Generated output must satisfy:

- Every path has a clear goal
- Every path includes run instructions
- Beginner path is sufficiently detailed
- Quick overview path is sufficiently brief
- Contributor path can guide a first PR
- Interview path is usable for project experience presentation
- No obvious hallucinated files
- All referenced files come from real scan results
- Uncertain content must be labeled "uncertain"
- Natural language, not machine-template style
- Output ready to be committed to a GitHub repo

## 13. Project Tagline

SourceGuide's core message:

**Turn any GitHub repository into guided source-code learning paths.**

Full English description:

SourceGuide doesn't just summarize a repository. It generates 4 guided source-code learning paths based on your purpose: Beginner Path, Quick Overview Path, Contributor Path, and Interview Path. Each path shows you how to run the project, where to start reading, and how to understand the core code.
