# 报告自动化快速教程
## 基本说明
本教程对知识水平要求不高，主要是把日常制作报告进行自动化的一种思路分享。
此外其中图表制作部分为用Python制作Excel形式表格做出了教程和示例，为office制作的报告升级为Python自动化制作提供既有的模板。

## 环境配置(可直接复制粘贴到终端中运行)
### 1. 报告制作独立环境（env_name请使用你所习惯的环境命名）
conda create -n env_name python=3.6
### 2. 激活环境
source activate env_name
### 3. 基于requirements.txt安装依赖包
pip install -r requirements.txt

## 使用方式
### 1. 在终端中使用cd命令进入此auto report文件夹所在目录
比如把 auto report文件夹放在Documents 文件夹中（Mac系统)，依次执行
```
cd ~
cd Documents
cd auto report
```
就进入了工作目录
### 2. 进入工作目录后，激活环境
```
source activate env_name
```
### 3. 打开ipython notebook
```
jupyter notebook
```
### 4. 在浏览器中打开的notebook界面打开ipynb文件查看教程

