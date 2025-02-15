
https://huggingface.co/kotoba-tech/kotoba-whisper-v2.1

```bash
pip install --upgrade pip
pip install --upgrade transformers accelerate torchaudio
pip install stable-ts==2.16.0
pip install punctuators==0.0.5
pip install moviepy
pip install fastapi
pip install soundfile
```

https://chatgpt.com/share/67b04b7a-f8c4-8002-95f9-4b60b904d5da

ollamaサーバと同じ機能をfastapiで作りたい

推論時にモデルがロードされていなかったらロードするようにして

指定されたモデル毎に推論方法を変更したい。モデル毎に推論コードを用意し、モデル名によって呼び出すようにしたい

モデルによってはトークナイザを必要とするものがある。これに対応したい


https://chatgpt.com/share/67b04e07-ecf4-8002-98dc-c9f85c0c7bb7

kotoba-whisper-v2.1 をつかった、OpenAI transcribe API互換のAPIサーバを FastAPIを使って、作りたい。

そのまま進めて。

kotoba_whisper の使い方は正しい?

https://huggingface.co/kotoba-tech/kotoba-whisper-v2.1 を参照して、kotoba-whisper を適切に利用したコードを書いて。

pipline に タスク名 "automatic-speech-recognition" を与えると、punctuatorを引数に与えられなくなるので、止めること。

このコードで必要なpythonパッケージを列挙せよ

サーバの起動方法は？

上記コードのファイル名は server.py とする。このときは?

python package に python-multipart は必要ない？

今回はどう？