# Qooling Forms 业务确认问卷

> 用途：请业务负责人填写本问卷，确认从 Qooling 下载的三个 Word 模板在 Odoo 首期迁移中的正式业务含义。  
> 对应需求：[SRS_qooling_forms.md](./SRS_qooling_forms.md)  
> 状态：已填写，部分业务规则仍待确认  
> 创建日期：2026-09-22

## 填写说明

- 请填写“业务确认”列；如不适用，请填写“NA”并说明原因。
- 如果需要选择，请填写正式选项，不要只填写“同上”。
- 如果不同仓库、货物类型或 ADR 状态有不同规则，请在备注中分别说明。
- 未确认的问题不会被视为默认值，也不会直接转化为 Odoo 模型或阻断规则。
- 填写完成后，本问卷将用于更新 SRS，并作为后续 TDD 的业务输入。

## 一、通用流程与权限

| 编号     | 待确认问题                                                                   | 业务确认                                                | 备注/依据 |
| ------ | ----------------------------------------------------------------------- | --------------------------------------------------- | ----- |
| GEN-01 | Inbound、Outbound、Weekly Temperature Control 是否全部纳入首期？如果分阶段，请给出顺序和每阶段范围。 | 全部放在首期                                              |       |
| GEN-02 | 三类表单由哪些角色创建、填写、提交、复核、跟进和关闭？                                             | 库管创建，仓库主管复核                                         |       |
| GEN-03 | 是否按仓库、公司、客户或业务区域隔离表单数据？具体隔离边界是什么？                                       | location即仓库，后面增加project，ref_no和业务单据关联，不需要公司，客户或业务区域 |       |
| GEN-04 | 表单的日期/时间使用哪个时区？由系统自动记录，还是允许用户手工修改？                                      | 系统自动记录，用户可以修改                                       |       |
| GEN-05 | 草稿是否允许反复修改？已提交记录是否允许更正？如允许，是否必须保留原始值和更正历史？                              | 草稿可以反复修改，已提交必须撤回到草稿状态修改，不需要保留原始值和更正历史               |       |
| GEN-06 | 哪些字段是提交前必填？哪些检查项未通过时必须阻止提交？                                             | 这个问题太大，你应该分表单和字段进行提问                                |       |
| GEN-07 | 发现异常时，是只保留表单异常，还是自动创建 Issue/Task/Procedure？责任人和关闭条件是什么？                 | 不懂你的异常是指什么                                          |       |
| GEN-08 | 表单是否需要关联 Odoo 入库单、出库单、运输单、产品、批次或集装箱记录？由用户选择还是系统自动匹配？                    | 关联，用户选择对象和ID                                        |       |
| GEN-09 | 三类表单的照片、备注和签名是否必填？允许上传哪些文件类型和数量？                                        | 签名提交时必填，照片，备注非必填                                    |       |
| GEN-10 | 是否需要迁移 Qooling 历史表单？如果需要，迁移时间范围、字段范围和附件范围是什么？                           | 不需要                                                 |       |

## 二、Inbound / 货物接收表

来源模板：[货物接收表.docx](/Users/lijianqiang/Documents/odoo18_qooling/docs/requirement/货物接收表.docx)

### 2.1 基础字段和选项

| 编号    | 待确认问题                                                               | 业务确认                                                                                                                                         | 备注/依据 |
| ----- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| IN-01 | `Location` 的正式选项是什么？当前材料出现 `MAS`、`SHA`、`SPN`，是否完整？                  | 就是仓库档案，必填                                                                                                                                    |       |
| IN-02 | `Supervisor` 是否必须填写？是否只能从 Odoo 用户/员工中选择？                            | 用户，必填                                                                                                                                        |       |
| IN-03 | `Goods Status` 的正式选项是什么？是否包括 Bonded、T1、Free/Union goods？            | 1、Vrije goederen (unions goods) / Free union goods (not bonded) / 自由商品（工会商品）
2、T1 (niet-uniegoederen) / T1 (non-union goods) / T1（非统一货物）
，必填 |       |
| IN-04 | `Unloading permission received?` 的选项是什么？是否为 Yes/No？选择 No 是否阻止提交或卸货？ | 1、Ja / Yes / 是的
2、Nee, stop het lossen en vraag project manager / No, stop unloading and ask project manager / 不，停止卸货并询问项目经理
，必填             |       |
| IN-05 | `MRN Number` 的格式、是否必填、是否需要校验唯一性或格式？                                 | 文本，非必填                                                                                                                                       |       |
| IN-06 | `Seal Number` 的格式和是否必填？一个集装箱是否允许多个密封编号？                             | 文本，非必填，允许，用逗号连接                                                                                                                              |       |
| IN-07 | `SKAL / BIO Product` 的正式选项是什么？是否为 Yes/No/Not Applicable？            | 1、Ja / Yes / 是的
2、Nee/ No / 不是                                                                                                               |       |
| IN-08 | `B/L` 是否必填？是否需要关联 Odoo 入库或运输业务？                                     | 文本，非必填                                                                                                                                       |       |
| IN-09 | `Container Number / Shipment Number` 是二选一还是可同时填写？格式如何校验？            | 文本，非必填                                                                                                                                       |       |
| IN-10 | `Number` 是 Qooling 表单编号、业务编号还是人工填写编号？是否由系统自动生成？                     | 系统自动生成                                                                                                                                       |       |
| IN-11 | `Filled in by` 与仓库操作员是否是同一概念？是否自动取当前用户？                             | 自动取当前用户                                                                                                                                      |       |
| IN-12 | `Filing date` 是提交日期、归档日期还是人工填写日期？                                   | 填写日期                                                                                                                                         |       |

### 2.2 检查项和条件规则

| 编号    | 待确认问题                                                                                       | 业务确认                                                                                                                                                                                                                                                                                                                      | 备注/依据 |
| ----- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| IN-13 | 模板中的 `Checkbox list` 具体包含哪些检查项？请列出每一项的正式名称。                                                 | 1、Gecontroleerd op zichtbare schade of verpakkingsproblemen/Checked for visible damage or packaging issues / 检查是否有明显损坏或包装问题
2、Aantal ontvangen is gecontroleerd/Number received has been checked / 已检查收到的号码
3、Productkwaliteit en -conditie zijn gecontroleerd/Product quality and condition have been checked/产品质量和状况已检查 |       |
| IN-14 | `Checkbox list` 每一项的选项是什么？例如 Yes/No、合格/不合格、N/A。                                             | 同in-13                                                                                                                                                                                                                                                                                                                    |       |
| IN-15 | `Packaging condition` 的正式选项和异常处理是什么？                                                        | `Good`；`Not good`：停止卸货并联系项目经理获取进一步指示                                                                                                                                                                                                                                                                                                                   |       |
| IN-16 | 是否需要记录批次/批号、数量、标签可读性、纸箱数量和托盘数量？这些字段是否在 Checkbox list 中？                                     | 否                                                                                                                                                                                                                                                                                                                         |       |
| IN-17 | `Gas measurement` 是否使用 Yes/No/Not Applicable？什么情况下选择 Not Applicable？                        | `Ja / Yes / 是的`；`Nee / No / 不`；`n.v.t. / Not Applicable / 不适用`，由用户选择                                                                                                                                                                                                                                                                                                              |       |
| IN-18 | 气体测量的 `Status` 正式选项是什么？是否需要记录测量值、单位、时间和仪器？                                                  | 1、Veilig / Safe / 安全的
2、Ventilatie nodig / Ventilation required / 需要通风
3、Gevaarlijk / Dangerous / 危险的                                                                                                                                                                                                                     |       |
| IN-19 | `Ventilated` 的正式选项是什么？选择 No 或异常状态是否阻止收货？                                                    | 1、Ja / Yes / 是的
2、n.v.t / not applicable / 不适用                                                                                                                                                                                                                                                                            |       |
| IN-20 | `Status after ventilation` 的正式选项是什么？通风后仍不合格时如何处理？                                           | 1、Veilig / Safe / 安全的
2、Ventilatie nodig / Ventilation required / 需要通风
3、Gevaarlijk / Dangerous / 危险的                                                                                                                                                                                                                     |       |
| IN-21 | `ADR` 的正式选项是什么？ADR 为 Yes 时必须填写哪些字段和检查项？                                                     | 1、Ja / Yes / 是的
2、Nee / No / 不
yes时，IN-22，IN-23显示必填，no时，IN-22，IN-23隐藏                                                                                                                                                                                                                                                     |       |
| IN-22 | `UN Number` 是否只允许 `3171`、`3480`、`3481`？是否还存在其他编号？                                           | 只允许3171，3480，3481                                                                                                                                                                                                                                                                                                         |       |
| IN-23 | `Temperature measured` 和 `Temperature of each pallet is registered` 是 Yes/No 选择，还是需要记录实际温度？ | 1、Ja / Yes / 是的<br/>2、Nee / No / 不                                                                                                                                                                                                                                                                                        |       |
| IN-24 | `Average temperature per pallet` 的单位、允许范围和异常阈值是什么？                                          | 这个不归IT管，用户录入                                                                                                                                                                                                                                                                                                              |       |
| IN-25 | 发现包装、货物、气体、通风、温度或 ADR 异常时，是否允许提交？提交后必须执行什么处置？                                               | 这个不管IT管，用户决策                                                                                                                                                                                                                                                                                                              |       |

## 三、Outbound / 出库表

来源模板：[出库表.docx](/Users/lijianqiang/Documents/odoo18_qooling/docs/requirement/出库表.docx)

### 3.1 基础字段和时间

| 编号     | 待确认问题                                                        | 业务确认                    | 备注/依据 |
| ------ | ------------------------------------------------------------ | ----------------------- | ----- |
| OUT-01 | `Reference / Verzendingsnummer` 的正式含义和格式是什么？是否必须关联 Odoo 出库单？ | 手工录入，无需关联               |       |
| OUT-02 | 到达时间、开始装载时间和结束装载时间是否全部必填？时间顺序如何校验？                           | 必填，到达时间<=开始装载时间<=结束转载时间 |       |
| OUT-03 | `Supervisor / Manager` 是否必填？是否自动取当前负责人？                      | 必填，手工选择用户               |       |
| OUT-04 | `Goods type` 的正式选项是什么？是否包括 Bonded、Non-Bonded？                | Bonded、Non-Bonded？      |       |
| OUT-05 | `MRN Number` 和 `Seal Number` 是否必填？格式如何校验？                    | 非必填，文本型                 |       |
| OUT-06 | `MRN checked before release` 是否为放行前强制检查？未核查时是否禁止提交或放行？       | 这个不归IT管，用户决策            |       |
| OUT-07 | `Filled in by`、`Filing date` 和 `Number` 的含义及生成规则是什么？         | 系统用户，系统时间，自动编号          |       |

### 3.2 货物、ADR 和装载检查

| 编号     | 待确认问题                                                         | 业务确认                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 备注/依据 |
| ------ | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| OUT-08 | `Check Loading` 具体包含哪些检查项？请列出完整清单。                            | 1、Gecontroleerd op zichtbare schade of verpakkingsproblemen
 2、Geladen hoeveelheid is gecontroleerd                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |       |
| OUT-09 | `Cargo inspection` 具体包含哪些检查项？是否包括包装、损坏、标识、数量和货物固定？            | Ladinginspectie/Cargo inspection/货物检查<br/><br/> Verpakkingstoestand/Packaging condition/包装状态<br/><br/> Juiste etikettering/Correct labeling/正确标识<br/><br/> Vastzetten van goederen in de vrachtwagen voor transport/Securing goods in the truck for transport/在卡车上固定货物以备运输                                                                                                                                                                                                                                                                                                                     |       |
| OUT-10 | `Vehicle inspection` 具体包含哪些检查项？请列出车辆证书、灭火器、ADR 标志等正式清单。       | Voertuigcontrole/ Vehicle inspection/车辆检验<br/><br/> ADR-certificaat van goedkeuring/ADR certificate of approval/ADR认证证书<br/><br/> Brandblusser/Fire extinguisher/灭火器<br/><br/> ADR-borden/ADR signs/ADR标志<br/><br/> Ladingszekeringsmateriaal/Load securing material/货物固定材料<br/><br/> Schriftelijke instructies (TREM-kaarten)/Written instructions (TREM cards)/书面说明（TREM卡片）                                                                                                                                                                                                                  |       |
| OUT-11 | `Driver check` 具体包含哪些检查项？请列出司机证书、防护用品和其他要求。                   | Chauffeurscontrole/Driver check/驾驶员检查<br/><br/> ADR-chauffeurscertificaat/ADR driver certificate/ADR驾驶员证书<br/><br/> Reflecterend veiligheidsvest/Reflective safety vest/反光安全背心<br/><br/> Oogbescherming/Eye protection/护目装置<br/><br/> Beschermende handschoenen/Protective gloves/防护手套<br/><br/> Stopblokken/Stop blocks/停止块<br/><br/> Afdekzeil/Tarpaulin/帆布<br/><br/> Zaklamp/Flashlight/手电筒<br/><br/> Schep/Spade/铲子<br/><br/> Opvangbak/Drip tray/滴水盘<br/><br/> Oogspoelfles/Eyewash bottle/洗眼瓶<br/><br/> Twee vrijstaande gevarendriehoeken/Two freestanding warning triangles/两个独立式警示三角牌 |       |
| OUT-12 | 每个检查项的选项是什么？是否使用 Yes/No/Not Applicable？                       | 见上                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |       |
| OUT-13 | `ADR` 为 Yes 时，必须完成哪些车辆、司机和装载检查？                               | 是                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |       |
| OUT-14 | `UN Number` 是否只允许 `3171`、`3480`、`3481`？                       | 是                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |       |
| OUT-15 | `Proper Shipping Name` 的来源和填写规则是什么？是否由 UN 编号自动带出？             | 否，手工填写                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |       |
| OUT-16 | `Measured temperature (average, °C)` 的测量对象、单位、允许范围和异常阈值是什么？   | 这个不归IT管，用户填写                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |       |
| OUT-17 | `Loading plan discussed with driver?` 是否为强制 Yes？选择 No 是否阻止提交？ | 不强制                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |       |
| OUT-18 | ADR 分离/兼容性检查在非 ADR 货物时应选择 N/A 还是自动隐藏？                         | 不隐藏                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |       |
| OUT-19 | 重量分布检查的判断标准和不合格处置是什么？                                         | 这个不归IT管，用户决策                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |       |

### 3.3 司机、仓库签名和证据

| 编号     | 待确认问题                                                     | 业务确认       | 备注/依据 |
| ------ | --------------------------------------------------------- | ---------- | ----- |
| OUT-20 | `Driver's comments` 是否必填？异常时是否必须填写？                       | 否          |       |
| OUT-21 | `Driver's signature agreement` 是否必填？司机拒绝签名时如何处理？          | 必填，手写，不能保存 |       |
| OUT-22 | `Photo of cargo` 是否必填？需要几张照片、何时拍摄、是否必须包含装载完成状态？           | 已确认：非必填，不作为提交阻断条件   |       |
| OUT-23 | `Warehouse operator comments` 是否必填？                       | 否          |       |
| OUT-24 | `Warehouse operator signature` 是否必填？签名是手写签名、电子确认还是当前用户身份？ | 必填，手写，不能保存 |       |
| OUT-25 | 车辆、司机、货物或装载检查不合格时，是否禁止出库放行？谁可以批准例外？                       | 人工复核决定，系统只记录结果      |       |

## 四、Weekly Temperature Control / 每周温度控制记录表

来源模板：[每周温度控制记录表.docx](/Users/lijianqiang/Documents/odoo18_qooling/docs/requirement/每周温度控制记录表.docx)

### 4.1 周期和基础字段

| 编号     | 待确认问题                                                | 业务确认       | 备注/依据 |
| ------ | ---------------------------------------------------- | ---------- | ----- |
| TMP-01 | 温度控制是否严格每周一次？周期按自然周、工作周还是上次检查后 7 天计算？                | 目前的记录是每天都有 |       |
| TMP-02 | `Manager` 是否必须填写？是否自动取当前负责人？                         | 选择用户       |       |
| TMP-03 | `Customer` 是否必须填写？是否允许一个记录对应多个客户？                    | 必填         |       |
| TMP-04 | `Container Number` 是否必须填写？一个温度记录是否允许多个集装箱？           | 必填         |       |
| TMP-05 | `Number`、`Filled in by` 和 `Filing date` 的含义及生成规则是什么？ | 自动，系统，系统   |       |

### 4.2 托盘温度

| 编号     | 待确认问题                                         | 业务确认                     | 备注/依据 |
| ------ | --------------------------------------------- | ------------------------ | ----- |
| TMP-06 | 每次实际检查是否只填写 `Total Pallets` 数量对应的托盘字段，其余字段留空？ | odoo里不需要固定65个，用户动态记录托和温度 |       |
| TMP-07 | 是否允许实际托盘数量超过 65 个？如果超过，如何处理？                  | 超过65个，新单                 |       |
| TMP-08 | 温度单位是否固定为摄氏度（°C）？是否允许其他单位？                    | 摄氏度                      |       |
| TMP-09 | 每个托盘填写单次温度、平均温度，还是允许多次测量并保存原始读数？              | 人工复核决定，系统只记录结果                    |       |
| TMP-10 | 托盘温度的正常范围、预警阈值和强制隔离阈值是什么？                     | 人工复核决定，系统只记录结果                    |       |
| TMP-11 | 截图中的电池温度 `>40°C` 是否为正式隔离阈值？是否适用于所有产品和托盘？      | 人工复核决定，系统只记录结果                    |       |
| TMP-12 | 多个托盘异常时，是否必须在集装箱外适应约 20 分钟后复测？等待时间是否固定？       | 人工复核决定，系统只记录结果                    |       |
| TMP-13 | 复测仍异常时，隔离对象、责任人、位置和后续流程是什么？                   | 人工复核决定，系统只记录结果                    |       |

### 4.3 损坏、泄漏和存储稳定性

| 编号     | 待确认问题                                        | 业务确认                                                                                                                                                                                                   | 备注/依据 |
| ------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----- |
| TMP-14 | 包装可见损坏的正式选项是什么？选择 Yes 后是否必须填写备注、照片或创建 Issue？ | - Zijn er beschadigingen zichtbaar aan de verpakking? / Is there any visible damage to the packaging? / 包装是否有可见损坏？<br/>  <br/>  checkbox-Nee / No / 否                                                  |       |
| TMP-15 | 未包装产品壳体可见损坏的正式选项和处理规则是什么？                    | - Zijn er beschadigingen zichtbaar aan de behuizing van onverpakt producten? / Is there any visible damage to the casing of unpackaged products? / 未包装产品的壳体是否有可见损坏？<br/>  <br/>  checkbox-Nee / No / 否 |       |
| TMP-16 | 电解液泄漏的正式选项和处理规则是什么？是否立即隔离？                   | 人工复核决定，系统只记录结果                                                                                                                                                                                                  |       |
| TMP-17 | 存储稳定性的判断标准是什么？检查托盘放置、堆叠方式和哪些其他条件？            | 人工复核决定，系统只记录结果                                                                                                                                                                                                  |       |
| TMP-18 | 上述任一异常是否阻止提交？是否允许先提交为异常待处理？                  | 人工复核决定，系统只记录结果                                                                                                                                                                                                  |       |

### 4.4 证据和签名

| 编号     | 待确认问题                                       | 业务确认  | 备注/依据 |
| ------ | ------------------------------------------- | ----- | ----- |
| TMP-19 | `Attach photo (if necessary)` 在什么情况下必须上传照片？ | 已确认：图片上传非强制，不作为提交阻断条件 |       |
| TMP-20 | `Comments` 是否在异常时必填？                        | 否     |       |
| TMP-21 | `Signature` 是否必填？签名代表谁的确认？                  | 必填，手写 |       |

## 五、确认完成检查

| 检查项                             | 完成情况 |
| ------------------------------- |:----:|
| 三类表单的字段选项已确认                    |      |
| 三类表单的必填字段已确认                    |      |
| 三类表单的阻断检查项已确认                   |      |
| ADR 和 UN 编号规则已确认                |      |
| 温度单位、阈值、复测和隔离规则已确认              |      |
| 异常、Issue/Task/Procedure 跟进规则已确认 |      |
| 签名、照片、备注和归档规则已确认                |      |
| 角色、权限和数据隔离已确认                   |      |
| 是否迁移历史 Qooling 数据已确认            |      |

## 六、业务负责人确认

| 项目      | 内容  |
| ------- | --- |
| 业务负责人   |     |
| 所属部门    |     |
| 确认日期    |     |
| 签名/确认方式 |     |
| 补充说明    |     |
