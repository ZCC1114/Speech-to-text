# Speech-to-text

根据上传的语音文件，自动识别并输出 AB 对话形式。

## 使用说明

1. 安装依赖（确保系统已安装 `ffmpeg`）：
   ```bash
   pip install -U openai-whisper pyannote.audio
   ```
   `pyannote.audio` 需要额外的依赖，可参考其官方文档进行安装。

2. 访问 <https://hf.co/pyannote/speaker-diarization> 接受协议，并在
   <https://hf.co/settings/tokens> 创建访问令牌（假设为 `YOUR_TOKEN`）。
   将令牌保存到环境变量 `HF_TOKEN`：
   ```bash
   export HF_TOKEN=YOUR_TOKEN
   ```

3. 运行脚本：


脚本会调用 `openai-whisper` 进行转写，并通过 `pyannote.audio` 完成说话人分离，最终按 “A:” / “B:” 的形式保存到指定文件。
4. 启动 Web 测试页：

脚本会调用 `whisper` 进行转写，并通过 `pyannote.audio` 完成说话人分离，最终按 “A:” / “B:” 的形式保存到指定文件。

