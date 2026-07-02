# 05 输出格式化 Prompt

## 目标

将最终修订版任职资格标准整理为 Markdown 预览表和 TSV 可复制版。

## 必读文件

- `config/output_format.md`
- `templates/markdown_preview_template.md`
- `templates/tsv_output_template.md`
- `templates/validation_report_template.md`

## 固定输出顺序

1. 拆解逻辑说明
2. Markdown 预览表
3. 校验报告
4. 关键修订说明
5. 人工复核重点
6. TSV 可复制版

## TSV 注意事项

- TSV 必须放在最后。
- TSV 使用独立代码块。
- TSV 代码块前可以有标题，但代码块后不要再解释 TSV。
- TSV 行内使用 Tab 分隔。
- 单元格内不要换行。
- 多条行为标准用 `1、` `2、` `3、` 连接。
