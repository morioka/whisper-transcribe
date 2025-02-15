import torch
from transformers import pipeline
from moviepy import VideoFileClip

import argparse
import os
import tempfile

def main(args):
    sample = args.audio_file
    return_timestamps = args.return_timestamps
    punctuation = not args.disable_punctuation
    language = args.language

    if not os.path.isfile(sample):
        return

    with tempfile.NamedTemporaryFile(suffix='wav', delete=False) as fp:
        fp.close()
    
        # 動画ファイルなら音声部分を抽出する
        ext = sample.lower().rsplit(".", 1)[-1]
        if ext in ["mp4", "mkv", "avi", "mov"]:
            clip = VideoFileClip(sample)
            clip.audio.write_audiofile(fp.name, codec="pcm_s16le")
            sample = fp.name    # 書き起こし対象を音声ファイルに変更

        # 以下、ベースは kotoba-whisper-v2.1 サンプルコード
        # https://huggingface.co/kotoba-tech/kotoba-whisper-v2.1

        # config
        model_id = "kotoba-tech/kotoba-whisper-v2.1"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model_kwargs = {"attn_implementation": "sdpa"} if torch.cuda.is_available() else {}
        generate_kwargs = {"language": language, "task": "transcribe"}

        # load model
        pipe = pipeline(
            model=model_id,
            torch_dtype=torch_dtype,
            device=device,
            model_kwargs=model_kwargs,
            batch_size=16,
            trust_remote_code=True,
            punctuator=punctuation
        )

        # run inference
        result = pipe(sample, return_timestamps=return_timestamps, generate_kwargs=generate_kwargs)
        print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='transcribe', usage='%(prog)s [options]')
    parser.add_argument('audio_file', type=str, help='音声ファイル')
    parser.add_argument('--return_timestamps', help='タイプスタンプを付与', action='store_true')
    parser.add_argument('--disable_punctuation', help='文区切りを無効化', action='store_true')
    parser.add_argument('--language', help='音声言語', type=str, default='ja')
    args = parser.parse_args()
    main(args)
