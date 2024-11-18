# Edge_Tts_Pop_Api
> customize api by edge_tts for sample development

**基于edge_tts封装的在线tts合成服务**

## 部署
1. 克隆仓库到本地，运行main.py即可本地运行
2. 基于DockFile可构建自定义的docker镜像，按需选择暴露端口

## 使用
1. 使用Post请求

> post请求会返回音频流文件.需要保存到本地后播放

> http://localhost:10010/synthesize
> - text: 需要合成的文本
> - voice: 合成音色
> - rate: 音频速率
> - volume: 音频音量


 ```kotlin
  //Kotlin方法模拟播放，使用Ktor和JPlayer
  fun requestAudio(text: String, gson: Gson, audioPlayer: AudioPlayer) {
    runBlocking {
        val client = HttpClient(CIO) {
            install(ContentNegotiation) {
                json(Json {
                    ignoreUnknownKeys = true
                    prettyPrint = true
                })
            }
            install(Logging) {
                level = LogLevel.INFO
            }
        }

        val requestBody = mapOf(
            "text" to text,
            "voice" to "Female-XiaoxiaoNeural",
            "rate" to 12,
            "volume" to 0
        )

        try {
            val response: HttpResponse = client.post("http://localhost:8000/synthesize") {
                contentType(ContentType.Application.Json)
                setBody(gson.toJson(requestBody))
            }

            if (response.status.value == 200) {
                val file = File("output.mp3")
                
                //保存音频文件到本地
                FileOutputStream(file).use { outputStream ->
                    val byteChannel: ByteReadChannel = response.bodyAsChannel()
                    val buffer = ByteArray(4096)
                    while (!byteChannel.isClosedForRead) {
                        val bytesRead = byteChannel.readAvailable(buffer)
                        if (bytesRead > 0) {
                            outputStream.write(buffer, 0, bytesRead)
                        }
                    }
                }
                println("Audio saved successfully as output.wav")
                
                //写入结束后播放
                playMp3(file)
            } else {
                println("Request failed with status code: ${response.status.value}")
            }
        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            client.close()
        }
    }
}

fun playMp3(file: File) {
    try {
        val player = Player(FileInputStream(file))
        player.play()
    } catch (e: JavaLayerException) {
        e.printStackTrace()
    } catch (e: Exception) {
        e.printStackTrace()
    }
}
```

2. 使用Get请求

> get请求会返回一个可直接播放的音频文件

> http://localhost:10010/stream_audio?text=%E4%BB%8A%E5%A4%A9%E7%9A%84%E5%A4%A9%E6%B0%94%E6%80%8E%E4%B9%88%E6%A0%B7&voice=Female-XiaoxiaoNeural&rate=12&volume=0
>
> - text: 需要合成的文本
> - voice: 合成音色
> - rate: 音频速率
> - volume: 音频音量

## 补充
### 合成音色
> 音色存储在constant, 若为及时同步edge-tts官方, 请自行补充。
```python
SUPPORTED_VOICES = {
    'Female-AnaNeural': 'en-US-AnaNeural',
    'Female-AriaNeural': 'en-US-AriaNeural',
    'Male-ChristopherNeural': 'en-US-ChristopherNeural',
    'Male-EricNeural': 'en-US-EricNeural',
    'Male-GuyNeural': 'en-US-GuyNeural',
    'Female-JennyNeural': 'en-US-JennyNeural',
    'Female-MichelleNeural': 'en-US-MichelleNeural',
    'Male-RogerNeural': 'en-US-RogerNeural',
    'Male-SteffanNeural': 'en-US-SteffanNeural',
    'Female-XiaoxiaoNeural': 'zh-CN-XiaoxiaoNeural',
    'Female-XiaoyiNeural': 'zh-CN-XiaoyiNeural',
    'Male-YunjianNeural': 'zh-CN-YunjianNeural',
    'Male-YunxiNeural': 'zh-CN-YunxiNeural',
    'Male-YunxiaNeural': 'zh-CN-YunxiaNeural',
    'Male-YunyangNeural': 'zh-CN-YunyangNeural',
}
```