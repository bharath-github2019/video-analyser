import os
from openai import OpenAI


class VideoAI:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("SHARED_SERVICE_BASE_URL"),
            api_key=os.getenv("SHARED_SERVICE_API_KEY"),
        )
        self.model = os.getenv("SHARED_SERVICE_MODEL", "azure.gpt-4o")
        self.frames_b64 = []
        self.history = []

    def load_video(self, frames_b64):
        self.frames_b64 = frames_b64
        self.history = [{
            "role": "system",
            "content": (
                "You are a video analysis assistant. The user has loaded a video, "
                "and you have its evenly-spaced frames in chronological order. "
                "Answer questions about the video accurately and concisely."
            )
        }]

    def ask(self, question):
        if len(self.history) == 1:
            # First turn — include all frames with the question
            content = [{"type": "text", "text": question}]
            for b64 in self.frames_b64:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64}",
                        "detail": "low"
                    }
                })
            self.history.append({"role": "user", "content": content})
        else:
            # Follow-up — text only (model already has the frames)
            self.history.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer
