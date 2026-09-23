# Outbound Form Human Verification Record（HVR）

> 文档状态：Completed
> Intent ID：`INTENT-OUTBOUND-FORM`
> CC：[Coding_Contract_Outbound_Form.md](../intent/Coding_Contract_Outbound_Form.md) `v1.0.0 Frozen`
> IHR：[IHR_INTENT-OUTBOUND-FORM.md](./IHR_INTENT-OUTBOUND-FORM.md)
> ATR：[ATR_INTENT-OUTBOUND-FORM.md](./ATR_INTENT-OUTBOUND-FORM.md)

## 1. Verification Metadata

| 字段 | 值 |
|---|---|
| Environment | Odoo 18 本地实例 `http://127.0.0.1:18087`；Playwright 已启动 |
| Browser / Device / PDA | Chrome/Web；PDA 触控等效视口 |
| Human Verifier | 用户确认 |
| Verification Start | 2026-09-23 10:05 (UTC+8) |
| Verification End | 2026-09-23 10:14 (UTC+8) |

## 2. Required Scenarios

| 场景 | 验证内容 | 当前结果 |
|---|---|---|
| `HVR-OUTBOUND-001` | Web 创建、保存、查询和提交 | PASS |
| `HVR-OUTBOUND-002` | Web 司机和仓库操作员双签名 | PASS |
| `HVR-OUTBOUND-003` | PDA 触控布局、填写和双签名 | PASS |
| `HVR-OUTBOUND-004` | 时间顺序和提交错误提示 | PASS |
| `HVR-OUTBOUND-005` | 多语言字段和选择值 | PASS |
| `HVR-OUTBOUND-006` | 异常结果只记录，不自动阻止放行或创建流程 | PASS |

## 3. Current Status

| 指标 | 值 |
|---|---|
| Required Scenarios | 6 |
| PASS | 6 |
| FAIL | 0 |
| BLOCKED | 0 |
| NOT RUN | 0 |
| Current Evidence Set | User-confirmed Web/PDA HVR run on Outbound form `OUT/00016` |

## 4. Verification Discipline

- 自动化测试 PASS 不得转换为 HVR PASS；
- Agent 不得冒充人类验证者；
- PDA 必须在真实 PDA 或等效触控设备上验证；
- 双签名必须验证图像、签名人和签名时间均可重新查看；
- 异常结果只记录事实，不得把人工复核边界验证成自动业务结论。

## 5. Run History（Append-only）

### 2026-09-23 — User-confirmed HVR run

用户确认 `HVR-OUTBOUND-001` 至 `HVR-OUTBOUND-006` 全部通过，验证对象为
Outbound Form `OUT/00016`。本次记录只反映用户实际确认的结果；不将自动化
测试结果替代人工验证，也不将异常结果解释为自动放行或自动阻止。
