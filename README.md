# Qooling Forms

Qooling Forms 是基于 Odoo 18 的仓储质量检查模块，提供 Inbound（入库）、
Outbound（出库）和 Temperature Control（温度记录）三类业务表单。

当前版本：`v1.0.0`

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

## 目录结构

```text
mymodules/wd_qooling_app/   Odoo 自定义模块
docs/context/designing/     SRS、TDD 和设计基线
docs/context/intent/        Coding Contract
docs/context/history/       IHR、ATR、HVR 实施与验证记录
docs/context/report/        PVR、PCR 项目收口记录
```

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

## 使用入口

登录 Odoo 后进入 Qooling 菜单：

1. 选择 Inbound、Outbound 或 Temperature；
2. 可以从 Web 表单或 PDA 表单开始录入；
3. 使用“保存草稿”暂存记录；
4. PDA 入口先显示历史看板，可以打开草稿或已提交记录；
5. 已提交记录为只读；
6. 使用证据区域上传图片、录制视频或附加媒体；
7. 在签名区域完成签名后提交记录。

PDA 看板支持：

- `From` / `To` 日期范围，包含起止日期；
- 单据编号模糊搜索；
- 状态下拉筛选；
- `Filter` 和 `Clear`；
- 筛选区折叠和展开；
- 桌面表格和窄屏卡片显示。

## 语言

英语是源码默认语言和 fallback。用户语言由 Odoo 用户设置决定：

- English：使用英语源字符串；
- Nederlands：使用 `nl_NL`；
- 简体中文：使用 `zh_CN`。

修改翻译目录后，需要执行模块升级并重新加载浏览器资源。

## 证据限制

- 图片单个最大 `10 MB`；
- 视频单个最大 `100 MB`；
- 每条记录最多 `20` 个媒体文件；
- 提交后媒体和表单内容只读；
- 不执行服务端视频转码或独立缩略图服务。

## 验证和发布

项目级验证记录：

- [PVR](docs/context/report/PVR-20260924-001.md)
- [PCR](docs/context/report/PCR-20260924-001.md)
- [中文/荷兰语 i18n HVR](docs/context/history/HVR_INTENT-WD-QOOLING-I18N.md)

v1.0.0 已完成项目收口并创建 Git tag：

```text
v1.0.0
```

## 开发纪律

详细用户操作见 [用户操作指南](docs/INSTRUCTION.md)。
