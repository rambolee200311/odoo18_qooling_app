# Temperature Record Human Verification Record（HVR）

> 文档状态：In Progress
> Intent ID：`INTENT-TEMPERATURE-RECORD`
> CC：[Coding_Contract_Temperature_Record.md](../intent/Coding_Contract_Temperature_Record.md) `v1.0.0 Frozen`
> IHR：[IHR_INTENT-TEMPERATURE-RECORD.md](./IHR_INTENT-TEMPERATURE-RECORD.md)
> ATR：[ATR_INTENT-TEMPERATURE-RECORD.md](./ATR_INTENT-TEMPERATURE-RECORD.md)

## 1. Verification Metadata

| 字段 | 值 |
|---|---|
| Environment | 尚未执行 |
| Browser / Device / PDA | 尚未指定 |
| Human Verifier | 尚未指定 |
| Verification Start | 尚未执行 |
| Verification End | 尚未执行 |

## 2. Required Scenarios

| 场景 | 验证内容 | 当前结果 |
|---|---|---|
| `HVR-TEMP-001` | Web 创建、保存、查询和提交 | NOT RUN |
| `HVR-TEMP-002` | Enter 输入温度后新增明细、清空并回焦 | NOT RUN |
| `HVR-TEMP-003` | 连续生成 `pallet1`、`pallet2`、`pallet3` | NOT RUN |
| `HVR-TEMP-004` | 草稿修改温度，单行删除被拒绝 | NOT RUN |
| `HVR-TEMP-005` | 清空全部确认、取消和重新从 `pallet1` 采集 | NOT RUN |
| `HVR-TEMP-006` | PDA 触控录入和数字键盘 | NOT RUN |
| `HVR-TEMP-007` | 多语言字段和选择值 | NOT RUN |
| `HVR-TEMP-008` | 异常结果只记录，不自动触发业务流程 | NOT RUN |

## 3. Current Status

| 指标 | 值 |
|---|---|
| Required Scenarios | 8 |
| PASS | 0 |
| FAIL | 0 |
| BLOCKED | 0 |
| NOT RUN | 8 |
| Current Evidence Set | None |

## 4. Verification Discipline

- 自动化测试 PASS 不得转换为 HVR PASS；
- Agent 不得冒充人类验证者；
- PDA 必须在真实 PDA 或等效触控设备上验证；
- 清空全部动作必须验证二次确认和取消后的数据不变；
- 不得将温度或检查结果解释为自动隔离、复测、放行或库存结论。

## 5. Handoff

Temperature Record UI 实现并完成 ATR 后，才能启动本 HVR。所有场景必须基于
真实 UI、真实记录和真实用户验证追加 Run 记录。
