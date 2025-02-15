from fastapi import FastAPI, File, UploadFile, Form
import torch
from transformers import pipeline
from typing import Optional
import io
import soundfile as sf
import numpy as np

app = FastAPI()

# モデルとパイプラインの設定
model_id = "kotoba-tech/kotoba-whisper-v2.1"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
device = 0 if torch.cuda.is_available() else -1  # 'cuda:0' または 'cpu'
model_kwargs = {"attn_implementation": "sdpa"} if torch.cuda.is_available() else {}
generate_kwargs = {"language": "ja", "task": "transcribe"}

# パイプラインの初期化
asr_pipeline = pipeline(
    model=model_id,
    torch_dtype=torch_dtype,
    device=device,
    model_kwargs=model_kwargs,
    batch_size=1,   # この部分は手で修正。環境依存だろう
    trust_remote_code=True,
    punctuator=True  # 句読点を追加する場合は True、無効にする場合は False
)

@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...),
    prompt: Optional[str] = Form(None),
    temperature: Optional[float] = Form(0.0),
    language: Optional[str] = Form("ja"),
    response_format: Optional[str] = Form("json"),
    task: Optional[str] = Form("transcribe")
):
    """
    OpenAI Transcribe API 互換のエンドポイント。
    """
    audio_bytes = await file.read()
    audio_file = io.BytesIO(audio_bytes)
    
    # 音声データの読み込み
    audio_input, sample_rate = sf.read(audio_file)

    # チャンネル数の確認
    if audio_input.ndim > 1:
        # ステレオやそれ以上の場合、モノラルに変換
        audio_input = np.mean(audio_input, axis=1)

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
    
    if response_format == "verbose_json":
        return result
    
    return {"text": result["text"]}
