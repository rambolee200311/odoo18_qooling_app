# Qooling Forms 项目使用与实施说明

## 1. 适用范围

本文档说明 Qooling Forms v1.0.0 的安装、运行、验证和后续变更方式。
它面向开发人员、测试人员、实施人员和仓库业务用户。

## 2. 运行环境

- Odoo 18；
- Python 虚拟环境；
- PostgreSQL 由 Odoo 配置管理；
- 自定义模块目录：`mymodules/wd_qooling_app`；
- 推荐通过 Odoo ORM 访问业务数据；
- 不直接修改 Odoo 官方核心代码和官方模块。

## 3. 用户操作

### 3.1 Web 表单

1. 登录 Odoo；
2. 进入 Qooling 菜单；
3. 打开 Inbound、Outbound 或 Temperature；
4. 填写字段并保存草稿；
5. 按业务流程完成检查、媒体证据和签名；
6. 提交后记录进入只读状态。

### 3.2 PDA 表单

1. 从 Qooling PDA 入口进入对应业务类型；
2. 看板默认显示历史记录；
3. 使用日期、编号或状态筛选记录；
4. 草稿使用“编辑草稿”继续填写；
5. 已提交记录只能打开查看；
6. 使用“新建记录”创建新的 PDA 单据。

### 3.3 媒体和签名

- 图片可以拍照或上传；
- 视频可以录制或上传；
- 可以上传多个媒体文件；
- 记录保存后媒体与业务单据关联；
- 提交后不能继续编辑媒体；
- 签名必须在相应表单要求下完成；
- 删除媒体失败时页面必须显示错误通知。

## 4. 语言设置

语言由 Odoo 用户偏好控制，不由模块强制设置。

| 用户语言 | 代码 | 说明 |
|---|---|---|
| English | 默认 | 源字符串和 fallback |
| Nederlands | `nl_NL` | 荷兰语 |
| 简体中文 | `zh_CN` | 简体中文 |

如果修改了 `.po` 文件：

1. 执行模块升级；
2. 重新登录或刷新浏览器资源；
3. 检查 Web 和 PDA 的字段、选项、状态、错误提示和按钮；
4. 同时验证 Inbound、Outbound、Temperature 三类表单。

## 5. 开发变更流程

项目采用以下顺序：

```text
需求/SRS
  -> TDD
  -> Coding Contract
  -> 实施
  -> IHR
  -> ATR
  -> HVR
  -> FR
  -> PVR
  -> PCR
  -> Project Final Review
```

### 5.1 变更前

- 明确需求和适用范围；
- 检查已有 SRS、TDD、Coding Contract 和历史记录；
- 对行为变化先起草并冻结 Coding Contract；
- 明确 Web、PDA、权限、翻译、媒体和验证影响。

### 5.2 实施中

- 使用现有 ORM、服务、组件和翻译机制；
- 前端动态文案使用 Odoo `_t`；
- 不使用裸 SQL、`psql` 或直接数据库驱动；
- 不修改 Odoo 官方核心；
- 不删除文件或数据，除非获得明确授权；
- 错误必须显式显示，不能静默失败；
- 保持默认英语 fallback；
- 同步更新直接相关文档。

### 5.3 实施后

至少执行与变更范围匹配的检查：

```bash
node --check <changed-js-file>
msgfmt --check -o /tmp/catalog.mo <catalog.po>
```

XML 变更应进行 XML 解析检查，Odoo 模块变更应执行模块升级。
最终用户行为必须通过浏览器验证；自动化结果不能代替人工 HVR。

## 6. 翻译开发规则

- 源代码中的英语是默认显示内容；
- JavaScript 动态字符串必须通过 `_t("English source")`；
- PO 条目必须保留 Odoo 的 `module: wd_qooling_app` 元数据；
- JavaScript 条目使用 Odoo 识别的 `odoo-javascript` 标记；
- 不翻译模型名、字段技术名、技术缩写和单据编号；
- 用户可见字段名、下拉选项、按钮、错误和通知必须覆盖；
- 修改翻译后必须重新执行 Odoo 模块升级。

## 7. 发布检查清单

- [ ] 所有适用 SRS/TDD 已冻结；
- [ ] Coding Contract、IHR、ATR、HVR 可追溯；
- [ ] Web/PDA 三类表单验证通过；
- [ ] 英语、荷兰语、简体中文验证通过；
- [ ] 完整项目级回归测试通过；
- [ ] 最终权限矩阵通过；
- [ ] PVR 状态为 `COMPLETE`；
- [ ] PCR Closure 为 `SATISFIED`；
- [ ] Project Final Review 已确认发布；
- [ ] 创建并推送版本 tag。

## 8. 当前版本

- 版本：`v1.0.0`
- 模块版本：`18.0.1.0.0`
- PVR：[PVR-20260924-001](context/report/PVR-20260924-001.md)
- PCR：[PCR-20260924-001](context/report/PCR-20260924-001.md)
