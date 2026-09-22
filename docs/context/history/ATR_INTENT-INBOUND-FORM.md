# Inbound Form Automated Test Record（ATR）

> 文档状态：In Progress  
> Intent ID：`INTENT-INBOUND-FORM`  
> IHR：[IHR_INTENT-INBOUND-FORM.md](./IHR_INTENT-INBOUND-FORM.md)  
> CC：`v1.0.0 Frozen`  
> 模块：`wd_qooling_app`

## 1. Execution Metadata

| 字段 | 值 |
|---|---|
| Environment | Odoo 18，数据库 `odoo18ce`，共享虚拟环境 |
| Test Framework | Odoo `--test-enable` / `TransactionCase` |
| Code Baseline（当前） | 工作区实施代码，ACL 与签名组件修复后，待提交 |
| Branch | `main` |
| Executed By | Copilot Agent |
| Execution Window | 2026-09-22 17:48–18:03（+08:00） |

## 2. Test Contract Baseline

| 来源 | ID | 验证点 |
|---|---|---|
| CC Test Contract | `CC-TEST-001` | 创建和保存草稿 |
| CC Test Contract | `CC-TEST-002` | 必填字段和签名提交 |
| CC Test Contract | `CC-TEST-004` | UN Number 选择限制 |
| CC Test Contract | `CC-TEST-005` | 记录结果不触发处置 |
| CC Test Contract | `CC-TEST-008` | 照片和备注非必填 |
| TDD Guardrail | `T-SCOPE-001`、`T-DATA-001`、`T-SIGN-001` | 记录边界、数据约束和签名证据 |

## 3. Current Automated Test Status

| 指标 | 值 |
|---|---|
| Required Automated Tests | 7 test methods |
| PASS | 7（最新 Run） |
| FAIL | 0（最新 Run） |
| SKIPPED | 0 |
| BLOCKED | 0 |
| NOT RUN | 0（已执行的 7 项） |
| Latest Valid Run | `ATR-RUN-003` |
| Evidence Baseline Match | Yes（当前实施代码，提交前工作区基线） |

## 4. Core Test Contract Coverage Matrix

| CC / TEST 来源 | Automated Test | Run | Result | Evidence |
|---|---|---|---|---|
| `CC-TEST-001` | `test_create_and_save_draft` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-002` | `test_submit_requires_signature`、`test_submit_persists_submission_and_signature` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-003` | `test_adr_requires_related_fields_on_submit` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-004` | `test_adr_requires_related_fields_on_submit` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-005` | `test_record_values_do_not_create_workflow` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-008` | `test_optional_photo_and_comments` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-010` | `test_reset_to_draft` | `ATR-RUN-002` | PASS | `/tmp/wd_qooling_final_test2.log` |
| `CC-TEST-006` | Web/PDA signature UI | HVR-RUN-002 / HVR-RUN-003 | PASS（HVR） | HVR record |
| `CC-TEST-007` | Multi-language UI | HVR-RUN-003 | PASS（HVR） | HVR record |
| `CC-TEST-009` | PDF entry consistency | — | BLOCKED | `TD-006` unresolved |

## 5. Test Run History（Append-only）

### ATR-RUN-001

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-22 17:48（+08:00） |
| Code Baseline | 初次实施工作区 |
| Invocation | `odoo-bin -u wd_qooling_app --test-enable --stop-after-init --http-port=18074 --workers=0` |
| Scope | `wd_qooling_app` 模块测试 |
| Executed | 7 |
| PASS / FAIL / SKIPPED / BLOCKED | 6 / 1 / 0 / 0 |
| Result | FAIL |
| Evidence | `/tmp/wd_qooling_upgrade.log` |
| Follow-up | `IHR-003`、`IHR-004` |

失败事实：

- `test_submit_persists_submission_and_signature` 发现直接写入签名后提交没有自动保存 Signer；
- 同一 Run 中序列权限问题已在实施修复前解决。

### ATR-RUN-002

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-22 17:49（+08:00） |
| Code Baseline | 修复后的当前实施工作区 |
| Invocation | `odoo-bin -u wd_qooling_app --test-enable --stop-after-init --http-port=18076 --workers=0` |
| Scope | `wd_qooling_app` 模块测试 |
| Executed | 7 |
| PASS / FAIL / SKIPPED / BLOCKED | 7 / 0 / 0 / 0 |
| Result | PASS |
| Evidence | `/tmp/wd_qooling_final_test2.log` |
| Follow-up | 需在提交后重新执行相关测试以绑定最终 Commit |

### ATR-RUN-003

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-22 18:03（+08:00） |
| Code Baseline | ACL 与签名组件修复后的当前实施工作区 |
| Invocation | `odoo-bin -u wd_qooling_app --test-enable --stop-after-init --http-port=18086 --workers=0` |
| Scope | `wd_qooling_app` 模块测试 |
| Executed | 7 |
| PASS / FAIL / SKIPPED / BLOCKED | 7 / 0 / 0 / 0 |
| Result | PASS |
| Evidence | `/tmp/wd_qooling_update7.log` |
| Follow-up | 提交后绑定最终 Commit |

测试日志同时记录了数据库中既有 `wd_advanced_m2o_record_panel` 缺失模块警告；该问题不属于本 CC，未修改。

## 6. Regression Verification

| CC-PRESERVE | 回归测试 | Run | Result |
|---|---|---|---|
| `CC-PRESERVE-001` | `test_record_values_do_not_create_workflow` | `ATR-RUN-002` | PASS |
| `CC-PRESERVE-002` | `test_optional_photo_and_comments` | `ATR-RUN-002` | PASS |
| `CC-PRESERVE-003` | `test_reset_to_draft` | `ATR-RUN-002` | PASS |
| `CC-PRESERVE-004` | `test_submit_persists_submission_and_signature` | `ATR-RUN-002` | PASS |

## 7. Issues

| ID | TEST | Run | 类型 | 原因 | Status | Follow-up |
|---|---|---|---|---|---|---|
| ATR-ISSUE-001 | `test_submit_persists_submission_and_signature` | `ATR-RUN-001` | FAIL | 提交时未写入 Signer 和 Signature time | Resolved | `IHR-004`、`ATR-RUN-002` |
| ATR-ISSUE-002 | PDF entry consistency | — | BLOCKED | `TD-006` 尚未确认 | Open | SRS/TDD/CC 修订后追加测试 |

## 8. Handoff Summary

- 当前自动化测试最新结果：7/7 PASS；
- `ATR-RUN-001` 的失败记录保留；
- UI、PDA、语言和 PDF 入口仍需 HVR 或后续决策；
- 当前 ATR 不代表 Human Verification 或 Merge Approval。
