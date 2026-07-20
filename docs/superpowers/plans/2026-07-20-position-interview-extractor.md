# Position Interview Extractor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在当前项目中新增独立的 `position-interview-extractor` Skill，将 HR 岗位基本信息表和访谈转写稿提炼为可人工审核的岗位事实稿，并在确认后输出兼容现有任职资格生成 Skill 的清洁岗位信息包。

**Architecture:** 新 Skill 与 `qualification-standard-generator` 平级，不读取或调用原 Skill 的内部提示词。新 Skill 采用“材料检查 → 岗位事实提炼 → 人工确认 → 清洁信息包”四步流程，职级差异按岗位整体、任务组和单项任务分层稀疏表达。第一版通过固定 Markdown 模板交接，不处理音视频转写、批量岗位、Excel 或自动调用原 Skill。

**Tech Stack:** Markdown Skill instructions, YAML agent metadata, Python-based Skill validation scripts, Git.

## Global Constraints

- 只处理公司专业类岗位，不处理管理岗位任职资格体系。
- 新 Skill 只提炼岗位事实，不生成行为模块、行为要项或四职级行为标准。
- 必须设置人工审核关口；审核状态不是“已确认”时，不输出可直接提交生成 Skill 的最终清洁信息包。
- 关键任务必须为 5–10 条，并尽量包含输入或场景、动作、对象、产出或目的。
- 职级差异完全选填，允许只覆盖岗位整体、任务组、单项任务或部分职级。
- 未获得职级差异时必须明确标记缺失，不得将缺失解释为不适用。
- 事实审核阶段只允许“专家明确、AI 归纳、缺失、存在冲突”，不得混入系统规则预测。
- 使用“专业工作职责与要求差异”，不使用泛化的“能力差异”作为正式字段名。
- 新 Skill 包内不创建独立 README；项目级说明放在根目录和 `docs/`。
- 不修改源 Excel，不改写现有案例库，不顺手重构原 Skill。

---

## Planned File Structure

```text
position-interview-extractor/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── config/
│   ├── input_requirements.md
│   └── workflow.md
├── prompts/
│   ├── 01_material_intake_prompt.md
│   ├── 02_fact_extraction_prompt.md
│   ├── 03_review_confirmation_prompt.md
│   └── 04_handoff_formatting_prompt.md
├── rules/
│   ├── key_task_extraction_rules.md
│   ├── level_difference_extraction_rules.md
│   └── validation_rules.md
├── references/
│   └── interview_guide.md
└── templates/
    ├── hr_basic_info_template.md
    ├── fact_review_template.md
    └── clean_handoff_template.md

tests/position-interview-extractor/
├── README.md
├── fixtures/
│   ├── complete_mixed-level-transcript.md
│   ├── sparse-level-transcript.md
│   └── conflicting-boundary-transcript.md
└── expected/
    ├── complete-mixed-level-checklist.md
    ├── sparse-level-checklist.md
    └── conflicting-boundary-checklist.md
```

`position-interview-extractor/` 只包含 Skill 运行所需文件。测试说明和测试材料放在项目级 `tests/`，避免把开发材料发布进 Skill 包。

### File responsibilities

- `SKILL.md`: 触发条件、能力边界、四步主流程和按需读取文件的路由。
- `agents/openai.yaml`: Skill 在 Codex UI 中的名称、描述和默认调用示例。
- `config/input_requirements.md`: 两类输入材料、必填字段、允许缺失项和材料完整性判断。
- `config/workflow.md`: 四阶段状态转换、人工确认口令和禁止越过审核关口的规则。
- `prompts/01_material_intake_prompt.md`: 首次调用、缺失材料和输入冲突的响应格式。
- `prompts/02_fact_extraction_prompt.md`: 从转写稿抽取岗位事实和候选关键任务的执行步骤。
- `prompts/03_review_confirmation_prompt.md`: 输出审核稿、接收修改、确认审核状态。
- `prompts/04_handoff_formatting_prompt.md`: 将已确认事实映射成清洁岗位信息包。
- `rules/key_task_extraction_rules.md`: 任务识别、合并、拆分、排除和颗粒度规则。
- `rules/level_difference_extraction_rules.md`: 三层稀疏职级差异、来源标记和作用范围规则。
- `rules/validation_rules.md`: 输出前完整性、事实忠实度、边界和交接兼容性检查。
- `references/interview_guide.md`: 已确认的 90 分钟访谈提纲，供用户需要访谈设计或解释转写标记时读取。
- `templates/hr_basic_info_template.md`: HR 访谈前填写的岗位基本信息表。
- `templates/fact_review_template.md`: 保留来源、证据、缺失和冲突的人工审核稿。
- `templates/clean_handoff_template.md`: 审核后提交原 Skill 的固定格式。

---

### Task 1: Scaffold the New Skill and Lock Its Trigger Boundary

**Files:**
- Create: `position-interview-extractor/SKILL.md`
- Create: `position-interview-extractor/agents/openai.yaml`
- Create directories: `position-interview-extractor/config/`, `position-interview-extractor/prompts/`, `position-interview-extractor/rules/`, `position-interview-extractor/templates/`

**Interfaces:**
- Consumes: confirmed architecture in `docs/superpowers/specs/2026-07-20-interview-skill-handoff-design.md`
- Produces: Skill name `position-interview-extractor` and the canonical four-stage workflow used by all later tasks

- [ ] **Step 1: Run the required Skill initializer**

Run:

```bash
python3 /Users/oceanzhang/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  position-interview-extractor \
  --path . \
  --resources references \
  --interface 'display_name=岗位访谈提炼' \
  --interface 'short_description=从岗位访谈转写中提炼可审核的岗位关键任务与职级差异' \
  --interface 'default_prompt=使用 $position-interview-extractor 整理这份岗位基本信息和访谈转写稿，先输出岗位事实审核稿。'
```

Expected: creates `position-interview-extractor/SKILL.md`, `position-interview-extractor/agents/openai.yaml`, and `position-interview-extractor/references/`.

- [ ] **Step 2: Create the focused resource directories**

Run:

```bash
mkdir -p position-interview-extractor/config \
  position-interview-extractor/prompts \
  position-interview-extractor/rules \
  position-interview-extractor/templates
```

Expected: all four directories exist and are empty.

- [ ] **Step 3: Replace the generated SKILL.md with the minimal workflow entry point**

Use `apply_patch` to make `position-interview-extractor/SKILL.md` contain these exact sections and rules:

```markdown
---
name: position-interview-extractor
description: Extract and refine company岗位事实、5-10条关键任务、工作对象、流程、产出、协同边界及稀疏职级职责差异 from an HR岗位基本信息表 and a岗位专家访谈转写稿. Use when HR needs to turn a professional-position interview transcript into an人工可审核岗位事实稿 and, only after confirmation, a clean input package for qualification-standard-generator. Do not use to generate任职资格行为模块、行为要项或行为标准.
---

# Position Interview Extractor

## Purpose

从岗位基本信息表和完整访谈转写稿中提炼岗位事实。先输出人工审核稿；仅在用户明确确认后输出清洁岗位信息包。

## Hard Boundaries

- 只处理单个专业类岗位。
- 不生成行为模块、行为要项或四职级行为标准。
- 不将学历、年限、性格、通用素质、领导力或价值观写入岗位关键任务。
- 不将 AI 推测写成专家事实。
- 不要求每项任务或每个职级都有差异信息。
- 未经人工确认，不输出审核状态为“已确认”的清洁岗位信息包。

## Workflow

1. 读取 `config/input_requirements.md` 和 `prompts/01_material_intake_prompt.md`，检查 HR 基本信息表与完整转写稿。
2. 材料满足条件后，读取 `rules/key_task_extraction_rules.md`、`rules/level_difference_extraction_rules.md`、`rules/validation_rules.md`、`templates/fact_review_template.md` 和 `prompts/02_fact_extraction_prompt.md`，输出岗位事实审核稿。
3. 等待人工修改或确认。读取 `config/workflow.md` 和 `prompts/03_review_confirmation_prompt.md` 处理反馈。未确认前不得进入下一步。
4. 用户明确确认后，读取 `templates/clean_handoff_template.md` 和 `prompts/04_handoff_formatting_prompt.md`，输出清洁岗位信息包。

## Output Contract

- 第一阶段输出：岗位事实审核稿，保留来源、证据摘要、缺失与冲突。
- 第二阶段输出：审核后的清洁岗位信息包，可提交 `qualification-standard-generator`。
- 职级差异按岗位整体、工作领域或任务组、单项任务三个层级稀疏表达。
```

- [ ] **Step 4: Validate metadata and structure**

Run:

```bash
python3 /Users/oceanzhang/.codex/skills/.system/skill-creator/scripts/quick_validate.py position-interview-extractor
```

Expected: validation succeeds with no frontmatter or naming errors.

- [ ] **Step 5: Commit the scaffold**

```bash
git add position-interview-extractor/SKILL.md position-interview-extractor/agents/openai.yaml
git commit -m "Add interview extractor skill scaffold"
```

---

### Task 2: Define Inputs, Workflow States, and the Interview Reference

**Files:**
- Create: `position-interview-extractor/config/input_requirements.md`
- Create: `position-interview-extractor/config/workflow.md`
- Create: `position-interview-extractor/templates/hr_basic_info_template.md`
- Create: `position-interview-extractor/references/interview_guide.md`

**Interfaces:**
- Consumes: canonical four-stage workflow from Task 1
- Produces: input field names `职类`, `职务子类`, `所在部门`, `岗位名称`, `当前实际覆盖职级`, `受访专家主要熟悉职级`, `访谈日期`; workflow states `材料待补充`, `待人工审核`, `已确认`

- [ ] **Step 1: Add the HR basic information template**

Create `templates/hr_basic_info_template.md` with the fixed fields:

```text
【岗位基本信息】
职类：
职务子类：
所在部门：
岗位名称：
当前实际覆盖职级：
受访专家姓名/角色：
受访专家主要熟悉职级：
访谈日期：
```

Document that “当前实际覆盖职级” describes organization setup, while “专家主要熟悉职级” describes evidence coverage; neither substitutes for the other.

- [ ] **Step 2: Define input acceptance and missing-data rules**

Create `config/input_requirements.md` with these decisions:

- Both the HR basic information form and full transcript are required to start extraction.
- Missing `职类`, `职务子类`, `所在部门`, `岗位名称`, or transcript blocks extraction.
- Missing or partial level-difference information does not block extraction.
- A transcript may be pasted text or a readable text/Markdown file; v1 does not transcribe audio or video.
- Conflicts between the form and transcript must be preserved as confirmation items.
- The Skill must not infer that an uncovered level is inapplicable.

- [ ] **Step 3: Define the review state machine**

Create `config/workflow.md` with this exact transition model:

```text
材料待补充
  → 材料完整
  → 待人工审核
  → 用户提出修改：继续停留在待人工审核
  → 用户明确确认：已确认
  → 输出清洁岗位信息包
```

Specify accepted confirmation language such as “确认岗位信息”“审核通过”“按此版本提交”，and state that ambiguous replies such as “可以看看下一步” do not count as confirmation.

- [ ] **Step 4: Convert the approved interview design into a runtime reference**

Create `references/interview_guide.md` by condensing `docs/superpowers/specs/2026-07-17-position-key-task-interview-design.md` to:

- 90-minute allocation;
- opening script;
- job-positioning questions;
- work panorama questions;
- per-task probes for scene/input/action/output/evaluation/boundary/complexity;
- sparse level-difference probes;
- organization-contribution questions;
- transcript topic markers.

Do not copy project history, architecture discussion, acceptance criteria, or implementation notes into the runtime reference.

- [ ] **Step 5: Validate no unsupported scope was introduced**

Run:

```bash
rg -n "音频转写|视频转写|批量生成|自动调用|行为模块|行为标准" position-interview-extractor
```

Expected: any matches appear only in explicit prohibitions or scope boundaries; no workflow promises those capabilities.

- [ ] **Step 6: Commit input and workflow definitions**

```bash
git add position-interview-extractor/config position-interview-extractor/templates/hr_basic_info_template.md position-interview-extractor/references/interview_guide.md
git commit -m "Define interview extraction inputs and review flow"
```

---

### Task 3: Implement Key-Task and Sparse Level-Difference Rules

**Files:**
- Create: `position-interview-extractor/rules/key_task_extraction_rules.md`
- Create: `position-interview-extractor/rules/level_difference_extraction_rules.md`
- Create: `position-interview-extractor/rules/validation_rules.md`

**Interfaces:**
- Consumes: accepted input fields and review states from Task 2
- Produces: 5–10 `关键任务`; source labels `[专家明确]`, `[AI归纳]`, `[缺失]`, `[存在冲突]`; scope values `岗位整体`, `工作领域或任务组`, `单项任务`

- [ ] **Step 1: Write key-task extraction rules**

Create `rules/key_task_extraction_rules.md` covering:

- candidate extraction from repeated mentions and concrete examples;
- merge when purpose, object, output, and responsibility boundary are substantially the same;
- keep one complete task rather than splitting every sequential step;
- split when purpose, output, or responsibility boundary differs;
- retain low-frequency but high-impact professional work;
- exclude temporary errands, generic capabilities, people-management requirements, and collaborators' primary duties;
- produce 5–10 tasks, each with `任务名称 + 标准化描述`;
- standard description form: `基于【输入/依据/场景】，完成【关键动作】，形成【产出/结果】，确保或支撑【评价要求/业务目的】`;
- when evidence is insufficient, leave the subfield missing and flag it instead of inventing facts.

- [ ] **Step 2: Write the sparse level-difference rules**

Create `rules/level_difference_extraction_rules.md` with:

```text
层级一：岗位整体
层级二：工作领域或任务组
层级三：单项任务
```

For every difference record require:

```text
差异主题：
适用层级：
适用关键任务：
明确不适用的任务：
各职级职责与要求差异：
信息来源：
人工确认状态：
```

State that blank levels remain `[缺失]`; `[不适用]` is allowed only when explicitly supported by actual level scope or confirmed expert evidence. Do not create `[规则预测]` during fact extraction.

- [ ] **Step 3: Write validation rules**

Create `rules/validation_rules.md` with checks for:

- 5–10 tasks;
- action, object, and output/purpose coverage;
- duplicates and boundary overlap;
- main workflow and output coverage;
- collaborator-duty leakage;
- prohibited generic capability content;
- unsupported facts;
- level-difference scope binding;
- missing level information incorrectly marked inapplicable;
- unresolved form/transcript conflicts;
- handoff compatibility with the existing required fields.

The validation result must be one of `可以进入人工审核`, `需要补充材料`, or `存在重大冲突`.

- [ ] **Step 4: Cross-check terminology consistency**

Run:

```bash
rg -n "能力差异|规则预测|不适用|专家明确|AI归纳|存在冲突|工作领域或任务组" position-interview-extractor/rules
```

Expected:

- “能力差异” appears only in an explicit terminology prohibition, if present;
- “规则预测” appears only in a prohibition;
- every use of “不适用” states its evidence requirement;
- the four fact-stage source labels are defined consistently.

- [ ] **Step 5: Commit extraction and validation rules**

```bash
git add position-interview-extractor/rules
git commit -m "Add interview fact extraction rules"
```

---

### Task 4: Build the Two Output Templates and Four Prompts

**Files:**
- Create: `position-interview-extractor/templates/fact_review_template.md`
- Create: `position-interview-extractor/templates/clean_handoff_template.md`
- Create: `position-interview-extractor/prompts/01_material_intake_prompt.md`
- Create: `position-interview-extractor/prompts/02_fact_extraction_prompt.md`
- Create: `position-interview-extractor/prompts/03_review_confirmation_prompt.md`
- Create: `position-interview-extractor/prompts/04_handoff_formatting_prompt.md`

**Interfaces:**
- Consumes: task schema, source labels, scope values, and workflow states from Tasks 2–3
- Produces: `岗位访谈提炼审核稿` and `审核状态：已确认` clean handoff matching Section 6 of the design spec

- [ ] **Step 1: Create the fact review template**

Create `templates/fact_review_template.md` with these fixed sections:

1. 岗位基本信息；
2. 岗位定位；
3. 5–10 项候选关键任务, each containing scene/input/action/output/evaluation/boundary/complexity/source/evidence/completeness;
4. 岗位整体差异；
5. 工作领域或任务组差异；
6. 单项关键任务差异；
7. 信息缺口与冲突；
8. 建议人工确认事项。

The template must not contain system-predicted level differences.

- [ ] **Step 2: Create the clean handoff template**

Create `templates/clean_handoff_template.md` with the exact top-level blocks:

```text
【审核信息】
【岗位基本信息】
【岗位定位】
【岗位关键任务】
【典型复杂场景】
【已确认的专业工作职责与要求差异】
【职级差异信息说明】
【其他可选信息】
```

Include `审核状态：已确认`, reviewer, review date, 5–10 task slots, all three optional level-difference scopes, uncovered scope, and `允许生成 Skill 使用内置通用职级规则补充：是 / 否`.

- [ ] **Step 3: Create the material-intake prompt**

`prompts/01_material_intake_prompt.md` must:

- display the HR form when missing;
- request the full text transcript;
- ask only for missing blocking information;
- explicitly state that level differences may be partial or absent;
- refuse to start extraction without the form and transcript.

- [ ] **Step 4: Create the fact-extraction prompt**

`prompts/02_fact_extraction_prompt.md` must execute this order:

```text
识别基本信息
→ 分段标记转写主题
→ 提取候选任务及证据
→ 合并或拆分任务
→ 排除非核心或越界事项
→ 形成 5–10 条任务
→ 提炼三层稀疏职级差异
→ 校验
→ 输出岗位事实审核稿
```

Require concise evidence summaries, not long transcript quotations.

- [ ] **Step 5: Create the review-confirmation prompt**

`prompts/03_review_confirmation_prompt.md` must:

- keep the state at `待人工审核` when the user requests changes;
- revise only the fields implicated by feedback;
- display remaining gaps and conflicts after revision;
- move to `已确认` only on explicit confirmation;
- never treat missing level differences as a blocking defect.

- [ ] **Step 6: Create the handoff-formatting prompt**

`prompts/04_handoff_formatting_prompt.md` must:

- check `审核状态：已确认` before formatting;
- omit transcript evidence and AI reasoning;
- preserve explicitly unresolved non-blocking review notes separately;
- map 5–10 tasks and special notes to the existing generator input vocabulary;
- keep sparse level differences scoped;
- write an explicit no-reliable-level-information statement instead of empty output when all differences are missing.

- [ ] **Step 7: Verify the human gate appears in every relevant layer**

Run:

```bash
rg -n "已确认|待人工审核|未经.*确认|明确确认" \
  position-interview-extractor/SKILL.md \
  position-interview-extractor/config/workflow.md \
  position-interview-extractor/prompts \
  position-interview-extractor/templates
```

Expected: the entry point, workflow, review prompt, handoff prompt, and clean template all enforce or reflect the confirmation gate.

- [ ] **Step 8: Commit prompts and templates**

```bash
git add position-interview-extractor/prompts position-interview-extractor/templates
git commit -m "Add interview review and handoff workflow"
```

---

### Task 5: Add Representative Forward-Test Fixtures

**Files:**
- Create: `tests/position-interview-extractor/README.md`
- Create: `tests/position-interview-extractor/fixtures/complete_mixed-level-transcript.md`
- Create: `tests/position-interview-extractor/fixtures/sparse-level-transcript.md`
- Create: `tests/position-interview-extractor/fixtures/conflicting-boundary-transcript.md`
- Create: `tests/position-interview-extractor/expected/complete-mixed-level-checklist.md`
- Create: `tests/position-interview-extractor/expected/sparse-level-checklist.md`
- Create: `tests/position-interview-extractor/expected/conflicting-boundary-checklist.md`

**Interfaces:**
- Consumes: complete Skill from Tasks 1–4
- Produces: repeatable test inputs and observable pass/fail criteria without embedding a single exact generated answer

- [ ] **Step 1: Write the complete mixed-level fixture**

Create a synthetic professional-position transcript that contains:

- valid HR basic information;
- 7 distinct key tasks;
- repeated descriptions requiring merging;
- overall level differences for all four levels;
- task-group differences for planning tasks;
- a single-task difference for complex exception handling;
- one collaborator duty that must not become a key task;
- one generic capability statement that must be excluded.

Do not copy mature case-library wording.

- [ ] **Step 2: Write its acceptance checklist**

The expected checklist must require:

- 5–10 final tasks and no duplicate planning task;
- collaborator duty excluded or correctly placed in boundary information;
- generic capability excluded;
- all three level-difference scopes preserved;
- source labels included;
- output stops at the review draft before confirmation.

- [ ] **Step 3: Write the sparse-level fixture and checklist**

Create a transcript in which the expert mainly knows the主管 level, provides one overall专员/主管 comparison, and cannot describe经理/总监 or per-task differences.

The checklist must require:

- task extraction still completes;
- missing levels are `[缺失]`, not `[不适用]`;
- no `[规则预测]` appears in the fact review;
- the final clean handoff, after simulated confirmation, states that the generator may use built-in rules for uncovered scopes.

- [ ] **Step 4: Write the conflicting-boundary fixture and checklist**

Create a transcript where the form says the target position owns a process, while the expert later says another department owns approval and the target position only prepares inputs.

The checklist must require:

- conflict is preserved and highlighted;
- disputed ownership is not silently assigned to the target position;
- validation result is `存在重大冲突` or `需要补充材料`;
- no clean handoff is produced before explicit resolution and confirmation.

- [ ] **Step 5: Document the manual forward-test procedure**

In `tests/position-interview-extractor/README.md`, specify:

1. invoke the Skill with one fixture;
2. save the review-draft output under a temporary local test output path;
3. score every checklist item pass/fail;
4. simulate user corrections and explicit confirmation where applicable;
5. verify clean handoff separately;
6. do not commit generated test outputs unless they expose a stable regression worth preserving.

- [ ] **Step 6: Commit fixtures and checklists**

```bash
git add tests/position-interview-extractor
git commit -m "Add interview extractor test fixtures"
```

---

### Task 6: Validate the Skill and Its Handoff Compatibility

**Files:**
- Modify if validation reveals issues: `position-interview-extractor/SKILL.md`
- Modify if validation reveals issues: files under `position-interview-extractor/config/`, `prompts/`, `rules/`, `templates/`
- Test: `tests/position-interview-extractor/`

**Interfaces:**
- Consumes: complete Skill and fixtures
- Produces: validated standalone Skill and evidence that its clean handoff fits the current generator input contract

- [ ] **Step 1: Run structural validation**

Run:

```bash
python3 /Users/oceanzhang/.codex/skills/.system/skill-creator/scripts/quick_validate.py position-interview-extractor
find position-interview-extractor -maxdepth 3 -type f | sort
```

Expected: quick validation succeeds; file list contains only the planned runtime files and no Skill-level README.

- [ ] **Step 2: Check references from SKILL.md**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

root = Path("position-interview-extractor")
required = [
    "config/input_requirements.md",
    "config/workflow.md",
    "prompts/01_material_intake_prompt.md",
    "prompts/02_fact_extraction_prompt.md",
    "prompts/03_review_confirmation_prompt.md",
    "prompts/04_handoff_formatting_prompt.md",
    "rules/key_task_extraction_rules.md",
    "rules/level_difference_extraction_rules.md",
    "rules/validation_rules.md",
    "references/interview_guide.md",
    "templates/hr_basic_info_template.md",
    "templates/fact_review_template.md",
    "templates/clean_handoff_template.md",
]
missing = [path for path in required if not (root / path).is_file()]
assert not missing, missing
print("OK")
PY
```

Expected: `OK`.

- [ ] **Step 3: Check forbidden and required terminology**

Run:

```bash
rg -n "学历|年限|通用素质|领导力|价值观|规则预测|能力差异" position-interview-extractor
rg -n "专业工作职责与要求差异|岗位整体|工作领域或任务组|单项任务|审核状态" position-interview-extractor
```

Expected: forbidden terms appear only in exclusions; required handoff terms appear in rules, prompts, and templates.

- [ ] **Step 4: Verify compatibility with the current generator form**

Compare `position-interview-extractor/templates/clean_handoff_template.md` with `qualification-standard-generator/config/user_input_form.md` and verify the clean handoff always provides:

```text
职类
职务子类
所在部门
岗位名称
适用职级范围
至少 5 条岗位关键任务
主要工作对象
主要工作流程
主要产出物
```

Expected: all current required generator fields have a direct source field; sparse level differences map into the existing optional `特殊职级差异` field without requiring one difference per task.

- [ ] **Step 5: Execute the three forward tests**

Run each fixture through the Skill and score its checklist. Expected:

- complete mixed-level fixture: every checklist item passes;
- sparse-level fixture: every checklist item passes without invented level facts;
- conflicting-boundary fixture: clean handoff is blocked until conflict resolution.

If a test fails, make the smallest rule or prompt correction that addresses the observed failure, rerun that fixture, then rerun the other two for regression.

- [ ] **Step 6: Run final diff checks**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only planned files are modified or untracked. Existing unrelated `docs/test-records/` content remains untouched.

- [ ] **Step 7: Commit validation fixes, if any**

```bash
git add position-interview-extractor tests/position-interview-extractor
git commit -m "Validate interview extractor workflow"
```

Skip this commit if validation required no changes.

---

### Task 7: Update Project-Level Documentation After the Skill Passes

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/README.md`

**Interfaces:**
- Consumes: validated Skill and final file structure
- Produces: accurate project scope and maintenance guidance for both Skills

- [ ] **Step 1: Update the root README**

Make only these project-level additions:

- state that the repository contains two cooperating Skills;
- describe step one as interview fact extraction and step two as qualification generation;
- add `position-interview-extractor/` to the directory table;
- document the mandatory human confirmation between Skills;
- keep the original generator constraints unchanged.

- [ ] **Step 2: Update AGENTS.md scope and important files**

Add the new Skill to project scope, list its `SKILL.md`, input requirements, workflow, extraction rules, templates, and project-level tests. Preserve all existing generator rules and source-Excel restrictions.

- [ ] **Step 3: Update docs/README.md index**

Add links to:

- `docs/superpowers/specs/2026-07-17-position-key-task-interview-design.md`;
- `docs/superpowers/specs/2026-07-20-interview-skill-handoff-design.md`;
- `docs/superpowers/plans/2026-07-20-position-interview-extractor.md`;
- `tests/position-interview-extractor/README.md`.

- [ ] **Step 4: Check for stale single-Skill language**

Run:

```bash
rg -n "本项目建设 `qualification-standard-generator` Skill|只包含一个 Skill|单一 Skill" README.md AGENTS.md docs
```

Expected: no stale statement incorrectly claims the project contains only the generator Skill. Historical design notes may remain unchanged when clearly historical.

- [ ] **Step 5: Commit project documentation**

```bash
git add README.md AGENTS.md docs/README.md
git commit -m "Document two-skill qualification workflow"
```

---

### Task 8: Final End-to-End Verification

**Files:**
- Verify only; modify the smallest directly responsible file if a failure is found

**Interfaces:**
- Consumes: all prior tasks
- Produces: implementation ready for user review

- [ ] **Step 1: Re-run Skill validation and reference checks**

Run the validation commands from Task 6 Steps 1–3.

Expected: all commands pass with no missing files or unsupported promises.

- [ ] **Step 2: Re-run representative workflow checks**

Verify these three user journeys:

1. complete materials → fact review → explicit confirmation → clean handoff;
2. sparse level information → fact review with missing markers → confirmation → clean handoff allowing built-in rule supplementation;
3. conflicting responsibility boundary → fact review with conflict → handoff blocked.

Expected: each journey follows the designed state transition and output contract.

- [ ] **Step 3: Verify the original Skill was not unintentionally changed**

Run:

```bash
git diff 8e912d6 -- qualification-standard-generator
```

Expected: no changes under `qualification-standard-generator/` in the first implementation. Any later compatibility enhancement must be planned and reviewed separately.

- [ ] **Step 4: Run project-wide Markdown and stale-text checks**

Run:

```bash
git diff --check
rg -n "5 个成熟|五个成熟|相对时间|旧数量" README.md AGENTS.md docs position-interview-extractor qualification-standard-generator
```

Expected: no new stale quantities or placeholder wording introduced by this implementation.

- [ ] **Step 5: Review commit history and hand off**

Run:

```bash
git log --oneline --max-count=10
git status --short
```

Expected: task commits are focused; only the pre-existing unrelated `docs/test-records/` may remain untracked.

