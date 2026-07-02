# 04 校验与自动修订 Prompt

## 目标

对生成结果进行质量校验，输出问题清单，并自动修订一版。

## 必读文件

- `rules/validation_and_revision_rules.md`
- `rules/mece_rules.md`
- `rules/behavior_standard_writing_rules.md`
- `rules/level_difference_rules.md`

## 校验步骤

1. 检查结构完整性。
2. 检查内容规范性。
3. 检查职级区分度。
4. 检查 MECE 质量。
5. 检查输出格式合规性。
6. 基于问题自动修订。

## 输出要求

- 不输出完整修订前版本。
- 输出自动修订后的最终版。
- 输出校验报告。
- 输出关键修订说明。
- 输出人工复核重点。

## 校验报告格式

```text
【校验结论】
通过 / 需修订 / 严重不通过

【主要问题】
1.
2.
3.

【自动修订动作】
1.
2.
3.

【人工复核重点】
1.
2.
3.
```
