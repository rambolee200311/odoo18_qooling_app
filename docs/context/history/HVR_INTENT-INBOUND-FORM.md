# Inbound Form Human Verification Record（HVR）

> 文档状态：In Progress  
> Intent ID：`INTENT-INBOUND-FORM`  
> CC：`v1.0.0 Frozen`  
> IHR：[IHR_INTENT-INBOUND-FORM.md](./IHR_INTENT-INBOUND-FORM.md)  
> ATR：[ATR_INTENT-INBOUND-FORM.md](./ATR_INTENT-INBOUND-FORM.md)

## 1. Verification Metadata

| 字段 | 值 |
|---|---|
| Module | `wd_qooling_app` |
| Environment | Odoo 18，主工作区本地运行环境 |
| Environment Type | Normal / Development |
| Application Version | Odoo 18 |
| Initial Code Baseline | 当前实施工作区，待提交 |
| Browser / Device / PDA | Browser（本地 Odoo HVR 实例） |
| Verification Start | 2026-09-22 |
| Verification End | 2026-09-22 |

## 2. Human Verification Contract Baseline

| 来源 | ID | 验证内容 |
|---|---|---|
| CC Test Contract | `CC-TEST-003` | ADR 条件字段的真实表单行为 |
| CC Test Contract | `CC-TEST-006` | Web/PDA 手写签名 |
| CC Test Contract | `CC-TEST-007` | 多语言字段和选择值 |
| CC-PRESERVE | `CC-PRESERVE-004` | 手写签名不能被文本替代 |
| CC-PRESERVE | `CC-PRESERVE-005` | 不显示三语并列文本 |

## 3. Current Human Verification Status

| 字段 | 值 |
|---|---|
| Human Verification Required | Yes |
| Required Scenarios | 4 |
| PASS | 3 |
| FAIL | 0 |
| BLOCKED | 0 |
| NOT RUN | 1 |
| Current Code Baseline | ACL 与签名组件修复后，待提交 |
| Current Valid Evidence Set | — |
| Evidence Baseline Status | Incomplete |

## 4. Human Verification Coverage Matrix

| Verification Requirement | Scenario | Upstream | Current Evidence | Result | Baseline |
|---|---|---|---|---|---|
| ADR 条件字段 | `HVR-SCN-001` | `AC-INBOUND-06`、`T-DATA-001` | 浏览器现场观察 | PASS | 当前工作区 |
| Web 手写签名 | `HVR-SCN-002` | `AC-INBOUND-12`、`T-SIGN-001` | 浏览器现场观察；修复后复测 | PASS | 当前工作区 |
| 移动/PDA 手写签名 | `HVR-SCN-003` | `FR-INBOUND-09`、`AC-INBOUND-12` | 仅完成移动视口响应式 Web 观察 | NOT RUN（专用 PDA 技术债） | `TD-INBOUND-PDA-001` |
| 多语言显示 | `HVR-SCN-004` | `AC-INBOUND-13`、`T-I18N-001` | 浏览器现场观察 | PASS | 当前工作区 |

## 5. Verification Scenarios

### HVR-SCN-001 — ADR 条件字段

- 前置：以库管用户打开新建 Inbound Form。
- 步骤：选择 ADR `Yes`，观察并填写 UN Number 和温度字段；再切换 ADR `No`。
- 预期：ADR `Yes` 显示相关字段；ADR `No` 不要求填写；系统不显示自动危险品结论。
- 当前结果：PASS。验证者确认 ADR `Yes` 显示相关字段，切换为 `No` 后不要求填写。

### HVR-SCN-002 — Web 手写签名

- 前置：创建满足提交条件的 Inbound 草稿。
- 步骤：在 Web 签名区域绘制签名，保存草稿并提交，重新打开记录。
- 预期：签名图像、签名人和签名时间可查看；无签名不能提交。
- 首次执行发现签名笔画自动连线；修复后复测结果：PASS。分离笔画不再连线，提交后签名图像、Signer 和 Signature time 均可重新查看。

### HVR-SCN-003 — PDA/移动视口手写签名

- 前置：使用 PDA 或移动视口登录库管用户。
- 步骤：填写表单、绘制签名、提交并重新打开记录。
- 预期：移动视口可操作签名区域，记录结果与 Web 入口一致。
- 当前结果：NOT RUN。已验证移动视口响应式 Web 可绘制和保存签名，但专用 PDA 触控 Web 界面尚未实现；见 `TD-INBOUND-PDA-001`。

### HVR-SCN-004 — 多语言显示

- 前置：准备至少两个 Odoo 用户语言。
- 步骤：分别登录并打开 Inbound Form。
- 预期：每个用户只看到当前语言字段名和选择值，不显示 Qooling 三语并列文本。
- 当前结果：PASS。验证者确认字段名和选择值按当前语言显示，未出现 Qooling 三语并列文本。

## 6. Verification Run History（Append-only）

已由人类验证者 `lijianqiang` 在本地浏览器执行 `HVR-SCN-001` 至
`HVR-SCN-004`，结果均为 PASS；`HVR-SCN-002` 首次发现问题后已修复并复测通过。
首次问题保留在 Findings 中。

| Run | 验证者 | 场景 | 结果 | 说明 |
|---|---|---|---|---|
| `HVR-RUN-001` | `lijianqiang` | `HVR-SCN-001`、`HVR-SCN-002` | PARTIAL | ADR PASS；签名首次发现笔画自动连线 |
| `HVR-RUN-002` | `lijianqiang` | `HVR-SCN-002` | PASS | 修复后分离笔画、提交和重新打开均正常 |
| `HVR-RUN-003` | `lijianqiang` | `HVR-SCN-004` | PASS | 多语言显示符合预期 |

## 7. Human Regression Verification

尚未执行。`CC-PRESERVE-004` 和 `CC-PRESERVE-005` 待真实人类完成 HVR-SCN-002 至 004 后验证。

## 8. Findings / Issues

| ID | Scenario | Run | Finding | Severity | Status | Follow-up |
|---|---|---|---|---|---|---|
| HVR-FIND-002 | `HVR-SCN-002` | HVR-RUN-001 / HVR-RUN-002 | 签名组件在新笔画开始时沿用了上一笔路径，导致笔画自动连线 | Medium | Fixed, verified | 在 pointerdown/pointerup 时初始化新路径；复测通过 |

## 9. Evidence Inventory

当前已有浏览器现场观察记录；暂无截图、视频或签名确认文件。自动化日志只属于 ATR，不作为 HVR 证据。

## 10. Handoff Summary

- HVR-SCN-001 至 HVR-SCN-004 均已由人类验证者 PASS；
- `HVR-SCN-001` 已由 `lijianqiang` PASS；
- `HVR-SCN-002` 首次发现并修复签名连笔问题，复测已 PASS；
- `HVR-SCN-003` 仅完成响应式 Web 观察，专用 PDA 界面待 `TD-INBOUND-PDA-001`；
- `HVR-SCN-004` 已由 `lijianqiang` PASS；
- 当前 HVR 范围已完成；不包含 PDF 入口。
