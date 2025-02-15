# whisper-transcribe

そっけない、音声書き起こし。

- windows app側で、音声ファイルのドロップ、書き起こし・要約依頼
- server側で、openai whisper api互換の書き起こし
- 要約はどこかのopenai chatcompletions api互換のLLMにおまかせ


## 準備

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install tkinterdnd2 openai moviepy requests
```

## 利用

```bash
python app.py
```

OpenAI Whisper trasnscribe API互換相手に書き起こし。テキストの応答のみを想定。
OpenAI ChatCompletions API互換相手に要約。

それぞれは当初はOpenAI のもので。そのあとで互換サーバで。


## アプリコード作成のプロンプト

tkinterを使って、音声書き起こしアプリをつくる。音声ファイルをドロップする。そのファイルを書き起こしサーバに送る。apiはopenai transcribe apiと同じ。但しrequestsを使うこと。得た書き起こしを、表示すること。さらに要約するようopenai chat apiを使うこと。結果を別に表示すること。それぞれの結果はコピーできること

具体的にコード例を作れ

動画がドロップされたときにはmoviepyを使って音声を抽出して、transcribe apiに投げること

変更されなかった部分を含めて全コードを出力して。

要約方針を指示する入力部分も欲しい。それを要約の際のシステムプロンプトに使う。
よって、表示は、上から、書き起こし、要約指示、要約結果の順に並ぶ。

書き起こした後、すぐに要約するのではなく、「要約」ボタンを押してから、書き起こし結果を要約するようにしたい。これで、一度の書き起こし結果に対して、要約のシステムプロンプトを様々に変更して、様々な要約を作ることができると期待する。修正後のコード全てを出力して。

OPENAI_API_KEYは環境変数OPENAI_API_KEYから取得するようにして。
また、from moviepy.editor import VideoFileClip　の個所は、最新版では from moviepy import VideoFileClip が正しい。修正後のコードをすべて出力して。

transcribe APIとchatcompletions APIのエンドポイントURLが異なるかもしれないので、別個にOPENAI_BASE_URL相当のものを設定できること。OPENAI_API_KEYも個別に設定できること。修正後のコード全てを出力して。

