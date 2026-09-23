# Temperature Record Automated Test Record（ATR）

> 文档状态：In Progress
> Intent ID：`INTENT-TEMPERATURE-RECORD`
> IHR：[IHR_INTENT-TEMPERATURE-RECORD.md](./IHR_INTENT-TEMPERATURE-RECORD.md)
> CC：`v1.0.0 Frozen`，Approved for Implementation
> 模块：`wd_qooling_app`

## 1. Execution Metadata

| 字段 | 值 |
|---|---|
| Environment | Odoo 18 / database `odoo18ce` |
| Test Framework | Odoo TransactionCase / View/HTTP / Playwright，按 TDD/CC |
| Code Baseline | Working tree, implementation pending commit |
| Executed By | Copilot |
| Latest Valid Run | 2026-09-23, module upgrade with `--test-enable --stop-after-init` |

## 2. Test Contract Baseline

| 测试 ID | 覆盖 |
|---|---|
| `CC-TEMP-TEST-001` | 创建、保存、重读草稿 |
| `CC-TEMP-TEST-002` | 必填字段和签名 |
| `CC-TEMP-TEST-003` | 动态 1、2 和多个托盘 |
| `CC-TEMP-TEST-004` | 超过 65 个托盘不截断 |
| `CC-TEMP-TEST-005` | Enter 快速录入 |
| `CC-TEMP-TEST-006` | 连续托盘编号 |
| `CC-TEMP-TEST-007` | 编辑和单行删除边界 |
| `CC-TEMP-TEST-008` | 清空全部托盘明细 |
| `CC-TEMP-TEST-009` | 人工异常状态 |
| `CC-TEMP-TEST-010` | 结果只保存 |
| `CC-TEMP-TEST-011` | 未授权访问 |
| `CC-TEMP-TEST-012` | 温度类型错误 |
| `CC-TEMP-TEST-013` | 上传失败 |

## 3. Current Automated Test Status

| 指标 | 值 |
|---|---|
| Required Tests | 13 |
| PASS | 3 |
| FAIL | 0 |
| BLOCKED | 0 |
| NOT RUN | 10 |
| Latest Valid Run | 16 tests loaded, 0 failed, 0 errors |

The three implemented TransactionCase tests cover dynamic pallet creation and
numbering, single-line deletion protection with clear-all restart, and signature
and supervisor state actions. The remaining contract tests require additional
UI/negative-path coverage and are not marked PASS.

## 4. Handoff

实现代码创建后，必须先执行 ORM/权限/视图针对性测试，再追加真实测试 Run。
没有执行的测试不得记录为 PASS；自动化测试 PASS 不能替代 PDA、签名或人工
复核 HVR。
