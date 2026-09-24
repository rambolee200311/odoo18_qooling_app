# Qooling Forms

Qooling Forms 是基于 Odoo 18 的仓储质量检查模块，提供 Inbound（入库）、
Outbound（出库）和 Temperature Control（温度记录）三类业务表单。

当前版本：`v1.0.0`

兼容 Odoo 18 Community / Enterprise，依赖 `base`、`web` 和 `stock`，使用
Python 3.10+ 的 Odoo 运行环境。

## 功能概览

- Web 和 PDA 双入口；
- Inbound、Outbound、Temperature 表单；
- 草稿保存、历史记录和已提交记录只读查看；
- PDA 单据编号和历史看板；
- 日期、单据编号模糊搜索、状态筛选；
- 图片、视频和附件证据；
- PDA/Web 手写签名；
- 英语默认语言；
- 荷兰语（`nl_NL`）和简体中文（`zh_CN`）翻译；
- 桌面表格和 PDA 窄屏卡片布局；
- Odoo ORM、权限和标准模块升级流程。

## 快速开始

1. 将 `mymodules` 加入 Odoo 的 `addons_path`。
2. 按下方安装命令安装 `wd_qooling_app`。
3. 登录 Odoo，确认主菜单出现 **Qooling**。
4. 进入后确认可以看到 Inbound、Outbound 和 Temperature 三个入口。
5. 选择业务类型，开始创建记录。

## 目录结构

```text
mymodules/wd_qooling_app/   Odoo 自定义模块
docs/context/designing/     SRS、TDD 和设计基线
docs/context/intent/        Coding Contract
docs/context/history/       IHR、ATR、HVR 实施与验证记录
docs/context/report/        PVR、PCR 项目收口记录
```

`mymodules/` 是 Odoo 模块源码，`docs/` 是项目文档；`docs/` 不会随
Odoo 模块安装包发布。

## 安装

将 `mymodules` 加入 Odoo 的 `addons_path`，安装模块：

```bash
venv/bin/python odoo-bin -c odoo.conf \
  -d <数据库名> \
  -i wd_qooling_app \
  --stop-after-init \
  --addons-path=<odoo-addons>,<custom-addons>
```

升级已有模块：

```bash
venv/bin/python odoo-bin -c odoo.conf \
  -d <数据库名> \
  -u wd_qooling_app \
  --stop-after-init \
  --addons-path=<odoo-addons>,<custom-addons>
```

模块升级会载入 `mymodules/wd_qooling_app/i18n/` 下的翻译目录。

安装成功后，登录 Odoo 并进入 Qooling 菜单；如果能看到 Inbound、Outbound
和 Temperature 三个入口，即表示模块入口加载成功。

## 使用入口

登录 Odoo 后进入 Qooling 菜单：

1. 选择 Inbound、Outbound 或 Temperature；
2. 可以从 Web 表单或 PDA 表单开始录入；
3. 使用“保存草稿”暂存记录；
4. PDA 入口先显示历史看板，可以打开草稿或已提交记录；
5. 已提交记录为只读；
6. 使用证据区域上传图片、录制视频或附加媒体；
7. 在签名区域完成签名后提交记录。
8. 提交后记录、表单字段、媒体和签名均不可修改；本版本不提供撤回流程，
   如需重新录入，请创建新记录并按业务流程处理。

PDA 看板支持 `From` / `To` 日期范围（包含起止日期）、单据编号模糊搜索、
状态下拉筛选、筛选区折叠和展开，以及桌面表格和窄屏卡片显示。
`Filter` 会应用当前全部筛选条件；`Clear` 会清空全部筛选条件并恢复默认列表。

## 语言

英语是源码默认语言和 fallback。用户语言由 Odoo 用户设置决定：

- English：使用英语源字符串；
- Nederlands：使用 `nl_NL`；
- 简体中文：使用 `zh_CN`。

当前模块目录中已登记的用户可见字符串均提供荷兰语和简体中文译文。
新增用户可见字符串时，必须在 `i18n/nl.po` 和 `i18n/zh_CN.po` 中补充
对应译文，并执行模块升级；没有译文的字符串会回退为英语。

修改翻译目录后，需要执行模块升级并重新加载浏览器资源。

## 证据限制

- 图片单个最大 `10 MB`；
- 视频单个最大 `100 MB`；
- 每条记录最多 `20` 个媒体文件；
- 提交后媒体和表单内容只读；
- 不执行服务端视频转码或独立缩略图服务。

以上限制由媒体 Coding Contract 定义，当前为代码中的硬限制，不提供系统
参数配置。当前版本也不支持离线填报。

## 验证和发布

项目级验证记录：

- PVR（Project Verification Record，项目验证记录）：
  [PVR](docs/context/report/PVR-20260924-001.md)
- PCR（Project Closure Report，项目收口报告）：
  [PCR](docs/context/report/PCR-20260924-001.md)
- HVR（Human Verification Record，人工验证记录）：
  [中文/荷兰语 i18n HVR](docs/context/history/HVR_INTENT-WD-QOOLING-I18N.md)

v1.0.0 已完成项目收口并创建 Git tag：

[v1.0.0](https://github.com/rambolee200311/odoo18_qooling_app/releases/tag/v1.0.0)

## 已知限制

- 提交后不支持修改或撤回；
- 不支持离线填报；
- 不执行服务端视频转码；
- 不提供独立视频缩略图服务；
- 媒体数量和大小限制当前不可通过系统参数调整。

## Changelog

### v1.0.0

- 初始版本，包含 Inbound、Outbound 和 Temperature 三类表单；
- 支持 Web 和 PDA 双入口；
- 支持草稿、提交、历史看板和筛选；
- 支持图片、视频、附件和手写签名证据；
- 支持英语默认、荷兰语和简体中文；
- 完成项目 PVR、PCR 和 v1.0.0 发布收口。

## 用户操作指南

详细用户操作见 [用户操作指南](docs/INSTRUCTION.md)。
