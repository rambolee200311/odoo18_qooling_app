# PDA Media Evidence Automated Test Record（ATR）

> 文档状态：Partial; Odoo shell ORM Run Passed
> Intent ID：`INTENT-PDA-MEDIA-EVIDENCE`
> CC：[Coding_Contract_PDA_Media_Evidence.md](../intent/Coding_Contract_PDA_Media_Evidence.md) `v1.0.0 Frozen`
> IHR：[IHR_INTENT-PDA-MEDIA-EVIDENCE.md](./IHR_INTENT-PDA-MEDIA-EVIDENCE.md)
> 模块：`wd_qooling_app`

## 1. Execution Metadata

| 字段 | 值 |
|---|---|
| Environment | Odoo 18 / `http://127.0.0.1:18087` |
| Database | `odoo18ce` |
| Test Framework | Node syntax, Python compile, XML parse, Odoo TransactionCase, Playwright |
| Code Baseline | Working tree after CC-authorized implementation |
| Executed By | Copilot with shared browser |
| Execution Date | 2026-09-23 |

## 2. Test Contract Coverage

| CC Test | 覆盖内容 | 当前结果 |
|---|---|---|
| CC-MEDIA-TEST-001 | Web 图片上传和恢复 | PASS |
| CC-MEDIA-TEST-002 | Web 视频上传和播放 | PASS |
| CC-MEDIA-TEST-003 | PDA 拍照入口 | PASS |
| CC-MEDIA-TEST-004 | PDA 录制入口 | PASS |
| CC-MEDIA-TEST-005 | PDA 文件入口 | PASS |
| CC-MEDIA-TEST-006 | 图片/视频预览和删除入口 | PASS |
| CC-MEDIA-TEST-007 | PDA/Web 媒体恢复 | PASS |
| CC-MEDIA-TEST-008 | 权限边界 | BLOCKED |
| CC-MEDIA-TEST-009 | 失败处理 | PASS（前端静态/Playwright路径） |
| CC-MEDIA-TEST-010 | 大文件限制 | NOT RUN |
| CC-MEDIA-TEST-011 | 多文件上限 | PASS |
| CC-MEDIA-TEST-012 | 不支持格式 | PASS |

## 3. Current Automated Test Status

| 指标 | 值 |
|---|---|
| Required Automated Tests | 12 |
| PASS | 10 |
| FAIL | 0 |
| BLOCKED | 1 |
| NOT RUN | 1 |
| Latest Valid Run | `ATR-RUN-004` |
| Evidence Baseline Match | Yes（工作树基线） |

## 4. Test Run History

### ATR-RUN-001

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-23 |
| Code Baseline | Working tree |
| Scope | Syntax and asset structure |
| Invocation | `node --check`、`python3 -m py_compile`、XML parse、`git diff --check` |
| Executed | JavaScript/Python/XML checks |
| PASS / FAIL / BLOCKED | PASS / 0 / 0 |
| Result | PASS |
| Evidence | Tool output in session |
| Follow-up | Continue ORM and browser verification |

### ATR-RUN-002

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-23 |
| Code Baseline | Working tree after media metadata fix |
| Scope | Web/PDA Playwright integration |
| Invocation | Shared browser Playwright |
| Executed | Web and Temperature PDA image/video upload and preview |
| PASS / FAIL / BLOCKED | PASS / 0 / 0 |
| Result | PASS |
| Evidence | Web: 1 video + 3 images; PDA: image/video thumbnails and preview nodes |
| Follow-up | User human verification recorded in HVR |

### ATR-RUN-003

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-23 |
| Code Baseline | Working tree |
| Scope | Targeted Odoo Temperature TransactionCase |
| Invocation | `odoo-bin -d odoo18ce -u wd_qooling_app --test-enable --test-tags /wd_qooling_app:TestQoolingTemperatureRecord` |
| Executed | Blocked before tests loaded |
| PASS / FAIL / BLOCKED | 0 / 0 / 1 |
| Result | BLOCKED |
| Evidence | `psycopg2.OperationalError: fe_sendauth: no password supplied` |
| Follow-up | Re-run with valid PostgreSQL credentials |

### ATR-RUN-004

| 字段 | 值 |
|---|---|
| Timestamp | 2026-09-23 |
| Code Baseline | Working tree after CC-authorized implementation |
| Scope | Odoo shell ORM media rules |
| Invocation | `venv/bin/python odoo-bin shell -c odoo.conf` with current worktree addons |
| Executed | MIME rejection, 20-media limit, submitted read-only, Inbound/Outbound/Temperature `photo_ids` loading |
| PASS / FAIL / BLOCKED | 5 / 0 / 0 |
| Result | PASS |
| Evidence | `temperature_rejects_unsupported_mimetype=True`; `rejects_more_than_20_media=True`; `submitted_media_is_readonly=True`; all three models loaded `photo_ids` |
| Follow-up | None for executed ORM scope |

## 5. Regression Verification

| 保留项 | 回归测试 | Result |
|---|---|---|
| Web/PDA ORM and attachment semantics | Playwright media upload and reload | PASS |
| Existing temperature form workflow | Browser opened existing draft and Evidence tab | PASS |
| Odoo ORM constraints | TransactionCase | BLOCKED |

## 6. Handoff

ATR 不将 BLOCKED 或 NOT RUN 项伪造为 PASS。直接 PostgreSQL Run-003 的历史阻塞已由
项目标准 Odoo shell Run-004 完成 ORM 验证。仍需补跑：

- 权限边界；
- 10 MB/100 MB 文件限制。
