---
name: qualification-standard-generator
description: Use when generating, reviewing, or refining company岗位任职资格标准初稿 for a single professional岗位. This skill collects standardized岗位信息, creates行为模块/行为要项, generates专员/主管/经理/总监行为标准, validates quality, and outputs Markdown plus TSV for Excel. Use for HR/OTD任职资格标准 work, not for学历、年限、通用素质、领导力或价值观模型.
---

# Qualification Standard Generator

## Purpose

生成公司岗位任职资格标准初稿。本 Skill 只处理专业类岗位的专业工作项标准，不生成传统任职条件、学历年限、通用素质、领导力或价值观要求。

目标输出固定为：

```text
序号	行为模块	行为要项	专员行为标准	主管行为标准	经理行为标准	总监行为标准
```

## Use This Skill When

- 用户要为单个岗位生成任职资格标准初稿。
- 用户要基于岗位关键任务拆解行为模块、行为要项和分职级行为标准。
- 用户要把成熟岗位案例作为结构、写法或职级递进参考。
- 用户要校验任职资格标准是否符合公司规则。

不要用于：

- 管理岗位任职资格。
- 学历、年限、经验、专业背景、素质能力、领导力、价值观要求。
- 批量生成全部岗位。
- 直接生成 `.xlsx` 文件。

## Core Workflow

1. 读取 `config/user_input_form.md`，要求用户按标准表单提供岗位信息。
2. 按 `rules/qualification_definition.md` 判断任务是否属于本 Skill 范围。
3. 按 `references/position_map.md` 校验职类、职务子类和标准岗位口径。
4. 若必填信息不足，使用 `prompts/01_intake_prompt.md` 追问补齐。
5. 信息完整后，默认推荐分阶段生成。
6. 阶段一：读取 `rules/module_item_decomposition_rules.md` 和 `prompts/02_framework_generation_prompt.md`，生成行为模块和行为要项。
7. 阶段一必须等待用户确认；用户未确认前不得生成行为标准。
8. 阶段二：读取 `rules/behavior_standard_writing_rules.md`、`rules/level_difference_rules.md` 和 `prompts/03_behavior_standard_generation_prompt.md`，生成四级行为标准。
9. 读取 `rules/validation_and_revision_rules.md` 和 `prompts/04_validation_revision_prompt.md`，输出问题清单并自动修订一版。
10. 读取 `config/output_format.md`、`templates/markdown_preview_template.md`、`templates/tsv_output_template.md` 和 `prompts/05_output_formatting_prompt.md`，输出最终内容。

## Reference Selection

需要参考案例时，按以下顺序读取：

1. `references/position_map.md`：校验职类、职务子类、标准岗位。
2. `references/case_library/conversion_report.md`：查看案例成熟度、可学习点和禁用点。
3. `references/case_library/full_positions/`：优先读取同职类或相近职务子类的完整岗位案例。
4. `references/case_library/snippets/by_module/`：需要模块拆解参考时读取。
5. `references/case_library/snippets/by_behavior_item/`：需要行为要项颗粒度参考时读取。
6. `references/case_library/snippets/by_level_progression/`：需要职级递进参考时读取。
7. `references/writing_examples/action_type_examples.md`：需要行为标准句式和动作类型参考时读取。
8. `references/writing_examples/work_type_level_patterns.md`：需要通用工作类型的职级差异模式时读取。

案例使用限制：

- 不得直接复制成熟岗位案例内容到目标岗位。
- 标记为“行为模块与要项成熟，行为标准不成熟”的案例，只学习模块、要项和职级差异，不把其行为标准作为优质写法样例。
- 若案例与目标岗位业务背景不同，必须说明参考边界。

## Hard Rules

- 固定四级列：专员、主管、经理、总监。
- 即使岗位只适用部分职级，也必须保留四级列；不适用职级留空。
- 所有岗位必须包含固定行为模块“组织贡献”。
- “组织贡献”固定包含 2 个行为要项：平台/流程建设、人员培养。
- 组织贡献以外的岗位专业模块默认 4-6 个。
- 除组织贡献外，每个行为模块默认 3-5 个行为要项。
- 行为标准必须是工作项标准，必须体现行为动作、工作产出和可评价要求。
- 不强制量化，但必须可评价。
- TSV 必须放在最后，独立代码块，便于复制到 Excel。

## If More Business Rules Are Needed

如果生成或校验时缺少公司内部规则，不要臆造。请向用户索取，并建议用户补充到 `references/to_be_completed.md` 中对应章节。
