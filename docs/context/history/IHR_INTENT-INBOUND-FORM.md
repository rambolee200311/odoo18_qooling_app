# Inbound Form Implementation History Record（IHR）

> 文档状态：In Progress  
> Intent ID：`INTENT-INBOUND-FORM`  
> CC：[Coding_Contract_Inbound_Form.md](../intent/Coding_Contract_Inbound_Form.md) `v1.0.0 Frozen`  
> 模块：`wd_qooling_app`  
> 实施负责人：Copilot Agent  
> 开始时间：2026-09-22 17:46（+08:00）  
> 最后更新：2026-09-22 17:49（+08:00）  
> 当前实施状态：Implementation Complete（等待 ATR/HVR/FR）

## 1. 执行元数据

| 字段 | 值 |
|---|---|
| Branch | `main` |
| Base Commit | `fcde898` |
| Final Commit | 待提交 |
| PR | N/A |

## 2. Coding Contract 基线

| 项 | 引用 |
|---|---|
| Scope | CC §3 |
| Change Boundary | CC §4 |
| Required Behavior | `CC-CHANGE-001` 至 `CC-CHANGE-007` |
| Preservation | `CC-PRESERVE-001` 至 `CC-PRESERVE-005` |
| Guardrails | `T-SCOPE-001`、`T-DATA-001`、`T-SIGN-001`、`T-I18N-001`、`T-SEC-001`、`T-ORM-001`、`T-PDF-001`、`T-ERR-001` |
| Test Contract | `CC-TEST-001` 至 `CC-TEST-010` |
| Stop Conditions | CC §12 |
| Done Criteria | CC §13 |

## 3. 当前实施状态摘要

| 项 | 状态 |
|---|---|
| CC-CHANGE 落实进度 | 7 / 7（PDF 具体实现按 `TD-006` 阻塞） |
| Preservation Impact | None（待 HVR 验证） |
| Deviation | None |
| Stop Condition 触发 | No |
| Open Issues | 1（PDF 入口 `TD-006`） |
| Revert 发生 | No |
| 当前状态 | Implementation Complete |

## 4. 实施历史条目（Append-only）

### IHR-001

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-22 17:46（+08:00） |
| 阶段 | Implementation |
| Action | 创建 `wd_qooling_app` 模块骨架、manifest、模型、视图、安全、序列和测试目录 |
| Reason | 落实 `CC-CHANGE-001`、`CC-CHANGE-002` |
| Files / Components | `mymodules/wd_qooling_app/` |
| Contract Reference | `CC-CHANGE-001`、`CC-CHANGE-002`、`CC-PRESERVE-003` |
| Upstream Reference | `ORM-INBOUND-001` 至 `ORM-INBOUND-041`、`SVC-INBOUND-001` |
| Result | Completed |
| Deviation | None |
| Follow-up | ATR 验证 |

### IHR-002

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-22 17:47（+08:00） |
| 阶段 | Implementation |
| Action | 实现草稿、提交、撤回、签名审计信息、ADR 条件字段和 Selection 约束 |
| Reason | 落实 `CC-CHANGE-003`、`CC-CHANGE-004`、`CC-CHANGE-006` |
| Files / Components | `models/inbound_form.py`、`views/inbound_form_views.xml` |
| Contract Reference | `CC-CHANGE-003`、`CC-CHANGE-004`、`CC-CHANGE-006`、`CC-PRESERVE-001` |
| Upstream Reference | `SVC-INBOUND-002` 至 `SVC-INBOUND-004`、`T-SCOPE-001`、`T-SIGN-001` |
| Result | Completed |
| Deviation | None |
| Follow-up | HVR 验证 Web/PDA 手写签名 |

### IHR-003

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-22 17:48（+08:00） |
| 阶段 | Implementation |
| Action | 首次 Odoo 模块测试发现普通用户读取序列权限失败；改用 ORM `sudo()` 获取序列，并补充 Internal User 测试组 |
| Reason | 修复 `ATR-RUN-001` 失败，不改变业务语义 |
| Files / Components | `models/inbound_form.py`、`tests/test_inbound_form.py` |
| Contract Reference | `CC-CHANGE-001`、`T-ORM-001` |
| Upstream Reference | `TEST-INBOUND-001` |
| Result | Completed |
| Deviation | None |
| Follow-up | 追加 `ATR-RUN-002` |

### IHR-004

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-22 17:49（+08:00） |
| 阶段 | Implementation |
| Action | 首次测试发现直接写入签名 Binary 后提交未自动保存 Signer 和 Signature time；提交动作补充签名审计字段写入 |
| Reason | 修复 `ATR-RUN-001` 失败，满足签名证据契约 |
| Files / Components | `models/inbound_form.py`、`tests/test_inbound_form.py` |
| Contract Reference | `CC-CHANGE-003`、`CC-CHANGE-006`、`CC-PRESERVE-004` |
| Upstream Reference | `ORM-INBOUND-037` 至 `ORM-INBOUND-039`、`T-SIGN-001` |
| Result | Completed |
| Deviation | None |
| Follow-up | 追加 `ATR-RUN-002` |

### IHR-005

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-22 17:49（+08:00） |
| 阶段 | Implementation |
| Action | 保持 PDF 具体 Adapter、导入器和生成器未实现 |
| Reason | 遵守冻结 TDD `TD-006` 和 `T-PDF-001` |
| Files / Components | 无新增 PDF 组件 |
| Contract Reference | `CC-DEC-003`、`T-PDF-001` |
| Upstream Reference | TDD `TD-006` |
| Result | Blocked（按设计阻塞） |
| Deviation | None |
| Follow-up | PDF 业务入口确认后修订 TDD/CC |

## 5. 实际变更清单

| 路径 | 变更 |
|---|---|
| `mymodules/wd_qooling_app/__manifest__.py` | 新增模块声明、依赖和资源 |
| `mymodules/wd_qooling_app/models/inbound_form.py` | 新增 Inbound ORM、状态、提交和签名行为 |
| `mymodules/wd_qooling_app/views/inbound_form_views.xml` | 新增 List、Form、Search、菜单和 ADR 动态字段 |
| `mymodules/wd_qooling_app/security/` | 新增用户/复核组和 ACL |
| `mymodules/wd_qooling_app/data/ir_sequence_data.xml` | 新增记录编号序列 |
| `mymodules/wd_qooling_app/static/src/` | 新增 Web/PDA Canvas 手写签名字段 |
| `mymodules/wd_qooling_app/tests/` | 新增 7 项 Odoo TransactionCase |

## 6. Deviation / Stop 事件

无未经批准的 Deviation。PDF 具体实现按冻结设计处于 `TD-006` Blocked，不是未经批准的越界变更。

## 7. Open Issues

| ID | 描述 | 状态 | 后续 |
|---|---|---|---|
| IHR-ISSUE-001 | PDF 入口是上传现有 PDF 还是系统生成 PDF 尚未确认 | Open / Blocked | 业务确认后修订 TDD `TD-006` |

## 8. Handoff Summary

- Implementation：完成冻结 CC 中除 PDF 具体 Adapter 外的实现范围；
- ATR：`ATR-RUN-001` 保留失败记录，`ATR-RUN-002` 当前自动化测试通过；
- HVR：待真实人类验证 Web/PDA、移动视口、签名、多语言和记录查看；
- FR：尚未形成；
- Merge / Release：等待 Human Review。
