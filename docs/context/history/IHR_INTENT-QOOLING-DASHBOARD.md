# Qooling Dashboard Implementation History Record（IHR）

> 文档状态：In Progress
> Intent ID：`INTENT-QOOLING-DASHBOARD`
> CC：[Coding_Contract_Qooling_Dashboard.md](../intent/Coding_Contract_Qooling_Dashboard.md) `v1.0.0 Frozen`
> 实施状态：Implementation Authorized
> 实施批准日期：2026-09-23

## 1. 实施边界

- Dashboard 第一个模块为 `FORMS`；
- `FORMS` 下提供 `WEB` 和 `PDA` 两种模式；
- WEB 复用 Inbound、Outbound、Temperature 现有菜单和 action；
- PDA 仅保留待开发入口，本 Intent 不实现 PDA UI；
- 不修改三个既有 Form 的模型、字段、权限、状态或业务流程。

## 2. 执行元数据

| 字段 | 值 |
|---|---|
| Branch | `main` |
| Implementation Commit | Pending |
| PR | N/A |
| 当前状态 | Coding in progress; targeted Odoo tests passed |

## 3. 已实现内容

- `qooling_dashboard` client action；
- Dashboard `FORMS` 模块；
- `WEB` 模式入口按钮；
- `PDA (To be developed)` 预留入口；
- 既有 Inbound、Outbound、Temperature 菜单重挂到
  `FORMS / WEB`；
- Dashboard 入口复用既有 Form action。

实现文件：

- `mymodules/wd_qooling_app/static/src/js/qooling_dashboard.js`
- `mymodules/wd_qooling_app/static/src/xml/qooling_dashboard.xml`
- `mymodules/wd_qooling_app/views/qooling_dashboard_views.xml`
- `mymodules/wd_qooling_app/__manifest__.py`

验证结果：

- Python compile：通过；
- Dashboard XML 和 QWeb XML 解析：通过；
- Odoo targeted tests：17 tests loaded，0 failed，0 errors；
- 浏览器已验证 Dashboard、FORMS、WEB/PDA 展示及 Inbound Record 跳转。

## 4. 完成要求

- Dashboard 入口和 FORMS 模式视图完成；
- WEB 三个入口正确复用现有 action；
- PDA 待开发边界明确显示；
- Dashboard 权限和既有 Form ACL 验证通过；
- ATR、HVR 和回归测试记录真实结果后，才可完成实施。
