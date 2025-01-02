from enum import Enum
from typing import AsyncGenerator, Optional

import aiohttp
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
SENSE_TTS_API_KEY =os.getenv("SENSE_TTS_API_KEY")


class VoiceEmotion(Enum):
    NORMAL = "me_f_y_1001_normal"
    HAPPY = "me_f_y_1001_happy"
    SAD = "me_f_y_1001_sad"
    ANGRY_L1 = "me_f_y_1001_angryL1"
    ANGRY_L2 = "me_f_y_1001_angryL2"
    ANGRY_L3 = "me_f_y_1001_angryL3"




# 定义请求模型
class TTSRequest(BaseModel):
    text: str
    emotion: Optional[str] = VoiceEmotion.NORMAL.value
    text_id: Optional[str] = "1111"
    text_language: Optional[str] = "zh"


app = FastAPI()


async def generate_audio_chunks(text: str, emotion: str, text_id: str, text_language: str) -> AsyncGenerator[
    bytes, None]:
    url = "http://14.103.16.83:29010/audio/tts"

    headers = {
        "Authorization": f"Bearer {SENSE_TTS_API_KEY}",
        "Content-Type": "application/json"
    }

    # 请求主体
    payload = {
        "tts_model_name": emotion,
        "text": text,
        "text_id": text_id,
        "text_language": text_language,
        "ref_free": False,
        "return_format": "wav_stream"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            async for chunk in response.content.iter_chunked(32000):  # 使用较大的chunk size提高效率
                if chunk:
                    yield chunk

@app.get("/synthesize")
async def synthesize(
        text: str,
        emotion: str = VoiceEmotion.NORMAL.value,
        text_id: str = "1111",
        text_language: str = "zh"
):
    if not text:
        return {"error": "文本不能为空"}

    return StreamingResponse(generate_audio_chunks(text, emotion, text_id, text_language), media_type="audio/mp3")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=10011)
