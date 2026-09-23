# PDA Media Evidence Coding Contract

> 文档状态：Frozen
> 文档版本：v1.0.0
> 起草日期：2026-09-23
> 冻结日期：2026-09-23
> 实施状态：Authorized for Implementation
> 验证状态：Playwright and Human Verification Passed
> Intent ID：`INTENT-PDA-MEDIA-EVIDENCE`
> 模块：`wd_qooling_app`

## 0. 文档治理

本 Coding Contract（CC）定义 Inbound、Outbound 和 Temperature Record 三类
PDA/Web Evidence 的图片与视频证据能力。本 CC 只定义媒体上传、展示、预览、
删除和设备采集入口，不重新定义三个 Form 的字段、状态、权限、签名、提交或
人工复核语义；这些内容继续以各自已批准的 SRS、TDD 和 CC 为准。

本文件已获用户批准冻结。冻结固定媒体范围、边界、限制和验证要求；冻结不等于
实施授权。未获得明确实施授权前，不得继续扩大实现范围、提交或发布媒体功能。

冻结批准日期：2026-09-23。
实施授权日期：2026-09-23。
人工验证通过日期：2026-09-23。

### 0.1 上游文档对应关系

| Form | SRS | TDD | 本 CC 覆盖范围 |
|---|---|---|---|
| Inbound | [SRS_qooling_inbound_form.md](../designing/SRS_qooling_inbound_form.md) | [TDD_qooling_inbound_form.md](../designing/TDD_qooling_inbound_form.md) | 媒体证据 |
| Outbound | [SRS_qooling_outbound_form.md](../designing/SRS_qooling_outbound_form.md) | [TDD_qooling_outbound_form.md](../designing/TDD_qooling_outbound_form.md) | 媒体证据 |
| Temperature Record | [SRS_qooling_weekly_temperature_control.md](../designing/SRS_qooling_weekly_temperature_control.md) | [TDD_qooling_temperature_record.md](../designing/TDD_qooling_temperature_record.md) | 媒体证据 |

## 1. 目标

统一三类 Form 的媒体证据行为：

- Web Evidence 使用同一个可复用媒体 Gallery；
- Gallery 支持图片和视频附件；
- PDA 在移动设备上提供拍照和录制视频入口；
- PDA 仍支持从设备文件系统选择图片或视频；
- 图片和视频均通过 `ir.attachment` 关联到当前 Form；
- Web 与 PDA 重新打开记录后仍可查看已保存媒体；
- 媒体仅作为人工证据保存，不自动改变业务状态或触发后续流程。

## 2. 适用范围

适用模型：

| Form | 服务端媒体关系 |
|---|---|
| Inbound | `photo_ids` Many2many to `ir.attachment` |
| Outbound | 既有 `photo_ids` Many2many to `ir.attachment` |
| Temperature Record | 既有 `photo_ids` Many2many to `ir.attachment` |

旧的单图 Binary 字段只保留历史兼容用途，不作为新媒体上传入口。

## 3. Web Gallery 契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-MEDIA-WEB-001` | 上传 | 支持 `image/*` 和 `video/*` 附件，可多选 |
| `CC-MEDIA-WEB-002` | 图片展示 | 图片以缩略图展示，保持既有 Gallery 布局 |
| `CC-MEDIA-WEB-003` | 视频缩略图 | 缩略图位置显示视频首帧或明确的视频图标，不显示完整播放控件或伪装成图片 |
| `CC-MEDIA-WEB-004` | 预览 | 图片和视频均可在弹窗中查看；视频在弹窗内使用 HTML5 `<video controls>` 播放 |
| `CC-MEDIA-WEB-005` | 删除 | 只解除当前 Form 关系并删除当前附件，不影响其他媒体 |
| `CC-MEDIA-WEB-006` | 持久化 | 保存后重新进入 Web 表单，媒体仍可查看 |
| `CC-MEDIA-WEB-007` | 错误 | 上传、读取或删除失败必须显示明确错误 |
| `CC-MEDIA-WEB-008` | 单文件上限 | 图片不超过 10 MB，视频不超过 100 MB；超过上限明确拒绝 |
| `CC-MEDIA-WEB-009` | 记录上限 | 单条记录最多关联 20 个媒体文件；超过上限明确拒绝 |

媒体 URL 必须继续经过 Odoo Web 内容访问机制，不得引入公开外链或绕过权限
的静态文件路径。

## 4. PDA 采集入口契约

Inbound、Outbound、Temperature PDA 的 Evidence 步骤必须提供三个入口：

| 入口 | 浏览器行为 |
|---|---|
| Take photo | 使用 `accept="image/*" capture="environment"` 和设备后置摄像头采集图片 |
| Record video | 使用 `accept="video/*" capture="environment"` 和设备后置摄像头录制视频 |
| Attach media | 使用 `accept="image/*,video/*"` 从设备文件选择器选择一个或多个图片/视频 |

设备不支持 `capture="environment"` 或用户拒绝权限时，必须降级为普通文件选择
能力，并显示真实错误；不得伪造已采集或已上传成功。

## 5. PDA 媒体契约

| ID | 行为 | 预期 |
|---|---|---|
| `CC-MEDIA-PDA-001` | 草稿前上传 | 未创建当前 Form 草稿时，显示保存草稿提示，不创建孤立附件 |
| `CC-MEDIA-PDA-002` | 图片上传 | 创建图片附件并通过当前 Form 的 `photo_ids` 建立关系 |
| `CC-MEDIA-PDA-003` | 视频上传 | 创建视频附件并通过当前 Form 的 `photo_ids` 建立关系 |
| `CC-MEDIA-PDA-004` | 多媒体上传 | 多选文件逐个处理，单个失败不得伪造整体成功 |
| `CC-MEDIA-PDA-005` | 缩略图 | 图片显示图片缩略图；视频显示首帧或视频图标，点击后在弹窗播放 |
| `CC-MEDIA-PDA-006` | 预览 | 图片可放大，视频可播放；关闭预览不改变媒体关系 |
| `CC-MEDIA-PDA-007` | 删除 | 解除 Many2many 关系并删除对应附件 |
| `CC-MEDIA-PDA-008` | 恢复 | PDA 重新进入草稿后能加载图片和视频 |
| `CC-MEDIA-PDA-009` | 非必填 | 没有媒体不得阻止保存或提交 |
| `CC-MEDIA-PDA-010` | 文件限制 | 超过单文件或记录总数上限时拒绝并显示明确错误 |
| `CC-MEDIA-PDA-011` | 格式限制 | 不支持的 MIME 类型被拒绝，不静默丢弃 |

文件名和 MIME 类型必须来自上传文件；前端不得根据扩展名伪造 MIME 类型。媒体
上传继续经过 Odoo ORM、ACL 和 Record Rule。

### 5.1 草稿提示交互

未创建当前 Form 草稿时，点击任一媒体入口都必须阻止上传，并在页面顶部显示
错误横幅：“Save the draft before uploading media.” 用户必须先点击既有的
“Save draft”按钮；保存成功后，用户可以重新点击媒体入口上传。系统不自动创建
草稿，也不自动重试被阻止的文件。

## 6. 业务边界

媒体证据不得自动：

- 判断温度是否超限；
- 判断图片或视频是否合格；
- 触发异常、隔离、复测、放行或库存动作；
- 创建通知、工单或其他业务记录；
- 改变 Form 状态；
- 替代人工签名或提交校验。

媒体为空、媒体上传失败或媒体预览失败，不得改变既有 Form 的字段、状态和提交
规则；错误必须明确反馈给用户。

- 媒体上传、签名和提交之间没有新增顺序依赖；媒体可在签名前或签名后上传，提交
  是否需要签名继续按各 Form 已批准的 TDD 和 CC 执行。
- 媒体新增和删除只允许在 Form 草稿状态执行；提交后媒体只读，不能通过 Web 或
  PDA 修改已提交证据。

## 7. 权限和安全契约

- Web 和 PDA 必须使用相同的服务端媒体关系和权限边界；
- 未授权用户不能读取、上传、关联或删除媒体；
- 不得使用裸 SQL 或绕过 ORM 写入媒体关系；
- 不得将媒体内容写入仓库源码、临时公开目录或日志；
- 删除操作必须只针对当前 Form 关联的附件；
- 失败操作不得显示成功提示，也不得留下无法追踪的孤立关系。
- 本 CC 不要求媒体访问日志、Chatter 消息或独立审计模型；如业务需要，另立 CC。

## 8. 测试契约

| 测试 ID | 覆盖内容 | 类型 | 预期 |
|---|---|---|---|
| `CC-MEDIA-TEST-001` | Web 图片上传 | ORM/Playwright | 图片关联并可重新打开 |
| `CC-MEDIA-TEST-002` | Web 视频上传 | ORM/Playwright | 视频关联并可播放 |
| `CC-MEDIA-TEST-003` | PDA 拍照入口 | Playwright/人工 | 图片采集入口存在且可上传 |
| `CC-MEDIA-TEST-004` | PDA 录制入口 | Playwright/人工 | 视频采集入口存在且可上传 |
| `CC-MEDIA-TEST-005` | PDA 文件选择 | Playwright | 图片和视频均可选择 |
| `CC-MEDIA-TEST-006` | 预览和删除 | Playwright | 图片/视频预览及单项删除正确 |
| `CC-MEDIA-TEST-007` | 草稿恢复 | ORM/Playwright | PDA/Web 重新进入后媒体仍可见 |
| `CC-MEDIA-TEST-008` | 权限边界 | ORM/HTTP | 未授权访问被拒绝 |
| `CC-MEDIA-TEST-009` | 失败处理 | Playwright/ORM | 失败显示错误且不伪造成功 |
| `CC-MEDIA-TEST-010` | 大文件限制 | Playwright/ORM | 超过 10 MB 图片或 100 MB 视频被拒绝 |
| `CC-MEDIA-TEST-011` | 多文件上限 | Playwright/ORM | 超过 20 个媒体被拒绝；已成功文件保持正确 |
| `CC-MEDIA-TEST-012` | 不支持格式 | Playwright/ORM | `.exe` 等不支持类型被拒绝 |

## 9. 待用户确认事项

1. 是否批准三类 Form 统一支持图片和视频证据？
2. 是否批准 PDA 提供 `Take photo`、`Record video`、`Attach media` 三个入口？
3. 是否批准视频使用浏览器原生 HTML5 播放，不做转码和服务端缩略图？
   这意味着大视频文件直接存入 `ir.attachment`，部分视频编码（例如 H.265）
   可能无法在浏览器播放，也不会产生服务端缩略图；如需转码、压缩或格式限制，
   需要另立 CC。
4. 是否批准图片 10 MB、视频 100 MB、单条记录 20 个媒体的限制？
5. 是否批准继续使用现有 `ir.attachment` 和各 Form 的 `photo_ids` 关系？
6. 是否批准不抽取到公共模块，暂时继续由 `wd_qooling_app` 提供 Gallery？
   如需抽到 `wd_wms_widgets` 等公共模块，需要另行确认依赖关系和迁移范围。
7. 是否授权在本 CC 冻结后实施并进行模块升级、自动化测试和人工验证？

## 10. 验证记录

- Playwright 已验证 Temperature Record Web Evidence 图片和视频上传；
- Playwright 已验证 Temperature Record PDA 拍照、录制和附件入口；
- Playwright 已验证 Web/PDA 图片预览和视频弹窗播放；
- 用户已完成人工验证并确认通过。
