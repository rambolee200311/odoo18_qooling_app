# PDA Media Evidence Implementation History Record（IHR）

> 文档状态：Implementation Complete; ATR/HVR Recorded
> Intent ID：`INTENT-PDA-MEDIA-EVIDENCE`
> CC：[Coding_Contract_PDA_Media_Evidence.md](../intent/Coding_Contract_PDA_Media_Evidence.md) `v1.0.0 Frozen; Authorized for Implementation`
> 模块：`wd_qooling_app`
> 实施负责人：Copilot
> 开始时间：2026-09-23
> 最后更新：2026-09-23

## 1. 执行元数据

| 字段 | 值 |
|---|---|
| Branch | `agents/docs-review-summary` |
| Base Commit | `ae58978` |
| Implementation Commit | Pending |
| PR | N/A |
| 当前实施状态 | Implementation Complete; not committed |

## 2. Coding Contract 基线

本记录仅引用冻结 CC，不重新定义其范围：

- 媒体范围和上游 SRS/TDD：见 CC §0.1–§2；
- Web Gallery：见 CC §3；
- PDA 采集入口：见 CC §4；
- PDA 媒体和草稿提示：见 CC §5；
- 业务、权限和状态边界：见 CC §6–§7；
- 自动化测试契约：见 CC §8。

## 3. 当前实施状态摘要

| 项 | 状态 |
|---|---|
| CC-WEB 媒体行为 | 已完成 |
| CC-PDA 采集入口 | 已完成 |
| 服务端 MIME/大小/数量限制 | 已完成 |
| 提交后媒体只读 | 已完成 |
| Preservation Impact | Potential Impact；Inbound 新增 `photo_ids` |
| Deviation | None |
| Stop Condition 触发 | No |
| Open Issues | 0；直接 PostgreSQL Run 已由 Odoo shell ORM Run 替代验证 |
| 当前状态 | Implementation Complete |

## 4. 实施历史条目

### IHR-001

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-23 |
| 阶段 | Implementation |
| Action | 起草、修订并冻结 PDA Media Evidence CC，获得实施授权 |
| Reason | 固定 Web/PDA 图片视频范围、容量、状态和验证边界 |
| Files / Components | `docs/context/intent/Coding_Contract_PDA_Media_Evidence.md` |
| Contract Reference | CC §0–§9 |
| Result | Completed |
| Deviation | None |
| Follow-up | ATR/HVR 记录验证结果 |

### IHR-002

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-23 |
| 阶段 | Implementation |
| Action | 为 Inbound、Outbound、Temperature 统一增加图片/视频 Gallery 和 PDA 拍照、录制、附件入口 |
| Reason | 落实 Web/PDA 媒体证据契约 |
| Files / Components | `photo_gallery_field.js/xml/scss`；三套 PDA JS/XML；Inbound view |
| Contract Reference | CC-MEDIA-WEB-001–007；CC-MEDIA-PDA-001–009 |
| Result | Completed |
| Deviation | None |
| Follow-up | Playwright 和人工验证已记录 |

### IHR-003

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-23 |
| 阶段 | Implementation |
| Action | 增加共享 ORM 媒体约束，限制 MIME、文件大小、记录数量，并锁定提交后媒体 |
| Reason | 落实 CC 的服务端安全和状态边界 |
| Files / Components | `models/media_evidence.py`；Inbound/Outbound/Temperature models；tests |
| Contract Reference | CC-MEDIA-WEB-008–009；CC-MEDIA-PDA-010–011；CC §6–§7 |
| Result | Completed |
| Deviation | None |
| Follow-up | Odoo TransactionCase 需在可认证数据库环境重跑 |

### IHR-004

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-23 |
| 阶段 | Fix |
| Action | 修复 Web Gallery Many2many 记录未可靠携带 MIME 导致视频按图片渲染的问题 |
| Reason | Playwright 发现 Web 与 PDA 媒体类型渲染不一致 |
| Files / Components | `photo_gallery_field.js` 元数据加载 |
| Contract Reference | CC-MEDIA-WEB-003–004；CC-MEDIA-PDA-005–006 |
| Result | Completed |
| Deviation | None |
| Follow-up | Web 视频缩略图和弹窗播放已重新验证 |

### IHR-005

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-23 |
| 阶段 | Verification Support |
| Action | 使用临时图片和视频文件执行 Web/PDA 上传、预览和类型识别验证 |
| Reason | 提供 ATR/HVR 所需的实际 UI 证据 |
| Files / Components | Web Temperature Evidence；Temperature PDA Evidence |
| Contract Reference | CC-MEDIA-TEST-001–007 |
| Result | Completed |
| Deviation | None |
| Follow-up | 临时测试文件已清理 |

### IHR-006

| 字段 | 内容 |
|---|---|
| 时间 | 2026-09-23 |
| 阶段 | Verification |
| Action | 使用项目标准 `venv/bin/python odoo-bin shell -c odoo.conf` 在 ORM 环境验证媒体模型、MIME 拒绝、20 个媒体上限、提交后只读和三类 Form 字段加载 |
| Reason | 纠正此前直接 PostgreSQL 测试方式，遵循项目 Odoo shell 验证纪律 |
| Files / Components | `wd.qooling.media.evidence.mixin`；Inbound/Outbound/Temperature models |
| Contract Reference | CC-MEDIA-WEB-008–009；CC-MEDIA-PDA-010–011；CC §6–§7 |
| Result | Completed |
| Deviation | None |
| Follow-up | ATR-RUN-004 记录执行结果 |

## 5. 实际变更清单

- 新增 [media_evidence.py](../../mymodules/wd_qooling_app/models/media_evidence.py)；
- 修改三类 Form 模型和 Inbound Web View；
- 修改 [photo_gallery_field.js](../../mymodules/wd_qooling_app/static/src/js/photo_gallery_field.js)、
  XML 和 SCSS；
- 修改 Inbound、Outbound、Temperature PDA JS/XML；
- 增加媒体关系和限制测试；
- 新增本 Intent 的 ATR/HVR 文档。

## 6. 阻塞与后续

针对性 Odoo TransactionCase 执行被本地 PostgreSQL 认证阻塞：

```text
fe_sendauth: no password supplied
```

这次历史 Run 不作为有效 ORM 证据；后续 ORM 证据使用项目标准 Odoo shell。

## 7. Handoff

- 编码实施已完成；
- Playwright 验证已完成；
- 用户已确认人工验证通过；
- 尚未创建 Git commit；
- 在提交前应完成可认证数据库环境下的 ATR 重跑和最终 Review。
