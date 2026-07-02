# 文档索引

本目录用于沉淀 `qualification-standard-generator` 的开发计划、材料准备要求和规则细化过程。

## 文件说明

| 文件 | 用途 |
|---|---|
| `implementation-plan.md` | Skill 开发实现流程规划，包含分阶段建设步骤和验收标准 |
| `materials-checklist.md` | 用户需要提供的材料清单、案例信息模板和 Excel 模板要求 |
| `rule-refinement-checklist.md` | 行为标准写法、职级差异、动作词和颗粒度问题的规则细化记录 |
| `action-type-level-difference-template.md` | 通用工作类型与职级差异模式模板 |

## 使用方式

- 新增规则时，先更新对应规则文档，再同步到 `qualification-standard-generator/rules/` 或 `qualification-standard-generator/references/`。
- 新增案例时，先补充 `materials-checklist.md` 中的案例质量判断，再运行转换脚本生成案例库。
- 测试输出暴露的问题，应回写到规则或提示词，避免只修单次生成结果。
