# Inbound Form 技术设计说明书（TDD）

> 文档状态：Frozen
> 文档版本：v1.2.0
> 技术负责人：待指定
> 基线日期：2026-09-22
> 上游 SRS：[SRS_qooling_inbound_form.md](./SRS_qooling_inbound_form.md)
> 下游 Coding Contract：[Coding_Contract_Inbound_Form.md](../intent/Coding_Contract_Inbound_Form.md)

## 0. 文档说明

### 0.1 文档定位

本文档将冻结的 Inbound SRS 转换为 Odoo 18 技术实现方案，覆盖 ORM、字段约束、状态、权限、视图、签名、入口适配、测试和实现防护栏。

本 TDD 不新增业务语义。`Packaging condition`、`Unloading permission`、气体、通风和温度结果只保存为用户填写的记录值，不触发自动卸货、通知、异常工单、隔离、放行或库存动作。

### 0.2 上游基线

| 项 | 内容 |
|---|---|
| 业务基线 | Inbound SRS `v0.8.0`，已冻结 |
| 领域基线 | N/A；当前为简单 Form 记录，不建立 DDD |
| 执行边界 | Coding Contract `v0.1.0`，Draft |
| Odoo | `18.0` |
| Python | `>= 3.10` |

### 0.3 入口范围

本 TDD 仅覆盖 Web 和 PDA 入口，不包含 PDF 入口或 PDF 相关技术实现。

## 1. 技术上下文与基线冻结

### 1.1 技术栈

| 层次 | 选型 | 版本 | 说明 |
|---|---|---|---|
| 平台/框架 | Odoo | 18.0 | 项目基线 |
| 语言/运行时 | Python | >= 3.10 | 与 Odoo 18 兼容 |
| 数据库 | PostgreSQL | 由 Odoo 部署环境提供 | 不直接访问 |
| 后端数据访问 | Odoo ORM | Odoo 18 原生 | 禁止裸 SQL |
| Web UI | Odoo XML View / 原生 Web Client | Odoo 18 | 优先标准 Form/List/Search |
| PDA UI | 专用 PDA 触控 Web 入口 | Odoo 18 | 当前为技术债 `TD-INBOUND-PDA-001`，本版本仅有响应式 Web 基线 |
| 队列/缓存 | 无 | N/A | 本 Form 不需要异步或缓存 |

### 1.2 模块依赖

| 依赖 | 类型 | 用途 | 必需 |
|---|---|---|---|
| `base` | Odoo 官方模块 | 用户、公司和基础 ORM | 是 |
| `web` | Odoo 官方模块 | Web 表单和客户端 | 是 |
| `mail` | Odoo 官方模块 | 可选的记录追踪能力，是否启用待实现评估 | 否 |

不得为了 Inbound Form 引入队列、Redis、消息总线、独立服务或第三方前端框架。

### 1.3 已知技术债

`TD-INBOUND-PDA-001`：当前实现的 PDA 能力只是标准 Odoo Web 表单的响应式访问，
尚未实现专门的 PDA 触控 Web 界面。后续实现必须复用现有 ORM 和提交规则，
不得新增仓库业务流程。

## 2. 模块目录结构

```text
mymodules/wd_qooling_app/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── inbound_form.py
├── views/
│   ├── inbound_form_views.xml
│   └── menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── tests/
    ├── __init__.py
    └── test_inbound_form.py
```

不创建 `services/`、`adapters/`、`queue/` 或独立 Schema 目录。

## 3. ORM 模型设计

### 3.1 主模型

| 编号 | 技术设计 |
|---|---|
| ORM-INBOUND-001 | 新增模型 `wd.qooling.inbound.form`，对应一条 Inbound Form 记录 |
| ORM-INBOUND-002 | 使用 `name` 作为系统生成的 `Number`，通过 `ir.sequence` 生成 |
| ORM-INBOUND-003 | 使用 `state` 保存技术状态：`draft`、`submitted` |
| ORM-INBOUND-004 | 使用 `ref_no` 保存用户选择的业务参考；不自动创建或修改库存/物流单据 |
| ORM-INBOUND-005 | `create_uid` / `create_date` / `write_uid` / `write_date` 保存 ORM 审计信息；Filled in by 映射当前创建用户 |

### 3.2 字段契约

| ORM 编号 | 字段 | Odoo 类型 | 约束/说明 |
|---|---|---|---|
| ORM-INBOUND-010 | `location_id` | `Many2one` | 指向仓库档案，必填 |
| ORM-INBOUND-011 | `date` | `Date` | 默认当前日期，可修改 |
| ORM-INBOUND-012 | `supervisor_id` | `Many2one(res.users)` | 必填，用户选择 |
| ORM-INBOUND-013 | `goods_status` | `Selection` | `free_union_goods`、`t1` |
| ORM-INBOUND-014 | `unloading_permission` | `Selection` | `yes`、`no_stop_unloading`；只保存选择 |
| ORM-INBOUND-015 | `mrn_number` | `Char` | 非必填 |
| ORM-INBOUND-016 | `seal_number` | `Char` | 非必填；多个值由用户以逗号分隔 |
| ORM-INBOUND-017 | `skal_bio_product` | `Selection` | `yes`、`no` |
| ORM-INBOUND-018 | `bl_number` | `Char` | 非必填 |
| ORM-INBOUND-019 | `container_shipment_number` | `Char` | 非必填 |
| ORM-INBOUND-020 | `filled_in_by_id` | `Many2one(res.users)` | 创建时默认当前用户，只记录事实 |
| ORM-INBOUND-021 | `filing_date` | `Date` | 填写日期 |
| ORM-INBOUND-022 | `checked_visible_damage` | `Boolean` | Checkbox list 第一项 |
| ORM-INBOUND-023 | `checked_received_quantity` | `Boolean` | Checkbox list 第二项 |
| ORM-INBOUND-024 | `checked_product_quality` | `Boolean` | Checkbox list 第三项 |
| ORM-INBOUND-025 | `packaging_condition` | `Selection` | `good`、`not_good`；只保存结果 |
| ORM-INBOUND-026 | `gas_measurement` | `Selection` | `yes`、`no`、`not_applicable` |
| ORM-INBOUND-027 | `gas_measurement_status` | `Selection` | `safe`、`ventilation_required`、`dangerous` |
| ORM-INBOUND-028 | `ventilated` | `Selection` | `yes`、`not_applicable` |
| ORM-INBOUND-029 | `status_after_ventilation` | `Selection` | `safe`、`ventilation_required`、`dangerous` |
| ORM-INBOUND-030 | `adr` | `Selection` | `yes`、`no` |
| ORM-INBOUND-031 | `un_number` | `Selection` | `3171`、`3480`、`3481` |
| ORM-INBOUND-032 | `temperature_measured` | `Selection` | `yes`、`no` |
| ORM-INBOUND-033 | `pallet_temperature_registered` | `Selection` | `yes`、`no` |
| ORM-INBOUND-034 | `average_temperature_per_pallet` | `Float` | 摄氏度数值；不设置业务阈值判断 |
| ORM-INBOUND-035 | `photo` | `Binary` | 非必填；单个表单关联图片 |
| ORM-INBOUND-036 | `comments` | `Text` | 非必填 |
| ORM-INBOUND-037 | `warehouse_signature` | `Binary` | Web/PDA 手写签名图像，提交必填 |
| ORM-INBOUND-038 | `signer_id` | `Many2one(res.users)` | 签名用户 |
| ORM-INBOUND-039 | `signature_time` | `Datetime` | 签名时间 |
| ORM-INBOUND-040 | `submitted_by_id` | `Many2one(res.users)` | 提交用户 |
| ORM-INBOUND-041 | `submitted_at` | `Datetime` | 提交时间 |

字段的技术英文名不改变 SRS 业务语义；界面标签、帮助文本和 Selection 显示值必须提供 Odoo 翻译。

### 3.3 关系与权威

- `location_id` 的仓库档案为 Location 的唯一引用来源。
- 用户字段均引用 `res.users`，不复制用户姓名文本作为权威字段。
- 本模型不建立库存、采购、运输或项目对象的自动联动。
- Checkbox list 在 ORM 层暂按三个布尔字段实现；若业务确认要求其他控件或选项，须先修订 SRS/TDD。

## 4. 数据约束与索引

### 4.1 ORM 约束

| 编号 | 约束 |
|---|---|
| ORM-INBOUND-050 | `state` 只能为 `draft` 或 `submitted` |
| ORM-INBOUND-051 | `un_number` 的值只能为 `3171`、`3480`、`3481`；不对其他文本做业务推断 |
| ORM-INBOUND-052 | `state = submitted` 时，提交所需字段和 `warehouse_signature` 必须存在 |
| ORM-INBOUND-053 | `signer_id` 与 `signature_time` 必须与手写签名图像同时保存 |
| ORM-INBOUND-054 | 不对包装、气体、通风、温度或卸货许可值创建自动异常约束 |

约束必须在 ORM/模型层可验证，不能只依赖视图隐藏。

### 4.2 索引

- 对 `date`、`filled_in_by_id`、`ref_no` 建立查询所需索引，具体由 PostgreSQL/Odoo ORM 实现评估确定。
- 不为未确认的报表或业务流程预建索引。

## 5. JSON / 报文 Schema

当前不存在外部 JSON API，也不建立内部 JSON 作为第二套权威数据模型。


## 6. 领域行为实现

本 Form 不建立独立领域服务。记录行为直接通过 Odoo ORM 模型方法实现：

| 编号 | 方法/行为 | 技术要求 |
|---|---|---|
| SVC-INBOUND-001 | 创建草稿 | 默认 `state = draft`、`filled_in_by_id = env.user`、`name` 取序列 |
| SVC-INBOUND-002 | 保存草稿 | 允许反复保存；不自动计算业务结论 |
| SVC-INBOUND-003 | 提交 | 校验提交所需字段和手写签名，写入提交人和提交时间，设为 `submitted` |
| SVC-INBOUND-004 | 撤回 | 按权限将 `submitted` 改回 `draft`，不新增异常状态 |
| SVC-INBOUND-005 | 查询 | 使用标准 Odoo Search View，不实现自建查询层 |

提交方法不得调用通知、库存、工单、隔离、放行或外部业务服务。

## 7. 外部服务 Adapter

无外部服务 Adapter。


## 8. 异步队列、Worker、Cron

不使用队列、Worker 或 Cron。Inbound Form 的保存、提交、查看和查询均为同步 ORM 操作。

## 9. 状态机技术态

| 技术状态 | 允许动作 | 实现 |
|---|---|---|
| `draft` | 创建、填写、保存、修改、提交 | 标准 Odoo Form |
| `submitted` | 查看、人工复核、按权限撤回 | 标准按钮/权限控制 |

禁止增加 `exception_pending`、`closed` 或其他异常工作流状态。

## 10. 并发、事务与锁

- 使用 Odoo ORM 默认事务边界。
- 提交操作在单个事务内完成：校验字段、写入签名/提交信息、更新状态。
- 不使用手工 SQL 锁。
- `ir.sequence` 使用 Odoo 原生序列机制保证编号生成。
- 记录撤回和重新提交必须在 ORM 事务中完成；失败时整体回滚。

## 11. 异常、错误码与告警

| 编号 | 场景 | 技术处理 |
|---|---|---|
| ERR-INBOUND-001 | 提交缺少必填字段或签名 | 使用 Odoo 用户可见校验错误，保持草稿 |
| ERR-INBOUND-002 | Selection 值不在允许范围 | ORM 校验失败，拒绝保存 |
| ERR-INBOUND-003 | 无权限创建、提交、查看或撤回 | Odoo ACL/Record Rule 拒绝并显示权限错误 |
| ERR-INBOUND-004 | 图片或签名保存失败 | 显示真实错误，不伪造成功 |

异常处理不得创建隐式异常工作流或自动业务通知。

## 12. 安全与权限

### 12.1 ACL

| 角色 | 创建 | 读取 | 修改草稿 | 提交 | 撤回 | 复核查看 |
|---|---:|---:|---:|---:|---:|---:|
| 库管 | 是 | 是 | 是 | 是 | 按授权 | 是 |
| 仓库主管 | 按授权 | 是 | 按授权 | 按授权 | 按授权 | 是 |
| 未授权用户 | 否 | 否 | 否 | 否 | 否 | 否 |

具体 Odoo group、ACL 和 Record Rule 在实现前必须由项目权限设计确认；不得用隐藏按钮代替服务端权限。

### 12.2 数据安全

- 通过 ORM 访问所有记录。
- 不在日志记录签名原始数据、令牌、密码或服务器绝对路径。
- 图片和签名按 Odoo 附件/二进制字段安全策略保存。
- 不新增跨公司、客户或区域隔离语义。

## 13. UI 契约

### 13.1 Web/PDA

- 使用标准 Odoo Form View，移动端优先保持可操作布局。
- Selection 标签使用 Odoo 翻译，不显示三语并列文本。
- ADR 为 `Yes` 时显示 UN Number 和温度相关字段；为 `No` 时不要求填写。
- 签名使用 Odoo 可兼容的手写签名组件；若标准组件不足，才在 TDD 修订中定义最小 Owl 组件。
- 提交按钮必须触发服务端校验，不能只依赖前端必填属性。


### 13.3 稳定选择器

需要 Playwright 验证的自定义交互，必须在实现时为关键控件增加稳定 `data-testid`，并在测试契约中记录；不得硬编码业务记录 ID。

## 14. 测试设计

| 测试编号 | 类型 | 覆盖 |
|---|---|---|
| TEST-INBOUND-001 | Odoo TransactionCase | 创建、保存和重新读取草稿 |
| TEST-INBOUND-002 | Odoo TransactionCase | 提交必填字段和签名校验 |
| TEST-INBOUND-003 | Odoo TransactionCase | Selection 值和 UN Number 限制 |
| TEST-INBOUND-004 | Odoo TransactionCase | 提交只保存记录，不触发业务流程 |
| TEST-INBOUND-005 | Odoo TransactionCase | 草稿/已提交状态和撤回 |
| TEST-INBOUND-006 | Odoo View/HTTP Test | ACL、Record Rule 和用户权限 |
| TEST-INBOUND-007 | QUnit/OWL 或 Playwright | Web/PDA 手写签名持久化 |
| TEST-INBOUND-008 | Playwright | 多语言字段和选择值显示 |
| TEST-INBOUND-009 | Playwright | 移动视口填写和提交 |

没有真实执行的测试不得记录为 PASS。E2E 必须等待业务 UI 状态，不使用 `networkidle` 或固定 sleep 作为通用等待。

## 15. 可观测性

- 使用 Odoo 标准日志，仅记录模块事件、记录编号和错误上下文。
- 不记录签名图像、图片内容或敏感用户数据。
- 不新增指标、队列监控或外部追踪系统。
- 用户可见错误必须来自真实异常，不使用成功形状的静默回退。

## 16. 部署与运行前置

- 模块放置于 `mymodules/wd_qooling_app`。
- `__manifest__.py` 必须声明实际使用的官方依赖和数据文件。
- 安装/升级使用 Odoo 模块机制，不直接改数据库。
- 模块升级前执行针对性 ORM/视图测试。

## 17. 技术风险与防护

| 风险 | 防护 |
|---|---|
| 将表单异常扩展为业务流程 | `T-SCOPE-001`、提交回归测试 |
| 只靠 UI 隐藏实现 ADR 条件 | `T-DATA-001`，服务端校验与视图测试同时覆盖 |
| 签名被普通文本替代 | `T-SIGN-001`，验证图像、签名人和时间 |
| 多语言显示三语并列 | `T-I18N-001`，不同用户语言 E2E 验证 |
| 权限只在按钮层实现 | `T-SEC-001`，ACL/Record Rule 和真实用户测试 |

## 18. Implementation Guardrails

| 编号 | 防护栏 | 强制要求 | 验证 |
|---|---|---|---|
| T-SCOPE-001 | Form 记录边界 | 不得由字段值触发仓库业务动作或异常工作流 | TEST-INBOUND-004 |
| T-DATA-001 | 服务端数据正确性 | 关键必填、Selection 和签名约束必须在 ORM/模型层验证 | TEST-INBOUND-002、003 |
| T-SIGN-001 | 手写签名证据 | 提交必须有签名图像、签名人和签名时间 | TEST-INBOUND-002、007 |
| T-I18N-001 | 多语言 | 标签和 Selection 使用 Odoo 翻译，不硬编码三语并列 | TEST-INBOUND-008 |
| T-SEC-001 | 权限 | ACL/Record Rule 必须覆盖创建、读取、修改、提交和撤回 | TEST-INBOUND-006 |
| T-ORM-001 | 数据访问 | 只能通过 Odoo ORM，不得使用裸 SQL 或数据库驱动 | 代码审查 |
| T-ERR-001 | 错误透明 | 保存/提交/文件错误必须显式显示，不得静默成功 | TEST-INBOUND-002、运行验证 |

## 19. 需求追溯矩阵

| SRS ID | TDD 实现 |
|---|---|
| FR-INBOUND-01 至 04 | ORM-INBOUND-001 至 005、SVC-INBOUND-001 至 003 |
| FR-INBOUND-05 至 07 | SVC-INBOUND-004、005、SEC-ACL |
| FR-INBOUND-08、10 | UI 契约、TEST-INBOUND-007 至 009 |
| FR-INBOUND-11 | UI 动态行为、ORM-INBOUND-030 至 034、TEST-INBOUND-003 |
| FR-INBOUND-12、13 | ORM-INBOUND-026 至 034、SVC-INBOUND-002 |
| FR-INBOUND-14 | ORM-INBOUND-037 至 039、T-SIGN-001 |
| FR-INBOUND-15 | UI 契约、T-I18N-001 |
| BR-INBOUND-01 | ORM-INBOUND-037、TEST-INBOUND-002、T-SIGN-001 |
| BR-INBOUND-02 | T-SCOPE-001、ORM-INBOUND-054、TEST-INBOUND-004 |
| AC-INBOUND-01 至 16 | TEST-INBOUND-001 至 010 |

## 附录 A — 术语表

| 术语 | 含义 |
|---|---|
| Inbound Form | 货物接收记录表单 |
| 记录结果 | 用户填写并持久化的字段值 |
| 业务动作 | 卸货、通知、异常工单、隔离、放行或库存等超出 Form 记录范围的动作 |

## 附录 B — 技术决策记录

| TD 编号 | 决策 | 状态 |
|---|---|---|
| TD-001 | 使用单一 `wd.qooling.inbound.form` ORM 模型承载 Inbound Form 记录 | Draft |
| TD-002 | 使用 `draft` / `submitted` 两个技术状态，不建立异常工作流状态 | Draft |
| TD-003 | 使用 Odoo 原生 ORM、标准 XML View、ACL/Record Rule 和原生序列 | Draft |
| TD-004 | 不使用队列、缓存、外部服务或独立领域服务 | Draft |
| TD-005 | Checkbox list 暂按三个布尔字段保存；业务控件变化需回到 SRS/TDD | Draft |

## 附录 C — 版本变更记录

| 版本 | 日期 | 变更说明 | 状态 |
|---|---|---|---|
| v0.1.0 | 2026-09-22 | 基于冻结 Inbound SRS 和 Coding Contract 起草技术设计；明确 ORM、状态、权限、UI、测试和 Guardrails | Draft |
| v1.0.0 | 2026-09-22 | 经批准冻结；覆盖 Web/PDA 入口 | Frozen |
| v1.1.0 | 2026-09-22 | 根据业务更正移除 PDF 入口及其未决技术设计 | Revised |
| v1.2.0 | 2026-09-22 | 明确专用 PDA 触控 Web 界面为技术债，当前响应式 Web 不得宣称完成 PDA 专用界面 | Revised |

## 填写自查清单

- [ ] 技术负责人已指定
- [ ] 具体 ACL/Record Rule 已完成权限评审
- [ ] 签名组件方案已通过 Web/PDA 技术验证
- [x] TDD 已由人工 Review 冻结
- [ ] Coding Contract 已同步 TDD 版本并解除等待状态
