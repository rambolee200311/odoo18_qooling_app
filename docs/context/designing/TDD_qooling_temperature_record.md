# Temperature Record 技术设计文档（TDD）

> 文档状态：已修订，待重新冻结
> 文档版本：v1.1.0
> 上一冻结版本：v1.0.0（2026-09-23）
> 适用 Form：Weekly Temperature Control / Temperature Record  
> 依据：[SRS_qooling_weekly_temperature_control.md](./SRS_qooling_weekly_temperature_control.md)

## 1. 设计目标与边界

本 TDD 将温度控制表设计为“温度记录工具”，只保存用户填写的上下文、
托盘明细、检查结果、照片、备注、签名和人工处置结果。

系统不得自动执行温度异常判定、隔离、复测、通知、放行、库存或其他仓库
业务动作。系统可以保存用户填写的人工判断结果和处置结果，但不将其作为
自动化触发器。温度范围、`40°C` 阈值、测量次数、复测和处置均由人工复核决定。

## 2. 入口和运行模式

| 入口 | 设计 |
|---|---|
| Web | 标准 Odoo Web 表单，支持草稿、提交、查询、复核 |
| PDA | 与 Web 使用同一 ORM 和生命周期；当前先提供响应式表单，专用触控 UI 作为技术债 |

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

#### 3.1.1 检查字段选项集

四个检查字段统一使用二态 Selection；默认值为空，表示尚未填写，不将空值
解释为 `no`：

| 字段 | Selection 值 | 默认值 | 业务分支 |
|---|---|---|---|
| `packaging_damage` | `[('yes', 'Ja'), ('no', 'Nee')]` | 空 | `yes` 时记录程序 51/52 的人工处置说明 |
| `unpacked_housing_damage` | `[('yes', 'Ja'), ('no', 'Nee')]` | 空 | `yes` 时记录程序 51/52 的人工处置说明 |
| `electrolyte_leakage` | `[('yes', 'Ja'), ('no', 'Nee')]` | 空 | `yes` 时记录泄漏处置结果 |
| `storage_stability` | `[('yes', 'Ja'), ('no', 'Nee')]` | 空 | `yes` 时记录存储稳定性处置结果 |

程序 51/52 只是用户填写的人工处置参考或文本结果，不由系统自动启动、
通知或判定完成。若业务确认需要第三种答案，必须先修订本选项集和 SRS。

### 3.2 托盘温度明细

模型：`wd.qooling.temperature.record.line`

| 字段 | Odoo 类型 | 约束/说明 |
|---|---|---|
| `record_id` | Many2one | 必填，级联归属温度记录 |
| `sequence` | Integer | 用于用户排序，不表示固定托盘编号上限 |
| `pallet_reference` | Char | 系统连续生成的托盘标识，如 `pallet1`、`pallet2`；只读 |
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

正向实现：托盘明细通过 One2many 列表动态增删。用户点击“新增一行”创建
一条 `wd.qooling.temperature.record.line`；明细数量由用户实际填写决定，
不设上限。系统按当前记录内的录入顺序连续生成 `pallet1`、`pallet2`、
`pallet3` 等标识，用户不可手动修改编号。`total_pallets` 仅作为记录值，
不驱动明细生成或删除。

草稿中已存在的托盘明细不允许用户单独删除，但允许修改该托盘的温度、
测量结果、异常说明和人工处置结果。表单提供“清空全部托盘温度”操作；
用户二次确认后，系统一次性删除当前记录的全部托盘明细，下一次采集从
`pallet1` 重新开始。已提交记录必须先由主管撤回为草稿后才能修改。

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
| ORM-TEMP-010 | 草稿中的托盘明细不允许单独删除；允许修改温度；清空必须通过带确认的整批动作 |

## 5. 视图设计

### 5.1 基础区

显示日期、Manager、Customer、Container Number、Location、Filled in by、
Filing date、Number 和 Total Pallets。

### 5.2 托盘明细区

使用 One2many 可编辑列表和移动端可操作的明细表单，提供“新增一行”，
而不是固定 65 个输入框。明细至少显示托盘标识、温度、测量结果、异常说明
和人工处置结果。

#### 5.2.1 快速温度录入框

提供一个独立的“快速录入温度”输入框，作为连续录入托盘温度的主要入口：

1. 用户输入一个摄氏度数值；
2. 用户按 `Enter`；
3. 系统校验输入是有效数字；
4. 系统立即创建一条 `wd.qooling.temperature.record.line`，写入温度、
   当前序号、连续托盘标识（`pallet1`、`pallet2`……）和当前温度记录；
5. 输入框清空并重新获得焦点，等待下一条温度；
6. 明细列表即时显示新记录，并允许用户补录检查结果和处置说明；托盘编号
   由系统生成且不可编辑。

明细行不提供单行删除按钮。清空操作必须是显式的表单动作并要求二次确认；
取消确认不得改变任何已有温度明细。

快速录入框只负责新增一条原始温度明细，不自动判断温度是否异常、不自动
触发程序 51/52、不自动创建处置流程。输入为空或不是有效数字时，系统显示
明确错误且不创建空明细。按 `Enter` 不得生成固定数量的空行，也不得受 65
行模板限制。

PDA 上点击“新增一行”打开底部抽屉或全屏明细页面；保存后返回记录并保留
明细列表位置。温度字段使用数字输入控件，以便调用 PDA 数字键盘。若标准
Odoo Form 无法稳定满足该交互，必须先登记专用 PDA UI 技术债，不得用固定
65 行替代动态明细。

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

### 6.1 权限组

| 权限组 | 权限 |
|---|---|
| `group_temperature_user` | 创建、读取、修改草稿、保存和提交本人有权访问的记录 |
| `group_temperature_supervisor` | 包含 `group_temperature_user`；可复核、标记异常、关闭和撤回 |

两个组均为本模块新增组；不替换、不修改 Odoo 官方仓库权限组。实际用户
可同时加入现有仓库操作组和上述温度记录组，仓库主管额外加入
`group_temperature_supervisor`。

### 6.2 状态流转

| 动作 | 起始状态 | 目标状态 | 触发角色 | 是否记录审计时间/用户 |
|---|---|---|---|---|
| 保存草稿 | `draft` | `draft` | `group_temperature_user` | 否 |
| 提交 | `draft` | `submitted` | `group_temperature_user` | 是，写入 `submitted_by_id`/`submitted_at` |
| 标记异常 | `submitted` | `exception_pending` | `group_temperature_supervisor` | 是，写入消息/操作日志 |
| 关闭 | `exception_pending` | `closed` | `group_temperature_supervisor` | 是，写入消息/操作日志 |
| 撤回 | `submitted`、`exception_pending`、`closed` | `draft` | `group_temperature_supervisor` | 是，写入消息/操作日志 |

撤回不删除原字段值；是否允许修改由回到 `draft` 后的普通编辑权限决定。

## 7. 测试设计

| 测试 ID | 类型 | 覆盖 |
|---|---|---|
| `TEST-TEMP-001` | TransactionCase | 创建、保存和重新读取草稿 |
| `TEST-TEMP-002` | TransactionCase | 客户、集装箱、经理和签名提交约束 |
| `TEST-TEMP-003` | TransactionCase | 动态创建 1、2 和多个托盘明细 |
| `TEST-TEMP-004` | TransactionCase | 记录超过 65 个托盘时不截断、不补齐、不创建固定字段；用户可明确拆分 |
| `TEST-TEMP-003A` | View/HTTP/Playwright | 温度输入框按 Enter 创建一条明细并清空、回焦 |
| `TEST-TEMP-003B` | TransactionCase/Playwright | 连续生成 `pallet1`、`pallet2`、`pallet3`，编号只读 |
| `TEST-TEMP-003C` | TransactionCase/Playwright | 草稿不可单独删除已有明细，但可修改温度 |
| `TEST-TEMP-003D` | TransactionCase/Playwright | 确认清空全部明细后重新从 `pallet1` 采集；取消不改变记录 |
| `TEST-TEMP-005` | TransactionCase | 温度和异常结果只保存，不触发业务流程 |
| `TEST-TEMP-006` | TransactionCase | 人工异常状态和权限 |
| `TEST-TEMP-007` | View/HTTP | Web 表单字段、One2many 明细和状态按钮 |
| `TEST-TEMP-008` | Playwright | Web/PDA 明细新增、编辑、滚动和签名 |
| `TEST-TEMP-009` | Playwright | 多语言字段和选择值 |
| `TEST-TEMP-010` | TransactionCase | 无权限用户提交、复核、关闭和撤回被拒绝 |
| `TEST-TEMP-011` | TransactionCase | 缺少客户、集装箱号或签名时提交被拒绝 |
| `TEST-TEMP-012` | View/HTTP | 温度字段拒绝非数字输入并返回明确错误 |
| `TEST-TEMP-013` | View/HTTP | 图片上传失败时保留表单状态并显示真实错误 |

测试不得以“显示 65 行”作为通过条件；必须验证实际明细数量和原始值完整性。

## 8. 技术债和停止条件

- 专用 PDA 触控 JavaScript、图片多张上传、缩略图放大 panel 和 Chatter
  置底按既有技术债跟踪，不在本 TDD 中伪装为已完成；对应已登记编号为
  `TD-TEMP-001`（真实 PDA 触控交互）、`TD-INBOUND-002`、
  `TD-INBOUND-003` 和 `TD-INBOUND-004`。多语言字段和选择值验证另由
  `TD-TEMP-002` 跟踪。这些能力在本 TDD 中不实现，但模型和视图必须保留扩展点。
- 若实现需要自动判断温度、自动拆分记录、自动补齐托盘或固定 65 行，
  必须停止并先修订 SRS/TDD。
- 若引入库存、运输、隔离、放行或通知流程，必须停止并重新评审范围。

## 9. 冻结闸门

- [x] 托盘明细 One2many 方案经人工确认；
- [x] 快速温度录入框的 Enter 新增、清空和回焦交互经人工确认；
- [x] 托盘连续编号格式、起始值和只读行为经人工确认；
- [x] 单行不可删除、温度可修改、全部清空需二次确认的行为经人工确认；
- [x] 不固定 65 行、不截断超过 65 个实际托盘已确认；
- [x] Web/PDA 入口边界经人工确认；
- [x] 权限、签名和状态矩阵经人工确认；
- [x] 检查字段选项集、权限组和状态流转经业务确认；
- [ ] Coding Contract 创建并批准后，才可进入实施。
