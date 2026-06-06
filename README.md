<div align="center">

# 🎬 DubVoice — AI Automation Studio

**Powerful desktop automation toolkit for creators.**
Voiceover (TTS), AI image & video generation, a node-based workflow editor,
and a built-in local REST API (Webhook) for n8n / Make / Zapier.

[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)](https://github.com/Dubvoice/Dubvoice-Automation/releases)
[![Made with Python](https://img.shields.io/badge/made%20with-Python-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Powered by dubvoice.ai](https://img.shields.io/badge/powered%20by-dubvoice.ai-5b6cff)](https://www.dubvoice.ai)

</div>

---

## 📥 Download

| Platform | GitHub | Google Drive |
| :------- | :----- | :----------- |
| 🪟 **Windows** | <!-- GH_WIN -->[DubVoice-Windows.zip](https://github.com/Dubvoice/Dubvoice-Automation/releases/latest/download/DubVoice-Windows.zip) | <!-- DRIVE_WIN -->[Google Drive](https://drive.google.com/file/d/1C4XoHi049ogvlSfD9nlx0_FKMKZvOkfu/view?usp=sharing) |
| 🍎 **macOS — Intel** | <!-- GH_MAC_INTEL -->_coming soon_ | <!-- DRIVE_MAC_INTEL -->_coming soon_ |
| 🍎 **macOS — Apple Silicon** | <!-- GH_MAC_ARM -->_coming soon_ | <!-- DRIVE_MAC_ARM -->_coming soon_ |

---

## ✨ Features

- **🎙 Voiceover (TTS)** — ElevenLabs, Minimax, Edge, Kokoro. Live voice/credit counter.
- **🖼 Flow Image** — Nano Banana 2 / Nano Banana / Nano Banana Pro.
- **🎬 Flow Video** — Veo 3.1 Fast / Quality / Lite.
- **🔀 Workflow** — Node-based editor: Prompt → Image → Video → Extract Frame.
- **🔗 Webhook** — Local REST API server so external tools can drive generation.
- **🌍 Languages** — English / Türkçe / Español, switchable live.
- **ffmpeg bundled** — the workflow "Extract Frame" node works out of the box.

---

## 🚀 Getting Started

1. Download and extract the package (above).
2. Launch **DubVoice.exe**. No installation needed — it is portable.
3. Open the **Settings** tab and paste your dubvoice.ai API key (`sk_...`).
4. Pick a tab and start generating.

Configuration is stored in your user profile; generated files are saved under
`Documents/DubVoice`. **No API key ships with the app — you add your own.**

---

## 🔗 Webhook (Local REST API)

The **Webhook** tab runs a local REST API on `http://127.0.0.1:8765` so you can
automate DubVoice from **n8n, Make.com, Zapier**, or any Python / cURL script.
Full, always-current documentation lives inside the app on the Webhook tab.

```bash
# 1) submit an image job
curl -X POST http://127.0.0.1:8765/api/image/generate \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"prompt":"a red sports car at sunset","model":"nano-banana-pro","aspect_ratio":"16:9"}'
# -> {"task_id":"abc123","status":"pending"}

# 2) poll status
curl http://127.0.0.1:8765/api/status/abc123 -H "X-API-Key: YOUR_KEY"

# 3) download the result
curl http://127.0.0.1:8765/api/file/abc123 -H "X-API-Key: YOUR_KEY" -o result.png
```

| Method | Endpoint | Description |
| :----- | :------- | :---------- |
| `GET`  | `/api/health` | Server status |
| `GET`  | `/api/models` | Supported models |
| `POST` | `/api/image/generate` | Generate an image |
| `POST` | `/api/video/generate` | Generate a video |
| `POST` | `/api/tts/generate`   | Text-to-speech |
| `GET`  | `/api/status/{task_id}` | Job status |
| `GET`  | `/api/result/{task_id}` | Result (URL + local path) |
| `GET`  | `/api/file/{task_id}`   | The generated file |

---

## ❓ Support

- 🌐 Website: [dubvoice.ai](https://www.dubvoice.ai)
- 🐛 Found a bug? Open an [issue](https://github.com/Dubvoice/Dubvoice-Automation/issues).

---

<div align="center">
<sub>© DubVoice. All rights reserved. Powered by dubvoice.ai.</sub>
</div>
