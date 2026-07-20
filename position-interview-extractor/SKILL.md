---
name: position-interview-extractor
description: Use when HR needs help preparing or conducting a professional-position expert interview, or needs to turn a basic-information form and transcript into an auditable岗位事实稿 or confirmed input package for qualification-standard-generator.
---

# Position Interview Extractor

## Purpose

从岗位基本信息表和完整访谈转写稿中提炼岗位事实。先输出人工审核稿；仅在用户明确确认后输出清洁岗位信息包。

## Hard Boundaries

- 只处理单个专业类岗位。
- 不生成行为模块、行为要项或四职级行为标准。
- 不将学历、年限、性格、通用素质、领导力或价值观写入岗位关键任务。
- 不将 AI 推测写成专家事实。
- 职级差异完全选填，可仅覆盖岗位整体、任务组、单项任务或部分职级；未获得职级差异时必须标记为缺失，不得解释为不适用。
- 适用职级只能从专员、主管、经理、总监中选择；其他内部职级必须保留原值、明确映射并经审核人确认。
- 存在未覆盖职级或作用范围时，必须取得用户对内置规则补充的明确授权；拒绝授权时在补齐缺失事实前不得交接。
- 未经人工确认，不输出审核状态为“已确认”的清洁岗位信息包。

## Workflow

**用户要准备或开展岗位专家访谈时**，读取 `references/interview_guide.md` 协助设计提纲、追问或转写标记；该路径不得在没有完整转写稿时提前进入事实提炼。

1. 读取 `config/input_requirements.md` 和 `prompts/01_material_intake_prompt.md`，检查 HR 基本信息表与完整转写稿。
2. 材料满足条件后，读取 `rules/key_task_extraction_rules.md`、`rules/level_difference_extraction_rules.md`、`rules/validation_rules.md`、`templates/fact_review_template.md` 和 `prompts/02_fact_extraction_prompt.md`，输出岗位事实审核稿。
3. 等待人工修改或确认。读取 `config/workflow.md` 和 `prompts/03_review_confirmation_prompt.md` 处理反馈。未确认前不得进入下一步。
4. 用户明确确认后，读取 `templates/clean_handoff_template.md` 和 `prompts/04_handoff_formatting_prompt.md`，输出清洁岗位信息包。

## Output Contract

- 第一阶段输出：岗位事实审核稿，保留来源、证据摘要、缺失与冲突。
- 第二阶段输出：审核后的清洁岗位信息包，可提交 `qualification-standard-generator`。
- 职级差异按岗位整体、工作领域或任务组、单项任务三个层级稀疏表达。
