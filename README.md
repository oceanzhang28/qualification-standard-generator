# 任职资格 AI 生成工具

这个项目包含两个协作的 Skill：`position-interview-extractor` 先从岗位访谈中提炼经人工确认的岗位事实，`qualification-standard-generator` 再基于该确认信息生成公司专业类岗位的任职资格标准。

当前版本聚焦“任职资格标准”本身，不生成传统任职条件，也不覆盖管理岗位任职资格体系。

## 当前状态

- Skill 文件包已放在 `qualification-standard-generator/`。
- 岗位访谈提炼 Skill 文件包已放在 `position-interview-extractor/`。
- 使用流程分两步：先提炼岗位访谈事实并由人工明确确认，再将清洁岗位信息包交给任职资格生成 Skill。
- 输入表单、分阶段生成流程、行为模块拆解规则、行为标准写法规则、职级差异规则和校验规则已形成初版。
- 案例库已从 Excel 转为 Markdown，包含 5 个成熟或可参考案例，以及 1 个产品设计岗对照案例。
- 产品设计岗已完成一次阶段二测试输出，位置为 `outputs/product-design-stage2-v3.md`。
- 项目沟通和规则沉淀笔记保留在本地 Obsidian，不随安装仓库发布。

## 核心约束

- 适用对象：已了解公司任职资格模式的 HR 或业务人员。
- 适用岗位：专业类岗位。
- 固定职级：专员、主管、经理、总监。
- 固定模块：所有岗位必须包含“组织贡献”，并固定拆分为“平台/流程建设”和“人员培养”。
- 输出方式：先生成阶段一框架，经用户确认后，再生成阶段二四级行为标准。
- Skill 间交接：`position-interview-extractor` 的岗位事实审核稿必须经人工明确确认后，才能输出清洁岗位信息包并提交 `qualification-standard-generator`。
- 调整轮次：阶段一最多支持 2 轮调整，需要提示用户第一轮尽量一次性说全意见。
- 行为标准句式：优先按“基于/根据/通过/结合【输入/依据/场景】，完成【行为动作】，形成【产出/结果】，确保【衡量标准】”组织，但不强制每条都有前置情景。
- 行为标准颗粒度：一个行为要项下可以在单元格内用编号拆出多个工作细项，不能因为模块精简而压缩工作内容。
- 指标要求：可以使用定性评价，不强制量化。

## 目录说明

| 路径 | 用途 |
|---|---|
| `position-interview-extractor/` | 岗位访谈事实提炼、人工审核和清洁信息包交接 Skill |
| `qualification-standard-generator/SKILL.md` | Skill 入口说明 |
| `qualification-standard-generator/config/` | 用户输入表单、输出格式、流程配置 |
| `qualification-standard-generator/rules/` | 任职资格定义、拆解、写法、职级差异和校验规则 |
| `qualification-standard-generator/prompts/` | 分阶段生成和校验提示词 |
| `qualification-standard-generator/templates/` | 阶段一、阶段二、TSV 和校验报告模板 |
| `qualification-standard-generator/references/` | 职位图谱、案例库、写法示例和待补充清单 |
| `qualification-standard-generator/scripts/` | Excel 到 Markdown 案例库转换脚本 |
| `docs/` | 开发计划、材料清单和规则细化文档 |
| `outputs/` | 本地测试输出，不随安装仓库发布 |
| `任职资格参考标准/` | 本地源 Excel 案例和职位图谱，不随安装仓库发布 |

## 案例库

首批成熟或可参考案例：

- HRBP
- 有纺产品企划
- 产品研发
- 产品内容策划
- 电商运营

补充对照案例：

- 产品设计岗：版本不完全成熟，可用于学习精简模块结构、产品设计类工作细项拆分和测试迭代，不应把其中低颗粒度行为标准直接当作优质写法样例。

## 常用维护命令

转换案例库：

```bash
python3 qualification-standard-generator/scripts/excel_to_markdown_converter.py
```

核对 Skill 引用文件是否存在：

```bash
python3 - <<'PY'
from pathlib import Path
root = Path("qualification-standard-generator")
skill = (root / "SKILL.md").read_text(encoding="utf-8")
for path in [
    "config/user_input_form.md",
    "config/output_format.md",
    "config/skill_workflow.md",
    "rules/qualification_definition.md",
    "rules/module_item_decomposition_rules.md",
    "rules/behavior_standard_writing_rules.md",
    "rules/level_difference_rules.md",
    "rules/mece_rules.md",
    "rules/validation_and_revision_rules.md",
    "prompts/01_intake_prompt.md",
    "prompts/02_framework_generation_prompt.md",
    "prompts/03_behavior_standard_generation_prompt.md",
    "prompts/04_validation_revision_prompt.md",
    "prompts/05_output_formatting_prompt.md",
]:
    assert (root / path).exists(), path
print("OK")
PY
```

## 下一步

- 用更多岗位测试阶段一框架和阶段二行为标准输出。
- 补充高质量行为标准正反例，尤其是行为情景、职级动作词和多细项编号写法。
- 对产品设计岗测试结果继续回写规则，而不是直接人工修单次输出。
- 稳定后考虑生成 `.xlsx` 文件和迁移到 OpenClaw。
