# Outbound PDA Coding Contract

> 文档状态：Frozen
> 文档版本：v1.0.0
> 起草日期：2026-09-23
> 冻结日期：2026-09-23
> 实施状态：Authorized
> Intent ID：`INTENT-OUTBOUND-PDA`
> 技术债：`TD-OUTBOUND-PDA-001`
> 模块：`wd_qooling_app`
> 上游 SRS：[SRS_qooling_outbound_form.md](../designing/SRS_qooling_outbound_form.md)
> 上游 TDD：[TDD_qooling_outbound_form.md](../designing/TDD_qooling_outbound_form.md)
> 上游 CC：[Coding_Contract_Outbound_Form.md](./Coding_Contract_Outbound_Form.md)

## 0. 文档治理

本 Coding Contract（CC）只定义 Outbound Form 的 PDA 触控入口、货物图片证据
和司机/仓库操作员手写签名行为。本 CC 不重新定义 Outbound 的字段、状态、
权限、提交规则或人工复核边界；这些内容继续以冻结的 Outbound SRS、TDD 和
Outbound Form CC 为准。

本 CC 已获用户批准冻结，并已获得实施授权。冻结只固定实施边界；代码实现和验证
仍必须以本 CC、上游 SRS/TDD 及服务端 ORM 结果为准。

## 1. 目标

在 `FORMS / PDA / Outbound Record` 下提供适合窄屏触控设备的 Outbound 录入入口。
PDA 创建或修改的记录必须使用既有 `wd.qooling.outbound.form` ORM，并与 Web
表单共享字段语义、权限、生命周期和提交结果。

PDA 必须支持：

- 逐步填写 Outbound 字段和检查项；
- 保存可恢复的草稿；
- 上传和查看货物图片；
- 司机手写签名；
- 仓库操作员手写签名；
- 提交 Outbound 时司机和仓库操作员签名均为可选证据；签名存在时写入对应审计字段。

## 2. 范围冻结（草案）

### 2.1 In Scope

- Dashboard `FORMS / PDA / Outbound Record` 入口；
- Outbound PDA 专用 Owl/JavaScript 页面和窄屏触控样式；
- 分步或分区录入基础信息、装载时间、货物、ADR、车辆、司机和检查项；
- PDA 草稿创建、保存、恢复、错误反馈和提交；
- 货物图片上传、缩略图展示、单张放大预览和单张删除；
- 图片与当前 Outbound 记录的 ORM 关联；
- 司机签名和仓库操作员签名的独立触控画布；
- 签名清除、保存、恢复和 Web 端可见性；
- 司机签名人与签名时间、仓库签名人与签名时间的既有字段写入；
- 稳定的 `data-testid` 选择器，用于 PDA 自动化验证；
- Web/PDA 字段、状态、权限和提交结果一致；
- 直接相关的 ORM、ACL、ATR、HVR 和技术债追溯文档。

### 2.2 Out of Scope

- 新增独立 Outbound PDA ORM 模型；
- 复制或改写 `wd.qooling.outbound.form` 的业务字段和状态；
- PDF 上传、PDF 解析、PDF 生成或 PDF 归档；
- 条码扫描、离线缓存、断网同步或设备原生 API；
- 自动创建库存移动、运输、采购、销售、放行、隔离、通知或异常工单；
- 根据检查项、ADR、重量或温度结果自动阻止出库；
- 自动判断照片是否合格或自动判断签名是否代表业务批准；
- 修改 Odoo 官方代码；
- 修改既有 Inbound PDA、Temperature Record 或 Web Outbound 的业务语义。

## 3. PDA 页面契约（草案）

页面可以按实现需要调整步骤名称，但不得改变字段和证据语义。建议至少包含：

| 步骤 | 内容 |
|---|---|
| Details | Location、到达时间、Supervisor、Reference、Goods type、MRN、Seal 和装载时间 |
| Checks | Loading、Cargo、Vehicle、Driver 检查项 |
| ADR & temperature | ADR、UN Number、Proper Shipping Name 和 measured temperature |
| Evidence | Cargo photos、Driver comments、Warehouse operator comments |
| Driver signature | 司机手写签名、清除、保存和恢复 |
| Warehouse signature | 仓库操作员手写签名、清除、保存、恢复和提交 |

步骤导航必须提供当前进度、上一页和下一页。Submit 只在最终签名步骤提供，
并且仍必须调用服务端 Outbound 提交校验。

## 4. 图片证据契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-OUTBOUND-PDA-IMAGE-001` | 上传 | 允许选择一张或多张货物图片并关联当前 Outbound 记录 |
| `CC-OUTBOUND-PDA-IMAGE-002` | 缩略图 | 每张已上传图片独立显示缩略图 |
| `CC-OUTBOUND-PDA-IMAGE-003` | 放大 | 每张图片可在 popup 中查看大图，不使用右侧固定 panel |
| `CC-OUTBOUND-PDA-IMAGE-004` | 删除 | 用户可删除单张图片，其他图片和记录保持不变 |
| `CC-OUTBOUND-PDA-IMAGE-005` | 非必填 | 没有图片不得阻止草稿保存或提交 |
| `CC-OUTBOUND-PDA-IMAGE-006` | 持久化 | 保存草稿、重新进入 PDA 或打开 Web 表单后图片仍可查看 |
| `CC-OUTBOUND-PDA-IMAGE-007` | 错误 | 上传、删除或加载失败必须显示真实错误，不得显示成功 |

图片只作为 Outbound 记录证据保存，不触发库存、放行、运输或异常动作。

## 5. 签名契约

Outbound PDA 必须提供两个相互独立的手写签名：

1. Driver signature；
2. Warehouse operator signature。

| ID | 行为 | 预期 |
|---|---|---|
| `CC-OUTBOUND-PDA-SIGN-001` | 司机绘制 | 触控笔或手指可连续绘制多笔司机签名 |
| `CC-OUTBOUND-PDA-SIGN-002` | 仓库绘制 | 触控笔或手指可连续绘制多笔仓库签名 |
| `CC-OUTBOUND-PDA-SIGN-003` | 清除 | 只清除当前签名，不影响另一方签名 |
| `CC-OUTBOUND-PDA-SIGN-004` | 保存 | 签名图像、签名人和签名时间写入既有 Outbound 字段 |
| `CC-OUTBOUND-PDA-SIGN-005` | 恢复 | 保存后返回 PDA 或打开 Web 表单，签名仍可见 |
| `CC-OUTBOUND-PDA-SIGN-006` | 提交 | 司机和仓库签名均为可选；签名存在时必须保存对应签名人和签名时间 |
| `CC-OUTBOUND-PDA-SIGN-007` | 独立性 | 司机签名不得写入仓库签名字段，反之亦然 |
| `CC-OUTBOUND-PDA-SIGN-008` | 错误 | 签名保存或恢复失败必须显示真实错误，不得伪造成功 |

签名表示用户完成了记录确认；签名不能被解释为自动放行、质量批准或库存操作。

## 6. 必须保留的行为

| ID | 必须保留 |
|---|---|
| `CC-OUTBOUND-PDA-PRESERVE-001` | PDA 和 Web 使用相同 Outbound 字段、选择值和状态 |
| `CC-OUTBOUND-PDA-PRESERVE-002` | PDA 遵守相同 ACL、Record Rule 和服务端提交校验 |
| `CC-OUTBOUND-PDA-PRESERVE-003` | 图片为空不阻止提交；司机和仓库签名按本 CC 确认为可选 |
| `CC-OUTBOUND-PDA-PRESERVE-004` | 检查项、重量和温度只记录用户结果，不自动判定业务结论 |
| `CC-OUTBOUND-PDA-PRESERVE-005` | 提交失败不得改变为 submitted，不得显示成功提示 |
| `CC-OUTBOUND-PDA-PRESERVE-006` | Web Outbound 菜单、action 和表单行为保持不变 |

## 7. 允许修改的边界

| 类型 | 允许内容 |
|---|---|
| Dashboard | 增加 Outbound PDA 入口 |
| PDA assets | Outbound PDA Owl/JavaScript、模板和最小样式 |
| ORM 适配 | 仅复用既有 Outbound ORM 和签名/提交方法 |
| 图片 | 仅增加 Outbound 记录所需的图片关联/展示适配 |
| 测试 | PDA 触控、图片、两方签名、保存、提交、权限和 Web 回归 |
| 文档 | Outbound PDA CC、IHR、ATR、HVR、技术债和追溯记录 |

禁止通过前端隐藏替代服务端权限，禁止裸 SQL，禁止修改 Odoo 官方代码。

## 8. 权限和错误契约

- PDA 入口必须执行与 Web 相同的 Odoo ACL 和 Record Rule；
- 未授权用户不能通过 PDA 创建、读取、修改或提交 Outbound；
- 图片和签名的创建、读取、删除必须受服务端权限保护；
- 缺少必填字段或时间顺序错误时，必须显示明确错误并保持草稿；签名缺失不阻止提交；
- 网络、ORM、图片和签名错误不得被宽泛捕获后静默忽略；
- 成功反馈只能在对应 ORM 操作成功后显示。

## 9. 测试契约（草案）

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-OUTBOUND-PDA-TEST-001` | Dashboard Outbound PDA 入口 | Playwright | 可打开专用 PDA 页面 |
| `CC-OUTBOUND-PDA-TEST-002` | 窄屏字段与检查项 | Playwright | 主要字段可触控填写并保存 |
| `CC-OUTBOUND-PDA-TEST-003` | 图片多选上传 | Playwright/HTTP | 多张图片均与当前记录关联 |
| `CC-OUTBOUND-PDA-TEST-004` | 图片 popup 和单张删除 | Playwright | 放大、关闭和删除行为正确 |
| `CC-OUTBOUND-PDA-TEST-005` | 司机多笔签名 | Playwright/HVR | 可连续绘制、清除、保存和恢复 |
| `CC-OUTBOUND-PDA-TEST-006` | 仓库多笔签名 | Playwright/HVR | 可连续绘制、清除、保存和恢复 |
| `CC-OUTBOUND-PDA-TEST-007` | 两方签名提交 | ORM/Playwright | 无签名、单方签名和双方签名均按新规则提交 |
| `CC-OUTBOUND-PDA-TEST-008` | 草稿恢复 | Playwright/HTTP | 保存后重新进入，字段、图片和签名存在 |
| `CC-OUTBOUND-PDA-TEST-009` | 权限边界 | ORM/HTTP | 未授权用户被拒绝 |
| `CC-OUTBOUND-PDA-TEST-010` | Web 回归 | Odoo/Playwright | Web Outbound 行为不变 |
| `CC-OUTBOUND-PDA-TEST-011` | 真实 PDA 触控 | HVR | 真实 PDA 或等效触控设备通过 |

未执行的测试不得记录为 PASS。自动化验证不得替代真实 PDA 或等效设备 HVR。

## 10. 停止条件

遇到以下任一情况必须停止并修订上游文档或本 CC：

1. PDA 需要独立 Outbound 数据模型；
2. 图片或签名需要改变 Outbound 状态、权限或提交规则；
3. 需要库存、运输、放行、隔离、通知或异常工单动作；
4. 需要离线同步、条码扫描或设备原生 API；
5. 无法通过 ORM 保存图片、签名人和签名时间；
6. 无法在真实 PDA 或等效触控设备上完成签名和图片 HVR；
7. 需要修改 Odoo 官方代码或使用裸 SQL。

## 11. 完成闸门

- [ ] 用户批准本 CC 冻结；
- [ ] 用户另行授权实施；
- [ ] Outbound PDA 入口和页面完成；
- [ ] 图片上传、放大、删除和持久化通过；
- [ ] 司机和仓库两套签名的多笔绘制、保存和恢复通过；
- [ ] 无签名、单方签名和双方签名均按批准后的服务端规则验证；
- [ ] Web/PDA 回归测试通过；
- [ ] ATR 基于实际执行结果更新；
- [ ] 真实 PDA 或等效触控设备 HVR 通过；
- [ ] `TD-OUTBOUND-PDA-001` 关闭。

## 12. 用户确认与上游冲突

用户已确认以下设计：

| 编号 | 决定 | CC 处理 |
|---|---|---|
| 1 | 采用六步页面结构 | 纳入冻结范围 |
| 2 | Driver signature 和 Warehouse signature 使用独立页面 | 纳入冻结范围 |
| 3 | 图片实现与 Inbound 相同，使用 `ir.attachment` 多图关系 | 纳入冻结范围 |
| 4 | 保存草稿后重新进入 PDA 时恢复最后一个步骤 | 纳入冻结范围 |
| 5 | 提交前允许删除已上传图片 | 纳入冻结范围 |
| 6 | 司机和仓库签名均为可选，提交不强制任一签名 | 已同步修订上游文档，纳入冻结范围 |

Outbound SRS、TDD 和 Outbound Form CC 已同步为：签名是可选记录证据；签名存在
时保存签名图像、签名人和签名时间；缺少签名不阻止提交。
