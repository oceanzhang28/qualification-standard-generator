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
    "岗位性质（仅可选：专业类岗位 / 管理岗位）：",
    "仅可多选：专员、主管、经理、总监",
    "待映射的内部职级",
)
require(
    "position-interview-extractor/config/input_requirements.md",
    "只有明确填写“专业类岗位”才可进入事实提炼",
    "不得根据岗位名称",
)
require(
    "position-interview-extractor/prompts/01_material_intake_prompt.md",
    "确认值为“管理岗位”时",
    "确认值缺失、含糊或不在枚举内时",
    "不得根据岗位名称",
)
require(
    "position-interview-extractor/prompts/02_fact_extraction_prompt.md",
    "岗位性质已确认且为“专业类岗位”",
)
require(
    "position-interview-extractor/templates/fact_review_template.md",
    "岗位性质：专业类岗位",
)
require(
    "position-interview-extractor/prompts/03_review_confirmation_prompt.md",
    "岗位性质必须仍为“专业类岗位”",
)
require(
    "position-interview-extractor/prompts/04_handoff_formatting_prompt.md",
    "岗位性质必须已确认且为“专业类岗位”",
)
require(
    "position-interview-extractor/rules/validation_rules.md",
    "岗位性质与适用范围",
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
require(
    "tests/position-interview-extractor/fixtures/position-type-gate-regressions.md",
    "岗位性质：管理岗位",
    "岗位性质：待确认",
    "complete_mixed-level-transcript.md",
)
require(
    "tests/position-interview-extractor/expected/position-type-gate-regressions-checklist.md",
    "管理岗位",
    "含糊或非枚举值",
    "不得从岗位名称",
)
for fixture in (
    "complete_mixed-level-transcript.md",
    "sparse-level-transcript.md",
    "conflicting-boundary-transcript.md",
):
    require(
        f"tests/position-interview-extractor/fixtures/{fixture}",
        "岗位性质：专业类岗位",
    )

print("Runtime contract PASS: position type, consent, refusal, level mapping, and interview-guide routing are covered.")
