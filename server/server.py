from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading
import time

app = FastAPI()

# モデルの状態を保持
models = {}
lock = threading.Lock()

# モデルごとの推論関数を格納する辞書
inference_functions = {}

class LoadModelRequest(BaseModel):
    model_name: str

class InferenceRequest(BaseModel):
    model_name: str
    prompt: str

def register_inference_function(model_name: str, inference_function, requires_tokenizer: bool = True):
    """
    モデルごとの推論関数を登録する。
    """
    inference_functions[model_name] = {
        "function": inference_function,
        "requires_tokenizer": requires_tokenizer
    }

def load_model_internal(model_name: str, requires_tokenizer: bool):
    """
    モデルをロードする内部関数。
    """
    if requires_tokenizer:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        models[model_name] = {
            "model": model,
            "tokenizer": tokenizer,
            "last_used": time.time()
        }
    else:
        # トークナイザが不要なモデルの処理
        from transformers import AutoModelForSequenceClassification
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        models[model_name] = {
            "model": model,
            "tokenizer": None,
            "last_used": time.time()
        }

@app.post("/load_model")
async def load_model(request: LoadModelRequest):
    """
    明示的にモデルをロードするエンドポイント。
    """
    with lock:
        if request.model_name in models:
            return {"status": "already_loaded"}
        try:
            # トークナイザの必要性を判別してモデルをロード
            requires_tokenizer = inference_functions.get(request.model_name, {}).get("requires_tokenizer", True)
            load_model_internal(request.model_name, requires_tokenizer)
            return {"status": "loaded"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/unload_model")
async def unload_model(request: LoadModelRequest):
    """
    モデルを解放するエンドポイント。
    """
    with lock:
        if request.model_name in models:
            del models[request.model_name]
            return {"status": "unloaded"}
        raise HTTPException(status_code=404, detail="Model not loaded")

@app.post("/inference")
async def inference(request: InferenceRequest):
    """
    推論を行うエンドポイント。
    モデルごとの推論方法を選択して実行する。
    """
    with lock:
        if request.model_name not in models:
            try:
                # トークナイザの必要性を確認してモデルをロード
                requires_tokenizer = inference_functions.get(request.model_name, {}).get("requires_tokenizer", True)
                load_model_internal(request.model_name, requires_tokenizer)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
        
        # モデルデータを取得
        model_data = models[request.model_name]
        models[request.model_name]["last_used"] = time.time()

    # モデルごとの推論関数を呼び出し
    if request.model_name in inference_functions:
        inference_function = inference_functions[request.model_name]["function"]
        return inference_function(request.prompt, model_data)
    else:
        raise HTTPException(status_code=404, detail="Inference function not found for the specified model")

@app.get("/models")
async def list_models():
    """
    現在ロードされているモデルをリストするエンドポイント。
    """
    with lock:
        return {"models": list(models.keys())}

# 一定時間アイドルのモデルを解放
def cleanup_idle_models(idle_time=300):
    """
    一定時間アイドル状態のモデルを解放するバックグラウンドタスク。
    """
    while True:
        with lock:
            current_time = time.time()
            for model_name in list(models.keys()):
                if current_time - models[model_name]["last_used"] > idle_time:
                    del models[model_name]
        time.sleep(60)

# バックグラウンドスレッドでアイドルモデル解放
threading.Thread(target=cleanup_idle_models, daemon=True).start()

# モデルごとの推論関数
def gpt_inference(prompt, model_data):
    """
    GPTモデル用の推論関数（トークナイザが必要）。
    """
    tokenizer = model_data["tokenizer"]
    model = model_data["model"]
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=50)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": result}

def classification_inference(prompt, model_data):
    """
    分類モデル用の推論関数（トークナイザが不要）。
    """
    model = model_data["model"]
    # プレースホルダとして簡単な分類結果を返す（必要に応じてデータを整形）
    return {"response": f"Classification result for: {prompt}"}

# 推論関数をモデル名で登録
register_inference_function("gpt-model", gpt_inference, requires_tokenizer=True)
register_inference_function("classification-model", classification_inference, requires_tokenizer=False)
