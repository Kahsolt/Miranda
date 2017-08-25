# Miranda
    Miranda the sub-Project of Uranus...
    A face-detect based registering module using python2.7 :)

# Install
  - Linux
    - 安装软件仓库包依赖
      - apt install python2.7
      - apt install python-opencv
	- 安装python包依赖
	  - pip install requests
	  - pip install flask	(Optional, for the dummy server use)
  - Windows(制作一个Python环境)
    - 安装Miniconda2或纯Python2.7环境
	  - Miniconda: [https://conda.io/miniconda.html]
	  - Python2.7: [https://www.python.org/]
	- 安装python包依赖
	  - conda install numpy requests (For Miniconda2)
	  - pip install numpy requests (For Native Python2.7)
	- 添加OpenCV包
		- 下载OpenCV二进制发行包
		  - [http://opencv.org/releases.html]
		- 拷贝opencv的二进制文件到python的库文件夹中
		  - copy %OpenCV Root%\build\python\2.7\cv2.pyd %Python Root%\Lib\site-packages\

# Run 
- [startup]
  - python miranda.py
- [shutdown]
  - 按ESC键，销毁GUI释放内存需要等几秒钟:(

# Configs
  - Miranda/settings.py

# Dummy Test Server
  - python Miranda/server.py
  - 访问 [http://localhost:5000]
  - 主页可以控制服务端的状态，客户端应该会及时轮询响应变化

---
# TODO
  - 性能优化？
  - 多平台？
