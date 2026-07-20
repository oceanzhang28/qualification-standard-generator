from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def require(relative_path: str, *phrases: str) -> None:
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [phrase for phrase in phrases if phrase not in text]
    assert not missing, f"{relative_path} missing: {missing}"


require(
    "position-interview-extractor/templates/fact_review_template.md",
    "允许生成 Skill 使用内置通用职级规则补充：待确认 / 是 / 否 / 不需要",
    "待映射的内部职级",
    "内部职级映射确认状态：不需要 / 待确认 / 已确认",
    "审核人直接确认适用职级范围",
)
require(
    "position-interview-extractor/prompts/03_review_confirmation_prompt.md",
    "通用确认不等于补充授权",
    "选择“否”",
    "保持“待人工审核”",
    "不得根据受访专家主要熟悉职级",
    "明确确认映射关系",
    "审核人直接确认适用职级范围",
)
require(
    "position-interview-extractor/prompts/04_handoff_formatting_prompt.md",
    "适用职级范围只能包含“专员、主管、经理、总监”",
    "只能复制审核稿中已确认的选择",
    "不需要",
)
require(
    "position-interview-extractor/templates/hr_basic_info_template.md",
    "仅可多选：专员、主管、经理、总监",
    "待映射的内部职级",
)
require(
    "position-interview-extractor/rules/validation_rules.md",
    "适用职级枚举与映射",
    "补充授权",
)
require(
    "position-interview-extractor/SKILL.md",
    "preparing or conducting",
    "references/interview_guide.md",
)
require(
    "tests/position-interview-extractor/expected/review-gate-regressions-checklist.md",
    "含糊的通用确认",
    "明确拒绝补充",
    "非标准内部职级",
)

print("Runtime contract PASS: consent, refusal, level mapping, and interview-guide routing are covered.")
