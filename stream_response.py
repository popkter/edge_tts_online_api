# main.py
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import uvicorn

app = FastAPI()

async def event_stream():
    # 注意：SSE 对每条消息通常需要 "data: ...\n\n" 格式
    yield f"data: 这是第一个 chunk {datetime.now().strftime('%H:%M:%S')}\n\n"
    
    # 等待 3 秒，模拟后续消息延迟
    await asyncio.sleep(3)
    
    # 返回后续 chunk，每次间隔 1 秒
    for i in range(1, 6):
        await asyncio.sleep(1)
        yield f"data: 这是第 {i + 1} 个 chunk {datetime.now().strftime('%H:%M:%S')}\n\n"

@app.get("/stream")  # 通常 SSE 使用 GET
async def stream_response():
    # 加上 Cache-Control 以避免某些代理或浏览器缓存
    return StreamingResponse(
        event_stream(), 
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=10010)
