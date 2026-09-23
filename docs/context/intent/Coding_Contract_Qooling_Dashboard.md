# Qooling Dashboard Coding Contract

> 文档状态：Frozen
> 文档版本：v1.0.0
> 起草日期：2026-09-23
> 冻结日期：2026-09-23
> 实施状态：Approved for Implementation
> 实施批准日期：2026-09-23
> 模块：`wd_qooling_app`

## 0. 文档治理

本 CC 只冻结 Qooling Dashboard 的入口、导航和访问边界，不重新定义
Inbound Record、Outbound Record 或 Temperature Record 的字段、状态和业务
规则。三个 Form 的既有 SRS/TDD/CC 仍是各自功能的唯一业务基线。

本 CC 已获批准冻结并获得实施授权。实施仍必须遵守本 CC 的范围、停止条件、
测试契约和完成闸门，不得修改现有 Form 模型或改变现有 Form 状态流转。

## 1. 目标

将 Qooling 模块入口统一为 Dashboard。Dashboard 的第一个模块为 `FORMS`。
`FORMS` 下分为 `WEB` 模式和 `PDA` 模式：

| Dashboard 模块 | 模式 | Form |
|---|---|---|
| `FORMS` | `WEB` | Inbound Record、Outbound Record、Temperature Record |
| `FORMS` | `PDA` | 待开发 |

`WEB` 模式使用现有菜单和 action。`PDA` 模式当前只保留待开发边界，
不在本 CC 中实现。

## 2. 范围冻结

### 2.1 In Scope

- 新增 Qooling Dashboard 入口；
- Qooling 模块默认入口指向 Dashboard；
- Dashboard 第一个模块为 `FORMS`；
- `FORMS` 下展示 `WEB` 和 `PDA` 两种模式；
- `WEB` 模式复用现有菜单和 action，提供：
  - Inbound Record；
  - Outbound Record；
  - Temperature Record；
- `PDA` 模式仅保留待开发入口，不在本 CC 中实现；
- `WEB` 模式入口跳转到对应既有 Form 的标准 Odoo action；
- 保持现有 Form 模型、字段、权限、状态和提交行为不变；
- 对入口可见性和跳转目标提供视图/HTTP/Playwright 测试。

### 2.2 Out of Scope

- 不新增或复制 Inbound、Outbound、Temperature 的业务模型；
- 不改变三个 Form 的字段、状态、权限和提交规则；
- 不实现 PDA 模式的专用 JavaScript、数字键盘或设备 API；
- 不实现自动温度判断、异常流程、库存、隔离、放行、运输或通知；
- 不实现统计图表、KPI、报表、实时数据聚合或业务看板；
- 不实现 PDF、外部 API、单点登录或独立前端应用；
- 不修改 Odoo 官方代码。

## 3. 入口契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-CHANGE-001` | 进入 Qooling 模块 | 默认打开 Dashboard |
| `CC-CHANGE-002` | FORMS 模块 | 展示 `WEB` 和 `PDA` 两种模式 |
| `CC-CHANGE-003` | WEB 模式 | 复用现有菜单和 action |
| `CC-CHANGE-004` | PDA 模式 | 显示待开发状态，不实现 PDA 界面 |
| `CC-CHANGE-005` | Inbound 入口 | WEB 模式跳转既有 Inbound Record action |
| `CC-CHANGE-006` | Outbound 入口 | WEB 模式跳转既有 Outbound Record action |
| `CC-CHANGE-007` | Temperature 入口 | WEB 模式跳转既有 Temperature Record action |

PDA 模式未来可以具有不同的布局或入口参数，但不得因此创建第二套记录
模型，也不得产生不同的业务语义。当前 PDA 模式不属于实施范围。

## 4. 既有行为保留

| ID | 保留行为 |
|---|---|
| `CC-PRESERVE-001` | Inbound Record 继续使用既有模型、action、权限和状态流转 |
| `CC-PRESERVE-002` | Outbound Record 继续使用既有模型、action、权限和状态流转 |
| `CC-PRESERVE-003` | Temperature Record 继续使用既有动态托盘、签名和提交规则 |
| `CC-PRESERVE-004` | Dashboard 不自动创建、修改或删除任何 Form 记录 |
| `CC-PRESERVE-005` | 未授权用户不能通过 Dashboard 绕过既有 Form ACL |
| `CC-PRESERVE-006` | WEB 模式继续使用现有菜单和 action，不复制入口逻辑 |

## 5. 变更边界

### 5.1 允许修改

| 类型 | 范围 |
|---|---|
| XML 视图 | Qooling Dashboard 视图、菜单和 action |
| Web 资产 | Dashboard 所需的最小样式/交互资产 |
| 测试 | Dashboard 入口、权限和跳转测试 |
| 文档 | IHR、ATR、HVR 及相关追溯文档 |

### 5.2 禁止修改

- `wd.qooling.inbound.form`、`wd.qooling.outbound.form`、
  `wd.qooling.temperature.record` 的业务字段和状态；
- 既有 Form 的提交、签名、异常和清空逻辑；
- Odoo 官方模块和官方代码；
- 其他模块的菜单入口；
- 任何裸 SQL、外部数据库或绕过 ORM/ACL 的实现。

## 6. 权限契约

- Dashboard 入口必须使用 Odoo 菜单和 action 权限；
- PDA/WEB 模式分类不得成为绕过 ACL 的权限边界；
- 用户只能看到其已有权限允许访问的 Form 入口；
- 入口可见不等于记录可写；最终权限必须由目标 Form 的 ACL 和 Record Rule
  决定；
- 未授权访问必须返回标准 Odoo 权限拒绝，不得静默隐藏错误或伪造空页面。

## 7. 测试契约

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-TEST-001` | Qooling 模块入口 | HTTP/Playwright | 默认进入 Dashboard |
| `CC-TEST-002` | FORMS 模块 | View/Playwright | 显示 WEB 和 PDA 两种模式 |
| `CC-TEST-003` | WEB 模式入口 | View/Playwright | 复用现有菜单和 action |
| `CC-TEST-004` | PDA 模式入口 | View/Playwright | 显示待开发状态 |
| `CC-TEST-005` | Inbound 跳转 | Playwright | 打开既有 Inbound action |
| `CC-TEST-006` | Outbound 跳转 | Playwright | 打开既有 Outbound action |
| `CC-TEST-007` | Temperature 跳转 | Playwright | 打开既有 Temperature action |
| `CC-TEST-008` | 既有 Form 回归 | Odoo tests | 原有测试继续通过 |
| `CC-TEST-009` | 权限边界 | HTTP/ACL | 不得绕过既有 Form 权限 |

## 8. 停止条件

遇到以下任一情况必须停止并修订本 CC 或上游文档：

1. Dashboard 需要复制任一 Form 的业务字段或模型；
2. PDA 与 WEB 需要不同的业务状态或提交语义；
3. 入口需要绕过既有 ACL、Record Rule 或签名约束；
4. 需要新增统计、自动判断、库存或异常业务流程；
5. 需要修改既有 Form 的状态、字段或生命周期；
6. 无法证明六个入口均跳转到正确的既有 action。

## 9. 完成闸门

- [x] Dashboard 入口设计经用户批准；
- [ ] FORMS 模块、WEB 现有菜单/action 和 PDA 待开发边界经用户确认；
- [ ] WEB 三个入口与既有 action 建立追溯；
- [ ] 入口权限和 Form ACL 验证通过；
- [ ] Dashboard 测试契约执行并记录；
- [ ] 既有 Inbound、Outbound、Temperature 测试保持通过；
- [ ] IHR、ATR、HVR 更新；
- [x] 用户批准本 CC 冻结；
- [x] 用户另行授权实施。
