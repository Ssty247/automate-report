## 基本说明
此报告已经上传[github](https://github.com/LinshuZhang/automate-report)，clone下来之后查看更为方便。


## 环境配置(可直接复制粘贴到终端中运行)
### 1. 报告制作独立环境（env_name请使用你所习惯的环境命名）
conda create -n env_name python=3.6
### 2. 激活环境
source activate env_name
### 3. 基于requirements.txt安装依赖包
pip install -r requirements.txt

## 使用方式
### 1. 进入工作文件夹
在终端中使用cd命令进入此报告自动化教程要保存的文件夹目录
比如把此文件夹放在Documents 文件夹中（Mac系统)，依次执行
```
cd ~
cd Documents
```
就进入了工作目录
### 2. 下载教程
进入工作目录后，从github上clone本教程，方便直接执行查看
可以直接在Mac终端中执行如下：
```
git clone https://github.com/LinshuZhang/automate-report.git
```
这时候就已经在Documents文件夹中下载了教程文件夹 automate-report

### 3. 激活环境
执行如下，激活制作报告所用的独立python3环境
```
source activate env_name
```

### 4. 打开ipython notebook
```
jupyter notebook
```
### 4. 在浏览器中打开的notebook界面打开ipynb文件查看和执行此教程


