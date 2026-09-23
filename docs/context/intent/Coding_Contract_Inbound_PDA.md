# Inbound PDA Coding Contract

> 文档状态：Frozen
> 文档版本：v1.0.0
> 起草日期：2026-09-23
> 冻结日期：2026-09-23
> 实施状态：Approved for Implementation
> 实施批准日期：2026-09-23
> 技术债：`TD-INBOUND-PDA-001`
> 模块：`wd_qooling_app`

## 0. 文档治理

本 CC 专门处理 `TD-INBOUND-PDA-001`，为 Inbound Record 增加 PDA 触控 Web
入口和界面。本 CC 不重新定义 Inbound 的业务字段、状态、权限、签名语义或
提交规则；这些内容继续以 Inbound SRS、TDD 和已冻结的 Inbound CC 为准。

本 CC 已获批准冻结并获得实施授权。实施仍必须遵守本 CC 的范围、停止条件、
测试契约和完成闸门。

## 1. 目标

在 Dashboard 的 `FORMS / PDA` 模式下增加 Inbound Record PDA 入口，并提供
适合 PDA 触控操作的专用 Web 页面。

PDA 页面必须继续复用既有 `wd.qooling.inbound.form` ORM 记录、字段语义、
权限和生命周期。PDA 记录与 WEB 记录必须具有一致的业务结果。

## 2. 范围冻结

### 2.1 In Scope

- Dashboard `FORMS / PDA / Inbound Record` 入口；
- Inbound PDA 专用 Owl/JavaScript 页面；
- 适合触控的分区或分步字段填写；
- 大尺寸控件和清晰的上一项、下一项、保存、提交操作；
- PDA 触控签名画布；
- PDA 为窄屏布局，图片区域显示缩略图；
- 点击缩略图或放大操作后，在 popup 中查看大图，不使用右侧 panel；
- PDA 页面级加载、保存、提交和错误反馈；
- 稳定的 `data-testid` 选择器，支持 PDA E2E 验证；
- 复用既有 Inbound ORM、ACL、Record Rule、签名和提交方法；
- 保持现有 WEB Inbound 菜单和 action 行为不变。

### 2.2 Out of Scope

- 新增 Inbound ORM 模型或复制字段；
- 修改 Inbound 状态、权限、必填规则或提交语义；
- 条码扫描、库存移动、卸货控制、通知、隔离、放行或运输流程；
- 离线缓存、断网同步或设备原生 API；
- 图片多张上传、Chatter 置底；
- Outbound 或 Temperature Record PDA 页面；
- 修改 Odoo 官方代码或引入独立前端框架。

## 3. 行为契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-PDA-CHANGE-001` | PDA 入口 | 从 Dashboard `FORMS / PDA` 打开 Inbound PDA 页面 |
| `CC-PDA-CHANGE-002` | 触控填写 | 主要字段无需精确鼠标操作即可完成填写 |
| `CC-PDA-CHANGE-003` | 分步导航 | 页面提供清晰的下一项、上一项和当前进度反馈 |
| `CC-PDA-CHANGE-004` | 草稿保存 | 保存使用既有 Inbound ORM，错误显示在当前页面 |
| `CC-PDA-CHANGE-005` | 签名 | 触控笔或手指可绘制、清除和保存手写签名 |
| `CC-PDA-CHANGE-006` | 图片预览 | 窄屏显示缩略图，放大图使用 popup |
| `CC-PDA-CHANGE-007` | 提交 | 使用既有提交规则，成功后进入既有 `submitted` 状态 |
| `CC-PDA-CHANGE-008` | WEB 保持不变 | 现有 WEB 菜单、action 和表单行为不改变 |

## 4. 保留边界

| ID | 必须保留 |
|---|---|
| `CC-PDA-PRESERVE-001` | PDA 和 WEB 使用相同 Inbound 字段语义 |
| `CC-PDA-PRESERVE-002` | PDA 不绕过既有 ACL、Record Rule 和提交校验 |
| `CC-PDA-PRESERVE-003` | 检查结果只保存用户输入，不触发自动业务流程 |
| `CC-PDA-PRESERVE-004` | 签名仍记录签名图像、签名人和签名时间 |
| `CC-PDA-PRESERVE-005` | 保存或提交失败不得显示成功，不得静默吞错 |

## 5. 允许修改的边界

| 类型 | 范围 |
|---|---|
| Dashboard | 仅增加 Inbound PDA 入口 |
| Web assets | Inbound PDA Owl/JavaScript、模板和最小样式 |
| 服务端 | 仅增加 PDA 入口所需 action/路由适配，不改变 Inbound ORM 语义 |
| 测试 | PDA 触控、签名、保存、提交、权限和 WEB 回归测试 |
| 文档 | TD、IHR、ATR、HVR 和相关追溯文档 |

禁止修改既有 Inbound 业务模型字段、状态流转和 WEB 表单视图行为。

## 6. 权限和错误契约

- PDA 页面必须执行与 WEB 相同的 Odoo 权限检查；
- PDA 入口不能成为绕过 Inbound ACL 或 Record Rule 的后门；
- 未授权用户必须获得标准 Odoo 权限拒绝；
- 加载、保存、提交和签名失败必须显示真实错误；
- 不得使用前端隐藏替代服务端权限控制。

## 7. 测试契约

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-PDA-TEST-001` | Dashboard PDA Inbound 入口 | Playwright | 可打开专用 PDA 页面 |
| `CC-PDA-TEST-002` | 触控字段填写 | Playwright | 主要字段可用触控完成 |
| `CC-PDA-TEST-003` | 分步导航 | Playwright | 上一项/下一项和进度正确 |
| `CC-PDA-TEST-004` | PDA 草稿保存 | HTTP/Playwright | 使用既有 Inbound ORM 保存 |
| `CC-PDA-TEST-005` | PDA 手写签名 | Playwright | 可绘制、清除和保存签名 |
| `CC-PDA-TEST-006` | 窄屏图片预览 | Playwright | 缩略图可见，放大图在 popup 打开和关闭 |
| `CC-PDA-TEST-007` | PDA 提交 | HTTP/Playwright | 按既有规则进入 submitted |
| `CC-PDA-TEST-008` | 错误反馈 | Playwright | 失败显示真实错误，状态不伪造成功 |
| `CC-PDA-TEST-009` | 权限边界 | HTTP/ACL | 不得绕过既有 Inbound 权限 |
| `CC-PDA-TEST-010` | WEB 回归 | Odoo/Playwright | 现有 WEB 入口行为不变 |
| `CC-PDA-TEST-011` | 真实设备触控 | HVR | 真实 PDA 或等效触控设备通过 |

## 8. 停止条件

遇到以下任一情况必须停止并修订本 CC 或上游文档：

1. PDA 需要独立的 Inbound 数据模型；
2. PDA 与 WEB 需要不同的业务状态、字段语义或提交规则；
3. 实现需要库存、卸货、隔离、放行、通知或运输动作；
4. 无法复用既有 ORM、ACL 或签名提交边界；
5. 需要加入离线同步、条码扫描或设备 API；
6. 无法在真实 PDA 或等效触控设备上完成 HVR。

## 9. 完成闸门

- [x] CC 经用户批准冻结；
- [x] 用户另行授权实施；
- [ ] PDA Dashboard 入口完成；
- [ ] PDA 触控页面、签名、保存和提交完成；
- [ ] WEB 回归测试通过；
- [ ] ATR 全部测试基于真实结果记录；
- [ ] 真实 PDA 或等效设备 HVR 通过；
- [ ] `TD-INBOUND-PDA-001` 关闭。
