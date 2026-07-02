# GTNH 配方 Java 源码路径对照表

## 源码仓库

`GT5-Unofficial/src/main/java/gregtech/loaders/postload/recipes/`

## 配方文件对照

| 文件 | 内容 |
|------|------|
| DistilleryRecipes.java | 蒸馏/蒸馏室配方 |
| ChemicalRecipes.java | LCR 脱硫/CBD/TNM/HNO3/乙烯酮/乙酸/硫酸/甲烷水化 |
| MixerRecipes.java | 搅拌机配方（柴油等） |
| ElectrolyzerRecipes.java | 电解水/糖电解 |
| CentrifugeRecipes.java | 离心空气分离 |
| CompressorRecipes.java | 压缩空气 |
| GTProxy.java | 裂化自动生成 |
| CrackRecipeAdder.java | 裂化配方 |

## 配方双重验证流程

1. 查对应 Java 文件获取 EU/t、耗时、输入输出
2. 向用户确认 NEI 中显示数据是否一致
3. 若不一致，以 NEI 为准（可能被整合包魔改）
