# Inbound Form 软件需求规格说明书（SRS）

> 文档状态：已冻结  
> 文档版本：v0.6.0  
> 来源基线：[SRS_qooling_forms.md](./SRS_qooling_forms.md)  
> 字段证据：[货物接收表.docx](/Users/lijianqiang/Documents/odoo18_qooling/docs/requirement/货物接收表.docx)  
> 适用 Form：Inbound / 货物接收表

## 0. 文档边界

本文档只描述 Inbound Form 的字段、填写、提交和记录查看要求。Web、PDF、PDA、手写签名和 Odoo 多语言要求仅在适用于 Inbound Form 时纳入。

本文档不把 Form 记录项扩展为仓库业务流程，不定义自动卸货、自动通知、异常工单、隔离、放行或关闭动作，也不定义 Odoo 模型、数据库结构、XML 视图、ACL、前端组件或 PDF 技术实现。

## 1. Form 目的与使用场景

Inbound Form 用于记录货物接收过程中的基础信息、检查结果、气体和通风信息、温度信息以及相关证据。

本期支持：

- Web、PDF 和 PDA 入口填写 Inbound Form；
- 保存草稿并提交记录；
- 由授权用户查看和复核已提交记录；
- 使用 Odoo 多语言显示字段名、帮助文本和选择值；
- 在 Web 和 PDA 中绘制手写签名；
- 保存照片、备注和归档信息，其中照片和备注非必填。

`Packaging condition` 为 `Not good`、`Unloading permission` 为 `No` 或其他异常值，均作为表单记录结果。用户按照现有仓库作业要求进行后续处理，系统不自动执行处置。

## 2. 角色与录入入口

| 角色/入口 | Inbound Form 能力 |
|---|---|
| 库管 | 创建、填写、保存和提交 Inbound Form |
| 仓库主管 | 查看和复核 Inbound 记录 |
| Web | 填写、保存、提交、查看和复核 |
| PDA | 填写、保存、提交和绘制手写签名 |
| PDF | 填写并提交 Inbound 记录 |

Location 使用仓库档案并必填。表单通过 `ref_no` 记录业务参考，由用户选择业务对象和 ID；后续可增加 Project 维度。

不同录入入口产生的 Inbound 记录应具有一致的字段含义和记录结果。

## 3. 字段定义

### 3.1 基础字段

| 字段 | 类型/选择值 | 必填和说明 |
|---|---|---|
| Location | 仓库档案 | 必填 |
| Date | 日期 | 系统记录，用户可以修改 |
| Supervisor | Odoo 用户 | 必填，用户选择 |
| Goods Status | `Free union goods`、`T1` | 必填 |
| Unloading permission received? | `Yes`、`No, stop unloading and ask project manager` | 必填；系统保存所选结果和选项文本 |
| MRN Number | 文本 | 非必填 |
| Seal Number | 文本 | 非必填；允许多个，以逗号连接 |
| SKAL / BIO Product | `Yes`、`No` | 按表单填写 |
| B/L | 文本 | 非必填 |
| Container Number / Shipment Number | 文本 | 非必填 |
| Number | 系统生成编号 | 自动生成 |
| Filled in by | Odoo 当前用户 | 自动记录 |
| Filing date | 日期 | 记录填写日期 |

### 3.2 检查字段

| 字段 | 类型/选择值 | 必填和说明 |
|---|---|---|
| Checkbox list | 检查明显损坏或包装问题；检查收到的数量；检查产品质量和状况 | 保存用户填写的检查结果 |
| Packaging condition | `Good`、`Not good` | 保存用户选择；`Not good` 时由用户按照现有仓库作业要求处理 |
| Gas measurement | `Yes`、`No`、`Not Applicable` | 保存用户选择 |
| Gas measurement Status | `Safe`、`Ventilation required`、`Dangerous` | 保存用户选择 |
| Ventilated | `Yes`、`Not applicable` | 保存用户选择 |
| Status after ventilation | `Safe`、`Ventilation required`、`Dangerous` | 保存用户选择 |
| ADR | `Yes`、`No` | 保存用户选择 |
| UN Number | `3171`、`3480`、`3481` | ADR 为 `Yes` 时填写 |
| Temperature measured | `Yes`、`No` | ADR 为 `Yes` 时填写 |
| Temperature of each pallet is registered | `Yes`、`No` | ADR 为 `Yes` 时填写 |
| Average temperature per pallet | 摄氏度数值 | 用户录入温度相关信息，不自动判断是否异常 |

### 3.3 证据字段

| 字段 | 类型/选择值 | 必填和说明 |
|---|---|---|
| Photo | 图片 | 非必填，可与表单记录关联 |
| Comments | 文本 | 非必填 |
| Warehouse signature | Web/PDA 手写签名 | 提交必填 |
| Signer | Odoo 用户 | 保存签名人 |
| Signature time | 日期时间 | 保存签名时间 |

字段名、帮助文本和选择值按当前 Odoo 用户语言显示单一翻译，不显示 Qooling 的三语并列文本。

## 4. 表单行为

### 4.1 记录操作

#### FR-INBOUND-01 创建 Inbound 记录

授权库管可以创建 Inbound 草稿。

#### FR-INBOUND-02 填写 Inbound 字段

用户可以填写本 SRS 定义的基础字段、检查字段、温度字段和证据字段。

#### FR-INBOUND-03 保存草稿

用户可以保存草稿并反复修改；保存后的字段值在重新打开记录时保持不变。

#### FR-INBOUND-04 提交记录

用户完成提交所需字段和手写签名后，可以提交 Inbound 记录。提交结果和提交人、提交时间应被保存。

#### FR-INBOUND-05 查看和复核记录

授权用户可以查看已提交的 Inbound 记录。查看记录不自动触发仓库业务动作。

#### FR-INBOUND-06 修改已提交记录

按照已确认的权限，授权用户可以将已提交记录撤回为草稿后修改并重新提交。

#### FR-INBOUND-07 查询记录

授权用户可以按日期、执行人和业务参考查询 Inbound 记录。

### 4.2 录入入口

#### FR-INBOUND-08 Web 录入

Web 可以填写、保存、提交、查看和复核 Inbound 记录。

#### FR-INBOUND-09 PDF 录入

PDF 入口可以填写并提交 Inbound 记录；PDF 中的字段和签名应登记到同一 Inbound 记录。

#### FR-INBOUND-10 PDA 录入

PDA 可以填写、保存和提交 Inbound 记录，并支持直接绘制手写签名。

### 4.3 表单动态行为

#### FR-INBOUND-11 ADR 条件字段

当用户选择 ADR 为 `Yes` 时，显示并填写适用的 UN Number 和温度相关字段；当用户选择 ADR 为 `No` 时，不要求填写这些字段。该行为是表单字段显示和填写行为，不代表系统自动判断危险品检查结果。

#### FR-INBOUND-12 气体和通风结果

用户可以填写 Gas measurement、Gas measurement Status、Ventilated 和 Status after ventilation，系统保存用户选择。

#### FR-INBOUND-13 温度信息

用户可以录入温度测量状态、托盘温度登记状态和每托盘温度相关信息，系统保存用户填写结果，不自动判断温度是否异常。

#### FR-INBOUND-14 手写签名

Web 和 PDA 支持直接绘制手写签名，并保存签名图像、签名人和签名时间。姓名文本、勾选或键盘输入不能替代手写签名。

#### FR-INBOUND-15 多语言显示

字段名、帮助文本和选择值按当前用户语言显示对应翻译；同一界面不显示三语并列文本。

## 5. 业务规则

| 编号 | 规则 |
|---|---|
| BR-INBOUND-01 | 手写签名为提交所需字段；照片和备注非必填 |
| BR-INBOUND-02 | `Packaging condition`、`Unloading permission`、气体、通风和温度等结果由用户填写并由系统保存，系统不自动判断结果或执行后续处置 |

## 6. 记录状态

| 状态 | 含义 |
|---|---|
| 草稿 | 可以填写、保存和修改 |
| 已提交 | 已完成提交，保留提交结果、提交人和提交时间 |

复核是对已提交记录的查看和人工确认，不新增异常状态，不自动生成或关闭异常工作流。

## 7. 验收标准

| 编号 | 验收 |
|---|---|
| AC-INBOUND-01 | 授权库管创建 Inbound 后生成草稿 |
| AC-INBOUND-02 | Inbound 执行人、填写日期和提交信息能够保存并查看 |
| AC-INBOUND-03 | 草稿保存后重新打开，已填写内容仍存在 |
| AC-INBOUND-04 | 缺少提交所需字段或手写签名时不能提交 |
| AC-INBOUND-05 | 授权用户可以按日期、执行人和业务参考查询 Inbound 记录 |
| AC-INBOUND-06 | ADR 为 `Yes` 时可以填写适用的 UN Number 和温度相关字段；ADR 为 `No` 时不要求填写 |
| AC-INBOUND-07 | UN Number 只能使用 `3171`、`3480`、`3481` |
| AC-INBOUND-08 | `Packaging condition` 选择结果能够保存并在查看记录时正确显示 |
| AC-INBOUND-09 | `Unloading permission` 选择结果能够保存并在查看记录时正确显示 |
| AC-INBOUND-10 | 气体、通风和温度字段的用户填写结果能够保存并查看 |
| AC-INBOUND-11 | Web、PDF 和 PDA 入口产生的 Inbound 记录具有一致的字段含义和记录结果 |
| AC-INBOUND-12 | Web 和 PDA 可以绘制并保存手写签名、签名人和签名时间 |
| AC-INBOUND-13 | 用户只看到当前语言的字段名、帮助文本和选择值 |
| AC-INBOUND-14 | 照片和备注为空时，记录仍可以按其他提交条件提交 |
| AC-INBOUND-15 | 已提交记录可以按授权规则撤回为草稿、修改并重新提交 |
| AC-INBOUND-16 | 查看和复核已提交记录不会自动创建、关闭或推进异常业务流程 |

## 8. Open Questions

- Inbound Form 的 Checkbox list 是否需要进一步细化每项的录入控件和选项？
- 温度控制名称和实际每日记录频率如何统一？
- PDF 入口是上传现有 PDF，还是由系统生成 PDF？

## 9. 追溯范围

本 SRS 的需求来源为：

- [货物接收表.docx](/Users/lijianqiang/Documents/odoo18_qooling/docs/requirement/货物接收表.docx) 的字段占位符；
- 已确认的 Inbound 业务问卷回答；
- Qooling Forms 聚合 SRS 中归属于 Inbound Form 的内容。

本 SRS 不定义超出 Inbound Form 记录能力的仓库作业流程。

## 10. 版本记录

| 版本 | 日期 | 变更说明 | 变更人 |
|---|---|---|---|
| v0.1.0 | 2026-09-22 | 从聚合 Forms SRS 拆分 Inbound Form | Agent |
| v0.2.0 | 2026-09-22 | 补充 Packaging condition、Web/PDF/PDA、签名和图片非强制要求 | Agent |
| v0.3.0 | 2026-09-22 | 确认 Gas measurement 选项为 Yes、No、Not Applicable | Agent |
| v0.4.0 | 2026-09-22 | 明确温度和异常提交属于人工决策边界 | Agent |
| v0.5.0 | 2026-09-22 | 按 Form 记录工具定位收缩业务范围，移除自动处置和异常工作流，重编号并区分字段、表单行为和业务规则 | Agent |
| v0.6.0 | 2026-09-22 | 删除重复动态行为规则、无字段的复核结果要求和表单类型查询；移除提交后修改的历史语义，并明确 PDF 入口业务问题 | Agent |
