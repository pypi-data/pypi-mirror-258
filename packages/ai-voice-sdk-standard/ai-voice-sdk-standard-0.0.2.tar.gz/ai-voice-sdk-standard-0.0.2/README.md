# AI VOICE SDK

## 簡介
AI Voice是宏正自動科技的語音合成服務優聲學，使用本SDK是必須租用優聲學服務。租用服務請至`https://www.aivoice.com.tw/business/enterprise`上留下聯絡資料。<br>
宏正優聲學，推出限量企業標準版之語音合成服務，提供多個優質美聲，大量語音合成，歡迎企業用戶填寫表格連繫, 了解更多企業標準版方案細節!
<br><br>

## 需求
### Windows 
需要安裝Microsoft C++ Build Tools，不然下載相依套件時會報 `error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/` 錯誤，相關資訊 https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst
<br>

### Python
```
python >= 3.7
```
<br>

### 支援SSML版本
```
version == v1.2
```
<br>

## 安裝方式
- pip安裝SDK
```
pip install ai-voice-sdk-standard
```

- 手動安裝SDK
```shell
python -m pip install wheel
python setup.py sdist bdist_wheel # 建立SDK安裝檔
pip install dist\ai_voice_sdk_standard-x.x.x-py3-none-any.whl # 安裝SDK，其中 'x.x.x' 填入現在的版本號
```
<br>

## 使用方式
我們目前支援10個不同的聲優，而他們支援2種語言，包括中文和英文。以下範例程式是如何使用AI-Voice-SDK

- 執行方式有分為`一般`和`即時聲音播放`模式
    1. 使用`一般模式`，執行後文章送出到AI Voice server處理完以後，聲音資料送回來並合成一個`.wav`檔案
        ```py
        # 設定一般模式
        # RunMode.NORMAL為default值
        converter.config.set_run_model(aivoice.RunMode.NORMAL)
        ```
    2. 使用`即時聲音播放模式`，執行後文章送出到AI Voice server，將會開始`即時播放聲音`
        ```py
        # 設定即時聲音播放模式
        converter.config.set_run_model(aivoice.RunMode.LIVE_PLAY_AUDIO)
        ```

- 文字加入方式：文字，SSML格式，宏正優聲學RTF格式，文字檔，SSML格式檔案
    ```py
    # 加入文字
    converter.text.add_text(text = "歡迎體驗宏正優聲學，讓好聲音為您的應用提供加值服務。", position = -1)

    # 加入SSML格式
    converter.text.add_ssml_text(
        text = """<speak xmlns="http://www.w3.org/2001/10/synthesis" version="1.2" xml:lang="zh-TW">
        <voice name="Aaron">宏正自動科技的人工智慧語音合成技術，帶來超逼真
        <phoneme alphabet="bopomo" lang="TW" ph="ㄉㄜ˙">的</phoneme>
        合成語音
        <break time="300ms"/>
        ：自然、真實，讓您拉近與客戶的距離，提高滿意度，帶來轉換率。
        </voice></speak>""",
        position = -1
    )

    # 加入宏正優聲學RTF格式
    converter.text.add_webpage_text(
        text = """按下合成鍵之前，我們[:ㄇㄣˊ]建議您先確認2個[:ㄍㄜ˙]問題：
        您的文章轉成語音之後，是好聽流暢的嗎？[:1.2秒]
        您有[:ㄧㄡˇ]將閱讀文，轉為聆聽文嗎？
        """,
        rate = 1.01, pitch = 0, volume = 2.45, position = -1
    )

    # 讀取純文字檔加入
    converter.text.open_text_file(file_path="./textfile.txt", encode="utf-8", position=-1)

    # 讀取SSML格式的檔案
    converter.text.open_text_file(file_path="./ssmlfile.ssml", encode="utf-8", position=-1)
    ```

- 合成聲音教學
    - 使用環境變數設定Token和AI Voice Server URL
        - 使用`Command Prompt`環境變數設定Token和AI Voice Server URL
            ```console
            @rem 改為AI Voice網頁上的 API_ACCESS_TOKEN
            setx AI_VOICE_SDK_TOKEN your-token
            @rem Aten AI Voice Server URL
            setx AI_VOICE_URL https://www.aivoice.com.tw/business/enterprise
            ```

    - 完整程式
        ```py
        #coding:utf-8
        import os
        import ai_voice_sdk as aivoice

        # token = "API_ACCESS_TOKEN"
        token = os.environ.get('AI_VOICE_SDK_TOKEN')
        server = os.environ.get('AI_VOICE_URL')

        # 加入tokens內
        tokens = [token]

        # 建立轉換器設定檔
        # server_url 預設為 https://www.aivoice.com.tw/business/enterprise，可不填
        config = aivoice.ConverterConfig(tokens=tokens, server_url=server)

        # 選擇設定檔內選用的語音
        config.set_voice(aivoice.Voice.CALM_HANNAH)

        # 建立轉換器
        converter = aivoice.VoiceConverter(config=config)

        # 設定執行模式
        # RunMode.NORMAL為default值
        converter.config.set_run_mode(aivoice.RunMode.NORMAL)

        converter.text.add_text(text = "歡迎體驗宏正優聲學，讓好聲音為您的應用提供加值服務。", position = -1)
        converter.text.add_ssml_text(
            text = """<speak xmlns='http://www.w3.org/2001/10/synthesis' version='1.2' xml:lang='zh-TW'>
                <voice name='Aurora'>歡迎體驗宏正優聲學，讓好聲音為您的應用提供加值服務。</voice>
                <voice name='Jason'>歡迎體驗宏正優聲學，讓好聲音為您的應用提供加值服務。</voice>
            </speak>""",
            position = -1
        )
        converter.text.show()

        # 執行合成語音，且取得語音內容
        result = converter.run(interval_time=0, is_wait_speech=True)

        if result.status == aivoice.ConverterStatus.GetSpeechSuccess:
            print("Get speech data success.")
            # 將語音另存為"aivoice.wav"，且當語音數量超過一個時，將語音檔各別存為單一檔案
            result.save("aivoice", is_merge=True)
        else:
            if result.status == aivoice.ConverterStatus.GetSpeechFail:
                print(f"Error message: {result.error_message}")
            elif result.status == aivoice.ConverterStatus.ConverVoiceFail:
                print(f"Error message: {result.error_message}")
            else:
                print(f"Converter status: {result.status.name}, Detail: {result.detail}")
        ```

###  詳細教學： [Tutorial](./examples/tutorial.ipynb)