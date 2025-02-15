import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import requests
from moviepy import VideoFileClip

# OpenAI APIキーを環境変数から取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    messagebox.showerror("エラー", "環境変数 OPENAI_API_KEY が設定されていません。")
    exit()

def transcribe_audio(file_path):
    """ OpenAI Transcribe APIを使って音声を書き起こす """
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    files = {"file": open(file_path, "rb")}
    data = {"model": "whisper-1", "language": "ja"}

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()["text"]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("エラー", f"書き起こしに失敗しました: {e}")
        return None

def summarize_text():
    """ 「要約」ボタンを押したときに実行。書き起こし結果を要約する """
    text = transcription_text.get("1.0", tk.END).strip()
    summary_prompt = summary_prompt_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("警告", "書き起こし結果がありません。")
        return
    
    if not summary_prompt:
        summary_prompt = "以下の文章を簡潔に要約してください。"

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": summary_prompt},
                     {"role": "user", "content": text}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"]
        summary_text.delete("1.0", tk.END)
        summary_text.insert(tk.END, summary)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("エラー", f"要約に失敗しました: {e}")

def extract_audio_from_video(video_path):
    """ 動画ファイルから音声を抽出し、WAVに変換して保存 """
    try:
        clip = VideoFileClip(video_path)
        audio_path = video_path.rsplit(".", 1)[0] + ".wav"  # 同じ名前で.wavファイル作成
        clip.audio.write_audiofile(audio_path, codec="pcm_s16le")  # WAV形式で保存
        return audio_path
    except Exception as e:
        messagebox.showerror("エラー", f"音声抽出に失敗しました: {e}")
        return None

def on_drop(event):
    """ ファイルがドロップされたときの処理 """
    file_path = event.data.strip("{}")  # {} を削除
    ext = file_path.lower().rsplit(".", 1)[-1]

    # 動画なら音声を抽出
    temp_audio_path = None
    if ext in ["mp4", "mkv", "avi", "mov"]:
        temp_audio_path = extract_audio_from_video(file_path)
        if not temp_audio_path:
            return  # 失敗時は処理を中断
        file_path = temp_audio_path  # 書き起こし対象を音声ファイルに変更

    transcription = transcribe_audio(file_path)
    if transcription:
        transcription_text.delete("1.0", tk.END)
        transcription_text.insert(tk.END, transcription)

    # 一時的な音声ファイルを削除
    if temp_audio_path:
        os.remove(temp_audio_path)

def copy_to_clipboard(text_widget):
    """ テキストをクリップボードにコピー """
    root.clipboard_clear()
    root.clipboard_append(text_widget.get("1.0", tk.END).strip())
    root.update()
    messagebox.showinfo("コピー完了", "テキストがコピーされました")

# --- GUIセットアップ ---
root = TkinterDnD.Tk()
root.title("音声書き起こしアプリ")
root.geometry("600x650")

# ドロップエリア
drop_label = tk.Label(root, text="ここに音声・動画ファイルをドロップ", bg="lightgray", relief="ridge", width=50, height=4)
drop_label.pack(pady=10)
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", on_drop)

# 書き起こし結果
tk.Label(root, text="書き起こし結果").pack()
transcription_text = scrolledtext.ScrolledText(root, height=10)
transcription_text.pack(fill="both", expand=True, padx=10)
copy_btn1 = tk.Button(root, text="コピー", command=lambda: copy_to_clipboard(transcription_text))
copy_btn1.pack()

# 要約指示
tk.Label(root, text="要約指示（例: 箇条書きでまとめる）").pack()
summary_prompt_text = scrolledtext.ScrolledText(root, height=3)
summary_prompt_text.pack(fill="both", expand=True, padx=10)
summary_prompt_text.insert(tk.END, "以下の文章を簡潔に要約してください。")

# 要約ボタン
summary_btn = tk.Button(root, text="要約", command=summarize_text, bg="lightblue")
summary_btn.pack(pady=5)

# 要約結果
tk.Label(root, text="要約結果").pack()
summary_text = scrolledtext.ScrolledText(root, height=5)
summary_text.pack(fill="both", expand=True, padx=10)
copy_btn2 = tk.Button(root, text="コピー", command=lambda: copy_to_clipboard(summary_text))
copy_btn2.pack()

root.mainloop()
