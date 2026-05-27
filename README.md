# AI Video Analyser with OpenAI

An AI-powered chatbot that lets you ask questions about any local video file. Built with Python, OpenCV, and GPT-4o (Azure OpenAI via API keys).

---

## 🧠 How It Works

1. **Frame Extraction** — OpenCV opens the video, calculates total frames, and samples 10 evenly-spaced frames.
2. **Image Optimization** — Each frame is resized to ≤800px wide and JPEG-encoded.
3. **Base64 Encoding** — Frames are converted to base64 strings to fit in JSON API requests.
4. **AI Conversation** — Frames + question are sent to GPT-4o on the first turn. The chat history retains context for follow-up questions.
5. **Response** — GPT-4o returns a natural-language answer, which is printed to the terminal.

---

## Features

- **Local video support** — Works with MP4, AVI, MOV, MKV, and more
- **Multimodal AI** — Uses GPT-4o vision to understand video frames
- **Conversational interface** — Ask follow-up questions naturally
- **Fast & cost-efficient** — Smart frame sampling keeps API calls cheap
- **Secure config** — All credentials stored in `.env`
- **Modular design** — Clean separation between video, AI, and UI logic

---

## Architecture

```
┌──────────────┐     ┌────────────────────┐     ┌─────────────────┐
│  Video File  │ ──▶ │ Frame Extraction   │ ──▶ │ Base64 Encoding │
│   (.mp4)     │     │     (OpenCV)       │     │                 │
└──────────────┘     └────────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌──────────────┐     ┌────────────────────┐     ┌─────────────────┐
│  AI Answer   │ ◀── │   GPT-4o Vision    │ ◀── │  OpenAI SDK     │
│ (Terminal)   │     │ (Shared Service)   │     │  + Chat History │
└──────────────┘     └────────────────────┘     └─────────────────┘
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Video Processing | OpenCV (`opencv-python`) |
| AI Model | GPT-4o (multimodal vision) |
| API Client | OpenAI Python SDK |
| Configuration | python-dotenv |
| Backend Service | Azure OpenAI |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Access to PwC Shared Service (or any OpenAI-compatible endpoint)
- A video file to analyze

### 1. Clone the repository

```bash
git clone https://github.com/<bharath-github2019>/video-qa.git
cd video-qa
```

### 2. Create & activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SHARED_SERVICE_BASE_URL=<your_endpoint>
SHARED_SERVICE_API_KEY=<your_api_key>
SHARED_SERVICE_MODEL=azure.gpt-4o
```

### 5. Test connectivity

```bash
python test_endpoint.py
```

You should see `Status: 200` and a sample response.

---

## 💻 Usage

### Run with a video path
```bash
python main.py "C:\path\to\your\video.mp4"
```

### Or run interactively
```bash
python main.py
```
You'll be prompted to enter a video path.

### Example session

```
🎬 Video Q&A Chatbot (PwC Shared Service)
========================================
📂 Path to video file: sample.mp4

📊 Video info: 17.5s, 25.0 fps, 438 frames
🎞️  Extracting frames...
✅ Loaded 10 frames

💬 Ask questions about the video.

You: What is happening in this video?

🤖 AI: A man walks his golden retriever through a park, passing 
       benches and trees. The dog appears playful and energetic.

You: What color is the dog?

🤖 AI: Golden / light tan.

You: How many people appear?

🤖 AI: One person — the man walking the dog.

You: exit
👋 Bye!
```

---

## 🎮 Commands

| Command | Description |
|---------|-------------|
| Any text | Ask a question about the video |
| `reset` | Clear conversation history (keep video) |
| `new` | Load a different video |
| `exit` / `quit` | Close the chatbot |

---

## ⚙️ Configuration

You can tune the following in the code:

| Setting | File | Default | Description |
|---------|------|---------|-------------|
| `num_frames` | `main.py` | 10 | Frames extracted per video |
| `detail` | `ai.py` | `"low"` | Image detail (`low`/`high`) |
| `max_tokens` | `ai.py` | 500 | Max response length |
| Resize threshold | `video_processor.py` | 800px | Max frame width |


<img width="960" height="514" alt="Screenshot 2026-05-27 232359" src="https://github.com/user-attachments/assets/d80eefe9-49c0-4da9-a0ef-fa07fd4222d1" />

