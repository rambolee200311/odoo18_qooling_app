# Outbound Form Coding Contract

> 文档状态：Frozen
> 文档版本：v1.1.0
> 冻结日期：2026-09-23
> 实施状态：Approved for Implementation
> 实施批准日期：2026-09-23
> 上游 SRS：[SRS_qooling_outbound_form.md](../designing/SRS_qooling_outbound_form.md) `v1.1.0 Frozen`
> 上游 TDD：[TDD_qooling_outbound_form.md](../designing/TDD_qooling_outbound_form.md) `v1.1.0 Frozen`
> 适用 Form：Outbound / 出库表

## 0. 文档治理

本 Coding Contract（CC）冻结 Outbound Form 的实施范围、保留行为、禁止事项、
测试契约、停止条件和完成闸门，不重新定义 SRS 或 TDD 业务语义。

本 CC 已批准冻结并获得实施授权。编码仍必须遵守本文件以及冻结 SRS/TDD 的范围、
追溯、测试和停止条件。

## 1. 变更概述

| 字段 | 值 |
|---|---|
| Intent ID | `INTENT-OUTBOUND-FORM` |
| 工作类型 | 新功能 |
| 变更类型 | Odoo Form 记录能力迁移 |
| 目标 | 在 Odoo 18 中实现 Outbound 字段填写、草稿保存、提交、查询、复核和 Web/PDA 入口 |
| 模块边界 | 由实施前确认是新模块还是合并到现有 Qooling 模块 |
| 数据迁移 | 否 |

核心定位：

> Outbound Form 是记录工具。它保存用户填写的出库检查、签名和证据，
> 不自动升级为库存、运输、放行或异常业务流程。

## 2. 上游基线与追溯

### 2.1 SRS

| SRS 范围 | CC 处理 |
|---|---|
| FR-FORM-01 至 FR-FORM-06 | 在范围内 |
| FR-FORM-08、FR-FORM-09、FR-FORM-15 | 在范围内 |
| FR-FORM-20 至 FR-FORM-26 | 在范围内 |
| BR-FORM-01 至 BR-FORM-11 | 按 TDD 记录边界实现 |
| AC-01 至 AC-34 | 必须建立可执行测试或人工验证证据 |

### 2.2 TDD

技术基线为冻结的 `TDD_qooling_outbound_form.md v1.0.0`。任何字段、状态、
权限、入口或人工复核边界变更，必须先修订 TDD 和本 CC。

## 3. 范围冻结

### 3.1 In Scope

- 建立 Outbound Form 所需的 Odoo ORM 模型和序列；
- 实现 SRS 第 3 章的基础字段、时间字段、ADR、温度、检查项和证据字段；
- 实现 Check Loading、Cargo、Vehicle、Driver 的逐项记录；
- 实现草稿保存、提交、查询、复核查看和授权撤回；
- 实现司机和仓库操作员两套独立手写签名；
- 实现 Web/PDA 入口的一致字段语义和提交结果；
- 实现 Odoo 多语言字段名和选择值；
- 实现照片和备注的非必填保存；
- 建立 ORM、权限、视图、签名和 PDA 触控测试。

### 3.2 Out of Scope

- PDF 入口、PDF 上传、PDF 解析、PDF 生成或 PDF 归档；
- 自动库存移动、运输、采购、销售、放行或装载业务动作；
- 自动阻止出库放行；
- 自动通知、异常工单、隔离或关闭异常；
- 自动判断重量分布、温度范围或检查项是否合格；
- Qooling 历史数据迁移；
- Outbound 之外的 Inbound 或 Weekly Temperature Control 实现；
- 未经 TDD 定义的模型、字段、状态、接口或依赖。

### 3.3 非目标

- 不以字段结果推导业务结论；
- 不将司机或仓库签名替换为姓名文本、勾选或键盘输入；
- 不把照片设为提交阻断条件；
- 不用前端隐藏代替服务端权限；
- 不把 PDA 页面实现成仅缩小而不可操作的 Web 表单。

## 4. 允许的变更边界

| 类型 | 允许内容 |
|---|---|
| 模块 | 仅 TDD 确定的 Outbound 模块目录 |
| 模型 | 仅 `wd.qooling.outbound.form` 及 TDD 规定的辅助关系 |
| 字段 | 仅 SRS/TDD 已定义字段 |
| 视图 | Outbound 所需 Form/List/Search 和 PDA 触控界面 |
| 权限 | 库管、仓库主管和未授权用户的 TDD 权限矩阵 |
| 测试 | Outbound ORM、权限、视图、签名、多语言和 PDA 测试 |

禁止修改 Odoo 官方代码、使用裸 SQL、引入独立数据库或绕过 ORM。

## 5. 必需行为变更

| ID | 期望行为 | CC ID |
|---|---|---|
| 1 | 授权库管可创建并保存 Outbound 草稿 | `CC-OUTBOUND-CHANGE-001` |
| 2 | 保存 SRS 定义的基础、检查、温度、车辆和证据字段 | `CC-OUTBOUND-CHANGE-002` |
| 3 | 到达、开始装载、结束装载时间按顺序校验 | `CC-OUTBOUND-CHANGE-003` |
| 4 | 两套手写签名均为可选；存在时保存并可随记录提交 | `CC-OUTBOUND-CHANGE-004` |
| 5 | Web/PDA 产生一致字段语义和记录结果 | `CC-OUTBOUND-CHANGE-005` |
| 6 | 授权用户可查看、查询、复核和按权限撤回 | `CC-OUTBOUND-CHANGE-006` |
| 7 | 多语言界面不显示三语并列文本 | `CC-OUTBOUND-CHANGE-007` |

## 6. 必须保留的行为

| ID | 保留行为 | CC ID |
|---|---|---|
| 1 | 检查项不合格是否阻止放行由人工复核决定 | `CC-OUTBOUND-PRESERVE-001` |
| 2 | 重量分布标准由人工复核决定，系统只保存结果 | `CC-OUTBOUND-PRESERVE-002` |
| 3 | 温度范围和阈值由人工复核决定，系统不自动判断 | `CC-OUTBOUND-PRESERVE-003` |
| 4 | 温度控制名称和实际每日记录频率由用户决定 | `CC-OUTBOUND-PRESERVE-004` |
| 5 | 照片和备注非必填 | `CC-OUTBOUND-PRESERVE-005` |
| 6 | 司机和仓库操作员签名必须是手写签名 | `CC-OUTBOUND-PRESERVE-006` |

## 7. 禁止的业务升级

编码不得实现以下行为：

- 根据包装、车辆、驾驶员、固定、重量或温度结果自动阻止放行；
- 根据 ADR 或检查结果自动创建异常状态、工单、通知或隔离记录；
- 自动修改库存、运输、采购、销售或仓库作业数据；
- 自动把人工复核结果变成系统合格/不合格结论；
- 自动合并、覆盖或删除原始检查结果。

发现需要上述行为时必须停止编码并提交范围变更。

## 8. 数据、权限和错误契约

- 所有记录通过 Odoo ORM 保存和读取；
- `date_arrival <= start_loading_at <= end_loading_at` 必须在服务端校验；
- 两套签名图像、签名人和签名时间必须分别保存；
- 选择值必须由 ORM 约束限制；
- ACL/Record Rule 必须覆盖创建、读取、修改、提交、撤回和复核；
- 缺少必填字段或时间顺序错误时保持草稿并显示真实错误；签名缺失不阻止提交；
- 不允许静默吞错、成功形状回退或伪造提交成功。

## 9. 测试契约

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-OUTBOUND-TEST-001` | 创建、保存、重读草稿 | ORM | 字段值完整保持 |
| `CC-OUTBOUND-TEST-002` | 时间顺序 | ORM | 逆序时间不能提交 |
| `CC-OUTBOUND-TEST-003` | 两方签名提交 | ORM/UI | 无签名、单方签名和双方签名均可按规则提交 |
| `CC-OUTBOUND-TEST-004` | UN Number | ORM | 只允许 `3171`、`3480`、`3481` |
| `CC-OUTBOUND-TEST-005` | 检查和温度结果 | ORM | 只保存结果，不触发业务流程 |
| `CC-OUTBOUND-TEST-006` | 照片和备注 | ORM | 为空仍可按其他条件提交 |
| `CC-OUTBOUND-TEST-007` | ACL/Record Rule | ORM/HTTP | 未授权用户被拒绝 |
| `CC-OUTBOUND-TEST-008` | Web/PDA 签名交互 | Playwright/QUnit | 两个签名区域均可绘制并持久化 |
| `CC-OUTBOUND-TEST-009` | PDA 触控布局 | Playwright/HVR | 关键字段和操作适合触控设备 |
| `CC-OUTBOUND-TEST-010` | 多语言 | Playwright | 只显示当前语言 |

没有执行的测试不得记录为 PASS。自动化 PASS 不能替代 PDA 或签名的人工 HVR。

## 10. 实施停止条件

遇到以下任一情况必须停止并请求变更批准：

1. 需要增加 PDF 入口；
2. 需要自动放行、阻止放行或自动异常流程；
3. 需要新增 TDD 未定义的字段、状态、接口或依赖；
4. 需要修改现有 Inbound 或 Weekly Form；
5. 无法在 ORM 层表达关键约束；
6. PDA 触控界面无法通过真实设备或等效触控 HVR；
7. 任何测试只能通过伪造成功、静默吞错或跳过权限验证。

## 11. 完成闸门

实施完成前必须满足：

- [ ] SRS/TDD/CC 追溯矩阵完整；
- [ ] ORM、视图、安全和前端资源通过针对性测试；
- [ ] 两方签名的 Web/PDA 持久化通过；
- [ ] 时间顺序、UN Number 和权限测试通过；
- [ ] 人工复核边界无自动业务处置；
- [ ] PDA 触控 HVR 完成并记录真实结果；
- [ ] IHR、ATR、HVR 和 Final Report 更新；
- [ ] Human Review 批准后才能 Merge/Release。
