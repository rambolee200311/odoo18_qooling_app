# Temperature Record 技术设计文档（TDD）

> 文档状态：草稿  
> 文档版本：v0.1.0  
> 适用 Form：Weekly Temperature Control / Temperature Record  
> 依据：[SRS_qooling_weekly_temperature_control.md](./SRS_qooling_weekly_temperature_control.md)

## 1. 设计目标与边界

本 TDD 将温度控制表设计为“温度记录工具”，只保存用户填写的上下文、
托盘明细、检查结果、照片、备注、签名和人工处置结果。

系统不得自动判断温度是否异常，不得自动触发隔离、复测、通知、放行、
库存或其他仓库业务流程。温度范围、`40°C` 阈值、测量次数、复测和处置
均由人工复核决定，系统只保存结果。

## 2. 入口和运行模式

| 入口 | 设计 |
|---|---|
| Web | 标准 Odoo Web 表单，支持草稿、提交、查询、复核 |
| PDA | 与 Web 使用同一 ORM 和生命周期；当前先提供响应式表单，专用触控 UI 作为技术债 |
| PDF | 按 SRS 保留原始文件并登记字段、签名和处理结果；不得绕过 ORM 创建业务结论 |

“Weekly Temperature Control”名称和实际每日记录频率由用户决定。本 TDD
不创建提醒、定时任务或自动频率推导。

## 3. 核心数据模型

### 3.1 温度记录

模型：`wd.qooling.temperature.record`

| 字段 | Odoo 类型 | 约束/说明 |
|---|---|---|
| `name` | Char | 系统序列号，格式 `TMP/00001` |
| `state` | Selection | `draft`、`submitted`、`exception_pending`、`closed` |
| `date` | Datetime | 用户可修改的记录日期/时间 |
| `manager_id` | Many2one(`res.users`) | 必填 |
| `customer` | Char | 必填 |
| `container_number` | Char | 必填 |
| `location_id` | Many2one(`stock.warehouse`) | 适用地点 |
| `total_pallets` | Integer | 保存用户填写的实际托盘数量，不作为固定行数上限 |
| `pallet_line_ids` | One2many | 动态托盘温度明细 |
| `packaging_damage` | Selection | 保存包装损坏检查结果 |
| `unpacked_housing_damage` | Selection | 独立保存未包装产品壳体损坏结果 |
| `electrolyte_leakage` | Selection | 保存电解液泄漏结果 |
| `storage_stability` | Selection | 保存存储稳定性结果 |
| `temperature_exception_result` | Text/Selection | 保存用户填写的温度异常结果 |
| `disposition_result` | Text | 保存人工复核处置结果 |
| `photo_ids` | One2many | 当前可先映射附件；多图上传为技术债 |
| `comments` | Text | 非必填 |
| `signature` | Binary | 手写签名，提交必填 |
| `signer_id` | Many2one(`res.users`) | 签名人 |
| `signature_time` | Datetime | 签名时间 |
| `filled_in_by_id` | Many2one(`res.users`) | 默认当前用户 |
| `filing_date` | Date | 默认当前日期 |
| `submitted_by_id` | Many2one(`res.users`) | 提交人 |
| `submitted_at` | Datetime | 提交时间 |

### 3.2 托盘温度明细

模型：`wd.qooling.temperature.record.line`

| 字段 | Odoo 类型 | 约束/说明 |
|---|---|---|
| `record_id` | Many2one | 必填，级联归属温度记录 |
| `sequence` | Integer | 用于用户排序，不表示固定托盘编号上限 |
| `pallet_reference` | Char | 用户填写或扫描的托盘标识 |
| `temperature` | Float | 摄氏度原始读数 |
| `measurement_result` | Text/Selection | 保存用户或人工复核结果 |
| `exception_result` | Text | 保存该托盘的异常事实或说明 |
| `disposition_result` | Text | 保存人工处置结果 |

### 3.3 明确禁止的 65 托盘实现

- 不创建 `pallet_01` 至 `pallet_65` 等固定字段。
- 不创建 65 个固定表单区块或 65 个固定输入控件。
- 不因为模板展开到 `Pallet 65` 就预生成 65 条空明细。
- 用户实际有多少托盘，就创建多少条 `pallet_line_ids` 明细。
- 超过模板原有 65 行时，不丢弃、不截断、不自动伪造数据；明细模型本身不设
  65 行上限。
- 若按 SRS 的业务规则需要拆分超过 65 个托盘，必须由用户明确创建另一条温度
  记录并填写关联说明；系统不得偷偷拆分或改变原始记录。

`Total Pallets` 只作为记录值和核对信息保存；系统不得用它自动补齐、
删除或生成托盘明细。

## 4. ORM 约束和服务行为

| 编号 | 约束/行为 |
|---|---|
| ORM-TEMP-001 | `customer`、`container_number`、`manager_id` 和签名在提交时必填 |
| ORM-TEMP-002 | 草稿可保存、修改和重新读取 |
| ORM-TEMP-003 | 提交后保存提交人和提交时间 |
| ORM-TEMP-004 | 每个实际托盘使用独立 One2many 明细保存 |
| ORM-TEMP-005 | `total_pallets` 不驱动固定数量明细，也不限制明细数量 |
| ORM-TEMP-006 | 温度、损坏、泄漏和稳定性结果只保存，不自动判断 |
| ORM-TEMP-007 | 系统不自动创建隔离、复测、通知、放行或库存动作 |
| ORM-TEMP-008 | 照片和备注为空不得阻止草稿或提交 |
| ORM-TEMP-009 | 无复核权限的用户不能执行人工状态变更 |

## 5. 视图设计

### 5.1 基础区

显示日期、Manager、Customer、Container Number、Location、Filled in by、
Filing date、Number 和 Total Pallets。

### 5.2 托盘明细区

使用 One2many 可编辑列表和移动端可操作的明细表单，提供“新增一行”，
而不是固定 65 个输入框。明细至少显示托盘标识、温度、测量结果、异常说明
和人工处置结果。

### 5.3 检查与证据区

检查结果、人工处置、照片、备注和签名分开显示。照片为空不显示成功形态
的占位结果；签名图像、签名人和签名时间必须可重新查看。

## 6. 状态和权限

| 状态 | 含义 |
|---|---|
| `draft` | 可填写、保存和修改 |
| `submitted` | 已完成提交，等待或完成主管复核 |
| `exception_pending` | 人工标记需要后续处理 |
| `closed` | 人工确认处理完成 |

库管可以创建和填写记录；仓库主管可以复核、标记异常、关闭或撤回。
Record Rule 和 ACL 必须在服务端生效，不能只隐藏按钮。

## 7. PDF 登记边界

PDF 入口只负责登记原始文件、解析/人工录入的字段、签名和提交结果。
原始 PDF 必须保留为附件；缺少必填字段或签名时记录失败原因，不能将失败
文件标记为已提交。PDF 不得绕过 `wd.qooling.temperature.record` 和明细模型。

## 8. 测试设计

| 测试 ID | 类型 | 覆盖 |
|---|---|---|
| `TEST-TEMP-001` | TransactionCase | 创建、保存和重新读取草稿 |
| `TEST-TEMP-002` | TransactionCase | 客户、集装箱、经理和签名提交约束 |
| `TEST-TEMP-003` | TransactionCase | 动态创建 1、2 和多个托盘明细 |
| `TEST-TEMP-004` | TransactionCase | 记录超过 65 个托盘时不截断、不补齐、不创建固定字段；用户可明确拆分 |
| `TEST-TEMP-005` | TransactionCase | 温度和异常结果只保存，不触发业务流程 |
| `TEST-TEMP-006` | TransactionCase | 人工异常状态和权限 |
| `TEST-TEMP-007` | View/HTTP | Web 表单字段、One2many 明细和状态按钮 |
| `TEST-TEMP-008` | Playwright | Web/PDA 明细新增、编辑、滚动和签名 |
| `TEST-TEMP-009` | Playwright | 多语言字段和选择值 |
| `TEST-TEMP-010` | PDF/TransactionCase | 原始 PDF、字段、签名和失败原因可追溯 |

测试不得以“显示 65 行”作为通过条件；必须验证实际明细数量和原始值完整性。

## 9. 技术债和停止条件

- 专用 PDA 触控 JavaScript、图片多张上传、缩略图放大 panel 和 Chatter
  置底按现有 Form 技术债跟踪，不在本 TDD 中伪装为已完成。
- 若实现需要自动判断温度、自动拆分记录、自动补齐托盘或固定 65 行，
  必须停止并先修订 SRS/TDD。
- 若引入库存、运输、隔离、放行或通知流程，必须停止并重新评审范围。

## 10. 草稿冻结闸门

- [ ] 托盘明细 One2many 方案经人工确认；
- [ ] 不固定 65 行、不截断超过 65 个实际托盘已确认；
- [ ] Web/PDA/PDF 入口边界经人工确认；
- [ ] 权限、签名和状态矩阵经人工确认；
- [ ] Coding Contract 创建并批准后，才可进入实施。
