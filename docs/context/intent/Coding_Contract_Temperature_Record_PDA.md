# Temperature Record PDA / Images / Signature Coding Contract

> 文档状态：Frozen
> 文档版本：v1.0.0
> 起草日期：2026-09-23
> 冻结日期：2026-09-23
> 实施状态：Authorized for Implementation

实现决议：`photo_ids` 是唯一有效的 Temperature Record 图片证据入口；旧 `photo`
字段仅为历史数据兼容保留，不在 Web、PDA 或新业务流程中使用。
> 冻结批准日期：2026-09-23
> Intent ID：`INTENT-TEMPERATURE-RECORD-PDA`
> 上游 CC：[Coding_Contract_Temperature_Record.md](./Coding_Contract_Temperature_Record.md)
> 上游 TDD：[TDD_qooling_temperature_record.md](../designing/TDD_qooling_temperature_record.md)
> 适用 Form：Weekly Temperature Control / Temperature Record

## 0. 文档治理

本 Coding Contract（CC）只定义 Temperature Record 的 PDA 触控入口、动态温度
录入、图片证据和手写签名交互。本 CC 不重新定义 Temperature Record 的字段、
状态、权限、提交规则、托盘明细边界或人工复核语义；这些内容继续以冻结的
Temperature Record SRS、TDD 和主 CC 为准。

本文件已获批准冻结，但冻结不等于实施授权。任何编码、数据库迁移、菜单发布或
现有 Temperature Record Web 行为变更，都必须另行获得明确实施授权后进行。

## 1. 目标

在 `FORMS / PDA / Temperature Record` 下提供适合窄屏触控设备的温度记录入口。
PDA 创建或修改的记录必须使用既有 `wd.qooling.temperature.record` ORM，并与
Web 表单共享字段语义、权限、状态、提交结果和错误边界。

PDA 必须支持：

- 保存和恢复温度记录草稿；
- 连续录入实际托盘温度；
- 修改草稿中的托盘温度和人工结果；
- 上传、查看和删除货物/温度记录图片；
- 记录备注和检查结果；
- 手写签名、清除、保存和恢复；
- 在服务端必填校验通过且签名存在时提交记录。

## 2. 页面契约（草案）

建议使用以下步骤；实现可以调整步骤名称，但不得改变字段和证据语义：

| 步骤 | 内容 |
|---|---|
| Details | Date、Manager、Customer、Container number、Location、Filing date |
| Pallet temperatures | Quick temperature 输入、Enter 新增、托盘明细、温度修改 |
| Checks | Packaging damage、Unpacked housing damage、Electrolyte leakage、Storage stability |
| Evidence | 多图片、备注、人工温度异常结果和处置说明 |
| Signature | 手写签名、清除、恢复和提交 |

步骤导航必须显示当前进度，并提供上一页、下一页和保存草稿。Submit 只调用
服务端 Temperature Record 提交方法，不在前端复制提交规则。

## 3. 动态温度录入契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-TEMP-PDA-READING-001` | Enter 录入 | 有效数值创建一条实际托盘明细 |
| `CC-TEMP-PDA-READING-002` | 清空回焦 | 成功新增后输入框清空并重新获得焦点 |
| `CC-TEMP-PDA-READING-003` | 连续编号 | 由 ORM 生成 `pallet1`、`pallet2`、`pallet3`，编号只读 |
| `CC-TEMP-PDA-READING-004` | 修改 | 草稿中可修改温度及允许的人工结果字段 |
| `CC-TEMP-PDA-READING-005` | 非数字输入 | 显示明确错误，不创建空或伪造明细 |
| `CC-TEMP-PDA-READING-006` | 清空全部 | 只通过既有显式清空动作执行，并要求二次确认 |
| `CC-TEMP-PDA-READING-007` | 单行删除 | 不提供单行删除替代清空动作；ORM 继续拒绝非法单行删除 |

PDA 不预生成 65 条托盘、不创建固定托盘字段、不截断实际明细，也不根据温度
数值自动判断异常或启动程序 51/52。

## 4. 图片证据契约

图片采用与 Inbound/Outbound 已验证实现一致的 `ir.attachment` 多图关系和 Web
图片画廊语义。具体关系字段名须在实施前与 ORM/TDD 一起确定，不能同时保留
互相冲突的单图和多图业务入口。

| ID | 行为 | 预期 |
|---|---|---|
| `CC-TEMP-PDA-IMAGE-001` | 上传 | 支持一张或多张图片并关联当前 Temperature Record |
| `CC-TEMP-PDA-IMAGE-002` | 缩略图 | 每张图片独立显示 |
| `CC-TEMP-PDA-IMAGE-003` | 放大 | 图片在 popup 中查看，不使用固定右侧 panel |
| `CC-TEMP-PDA-IMAGE-004` | 删除 | 可删除单张图片，不影响其他图片或记录 |
| `CC-TEMP-PDA-IMAGE-005` | 持久化 | 保存、重新进入 PDA、打开 Web 表单后仍可查看 |
| `CC-TEMP-PDA-IMAGE-006` | 非必填 | 没有图片不得阻止草稿保存或提交 |
| `CC-TEMP-PDA-IMAGE-007` | 错误 | 上传、加载和删除失败显示真实错误，不显示成功 |

图片只作为温度记录证据保存，不触发隔离、复测、通知、放行、库存或其他仓库
业务流程。

## 5. 签名契约

Temperature Record 使用一套手写签名：

1. Temperature record signer signature。

| ID | 行为 | 预期 |
|---|---|---|
| `CC-TEMP-PDA-SIGN-001` | 绘制 | 手指或触控笔可以连续绘制多笔签名 |
| `CC-TEMP-PDA-SIGN-002` | 清除 | 只清除当前签名，不影响温度明细、图片和备注 |
| `CC-TEMP-PDA-SIGN-003` | 保存 | 签名图像、签名人和签名时间写入既有字段 |
| `CC-TEMP-PDA-SIGN-004` | 恢复 | 保存后返回 PDA 或打开 Web 表单，签名仍可见 |
| `CC-TEMP-PDA-SIGN-005` | 提交 | 按主 CC 规则，签名缺失时服务端拒绝提交 |
| `CC-TEMP-PDA-SIGN-006` | 独立性 | 签名只写入 Temperature Record 的签名字段 |
| `CC-TEMP-PDA-SIGN-007` | 错误 | 保存或恢复失败显示真实错误，不伪造成功 |

签名表示用户完成了记录确认，不能解释为自动温度判定、质量批准、隔离决定、
放行决定或库存操作。

## 6. 必须保留的边界

| ID | 必须保留 |
|---|---|
| `CC-TEMP-PDA-PRESERVE-001` | PDA 和 Web 使用相同 ORM、字段、状态和提交结果 |
| `CC-TEMP-PDA-PRESERVE-002` | PDA 遵守相同 ACL、Record Rule 和服务端校验 |
| `CC-TEMP-PDA-PRESERVE-003` | 温度、阈值、异常、复测和处置由人工复核决定 |
| `CC-TEMP-PDA-PRESERVE-004` | 检查字段空值表示未填写，不等价于 No |
| `CC-TEMP-PDA-PRESERVE-005` | 图片和备注为空不阻止保存或提交 |
| `CC-TEMP-PDA-PRESERVE-006` | 提交失败不得改变为 submitted，不得显示成功 |
| `CC-TEMP-PDA-PRESERVE-007` | 不自动创建隔离、复测、通知、放行、库存或异常工单 |

## 7. 权限和错误契约

- PDA 入口必须执行与 Web 相同的 Odoo ACL 和 Record Rule；
- 未授权用户不能通过 PDA 创建、读取、修改或提交 Temperature Record；
- 图片和签名的创建、读取、删除必须受服务端权限保护；
- 缺少 Date、Manager、Customer、Container number 或签名时，显示明确错误并
  保持草稿；
- 快速温度输入无效时，不得创建空明细；
- 网络、ORM、图片和签名错误不得被宽泛捕获后静默忽略；
- 成功反馈只能在对应 ORM 操作成功后显示。

## 8. 测试契约（草案）

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-TEMP-PDA-TEST-001` | Dashboard Temperature PDA 入口 | Playwright | 可打开专用 PDA 页面 |
| `CC-TEMP-PDA-TEST-002` | 窄屏基础字段 | Playwright | 可触控填写并保存草稿 |
| `CC-TEMP-PDA-TEST-003` | Enter 连续录入 | Playwright/ORM | 明细创建、清空并回焦 |
| `CC-TEMP-PDA-TEST-004` | 编号和明细编辑 | Playwright/ORM | 编号连续只读，草稿温度可修改 |
| `CC-TEMP-PDA-TEST-005` | 清空确认 | Playwright/ORM | 确认清空，取消不变，下一条从 pallet1 开始 |
| `CC-TEMP-PDA-TEST-006` | 多图片上传 | Playwright/HTTP | 图片均关联当前记录 |
| `CC-TEMP-PDA-TEST-007` | 图片放大和删除 | Playwright | popup、单张删除行为正确 |
| `CC-TEMP-PDA-TEST-008` | 签名绘制和恢复 | Playwright | 多笔绘制、清除、保存、恢复正确 |
| `CC-TEMP-PDA-TEST-009` | 提交校验 | Playwright/ORM | 必填字段和签名满足后提交 |
| `CC-TEMP-PDA-TEST-010` | Web/PDA 一致性 | Web/Playwright | 图片、签名和温度明细互相可见 |
| `CC-TEMP-PDA-TEST-011` | 权限和失败处理 | ORM/HTTP | 未授权、上传失败和提交失败真实反馈 |

自动化测试通过不得替代真实 PDA 或等效触控设备 HVR。未执行的 HVR 不得标记
为 PASS。

## 9. 实施停止条件

遇到以下任一情况必须停止并请求变更批准：

1. 需要自动判断温度、阈值、异常、隔离、复测或放行；
2. 需要固定 65 个托盘字段或预生成空明细；
3. 需要自动启动程序 51/52；
4. 需要新增状态、字段、接口或依赖而未同步修订上游 TDD；
5. 需要改变签名必填规则；
6. 需要将图片或签名写入独立于既有 Temperature Record 的新业务模型；
7. 需要修改 Odoo 官方代码、使用裸 SQL 或引入外部服务；
8. 无法在 ORM 层保持权限、提交和单行删除边界。

## 10. 完成闸门

- [ ] 上游 SRS/TDD/主 CC 与本 PDA CC 追溯一致；
- [ ] Temperature Record PDA ORM 适配、视图、安全和资源通过针对性测试；
- [ ] 动态托盘、Enter 录入、清空确认和单行删除边界通过测试；
- [ ] 多图片上传、放大、删除和持久化通过测试；
- [ ] 签名绘制、清除、恢复、审计字段和提交校验通过测试；
- [ ] Web/PDA 字段、状态和结果一致；
- [ ] 真实 PDA 或等效触控设备 HVR 完成；
- [ ] IHR、ATR、HVR 和 Final Report 更新；
- [x] 本 CC 已获用户批准冻结；
- [ ] 用户另行授权实施。
