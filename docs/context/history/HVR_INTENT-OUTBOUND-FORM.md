# Outbound Form Human Verification Record（HVR）

> 文档状态：In Progress
> Intent ID：`INTENT-OUTBOUND-FORM`
> CC：[Coding_Contract_Outbound_Form.md](../intent/Coding_Contract_Outbound_Form.md) `v1.0.0 Frozen`
> IHR：[IHR_INTENT-OUTBOUND-FORM.md](./IHR_INTENT-OUTBOUND-FORM.md)
> ATR：[ATR_INTENT-OUTBOUND-FORM.md](./ATR_INTENT-OUTBOUND-FORM.md)

## 1. Verification Metadata

| 字段 | 值 |
|---|---|
| Environment | 尚未准备 |
| Browser / Device / PDA | 尚未执行 |
| Human Verifier | 尚未指定 |
| Verification Start | 尚未执行 |
| Verification End | 尚未执行 |

## 2. Required Scenarios

| 场景 | 验证内容 | 当前结果 |
|---|---|---|
| `HVR-OUTBOUND-001` | Web 创建、保存、查询和提交 | NOT RUN |
| `HVR-OUTBOUND-002` | Web 司机和仓库操作员双签名 | NOT RUN |
| `HVR-OUTBOUND-003` | PDA 触控布局、填写和双签名 | NOT RUN |
| `HVR-OUTBOUND-004` | 时间顺序和提交错误提示 | NOT RUN |
| `HVR-OUTBOUND-005` | 多语言字段和选择值 | NOT RUN |
| `HVR-OUTBOUND-006` | 异常结果只记录，不自动阻止放行或创建流程 | NOT RUN |

## 3. Current Status

| 指标 | 值 |
|---|---|
| Required Scenarios | 6 |
| PASS | 0 |
| FAIL | 0 |
| BLOCKED | 0 |
| NOT RUN | 6 |
| Current Evidence Set | None |

## 4. Verification Discipline

- 自动化测试 PASS 不得转换为 HVR PASS；
- Agent 不得冒充人类验证者；
- PDA 必须在真实 PDA 或等效触控设备上验证；
- 双签名必须验证图像、签名人和签名时间均可重新查看；
- 异常结果只记录事实，不得把人工复核边界验证成自动业务结论。

## 5. Run History（Append-only）

当前没有 HVR Run。执行后追加验证者、设备、步骤、观察、结果和证据位置。
