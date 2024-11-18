from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
import edge_tts
from typing import AsyncGenerator
import uvicorn

from constant import SUPPORTED_VOICES

app = FastAPI()

async def generate_audio_chunks(text: str, voice: str, rate: int, volume: int) -> AsyncGenerator[bytes, None]:
    if rate >= 0:
        rates = f"+{rate}%"
    else:
        rates = f"{rate}%"

    if volume >= 0:
        volumes = f"+{volume}%"
    else:
        volumes = f"{volume}%"

    communicate = edge_tts.Communicate(text, SUPPORTED_VOICES[voice], rate=rates, volume=volumes)

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


@app.post("/synthesize")
async def synthesize(request: Request):
    data = await request.json()
    text = data.get("text", "")
    voice = data.get("voice", "Male-YunxiNeural")
    rate = data.get("rate", 0)
    volume = data.get("volume", 0)

    if not text:
        return {"error": "Text is required"}

    return StreamingResponse(
        generate_audio_chunks(text, voice, rate, volume),
        media_type="audio/mp3"
    )


#http://localhost:10010/stream_audio?text=%E4%BB%8A%E5%A4%A9%E7%9A%84%E5%A4%A9%E6%B0%94%E6%80%8E%E4%B9%88%E6%A0%B7&voice=Female-XiaoxiaoNeural&rate=12&volume=0
@app.get("/stream_audio")
async def stream_audio(text: str, voice: str, rate: int, volume: int):
    if not text:
        raise HTTPException(status_code=400, detail="Text Parameter is required")
    if not voice:
        voice = 'Female-XiaoxiaoNeural'
    if not rate:
        rate = 12
    if not volume:
        volume = 0
    return StreamingResponse(generate_audio_chunks(text, voice, rate, volume), media_type="audio/mp3")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=10010)