# whisper-transcribe

何の変哲もない、音声書き起こし。

- windows app側で、音声ファイルのドロップ、書き起こし・要約依頼
- server側で、openai whisper api互換の書き起こし。たとえば [morioka/tiny-openai-whisper-api](https://github.com/morioka/tiny-openai-whisper-api)。 Xinferenceのものでもよい。
- 要約はどこかのopenai chatcompletions api互換のLLMにおまかせ。たとえば ollama で。


## 準備

Windows 11上で。Python 3.13.2

```bash
git clone https://github.com/morioka/whisper-transcribe
cd whiper-transcribe
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install tkinterdnd2 openai moviepy requests
```

## 利用

```bash
cd whiper-transcribe
venv\Scripts\activate

python app.py
```

OpenAI Whisper trasnscribe API互換相手に書き起こし。テキストの応答のみを想定。
OpenAI ChatCompletions API互換相手に要約。

それぞれは当初はOpenAI のもので。そのあとで互換サーバで。


## アプリコード作成のプロンプト

chatgptにコード作成を指示した。出力したコードを確認しながら、指示を更新した。

https://chatgpt.com/share/67afff60-1a00-8002-ba25-689851cc5eef

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

要約のモデルには gpt-4o-miniを指定すること。修正後のコードをすべて出力して。

## サーバ

```bash
pip install --upgrade pip
pip install --upgrade transformers accelerate torchaudio
pip install stable-ts==2.16.0
pip install punctuators==0.0.5
pip intalll moviepy
```
