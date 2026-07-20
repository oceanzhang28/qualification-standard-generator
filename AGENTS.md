# AGENTS.md

本文件给后续在本项目中工作的 Codex/agent 使用。请先阅读 `README.md`，再按本文件约束执行。

## 项目范围

- 本项目建设两个协作的 Skill：`position-interview-extractor` 和 `qualification-standard-generator`。
- `position-interview-extractor` 从岗位基本信息表和完整访谈转写稿中提炼可审核的岗位事实；只有经人工明确确认后，才可将清洁岗位信息包交给 `qualification-standard-generator`。
- 目标是生成公司专业类岗位任职资格标准。
- 不生成传统任职条件。
- 不处理管理岗位任职资格体系。
- 固定职级为：专员、主管、经理、总监。

## 工作边界

- 保持改动小而明确，避免顺手重构。
- 不改动源 Excel，除非用户明确要求。
- 案例库内容来自 Excel 时，优先修改转换脚本并重新生成，不手工改写大量生成文件。
- 成熟案例原文必须保留，不擅自润色。
- 对标记为“不成熟”或“行为标准不成熟”的案例，只学习结构和差异，不把低颗粒度文字当作优质样例。
- Skill 包内不放独立 README，项目说明放在根目录和 `docs/`。

## 关键规则

- 所有岗位必须包含“组织贡献”模块。
- “组织贡献”固定包含“平台/流程建设”和“人员培养”2 个行为要项。
- 除“组织贡献”外，专业模块默认 4-6 个。
- 除“组织贡献”外，每个模块默认 3-5 个行为要项。
- 用户确认阶段一后才能进入阶段二。
- 阶段一最多支持 2 轮调整，输出时要提醒用户第一轮尽量说全意见。
- 行为标准不能全部机械地以动词开头；有输入、依据或场景时，应使用“基于/根据/通过/结合/围绕/针对/承接”等情景开头。
- 行为标准可以定性评价，不强制量化指标。
- 一个行为要项下可以用编号拆出多个行为标准细项。

## 重要文件

- 岗位访谈提炼 Skill 入口：`position-interview-extractor/SKILL.md`
- 岗位访谈输入要求：`position-interview-extractor/config/input_requirements.md`
- 岗位访谈审核工作流：`position-interview-extractor/config/workflow.md`
- 岗位关键任务提炼规则：`position-interview-extractor/rules/key_task_extraction_rules.md`
- 岗位职级差异提炼规则：`position-interview-extractor/rules/level_difference_extraction_rules.md`
- 岗位访谈输出模板：`position-interview-extractor/templates/fact_review_template.md`、`position-interview-extractor/templates/clean_handoff_template.md`
- 岗位访谈 Skill 项目级测试：`tests/position-interview-extractor/README.md`
- Skill 入口：`qualification-standard-generator/SKILL.md`
- 用户输入表单：`qualification-standard-generator/config/user_input_form.md`
- 工作流程：`qualification-standard-generator/config/skill_workflow.md`
- 行为标准写法：`qualification-standard-generator/rules/behavior_standard_writing_rules.md`
- 职级差异规则：`qualification-standard-generator/rules/level_difference_rules.md`
- 通用工作类型差异：`qualification-standard-generator/references/writing_examples/work_type_level_patterns.md`
- 案例库报告：`qualification-standard-generator/references/case_library/conversion_report.md`
- 开发计划：`docs/implementation-plan.md`
- 材料清单：`docs/materials-checklist.md`
- 规则细化记录：`docs/rule-refinement-checklist.md`
- 阶段笔记：本地 Obsidian 文件，不随安装仓库发布

## 验证建议

修改任一 Skill 的规则或提示词后，至少检查两个 Skill 的运行文件；修改访谈提炼 Skill 时同时运行其项目级契约测试：

```bash
find position-interview-extractor qualification-standard-generator -maxdepth 3 -type f | sort
python3 tests/position-interview-extractor/check_runtime_contract.py
```

转换案例库后，检查：

```bash
python3 qualification-standard-generator/scripts/excel_to_markdown_converter.py
```

生成或修改 Markdown 文档后，检查相对时间、旧数量和过时描述：

```bash
rg -n "5 个成熟|五个成熟|相对时间|旧数量" README.md AGENTS.md docs position-interview-extractor qualification-standard-generator tests/position-interview-extractor
```

## 输出偏好

- 给用户的阶段性文档尽量用 Markdown，便于存入 Obsidian。
- 面向 Excel 的最终结果需要同时提供 Markdown 预览和 TSV。
- TSV 内容要便于直接复制到 Excel。
