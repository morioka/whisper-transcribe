
## アプリコード作成のプロンプト

tkinterを使って、音声書き起こしアプリをつくる。音声ファイルをドロップする。そのファイルを書き起こしサーバに送る。apiはopenai transcribe apiと同じ。但しrequestsを使うこと。得た書き起こしを、表示すること。さらに要約するようopenai chat apiを使うこと。結果を別に表示すること。それぞれの結果はコピーできること

具体的にコード例を作れ

動画がドロップされたときにはmoviepyを使って音声を抽出して、transcribe apiに投げること

変更されなかった部分を含めて全コードを出力して。

要約方針を指示する入力部分も欲しい。それを要約の際のシステムプロンプトに使う。
よって、表示は、上から、書き起こし、要約指示、要約結果の順に並ぶ。

## 準備

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install tkinterdnd2 openai moviepy requsets
```
