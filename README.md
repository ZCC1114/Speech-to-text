# Speech-to-text

根据上传的语音文件，自动识别并输出 AB 对话形式。

## 使用说明

1. 安装依赖：
   ```bash
   pip install whisper pyannote.audio
   ```
   `pyannote.audio` 需要额外的依赖，可参考其官方文档进行安装。

2. 运行脚本：
   ```bash
   python ab_transcribe.py <audio_path> --output dialog.txt
   ```

脚本会调用 `whisper` 进行转写，并通过 `pyannote.audio` 完成说话人分离，最终按 “A:” / “B:” 的形式保存到指定文件。

