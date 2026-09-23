# Temperature Record Coding Contract

> 文档状态：草稿
> 文档版本：v0.1.0
> 实施状态：尚未授权
> 上游 SRS：[SRS_qooling_weekly_temperature_control.md](../designing/SRS_qooling_weekly_temperature_control.md) `v0.2.0 Draft`
> 上游 TDD：[TDD_qooling_temperature_record.md](../designing/TDD_qooling_temperature_record.md) `v1.0.0 Frozen`
> 适用 Form：Weekly Temperature Control / Temperature Record

## 0. 文档治理

本 Coding Contract（CC）冻结 Temperature Record 的实施范围、保存边界、
禁止事项、测试契约、停止条件和完成闸门，不重新定义上游 SRS/TDD 的业务语义。

在 CC 获得人工批准前，不得开始 Temperature Record 编码、数据库迁移或 UI
实现。任何字段、状态、入口、权限或人工复核边界变化，必须先修订冻结 TDD
及本 CC。

## 1. 实施目标

在 Odoo 18 中实现温度记录工具，支持：

- Web、PDA 和按 SRS 登记边界处理 PDF；
- 草稿保存、提交、查询和仓库主管人工复核；
- 客户、集装箱、日期、经理和归档字段；
- 动态托盘温度明细；
- Enter 快速录入并自动生成连续 `pallet1`、`pallet2`、`pallet3` 编号；
- 修改已有托盘温度；
- 明确确认后清空全部托盘明细并从 `pallet1` 重新采集；
- 损坏、泄漏、存储稳定性、温度异常和人工处置结果记录；
- 手写签名、照片、备注和 PDF 原件/处理结果保存。

## 2. 范围冻结

### 2.1 In Scope

- `wd.qooling.temperature.record` 主模型；
- `wd.qooling.temperature.record.line` 动态托盘明细模型；
- `TMP/00001` 序列；
- `draft`、`submitted`、`exception_pending`、`closed` 状态；
- `group_temperature_user` 和 `group_temperature_supervisor` 权限组；
- Web/PDA 共用字段、状态和 ORM 提交规则；
- 快速温度输入框的 Enter 新增、清空和回焦；
- 连续只读托盘编号；
- 草稿中修改温度但禁止单行删除；
- 二次确认的“清空全部托盘温度”操作；
- PDF 原始附件、导入状态和失败原因记录；
- ORM、视图、权限、HTTP、Playwright 和 PDF 登记测试。

### 2.2 Out of Scope

- 固定 `pallet_01` 至 `pallet_65` 字段或固定 65 行控件；
- 预生成 65 条空托盘记录；
- 自动截断、自动补齐或自动拆分实际托盘；
- 自动判断温度范围、`40°C` 阈值或异常；
- 自动隔离、复测、通知、放行、库存、运输或仓库业务流程；
- 自动启动程序 51/52 或判断程序已完成；
- 专用 PDA JavaScript、图片多张上传、缩略图放大 panel、Chatter 置底；
- 其他 Form 的模型、字段或流程；
- 修改 Odoo 官方代码、裸 SQL、独立数据库或外部服务。

## 3. 必需行为契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-TEMP-CHANGE-001` | 创建温度记录草稿 | 保存基础上下文和系统归档字段 |
| `CC-TEMP-CHANGE-002` | 动态增加托盘 | 每个实际托盘对应一条 One2many 明细 |
| `CC-TEMP-CHANGE-003` | 快速输入温度 | Enter 创建一条明细，清空并重新聚焦输入框 |
| `CC-TEMP-CHANGE-004` | 连续托盘编号 | 依次生成 `pallet1`、`pallet2`、`pallet3`，编号只读 |
| `CC-TEMP-CHANGE-005` | 修改温度 | 草稿中可修改已有托盘温度和结果字段 |
| `CC-TEMP-CHANGE-006` | 禁止单行删除 | 草稿中的已有托盘明细不能单独删除 |
| `CC-TEMP-CHANGE-007` | 清空全部明细 | 二次确认后删除全部明细，下一次采集从 `pallet1` 开始 |
| `CC-TEMP-CHANGE-008` | 提交 | 基础必填字段和签名满足后进入 `submitted` |
| `CC-TEMP-CHANGE-009` | 人工复核状态 | 主管可标记异常、关闭和撤回 |
| `CC-TEMP-CHANGE-010` | PDF 登记 | 原始 PDF、处理状态和失败原因可追溯 |

## 4. 必须保留的边界

| ID | 保留边界 |
|---|---|
| `CC-TEMP-PRESERVE-001` | 温度、阈值、异常、复测和处置结果由人工复核决定 |
| `CC-TEMP-PRESERVE-002` | 系统只保存人工判断和处置结果，不将其作为自动触发器 |
| `CC-TEMP-PRESERVE-003` | 图片和备注非必填，不阻止草稿或提交 |
| `CC-TEMP-PRESERVE-004` | 检查字段空值表示未填写，不等价于 `no` |
| `CC-TEMP-PRESERVE-005` | 程序 51/52 只作为人工处置参考，不自动启动 |
| `CC-TEMP-PRESERVE-006` | “Weekly Temperature Control”名称和每日频率由用户决定 |

## 5. 数据和错误契约

- 所有记录必须通过 Odoo ORM 保存和读取；
- `customer`、`container_number`、`manager_id` 和签名在提交时必填；
- 温度明细必须保存原始摄氏度值和人工结果；
- `total_pallets` 只保存用户填写值，不驱动明细创建、删除或数量限制；
- 快速输入为空或非数字时显示明确错误，不创建空明细；
- 单行删除请求必须被 ORM 拒绝，不能只隐藏前端按钮；
- 清空全部动作必须通过显式服务方法执行，并要求 UI 二次确认；
- 清空取消时不得修改任何已有明细；
- PDF 失败时写入 `pdf_import_status=failed` 和 `pdf_import_error`；
- 不允许静默吞错、成功形状回退或伪造提交成功。

## 6. 权限和状态契约

| 操作 | `group_temperature_user` | `group_temperature_supervisor` |
|---|---:|---:|
| 创建/读取/修改草稿 | 是 | 是 |
| 快速增加温度明细 | 是 | 是 |
| 修改草稿温度 | 是 | 是 |
| 清空全部托盘明细 | 是 | 是 |
| 提交 | 是 | 是 |
| 标记异常/关闭 | 否 | 是 |
| 撤回 | 否 | 是 |

状态流转必须为：

```text
draft -> submitted -> exception_pending -> closed
  ^          |              |              |
  +----------+--------------+--------------+
              supervisor reset to draft
```

撤回不删除字段值；已提交记录必须由主管撤回为草稿后才能修改。

## 7. 测试契约

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-TEMP-TEST-001` | 创建、保存、重读草稿 | ORM | 字段值完整保持 |
| `CC-TEMP-TEST-002` | 必填字段和签名 | ORM | 缺失时拒绝提交 |
| `CC-TEMP-TEST-003` | 动态 1、2 和多个托盘 | ORM | 明细数量等于实际录入数量 |
| `CC-TEMP-TEST-004` | 超过 65 个托盘 | ORM | 不截断、不补齐、不生成固定字段 |
| `CC-TEMP-TEST-005` | Enter 快速录入 | Playwright | 创建明细、清空并回焦 |
| `CC-TEMP-TEST-006` | 连续编号 | ORM/UI | `pallet1`、`pallet2`、`pallet3` 且只读 |
| `CC-TEMP-TEST-007` | 编辑和删除边界 | ORM/UI | 可改温度，单行删除被拒绝 |
| `CC-TEMP-TEST-008` | 清空全部 | Playwright/ORM | 确认后清空，取消不变，下一行是 `pallet1` |
| `CC-TEMP-TEST-009` | 人工异常状态 | ORM/HTTP | 仅主管可操作 |
| `CC-TEMP-TEST-010` | 结果只保存 | ORM | 不创建自动业务流程 |
| `CC-TEMP-TEST-011` | PDF 失败 | PDF/ORM | 原件和失败原因可追溯 |
| `CC-TEMP-TEST-012` | 未授权访问 | ORM/HTTP | 提交、复核、关闭和撤回被拒绝 |
| `CC-TEMP-TEST-013` | 温度类型错误 | View/HTTP | 非数字输入返回真实错误 |
| `CC-TEMP-TEST-014` | 上传失败 | View/HTTP | 表单状态不被伪造为成功 |

自动化测试 PASS 不得替代 PDA、签名和人工复核 HVR。

## 8. 实施停止条件

遇到以下任一情况必须停止并请求变更批准：

1. 需要固定 65 个托盘字段或 65 行控件；
2. 需要自动判断温度、阈值、异常、隔离或复测；
3. 需要自动拆分、补齐或删除原始托盘数据；
4. 需要自动启动程序 51/52；
5. 需要新增 TDD 未定义的字段、状态、接口或依赖；
6. 需要引入库存、运输、放行、通知或其他仓库业务流程；
7. 无法在 ORM 层表达单行删除禁令或清空确认边界；
8. 测试只能通过伪造成功、静默吞错或跳过权限验证。

## 9. 完成闸门

- [ ] SRS/TDD/CC 追溯矩阵完整；
- [ ] ORM、视图、安全和前端资源通过针对性测试；
- [ ] 动态托盘、Enter 录入和连续编号通过测试；
- [ ] 单行删除禁令、温度修改和清空全部动作通过测试；
- [ ] PDF 原件、失败状态和失败原因可追溯；
- [ ] Web/PDA 字段和状态一致；
- [ ] 人工复核边界无自动业务处置；
- [ ] IHR、ATR、HVR 和 Final Report 更新；
- [ ] 用户批准本 CC 后，才可授权实施。
