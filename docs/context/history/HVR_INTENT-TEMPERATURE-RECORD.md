# Temperature Record Human Verification Record（HVR）

> 文档状态：In Progress
> Intent ID：`INTENT-TEMPERATURE-RECORD`
> CC：[Coding_Contract_Temperature_Record.md](../intent/Coding_Contract_Temperature_Record.md) `v1.0.0 Frozen`
> IHR：[IHR_INTENT-TEMPERATURE-RECORD.md](./IHR_INTENT-TEMPERATURE-RECORD.md)
> ATR：[ATR_INTENT-TEMPERATURE-RECORD.md](./ATR_INTENT-TEMPERATURE-RECORD.md)

## 1. Verification Metadata

| 字段 | 值 |
|---|---|
| Environment | Odoo 18 Web, `http://127.0.0.1:18087` |
| Browser / Device / PDA | Shared browser page, desktop viewport |
| Human Verifier | Not recorded; browser interaction executed in shared session |
| Verification Start | 2026-09-23 14:05 +08:00 |
| Verification End | 2026-09-23 14:10 +08:00 |

## 2. Required Scenarios

| 场景 | 验证内容 | 当前结果 |
|---|---|---|
| `HVR-TEMP-001` | Web 创建、保存、查询和提交 | PASS |
| `HVR-TEMP-002` | Enter 输入温度后新增明细、清空并回焦 | PASS |
| `HVR-TEMP-003` | 连续生成 `pallet1`、`pallet2`、`pallet3` | PASS |
| `HVR-TEMP-004` | 草稿修改温度，单行删除被拒绝 | PASS |
| `HVR-TEMP-005` | 清空全部确认、取消和重新从 `pallet1` 采集 | PASS |
| `HVR-TEMP-006` | PDA 触控录入和数字键盘 | DEFERRED (`TD-TEMP-001`) |
| `HVR-TEMP-007` | 多语言字段和选择值 | DEFERRED (`TD-TEMP-002`) |
| `HVR-TEMP-008` | 异常结果只记录，不自动触发业务流程 | PASS |

## 3. Current Status

| 指标 | 值 |
|---|---|
| Required Scenarios | 8 |
| PASS | 6 |
| FAIL | 0 |
| BLOCKED | 0 |
| DEFERRED | 2 |
| NOT RUN | 0 |
| Current Evidence Set | Browser verification of `TMP/00016`, including signature and submit |

## 4. Verification Discipline

- 自动化测试 PASS 不得转换为 HVR PASS；
- Agent 不得冒充人类验证者；
- PDA 必须在真实 PDA 或等效触控设备上验证；
- 清空全部动作必须验证二次确认和取消后的数据不变；
- 不得将温度或检查结果解释为自动隔离、复测、放行或库存结论。

本次浏览器验证还发现并修复了快速录入组件的 `this.el` 引用错误，以及 Enter
事件重复触发问题。修复后使用 `TMP/00016` 完成了连续录入、修改、清空取消、
清空确认、重新从 `pallet1` 开始采集、签名和提交。提交后记录显示
`Submitted` 状态，并记录签名人为 `Mitchell Admin` 和签名时间。
随后执行 `Mark Exception`，记录进入异常待处理状态并仅显示 `Close` /
`Reset to Draft` 操作；未观察到库存、隔离、通知或放行等外部业务动作。

真实 PDA 触控设备验证和多语言验证不在本次 Web 浏览器验证范围内，分别由
`TD-TEMP-001` 和 `TD-TEMP-002` 跟踪，不将其误记为 PASS。

## 5. Handoff

Temperature Record UI 实现并完成 ATR 后，才能启动本 HVR。所有场景必须基于
真实 UI、真实记录和真实用户验证追加 Run 记录。
