# Inbound Form Coding Contract

> 文档状态：Frozen
> 文档版本：v1.0.0
> 实施状态：Approved for Implementation
> 实施批准日期：2026-09-22
> 上游 SRS：[SRS_qooling_inbound_form.md](../designing/SRS_qooling_inbound_form.md)
> 适用模块：`mymodules/wd_qooling_app`

## 0. 文档治理

本 Coding Contract（CC）只冻结 Inbound Form 本次实现的范围、保留行为、禁止事项、测试契约和完成闸门，不重新定义 SRS 业务语义。

Inbound TDD `v1.1.0` 已根据业务更正修订并冻结。本 CC 仅覆盖 Web 和 PDA 入口。

本 CC 已获批准进入实施。批准不解除范围、追溯、测试和停止条件；编码必须严格遵守本文件以及 TDD Guardrails。

## 1. 变更概述

| 字段 | 值 |
|---|---|
| Intent ID | `INTENT-INBOUND-FORM` |
| 模块 | `wd_qooling_app` |
| 工作类型 | 新功能 |
| 变更类型 | Odoo Form 记录能力迁移 |
| 目标 | 在 Odoo 18 中实现 Inbound Form 的字段填写、草稿保存、提交、查看和入口一致性 |
| 背景 | 将已冻结的 Qooling Inbound Form 记录能力迁移到 Odoo，不扩展为仓库业务流程 |

## 2. 上游基线与追溯

### 2.1 SRS 引用

| SRS ID | 标题 | 与本次 CC 的相关性 |
|---|---|---|
| FR-INBOUND-01 至 FR-INBOUND-07 | 记录操作 | 在范围内 |
| FR-INBOUND-08 至 FR-INBOUND-09 | Web、PDA 入口 | 在范围内，按 TDD 技术边界实现 |
| FR-INBOUND-11 至 FR-INBOUND-15 | 动态字段、签名、多语言 | 在范围内 |
| BR-INBOUND-01 至 BR-INBOUND-02 | 提交字段和结果保存边界 | 在范围内 |
| AC-INBOUND-01 至 AC-INBOUND-16 | Inbound 验收标准 | 在范围内 |

### 2.2 DDD 引用

N/A。当前项目尚无 Inbound DDD；不得为填写 CC 虚构领域对象或不变量。

### 2.3 TDD 引用

技术基线：[TDD_qooling_inbound_form.md](../designing/TDD_qooling_inbound_form.md)，当前为 `v1.0.0 Frozen`。


## 3. 范围冻结

### 3.1 In Scope

- 建立 Inbound Form 记录所需的 Odoo 数据结构；
- 实现 SRS 第 3 章定义的字段、选择值、必填性和多语言显示；
- 实现草稿保存、提交、查看和已提交记录按权限撤回为草稿；
- 实现 ADR 条件字段的表单显示和填写行为；
- 实现 Web/PDA 手写签名记录，包括签名图像、签名人和签名时间；
- 使 Web 和 PDA 入口产生具有一致字段含义和记录结果的 Inbound 记录；
- 保存可选照片和备注；
- 为 AC-INBOUND-01 至 AC-INBOUND-16 提供可验证测试。

### 3.2 Out of Scope

- 自动停止卸货；
- 自动联系或通知项目经理；
- 自动判断温度、气体、通风、包装或其他结果；
- 自动创建、推进或关闭异常工作流；
- 隔离、放行、仓库作业、库存操作或物流业务动作；
- Qooling 历史数据迁移；
- Outbound Form 和 Weekly Temperature Control；
- 未经 TDD 定义的额外模型、状态、字段、接口或依赖。

### 3.3 非目标

- 不实现仓库业务流程引擎；
- 不把 `Not good`、`No`、`Dangerous` 或温度结果转换为系统业务结论；
- 不自行拆分 Checkbox list 为更多业务字段；
- 不增加复核结果、复核意见、异常状态或更正历史字段；

## 4. 变更边界

### 4.1 允许

| 类型 | 详情 |
|---|---|
| 模块目录 | `mymodules/wd_qooling_app/` |
| 新增模型 | 仅 TDD 冻结后定义的 Inbound Form 模型 |
| 新增字段 | 仅 SRS 第 3 章字段 |
| 新增视图 | 仅 Inbound Form 所需的标准 Odoo Form/List/Search 视图 |
| 新增权限 | 仅库管创建/填写/提交、授权用户查看/复核所需权限 |
| 测试 | 仅 Inbound Form 相关 ORM、视图、权限和入口测试 |

### 4.2 禁止

| 类型 | 详情 |
|---|---|
| 官方代码 | 不修改 Odoo 官方核心代码或官方模块 |
| 数据访问 | 不使用 `psql`、裸 SQL 或数据库驱动；数据操作必须通过 Odoo ORM |
| 业务流程 | 不新增卸货、通知、异常、隔离、放行或库存自动动作 |
| 状态 | 不新增“异常待处理”“已关闭”等状态；只实现草稿和已提交 |
| 需求语义 | 不修改已冻结 SRS 的字段、选择值、必填性或人工处置边界 |
| 依赖 | 不引入未由 TDD 批准的新核心依赖 |
| 范围 | 不修改 Outbound、Weekly 或无关模块 |

## 5. 必需的行为变更

| ID | 当前行为 | 期望行为 | CC-CHANGE ID |
|---|---|---|---|
| 1 | 尚无 Inbound Odoo 记录实现 | 可创建并保存 Inbound 草稿 | CC-CHANGE-001 |
| 2 | 尚无 Inbound 字段实现 | 保存 SRS 第 3 章定义的字段和选择值 | CC-CHANGE-002 |
| 3 | 尚无提交能力 | 完成提交所需字段和手写签名后提交并保存提交信息 | CC-CHANGE-003 |
| 4 | 尚无条件字段行为 | ADR 为 `Yes` 时显示适用字段，`No` 时不要求填写 | CC-CHANGE-004 |
| 5 | 尚无入口一致性 | Web、PDA 记录具有一致字段含义和结果 | CC-CHANGE-005 |
| 6 | 尚无签名记录能力 | Web/PDA 保存签名图像、签名人和签名时间 | CC-CHANGE-006 |
| 7 | 尚无记录查询能力 | 授权用户可按日期、执行人和业务参考查询 | CC-CHANGE-007 |

## 6. 既有行为保留

| ID | 行为 / 契约 | 为什么不得改变 | CC-PRESERVE ID |
|---|---|---|---|
| 1 | `Packaging condition`、`Unloading permission`、气体、通风和温度结果只作为记录保存 | SRS 明确禁止自动处置和自动判断 | CC-PRESERVE-001 |
| 2 | 照片和备注非必填 | SRS BR-INBOUND-01 | CC-PRESERVE-002 |
| 3 | 状态仅为草稿和已提交 | SRS 第 6 章 | CC-PRESERVE-003 |
| 4 | 手写签名不能由姓名文本、勾选或键盘输入替代 | SRS FR-INBOUND-14 | CC-PRESERVE-004 |
| 5 | 字段名和选择值按用户语言显示，不显示三语并列文本 | SRS FR-INBOUND-15 | CC-PRESERVE-005 |

## 7. 适用的 TDD 防护栏

引用 TDD `v1.1.0 Revised` 中的 `T-SCOPE-001`、`T-DATA-001`、`T-SIGN-001`、`T-I18N-001`、`T-SEC-001`、`T-ORM-001` 和 `T-ERR-001`。

## 8. 数据 / 迁移影响

| 字段 | 值 |
|---|---|
| 需要迁移 | 否 |
| 迁移脚本 | N/A |
| 数据源 | 新建 Inbound Form 记录 |
| 目标 | Odoo ORM 模型 |
| 恢复 / 回滚策略 | 遵循 TDD 和人工 Review Gate；不得执行未经批准的破坏性更新 |
| 验证 | ORM 测试、升级测试和记录完整性验证 |

## 9. API / 集成影响

| 字段 | 值 |
|---|---|
| 修改的端点 | N/A；本次不新增外部入口协议 |
| 向后兼容 | N/A |
| Adapter 变更 | 当前无；本次不新增 Adapter |

## 10. 安全 / 权限影响

| 字段 | 值 |
|---|---|
| 新权限 | 库管创建/填写/提交；授权用户查看和复核 |
| 变更的 ACL | 按冻结 TDD 实现并通过权限测试 |
| 敏感数据暴露检查 | 不向用户暴露 SQL 回溯、令牌或服务器路径 |

## 11. 测试契约

| 测试 ID | 对应变更 | 上游来源 | 测试类型 | 预期结果 | 人工验证 | 原因 |
|---|---|---|---|---|---|---|
| CC-TEST-001 | 创建和保存草稿 | AC-INBOUND-01、03 | ORM/服务端 | 授权库管可创建，字段保存后可重新读取 | 否 | 核验基本记录能力 |
| CC-TEST-002 | 必填字段和签名提交 | AC-INBOUND-04 | ORM/服务端 | 缺少提交所需字段或签名时不能提交 | 否 | 防止不完整记录提交 |
| CC-TEST-003 | ADR 条件字段 | AC-INBOUND-06 | ORM/视图 | ADR 为 Yes/No 时字段显示和填写要求符合 SRS | 是 | 验证真实表单行为 |
| CC-TEST-004 | UN Number 选择限制 | AC-INBOUND-07 | ORM/视图 | 仅允许 `3171`、`3480`、`3481` | 否 | 防止字段值越界 |
| CC-TEST-005 | 记录结果不触发处置 | BR-INBOUND-02、AC-INBOUND-08 至 10、16 | ORM/回归 | 保存异常或温度结果不会创建、关闭或推进异常业务流程 | 否 | 防止 Form 业务流程化 |
| CC-TEST-006 | 手写签名证据 | AC-INBOUND-12 | QUnit/OWL 或 E2E | Web/PDA 可绘制并保存图像、签名人和时间 | 是 | 验证真实用户交互 |
| CC-TEST-007 | 多语言显示 | AC-INBOUND-13 | QUnit/E2E | 用户只看到当前语言字段名和选择值 | 是 | 验证用户界面语言行为 |
| CC-TEST-008 | 可选照片和备注 | AC-INBOUND-14 | ORM/服务端 | 照片和备注为空仍可按其他条件提交 | 否 | 防止错误增加阻断条件 |
| CC-TEST-009 | 入口结果一致性 | AC-INBOUND-11 | E2E/集成 | Web、PDA 记录的字段含义和结果一致 | 是 | 验证多入口记录一致性 |
| CC-TEST-010 | 查询和撤回 | AC-INBOUND-05、15 | ORM/服务端/E2E | 查询条件有效，授权撤回后可修改并重新提交 | 是 | 验证权限和生命周期 |

## 12. 停止条件 / 升级闸门

出现以下任一情况，必须停止实现并升级：

- 需要新增 SRS 未定义的字段、状态、业务结论或自动动作；
- 需要把异常结果转换成通知、工单、隔离、放行或库存操作；
- 需要新增核心模型、外部依赖、公共接口或权限语义；
- SRS 验收标准无法通过当前技术方案满足；
- TDD 缺失或与本 CC 冲突；
- 需要修改 Odoo 官方核心代码或使用 SQL 直接访问数据；
- 发现 Checkbox list 需要拆分为新的业务字段但尚无业务确认。

升级路径：先暂停编码，修订并冻结对应 SRS/TDD/CC，再继续。

## 13. 完成定义 / 关闭标准

| ID | 标准 | 闸门类型 |
|---|---|---|
| 1 | 所有 In-Scope 项均有对应 CC-CHANGE 实现 | 硬闸门 |
| 2 | 未修改禁止区域，未引入自动仓库业务流程 | 硬闸门 |
| 3 | CC-TEST-001 至 CC-TEST-010 已执行并取得证据 | 硬闸门 |
| 4 | CC-PRESERVE-001 至 CC-PRESERVE-005 已验证未改变 | 硬闸门 |
| 5 | 适用 TDD 防护栏已通过对应测试 | 硬闸门 |
| 6 | 需要人工验证的 Web/PDA 行为已完成 HVR | 硬闸门 |
| 7 | SRS、TDD、CC、测试和执行证据可追溯 | 硬闸门 |
| 8 | 人工 Review Gate 批准后才可合并或发布 | 硬闸门 |

## 14. 追溯矩阵

### 14.1 上游 SRS → CC

| 上游 ID | CC-CHANGE ID | 备注 |
|---|---|---|
| FR-INBOUND-01 至 03 | CC-CHANGE-001 | 创建和草稿 |
| FR-INBOUND-04 | CC-CHANGE-003 | 提交 |
| FR-INBOUND-05 至 07 | CC-CHANGE-007 | 查看、修改和查询 |
| FR-INBOUND-08 至 10 | CC-CHANGE-005 | 三种录入入口 |
| FR-INBOUND-11 | CC-CHANGE-004 | ADR 条件字段 |
| FR-INBOUND-12、13 | CC-CHANGE-002 | 气体、通风和温度字段 |
| FR-INBOUND-14 | CC-CHANGE-006 | 手写签名 |
| FR-INBOUND-15 | CC-CHANGE-002 | 多语言字段和选择值 |
| BR-INBOUND-01 | CC-CHANGE-003、006 | 签名和可选证据 |
| BR-INBOUND-02 | CC-CHANGE-002 | 结果只记录不自动处置 |
| AC-INBOUND-01 至 16 | CC-TEST-001 至 010 | 验收覆盖 |

### 14.2 CC → 上游

| CC ID | 上游 ID | 类型 |
|---|---|---|
| CC-CHANGE-001 至 007 | FR-INBOUND-* | SRS |
| CC-PRESERVE-001 至 005 | BR-INBOUND-*、FR-INBOUND-* | SRS |
| CC-TEST-001 至 010 | AC-INBOUND-*、BR-INBOUND-02 | SRS |

### 14.3 无 DDD 路径

当前执行链为：SRS → TDD → CC → TEST。DDD 为 N/A，不虚构领域编号。

## 附录 A — 变更决策

| CC-DEC ID | 决策 | 考虑的替代方案 | 理由 |
|---|---|---|---|
| CC-DEC-001 | 使用 Odoo 原生 ORM、标准视图和权限机制作为默认实现方向 | 引入额外 Repository、前端框架或独立服务 | 遵循 Odoo Engineering Guidelines 和已冻结 TDD |
| CC-DEC-002 | 不为异常结果创建自动业务动作 | 自动通知、工单、隔离或库存联动 | 保持 Qooling Form 的记录工具定位 |
| CC-DEC-003 | Checkbox list 暂不拆分为新业务字段 | 自行建立三个独立模型字段 | 当前 SRS 只确认检查内容，避免发明业务模型 |

## 附录 B — 术语表

| 术语 | 含义 |
|---|---|
| Inbound Form | 货物接收记录表单 |
| Qooling Form | 用于填写、保存、提交和查看检查结果的记录工具 |
| 入口 | Web 或 PDA 的录入方式 |
| 表单结果 | 用户填写并由系统保存的字段值，不等同于 Odoo 业务结论 |

## 附录 C — 版本历史

| 版本 | 日期 | 变更说明 | 状态 |
|---|---|---|---|
| v0.1.0 | 2026-09-22 | 基于已冻结 Inbound SRS 起草 Coding Contract；明确实现范围、禁止业务流程化和 TDD 前置闸门 | Draft |
| v1.1.0 | 2026-09-22 | 根据业务更正移除 PDF 入口，范围仅保留 Web/PDA | Revised |
