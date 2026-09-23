# Outbound Form Automated Test Record（ATR）

> 文档状态：In Progress
> Intent ID：`INTENT-OUTBOUND-FORM`
> IHR：[IHR_INTENT-OUTBOUND-FORM.md](./IHR_INTENT-OUTBOUND-FORM.md)
> CC：`v1.0.0 Frozen`，Approved for Implementation
> 模块：待实施确认

## 1. Execution Metadata

| 字段 | 值 |
|---|---|
| Environment | Workspace static validation only; Odoo runtime unavailable |
| Test Framework | Odoo TransactionCase / View/HTTP / Playwright，按 TDD |
| Code Baseline | Working tree (uncommitted) |
| Executed By | Copilot, 2026-09-23 |
| Latest Valid Run | N/A |

## 2. Test Contract Baseline

| 测试 ID | 覆盖 |
|---|---|
| `CC-OUTBOUND-TEST-001` | 创建、保存和重读草稿 |
| `CC-OUTBOUND-TEST-002` | 时间顺序校验 |
| `CC-OUTBOUND-TEST-003` | 两方签名提交 |
| `CC-OUTBOUND-TEST-004` | UN Number 限制 |
| `CC-OUTBOUND-TEST-005` | 检查和温度结果只保存 |
| `CC-OUTBOUND-TEST-006` | 照片和备注非必填 |
| `CC-OUTBOUND-TEST-007` | ACL/Record Rule |
| `CC-OUTBOUND-TEST-008` | Web/PDA 双签名交互 |
| `CC-OUTBOUND-TEST-009` | PDA 触控布局 |
| `CC-OUTBOUND-TEST-010` | 多语言显示 |

## 3. Current Automated Test Status

| 指标 | 值 |
|---|---|
| Required Tests | 10 |
| PASS | 0 |
| FAIL | 0 |
| BLOCKED | 10 |
| NOT RUN | 10 |
| Latest Valid Run | N/A |

## 4. Test Run History（Append-only）

### 2026-09-23 — Static preflight (not an Odoo ATR run)

- `python3 -m py_compile` passed for the Outbound model and tests.
- Python XML parsing passed for Outbound views, security, and sequence data.
- Odoo TransactionCase/View/HTTP tests: **BLOCKED / NOT RUN** (no Odoo
  executable or installed runtime was available in the workspace).
- Playwright/PDA and HVR: **NOT RUN**; no human-device evidence is claimed.

## 5. Handoff

Odoo ORM/权限/视图 tests and human PDA/signature HVR remain required before
release. HVR status is explicitly **NOT RUN**.
