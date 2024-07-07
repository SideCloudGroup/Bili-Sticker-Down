# Bili-Sticker-Down

## 介绍

'一键'下载B站装扮的表情包，并自动化进行超分辨率（使用[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)）和尺寸调整。

## 使用方法

1. 使用Git Clone或者下载ZIP文件到本地
2. 获取B站装扮ID。分享链接中的 `id=114514` 即为ID。
3. 调整配置文件 `config.toml`。填入装扮ID，并按需调整其他参数。
4. 如需使用超分辨率，请手动下载可执行文件。**如不需要使用则跳过此步骤**。以下是详细说明： \
   下载可执行文件：[Windows版](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip) / [Linux版](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip) / [macOS版](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-macos.zip) \
   解压所有文件到该项目目录的 `realesrgan` 文件夹内 \
   在配置文件中修改可执行文件路径
5. 安装依赖
    ```bash
   pip install -r requirements.txt
    ```
6. 运行程序
   ```bash
   python main.py
   ```

