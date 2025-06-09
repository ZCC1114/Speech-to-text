# Speech-to-text

根据上传的语音文件，自动识别并输出 AB 对话形式。

## 使用说明



## Node.js 实现

如果不方便配置 Python 环境，可以使用 Deepgram API 的 Node.js 版本。

1. 安装依赖（需要 Node.js）：
   ```bash
   npm install
   ```
2. 在 <https://console.deepgram.com/signup> 获取 API Key，保存到 `DEEPGRAM_API_KEY` 环境变量：
   ```bash
   export DEEPGRAM_API_KEY=YOUR_KEY
   ```
3. 转写音频：
   ```bash
   node dg_transcribe.js <audio_path> > dialog.txt
   ```
4. 启动 Web 页面：
   ```bash
   node dg_web_app.js
   ```
   在浏览器访问 `http://localhost:3000` 上传音频文件即可。

