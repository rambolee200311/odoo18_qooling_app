# Outbound Form Automated Test Record（ATR）

> 文档状态：In Progress
> Intent ID：`INTENT-OUTBOUND-FORM`
> IHR：[IHR_INTENT-OUTBOUND-FORM.md](./IHR_INTENT-OUTBOUND-FORM.md)
> CC：`v1.0.0 Frozen`，Approved for Implementation
> 模块：待实施确认

## 1. Execution Metadata

| 字段 | 值 |
|---|---|
| Environment | 尚未执行 |
| Test Framework | Odoo TransactionCase / View/HTTP / Playwright，按 TDD |
| Code Baseline | 尚未创建 |
| Executed By | 尚未执行 |
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
| BLOCKED | 0 |
| NOT RUN | 10 |
| Latest Valid Run | N/A |

## 4. Test Run History（Append-only）

当前没有 ATR Run。没有真实执行的测试不得记录为 PASS。

## 5. Handoff

实现代码创建后，先执行 ORM/权限/视图针对性测试，再追加测试 Run，
并将结果绑定到实际 Commit。
