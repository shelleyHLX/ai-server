# ai-server

[![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/deepmipt/DeepPavlov/blob/master/LICENSE) ![](https://img.shields.io/badge/Language-Python-blue.svg) ![](https://img.shields.io/badge/Python-3.X-red.svg)

server for NLP、CV、Speech AI application.

**ai-server**基于开源工具构建自然语言处理、图像处理、语音处理等多种人工智能服务。

## 特征
### 自然语言处理（NLP）

- [√] 词法分析
- [√] 词向量表示
- [√] 词义相似度
- [√] 短文本相似度
- [√] 语言模型
- [√] 情感倾向分析
- [√] 文章标签
- [√] 文章分类
- [√] 文本纠错
- [x] 文本审核


### 计算机视觉（CV）

- [√] 通用文字提取
- [x] 证件照提取
- [√] 图像识别
- [√] 图像检测
- [√] 图像修复
- [x] 对比度增强
- [x] 水印检测
- [x] 广告检测
- [x] 色情检测
- [x] 涉政检测
- [√] 图像质量检测
- [x] 标签搜图
- [x] 相似图片搜索
- [√] 图像比对
- [√] 图像着色
- [√] 特效合成
- [√] 数字化妆
- [x] 灵魂画师


### 语音技术（Speech）

- [√] 语音识别
- [√] 语音合成



## demo

http://www.borntowin.cn


## 使用说明

### 依赖安装
pip3 install -r requirements.txt

#### 安装过程记录
```
CentOS 7.5 安装


[问]如何在CentOS 7上安装python3?
[答]从EPEL仓库安装:
最新的EPEL 7仓库提供了Python3（python 3.6）的安装源，如果你使用CentOS7或更新的版本的系统你也可以按照下面的步骤很轻松的从EPEL仓库安装。
安装最新版本的EPEL
$ sudo yum install epel-release


用yum安装python 3.6:
$ sudo yum install python36


注意：上面的安装方法并未安装pip和setuptools，如果你要安装这两个库可以使用下面的命令：
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ sudo /usr/bin/python36 get-pip.py


[问]如何在CentOS 7上安装Nginx?
[答]第一步 - 添加Nginx存储库
要添加CentOS 7 EPEL仓库，请打开终端并使用以下命令：
sudo yum install epel-release
第二步 - 安装Nginx
现在Nginx存储库已经安装在您的服务器上，使用以下yum命令安装Nginx ：
sudo yum install nginx

在对提示回答yes后，Nginx将在服务器上完成安装。
第三步 - 启动Nginx
Nginx不会自行启动。要运行Nginx，请输入：
sudo systemctl start nginx

如果您正在运行防火墙，请运行以下命令以允许HTTP和HTTPS通信：
  1. sudo firewall-cmd --permanent --zone=public --add-service=http
  2. sudo firewall-cmd --permanent --zone=public --add-service=https
  3. sudo firewall-cmd --reload
您将会看到默认的CentOS 7 Nginx网页。
如果想在系统启动时启用Nginx。请输入以下命令：
sudo systemctl enable nginx


[问]Python.h：没有那个文件或目录？
[答]sudo yum install python-devel
由于我的是python36，以上命令不成功，下面可以：
sudo yum install python36-devel


[问]安装matplotlib库时，找不到tkinter包？
[答]yum install python3-tk


[问]出错：nginx: [error] invalid PID number “” in “/usr/local/var/run/nginx/nginx.pid”？
[答]解决办法：
$ sudo nginx -c /etc/nginx/nginx.conf
$ sudo nginx -s reload


[问]出错：Nginx 错误处理方法: bind() to 0.0.0.0:80 failed？
[答]解决方法：kill 占用端口的进程。
ps -ef|grep nginx
kill -9


[问]如何安装dlib?
[答]dib 安装方法：
Clone the code from github:
git clone https://github.com/davisking/dlib.git
Build the main dlib library (optional if you just want to use Python):
cd dlib
mkdir build; cd build; cmake ..; cmake --build .
Build and install the Python extensions:
cd ..
python3 setup.py install
At this point, you should be able to run python3 and type import dlib successfully.


[问]如何安装kenlm?
[答]按照官方方法编译按装：https://blog.csdn.net/mingzai624/article/details/79560063


[问]cmake Could NOT find ZLIB (missing: ZLIB_LIBRARY)?
[答]1. 安装zlib:yum install zlib1g zlib1g-dev
2. 执行这句语句就可以了:
cmake .. -DZLIB_INCLUDE_DIR=/usr/include -DZLIB_LIBRARY=/usr/lib
3. sudo pip3 install kenlm


[问]如何安装pyaudio?
[答]brew install portaudio (centos使用：yum install portaudio.不管用,用下面的自己编译）
pip3 install pyaudio


[问]Linux系统下pyaudio安装缺少文件问题error: portaudio.h: 没有那个文件或目录?
[答]源码编译安装portaudio:
pyaudio的运行需要依赖于portaudio这个库，应该先安装一个portaudio库

portaudio安装步骤：
　　a)下载portaudio库http://portaudio.com/download.html
wget http://portaudio.com/archives/pa_stable_v19_20140130.tgz

　　b)将下载的文件进行解压
tar -zxvf pa_stable_v19_20140130.tgz

　　c)进入解压后的portaudio文件，依次执行命令：
　　　　./configure
　　　　make
　　　　make install
　　d)进入~/.bashrc文件：vim ~/.bashrc
　　　　在文件最后一行加入  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
　　　　然后执行命令ldconfig

之后，pip3 install pyaudio


```




## 贡献及优化点（TODO）

* 主题提取
* 摘要提取
* 图片检索及细粒度识别
* 深度语音仿人声模型

## 参考

1. [基于文法模型的中文纠错系统](https://blog.csdn.net/mingzai624/article/details/82390382)
2. [Imageai](https://github.com/OlafenwaMoses/ImageAI)
3. [HanTTS](https://github.com/junzew/HanTTS)
4. [pix2pix](https://github.com/phillipi/pix2pix)
5. [chinese_ocr](https://github.com/YCG09/chinese_ocr)
6. [faceai](https://github.com/vipstone/faceai)
7. [pycorrector](https://github.com/shibing624/pycorrector)

