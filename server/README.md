
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

```
uvicorn server:app --reload
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

https://chatgpt.com/share/67b053a7-441c-8002-af25-11d3523af9b2

実際に動作させたところ、以下のエラーが生じた。アップロードされた音声は1chでなく、2chまたはそれ以上であるが、kotoba-whisperのパイプラインが1ch音声にしか対応していないものと考えられる。これへの対策を考えて。

=== エラーメッセージ ==
  File "/home/morioka/.cache/huggingface/modules/transformers_modules/kotoba-tech/kotoba-whisper-v2.1/57a9d8ab771a0124706b67d22509bedd07c36187/kotoba_whisper.py", line 199, in preprocess
    raise ValueError("We expect a single channel audio input for AutomaticSpeechRecognitionPipeline")
ValueError: We expect a single channel audio input for AutomaticSpeechRecognitionPipeline

実際、以下のコードになっている。soudfileパッケージで読み込む際に1ch音声にするできないか？

import soundfile as sf

    audio_bytes = await file.read()
    audio_file = io.BytesIO(audio_bytes)
    
    # 音声データの読み込み
    audio_input, sample_rate = sf.read(audio_file)
    
    # パイプラインの設定を更新
    generate_kwargs.update({
        "prompt": prompt,
        "temperature": temperature,
        "language": language,
        "task": task
    })
    
    # 文字起こし
    result = asr_pipeline(
        audio_input,
        chunk_length_s=15,
        return_timestamps=(response_format == "verbose_json"),
        generate_kwargs=generate_kwargs
    )