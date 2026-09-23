# Outbound Form 技术设计说明书（TDD）

> 文档状态：Frozen
> 文档版本：v1.0.0
> 基线日期：2026-09-22  
> 冻结日期：2026-09-22
> 上游 SRS：[SRS_qooling_outbound_form.md](./SRS_qooling_outbound_form.md) `v1.0.0`  
> 适用 Form：Outbound / 出库表

## 0. 文档定位与边界

本文档将冻结的 Outbound SRS 转换为 Odoo 18 技术设计，覆盖 ORM、字段约束、
Web/PDA 入口、签名、权限、状态、测试和实现防护栏。

本 TDD 不新增业务语义。检查项、重量分布、温度范围和异常结果均作为用户填写的
记录保存；人工复核决定是否阻止放行，系统不自动放行、阻止放行、通知或创建异常流程。

本期只有 Web 和 PDA 入口，不设计 PDF 入口、PDF 导入、PDF 解析或 PDF 生成。

## 1. 技术上下文

| 层次 | 选型 | 说明 |
|---|---|---|
| 平台 | Odoo 18 | 项目运行基线 |
| 后端 | Python >= 3.10 + Odoo ORM | 禁止裸 SQL 和独立数据库访问 |
| Web UI | Odoo XML View / Web Client | 标准 Form/List/Search 优先 |
| PDA UI | PDA 触控 Web 入口 | 与 Web 共享同一 Outbound 记录和提交规则 |
| 数据库 | PostgreSQL，由 Odoo 提供 | 仅通过 ORM 访问 |
| 异步能力 | 无 | 不引入队列、Worker、Cron 或缓存 |

不得为了 Outbound Form 引入独立前端框架、外部服务、库存联动或运输业务服务。

## 2. 模块边界与目录

建议模块目录：

```text
mymodules/wd_qooling_outbound/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── outbound_form.py
├── views/
│   └── outbound_form_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── data/
│   └── ir_sequence_data.xml
└── tests/
    ├── __init__.py
    └── test_outbound_form.py
```

最终模块名称、是否与现有 `wd_qooling_app` 合并，须在 Coding Contract 中明确；
本 TDD 不授权复制已有 Inbound 模型或把两个 Form 混成一个模型。

## 3. ORM 模型设计

### 3.1 主模型

| 编号 | 设计 |
|---|---|
| ORM-OUTBOUND-001 | 新增模型 `wd.qooling.outbound.form`，一条记录对应一份 Outbound Form |
| ORM-OUTBOUND-002 | `name` 使用 Odoo `ir.sequence` 生成表单编号 |
| ORM-OUTBOUND-003 | `state` 使用 `draft`、`submitted`、`exception_pending`、`closed`，具体异常状态只能由人工操作产生 |
| ORM-OUTBOUND-004 | `ref_no` 保存用户填写的业务参考，不自动创建或修改库存、运输、采购或销售单据 |
| ORM-OUTBOUND-005 | 使用 Odoo 创建/修改审计字段保存执行人和时间事实 |

### 3.2 字段契约

| 字段 | Odoo 类型 | 约束/说明 |
|---|---|---|
| `location_id` | Many2one(`stock.warehouse`) | 必填 |
| `date_arrival` | Datetime | 必填，可按权限修改 |
| `supervisor_id` | Many2one(`res.users`) | 必填 |
| `ref_no` | Char | 业务参考，非自动关联 |
| `start_loading_at` | Datetime | 必填 |
| `end_loading_at` | Datetime | 必填 |
| `goods_type` | Selection | `bonded`、`non_bonded` |
| `mrn_number` | Char | 非必填；`goods_type = non_bonded` 时 View 隐藏 |
| `seal_number` | Char | 非必填；`goods_type = non_bonded` 时 View 隐藏 |
| `mrn_checked_before_release` | Boolean/Selection | 只保存用户检查结果；`goods_type = non_bonded` 时 View 隐藏 |
| `adr` | Selection | `yes`、`no` |
| `un_number` | Selection | `3171`、`3480`、`3481`；`adr != yes` 时 View 隐藏 |
| `proper_shipping_name` | Char | 用户填写；`adr != yes` 时 View 隐藏 |
| `measured_temperature` | Float | 摄氏度数值，不设置自动阈值；`adr != yes` 时 View 隐藏 |
| `loading_plan_discussed` | Boolean/Selection | 不强制为 Yes |
| `adr_separation_compatibility` | Boolean/Selection | 非 ADR 时不自动隐藏或推断 |
| `weight_distribution` | Boolean/Selection/Text | 保存检查结果，标准由人工复核 |
| `driver_comments` | Text | 非必填 |
| `driver_signature` | Binary | 手写签名，提交必填 |
| `driver_signer_id` | Many2one(`res.users`) | 签名人 |
| `driver_signature_time` | Datetime | 签名时间 |
| `cargo_photo` | Binary | 非必填 |
| `warehouse_operator_comments` | Text | 非必填 |
| `warehouse_signature` | Binary | 手写签名，提交必填 |
| `warehouse_signer_id` | Many2one(`res.users`) | 签名人 |
| `warehouse_signature_time` | Datetime | 签名时间 |
| `filled_in_by_id` | Many2one(`res.users`) | 默认当前用户 |
| `filing_date` | Date | 系统填写日期 |

### 3.3 检查项

Check Loading、Cargo inspection、Vehicle inspection 和 Driver check 的每一项
使用独立 Boolean 或明确的 Selection 字段保存。不得把多个检查项压缩成一个无法
追溯的文本或总分。

## 4. ORM 约束与业务边界

| 编号 | 约束 |
|---|---|
| ORM-OUTBOUND-050 | Selection 值必须来自 SRS 规定选项 |
| ORM-OUTBOUND-051 | `date_arrival <= start_loading_at <= end_loading_at` |
| ORM-OUTBOUND-052 | `state = submitted` 时司机和仓库操作员签名图像及其审计字段必须存在 |
| ORM-OUTBOUND-053 | UN Number 只允许 `3171`、`3480`、`3481` |
| ORM-OUTBOUND-054 | 图片和备注为空不能阻止草稿保存或提交 |
| ORM-OUTBOUND-055 | 不根据检查、重量或温度结果自动创建异常、放行或阻止放行动作 |

时间顺序和签名完整性必须在 ORM/模型层校验，不能只依赖 View 属性。

## 5. 记录行为

| 编号 | 行为 | 技术要求 |
|---|---|---|
| SVC-OUTBOUND-001 | 创建草稿 | 默认 `state = draft`、填写人和编号 |
| SVC-OUTBOUND-002 | 保存草稿 | 允许反复修改，失败显示真实错误 |
| SVC-OUTBOUND-003 | 提交 | 校验时间、必填字段和两方手写签名，写入提交人和提交时间 |
| SVC-OUTBOUND-004 | 撤回 | 按权限将已提交记录撤回为草稿 |
| SVC-OUTBOUND-005 | 人工异常状态 | 只能由授权用户明确设置，不由字段结果自动触发 |
| SVC-OUTBOUND-006 | 查询 | 使用标准 Search View 支持日期、执行人和业务参考查询 |

提交方法不得调用库存、运输、采购、通知、隔离、放行或异常工单服务。

## 6. 状态与权限

| 状态 | 允许动作 |
|---|---|
| `draft` | 创建、填写、保存、修改和提交 |
| `submitted` | 查看、复核、按权限撤回 |
| `exception_pending` | 人工标记和查看，不自动生成 |
| `closed` | 人工关闭和查看，不自动生成 |

| 角色 | 创建/修改草稿 | 提交 | 查看 | 复核/异常状态 |
|---|---:|---:|---:|---:|
| 库管 | 是 | 是 | 是 | 按授权 |
| 仓库主管 | 按授权 | 按授权 | 是 | 是 |
| 未授权用户 | 否 | 否 | 否 | 否 |

ACL 和 Record Rule 必须在服务端生效，不能只隐藏按钮。

## 7. Web/PDA UI 契约

- Web 和 PDA 使用相同字段语义、状态和提交接口。
- PDA 页面必须适合触控操作；专用触控布局若超出标准 Form 能力，须在实现前补充 UI 设计。
- 检查项应保持可逐项操作和查看，不能只显示不可追溯的汇总值。
- 两个签名区域必须能区分司机签名和仓库操作员签名。
- 签名使用 Canvas/Owl 或经批准的 Odoo 签名组件，保存图像、签名人和时间。
- 界面只显示当前用户语言，不显示三语并列文本。
- 提交按钮必须触发服务端校验；前端 `required` 不能替代 ORM 校验。
- 自定义控件提供稳定 `data-testid`，不得以业务记录 ID 作为选择器。

## 8. 错误处理

| 编号 | 场景 | 处理 |
|---|---|---|
| ERR-OUTBOUND-001 | 缺少签名或必填字段 | 显示用户可见校验错误并保持草稿 |
| ERR-OUTBOUND-002 | 时间顺序错误 | 拒绝提交并明确提示 |
| ERR-OUTBOUND-003 | Selection 值非法 | ORM 拒绝保存 |
| ERR-OUTBOUND-004 | 无权限操作 | 使用 Odoo ACL/Record Rule 拒绝 |
| ERR-OUTBOUND-005 | 图片或签名保存失败 | 显示真实错误，不伪造成功 |

不得静默吞掉异常，不得把失败返回成已提交。

## 9. 测试设计

| 测试编号 | 类型 | 覆盖 |
|---|---|---|
| TEST-OUTBOUND-001 | TransactionCase | 创建、保存和重新读取草稿 |
| TEST-OUTBOUND-002 | TransactionCase | 必填字段、两方签名和提交 |
| TEST-OUTBOUND-003 | TransactionCase | 时间顺序校验 |
| TEST-OUTBOUND-004 | TransactionCase | UN Number 选择限制 |
| TEST-OUTBOUND-005 | TransactionCase | 图片和备注非必填 |
| TEST-OUTBOUND-006 | TransactionCase | 检查项结果只保存、不触发业务流程 |
| TEST-OUTBOUND-007 | TransactionCase | 撤回和人工异常状态权限 |
| TEST-OUTBOUND-008 | View/HTTP Test | ACL、Record Rule 和角色权限 |
| TEST-OUTBOUND-009 | Playwright/QUnit | Web/PDA 两个签名区域持久化 |
| TEST-OUTBOUND-010 | Playwright | 多语言字段和选择值 |
| TEST-OUTBOUND-011 | Playwright | PDA 触控布局填写和提交 |

没有执行的测试不得记录为 PASS。E2E 测试必须等待真实 UI 状态，不使用固定 sleep
或 `networkidle` 作为通用等待。

## 10. 可观测性与安全

- 只使用 Odoo 标准日志，记录记录编号和错误上下文。
- 不记录签名图像、照片内容、密码或令牌。
- 所有数据通过 Odoo ORM 访问，不使用裸 SQL。
- 不引入外部 API、队列、缓存或独立数据库。

## 11. 技术风险与停止条件

| 风险/停止条件 | 防护 |
|---|---|
| 将检查结果扩展为自动放行或阻止放行 | `ORM-OUTBOUND-055` 和回归测试 |
| 两方签名被一个字段替代 | 独立字段和 `TEST-OUTBOUND-009` |
| 仅靠前端校验时间或签名 | ORM 约束和 TransactionCase |
| PDA 被实现成不可操作的缩小 Web 表单 | PDA HVR 和触控布局验收 |
| 引入 PDF 入口 | 立即停止；不在本 TDD 范围内 |

### 11.1 已确认技术债

| 编号 | 技术债 | 当前状态 |
|---|---|---|
| TD-OUTBOUND-001 | 新增专用 PDA 触控 Web 界面和 PDA 专用 JavaScript 交互层；当前实现继续使用响应式标准 Form | Open |
| TD-OUTBOUND-002 | 支持货物照片多张上传；当前 `cargo_photo` 仅支持单张 Binary 图片 | Open |
| TD-OUTBOUND-003 | 图片区域只显示缩略图，点击图片放大镜后在右侧 panel 显示原图或大图 | Open |
| TD-OUTBOUND-004 | Chatter 在表单布局中始终固定在底部显示 | Open |

## 12. 追溯矩阵

| SRS 范围 | TDD 设计 |
|---|---|
| FR-FORM-01 至 FR-FORM-06 | ORM-OUTBOUND-001 至 005、SVC-OUTBOUND-001 至 004 |
| FR-FORM-08、FR-FORM-09、FR-FORM-15 | 第 6、7、9 节 |
| FR-FORM-20 至 FR-FORM-26 | 第 3、4、5 节 |
| BR-FORM-01 至 BR-FORM-11 | 第 4、5、6 节 |
| AC-01 至 AC-34 | 第 9 节测试设计 |

## 13. Freeze Record

- [x] 字段命名和每项检查控件完成技术评审；
- [x] 两个签名角色和签名持久化方案完成确认；
- [x] PDA 触控布局和设备验收基线完成确认；
- [x] ACL/Record Rule 与角色矩阵完成确认；
- [x] 测试矩阵映射到可执行测试；
- [ ] Coding Contract 创建并批准后，才可进入实施。

本 TDD 已获批准冻结。Coding Contract 仍须在实施前创建并批准。后续实现如需改变字段、状态、入口、权限或人工复核边界，
必须先修订本 TDD 及其下游 Coding Contract。
