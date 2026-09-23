# Outbound Form 软件需求规格说明书（SRS）

> 文档状态：已冻结
> 文档版本：v1.1.0
> 冻结日期：2026-09-23
> 来源基线：[SRS_qooling_forms.md](./SRS_qooling_forms.md)
> 字段证据：[出库表.docx](/Users/lijianqiang/Documents/odoo18_qooling/docs/requirement/出库表.docx)
> 适用 Form：Outbound / 出库表

## 0. 文档边界

本文档只承载 Outbound Form 的业务需求。Web、PDA、手写签名和 Odoo 多语言要求仅在其适用于 Outbound Form 时纳入。

## 1. 业务目标与范围

Outbound Form 用于记录出库装载、货物、ADR、车辆、驾驶员、温度、司机确认和仓库归档证据。

本期包含：

- Outbound Web 和 PDA 录入；
- 保存草稿、提交和仓库主管复核；
- 到达、开始装载和结束装载时间；
- Goods type、MRN、Seal Number 和放行前核查；
- Loading、Cargo、Vehicle、Driver 检查；
- ADR、UN Number、Proper Shipping Name 和平均测量温度；
- 司机/仓库手写签名、备注和货物照片。

## 2. 角色与入口

| 角色/入口 | Outbound 职责 |
|---|---|
| 库管 | 创建、填写和提交 Outbound Form |
| 仓库主管 | 复核 Outbound Form |
| Web | 录入、提交、手写签名和复核 |
| PDA | 录入、提交和手写签名 |

表单通过 `ref_no` 与业务单据关联，由用户选择业务对象和 ID。Location 使用仓库档案；后续可增加 Project 维度。

## 3. 字段和检查清单

| 字段/检查组 | 业务要求 |
|---|---|
| Location | 仓库档案 |
| Date and time arrival | 必填 |
| Supervisor/Manager | 手工选择用户，必填 |
| Reference | 手工录入，无需关联 |
| Start time loading | 必填 |
| End time of loading | 必填；到达时间 ≤ 开始装载时间 ≤ 结束装载时间 |
| Goods type | `Bonded`、`Non-Bonded` |
| MRN Number | 文本，非必填；Goods type 为 `Non-Bonded` 时不显示 |
| Seal Number | 文本，非必填；Goods type 为 `Non-Bonded` 时不显示 |
| MRN checked before release | 放行前核查结果；Goods type 为 `Non-Bonded` 时不显示 |
| ADR | ADR 状态 |
| UN Number | 只允许 `3171`、`3480`、`3481`；ADR 为 `No` 时不显示 |
| Proper Shipping Name | 手工填写；ADR 为 `No` 时不显示 |
| Measured temperature | 用户填写，单位为摄氏度；ADR 为 `No` 时不显示 |
| Loading plan discussed with driver | 不强制为 Yes |
| ADR separation/compatibility | 非 ADR 时不隐藏 |
| Weight distribution | 记录检查结果，人工复核标准 |
| Driver comments | 非必填 |
| Driver signature agreement | 手写签名，非必填；存在时保存签名 |
| Photo of cargo | 非必填，不作为提交阻断条件 |
| Warehouse operator comments | 非必填 |
| Warehouse operator signature | 手写签名，非必填；存在时保存签名 |
| Filled in by / Filing date / Number | 系统用户、系统时间、自动编号 |

检查组：

- Check Loading：明显损坏或包装问题；装载数量已检查；
- Cargo inspection：包装状态；正确标识；货物在卡车上固定；
- Vehicle inspection：ADR 认证证书；灭火器；ADR 标志；货物固定材料；TREM 卡/书面说明；
- Driver check：ADR 驾驶员证书；反光安全背心；护目装置；防护手套；止轮块；帆布；手电筒；铲子；滴水盘；洗眼瓶；两个独立警示三角牌。

## 4. 功能需求

### 4.1 Outbound 生命周期和入口

#### FR-FORM-01 创建表单记录

库管可以创建 Outbound 草稿。

#### FR-FORM-02 记录执行信息

系统记录用户和时间；用户可以修改日期/时间并选择关联业务对象和 ID。

#### FR-FORM-03 保存草稿

草稿可反复修改；保存失败不得显示为成功。

#### FR-FORM-04 提交表单

司机和仓库操作员手写签名均为可选证据；存在签名时保存签名人和签名时间。
仓库主管负责复核。

#### FR-FORM-05 查询历史记录

授权用户可按表单类型、日期、执行人和业务参考查询 Outbound 记录。

#### FR-FORM-06 Web 入口录入和提交

Web 录入、草稿、提交和复核必须使用与 PDA 相同的 Outbound 字段和生命周期。

#### FR-FORM-08 Web/PDA 统一复核

Web 和 PDA 产生的 Outbound 记录进入同一复核流程，字段语义、权限和状态一致。

#### FR-FORM-09 多语言字段和选择值

字段名、帮助文本和选择值按当前 Odoo 用户语言显示单一翻译，不显示三语并列文本。

#### FR-FORM-15 PDA/Web 手写签名

PDA 和 Web 均须支持用户直接绘制手写签名；保存签名图像、签名人和签名时间。

### 4.2 Outbound 专属需求

#### FR-FORM-20 记录出库参考和装载时间

记录 Reference、到达时间、开始装载时间、结束装载时间、MRN 和 Seal Number，并校验时间顺序。

#### FR-FORM-21 检查货物和包装

记录 Check Loading 和 Cargo inspection 的每项结果。

#### FR-FORM-22 检查装载过程

记录装载计划、司机讨论、ADR 分离/兼容性、重量分布、数量和货物固定。

#### FR-FORM-23 记录出库 ADR

记录 ADR、UN Number、Proper Shipping Name、车辆 ADR 证书、灭火器、ADR 标志、TREM 卡和司机 ADR 证书。

#### FR-FORM-24 上传装载照片

允许上传货物照片；照片非必填，不作为提交阻断条件。

#### FR-FORM-25 检查车辆和装载工具

记录 Vehicle inspection 和 Driver check 的完整检查项。

#### FR-FORM-26 记录出库归档信息

记录司机备注、司机手写签名、仓库操作员备注、仓库操作员手写签名、填写人、归档日期和表单编号。

## 5. 业务规则

| 编号 | Outbound 规则 |
|---|---|
| BR-FORM-01 | 已提交 Outbound 必须保留执行人和执行时间 |
| BR-FORM-02 | 草稿可修改；已提交记录撤回到草稿后修改，不保留原始值和更正历史 |
| BR-FORM-03 | ADR 为 Yes 时完成适用危险品检查 |
| BR-FORM-04 | UN Number 只允许 `3171`、`3480`、`3481` |
| BR-FORM-05 | 货物、车辆、驾驶员、固定或温度异常结果不得被记录为全部正常 |
| BR-FORM-07 | Outbound 结果可按类型、日期和执行人追溯 |
| BR-FORM-08 | 货物照片与 Outbound 记录关联 |
| BR-FORM-11 | 业务异常保留原始检查结果、说明和人工处置结果 |

司机和仓库操作员手写签名为非必填证据；其他检查是否阻止提交由人工复核决定，
系统只记录结果。

## 6. 状态与配置

| 状态 | Outbound 含义 |
|---|---|
| 草稿 | 可填写、保存和修改 |
| 已提交 | 已完成提交，等待或完成主管复核 |
| 异常待处理 | 存在人工标记的异常 |
| 已关闭 | 人工确认异常处理完成 |

已提交记录可由授权用户撤回至草稿。司机或仓库操作员缺少手写签名时不阻止保存或提交。

## 7. 验收标准

| 编号 | 验收 |
|---|---|
| AC-01 | 库管创建 Outbound 后生成草稿 |
| AC-02 | 执行人和时间被保存 |
| AC-03 | 草稿保存后重新打开，内容仍存在 |
| AC-04 | 必填字段缺失时不得提交；任一或两套签名缺失不阻止提交 |
| AC-05 | 授权用户可按类型、日期或执行人查询 Outbound |
| AC-08 | Cargo inspection 各项结果均被保存 |
| AC-09 | ADR 出库记录对应车辆、司机和装载检查 |
| AC-10 | 货物照片保存后仍与 Outbound 关联 |
| AC-14 | 无复核权限的用户不能执行复核 |
| AC-15 | 已提交 Outbound 可查看表单类型、执行人和执行时间 |
| AC-17 | Vehicle inspection 和 Driver check 各项均被保存 |
| AC-22 | Reference、到达时间和装载时间被保存并校验顺序 |
| AC-24 | 出库照片、备注、签名和归档信息可查看 |
| AC-27 | Web Outbound 可录入、提交和复核 |
| AC-30 | Web、PDA 的 Outbound 复核字段和状态一致 |
| AC-31 | 用户只看到当前语言的字段名和选择值 |
| AC-33 | PDA/Web 可绘制并保存司机和仓库手写签名 |
| AC-34 | 司机和仓库签名均为可选；签名存在时可查看签名人和签名时间 |

## 8. 已确认的人工复核边界

- 检查项不合格是否阻止出库放行，由人工复核决定；系统只记录检查结果，不自动阻止放行。
- 重量分布的判断标准由人工复核决定；系统只记录用户填写的结果。
- 温度范围和异常阈值由人工复核决定；系统只记录用户填写的温度结果，不自动判断异常。
- 温度控制名称和实际每日记录频率由用户决定；系统不自行统一名称、推导频率或自动改变记录要求。
