import os
import sys
from dotenv import load_dotenv
from video_processor import VideoProcessor
from ai import VideoAI

load_dotenv()


def main():
    print("\nVideo Q&A Chatbot")
    print("=" * 40)

    required = [
        "SHARED_SERVICE_BASE_URL",
        "SHARED_SERVICE_API_KEY",
        "SHARED_SERVICE_MODEL",
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        print(f"Missing in .env: {', '.join(missing)}")
        sys.exit(1)

    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = input("Provide path to video file: ").strip().strip('"')

    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        return

    processor = VideoProcessor()
    ai = VideoAI()

    info = processor.get_info(video_path)
    if info:
        print(f"\nVideo info: {info['duration']}s, {info['fps']} fps, {info['frames']} frames")

    print("🎞️  Extracting frames...")
    try:
        frames = processor.extract_frames(video_path, num_frames=10)
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"Loaded {len(frames)} frames\n")
    ai.load_video(frames)

    print("Ask questions about the video.")
    print("   Type 'exit' to quit, 'reset' to reload, 'new' for a new video.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            print("Bye!")
            break
        if question.lower() == "reset":
            ai.load_video(frames)
            print("Conversation reset.\n")
            continue
        if question.lower() == "new":
            new_path = input("New video path: ").strip().strip('"')
            if os.path.exists(new_path):
                video_path = new_path
                frames = processor.extract_frames(video_path, num_frames=10)
                ai.load_video(frames)
                print(f"New video loaded ({len(frames)} frames)\n")
            else:
                print("Not found.\n")
            continue

        try:
            answer = ai.ask(question)
            print(f"\nAI: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
