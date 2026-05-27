import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from video_processor import VideoProcessor
from ai import VideoAI

load_dotenv()

# ─────────────── Page Setup ───────────────
st.set_page_config(
    page_title="Video Q&A Chatbot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────── Custom CSS ───────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF4B4B, #FF8C42);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #888;
        margin-top: 0;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────── Session State ───────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "ai" not in st.session_state:
    st.session_state.ai = None
if "video_info" not in st.session_state:
    st.session_state.video_info = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None

# ─────────────── Header ───────────────
st.markdown('<p class="main-header">🎬 Video Q&A Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload a video and chat with AI about its content</p>', unsafe_allow_html=True)
st.divider()

# ─────────────── Sidebar ───────────────
with st.sidebar:
    st.header("⚙️ Settings")

    num_frames = st.slider(
        "Frames to extract",
        min_value=4,
        max_value=20,
        value=10,
        help="More frames = better understanding but higher cost"
    )

    detail_level = st.selectbox(
        "Image detail",
        options=["low", "high"],
        index=0,
        help="'high' costs more but gives better accuracy"
    )

    st.divider()
    st.header("📤 Upload Video")
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov", "mkv", "webm"],
        help="Supports MP4, AVI, MOV, MKV, WEBM"
    )

    if uploaded_file is not None:
        if st.button("🚀 Process Video", type="primary", use_container_width=True):
            with st.spinner("Processing video..."):
                try:
                    # Save to temp file
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                    tfile.write(uploaded_file.read())
                    tfile.close()
                    st.session_state.video_path = tfile.name

                    # Extract frames
                    processor = VideoProcessor()
                    info = processor.get_info(tfile.name)
                    frames = processor.extract_frames(tfile.name, num_frames=num_frames)

                    # Initialize AI
                    ai = VideoAI()
                    ai.detail = detail_level
                    ai.load_video(frames)

                    # Save to session
                    st.session_state.ai = ai
                    st.session_state.video_info = info
                    st.session_state.video_loaded = True
                    st.session_state.messages = []

                    st.success(f"✅ Loaded {len(frames)} frames!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.divider()

    if st.session_state.video_loaded:
        st.header("📊 Video Info")
        info = st.session_state.video_info
        st.metric("Duration", f"{info['duration']}s")
        st.metric("FPS", info['fps'])
        st.metric("Total Frames", f"{info['frames']:,}")

        st.divider()

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.ai:
                st.session_state.ai.load_video(st.session_state.ai.frames_b64)
            st.rerun()

        if st.button("📁 New Video", use_container_width=True):
            st.session_state.video_loaded = False
            st.session_state.messages = []
            st.session_state.ai = None
            st.session_state.video_info = None
            st.rerun()

    st.divider()
    st.caption("Powered by GPT-4o · OpenCV · Streamlit")

# ─────────────── Main Content ───────────────
if not st.session_state.video_loaded:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>👋 Welcome!</h3>
        <p>To get started:</p>
        <ol>
            <li>Upload a video using the sidebar</li>
            <li>Click "Process Video"</li>
            <li>Ask any question about the content</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💡 Example Questions")
        examples = [
            "What is happening in this video?",
            "How many people appear?",
            "Describe the setting and mood",
            "What objects are visible?",
            "Summarize the video in 2 sentences",
            "What's the main subject?"
        ]
        for ex in examples:
            st.markdown(f"- {ex}")

else:
    # Two-column layout: video preview + chat
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("🎥 Video Preview")
        if st.session_state.video_path and os.path.exists(st.session_state.video_path):
            st.video(st.session_state.video_path)

        with st.expander("📸 Extracted Frames"):
            if st.session_state.ai and st.session_state.ai.frames_b64:
                cols = st.columns(2)
                for i, b64 in enumerate(st.session_state.ai.frames_b64):
                    with cols[i % 2]:
                        st.image(
                            f"data:image/jpeg;base64,{b64}",
                            caption=f"Frame {i + 1}",
                            use_container_width=True
                        )

    with col2:
        st.subheader("💬 Chat")

        # Display history
        chat_container = st.container(height=500)
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Input
        if prompt := st.chat_input("Ask a question about the video..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing..."):
                        try:
                            answer = st.session_state.ai.ask(prompt)
                            st.markdown(answer)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer
                            })
                        except Exception as e:
                            error_msg = f"⚠️ Error: {e}"
                            st.error(error_msg)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": error_msg
                            })
