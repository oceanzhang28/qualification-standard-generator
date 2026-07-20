# 岗位访谈提炼器前测夹具

本目录保存 `position-interview-extractor` 的合成前测材料和人工验收清单。材料用于检验事实提炼、人工审核和清洁交接的边界；不包含任何真实岗位案例或期望生成答案。

## 手工前测步骤

1. 以一个 `fixtures/` 中的转写稿和其中的 HR 基本信息调用 Skill。
2. 将生成的岗位事实审核稿保存到临时本地测试输出路径，例如 `tmp/position-interview-extractor/<fixture-name>-review.md`。
3. 对相应 `expected/` 中的每一项逐条判定通过或失败，并记录观察结果。
4. 适用时模拟用户修正和明确确认；不得把修正意见或含糊回复当作确认。
5. 单独验证清洁岗位信息包：只有达到确认门槛的场景才能交接，且交接内容须符合对应清单。
6. 除非生成结果暴露可稳定复现的回归问题，否则不要提交临时生成的测试输出。

每次修改审核门禁或交接格式后，先运行：

```bash
python3 tests/position-interview-extractor/check_runtime_contract.py
```

## 夹具索引

| 夹具 | 关注点 | 对应清单 |
| --- | --- | --- |
| `complete_mixed-level-transcript.md` | 任务去重、范围边界、三层职级差异 | `complete-mixed-level-checklist.md` |
| `sparse-level-transcript.md` | 稀疏职级证据与确认后的规则补充 | `sparse-level-checklist.md` |
| `conflicting-boundary-transcript.md` | 表单与访谈的主责冲突 | `conflicting-boundary-checklist.md` |
| `review-gate-regressions.md` | 补充授权、拒绝补充与非标准职级映射门禁 | `review-gate-regressions-checklist.md` |
| `position-type-gate-regressions.md` | 管理岗位拒绝与岗位性质含糊时的前置阻断 | `position-type-gate-regressions-checklist.md` |
