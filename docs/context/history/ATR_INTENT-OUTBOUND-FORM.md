# Outbound Form Automated Test Record（ATR）

> 文档状态：In Progress
> Intent ID：`INTENT-OUTBOUND-FORM`
> IHR：[IHR_INTENT-OUTBOUND-FORM.md](./IHR_INTENT-OUTBOUND-FORM.md)
> CC：`v1.0.0 Frozen`，Approved for Implementation
> 模块：待实施确认

## 1. Execution Metadata

| 字段 | 值 |
|---|---|
| Environment | Odoo 18 runtime with PostgreSQL database `odoo18ce` |
| Test Framework | Odoo TransactionCase / View/HTTP / Playwright，按 TDD |
| Code Baseline | Working tree (pre-commit) |
| Executed By | Copilot, 2026-09-23 |
| Latest Valid Run | 2026-09-23, Odoo module upgrade/test run |

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
| PASS | 6 |
| FAIL | 0 |
| BLOCKED | 0 |
| NOT RUN | 4 |
| Latest Valid Run | 2026-09-23, 0 failed / 0 errors |

## 4. Test Run History（Append-only）

### 2026-09-23 — Odoo runtime test run

- `python3 -m py_compile` passed for the Outbound model and tests.
- Python XML parsing passed for Outbound views, security, and sequence data.
- Command:
  `venv/bin/python odoo-bin -c odoo.conf -d odoo18ce -u wd_qooling_app
  --test-enable --stop-after-init --workers=0`
- Odoo module run: **PASS**, 13 tests loaded, 0 failures, 0 errors.
- Covered TransactionCase tests: draft persistence, loading-time order,
  dual-signature submission, UN Number/evidence persistence, manual reviewer
  state changes, and ACL denial.
- Playwright/PDA and HVR: **NOT RUN**; no browser or human-device evidence is
  claimed.

## 5. Handoff

Odoo ORM/权限/视图 tests and human PDA/signature HVR remain required before
release. HVR status is explicitly **NOT RUN**.
