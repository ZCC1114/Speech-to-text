import argparse
from dataclasses import dataclass


import os
from typing import List, Tuple

import whisper
from pyannote.audio import Pipeline

@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: str


def transcribe(audio_path: str) -> List[Segment]:
    """Transcribe audio and assign speaker labels."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="zh")
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable not set; cannot load pyannote model")

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization", use_auth_token=hf_token
    )
    if pipeline is None:
        raise RuntimeError(
            "Failed to load 'pyannote/speaker-diarization'. Check HF_TOKEN and"
            " whether you've accepted the model license."
        )
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline(audio_path)

    segments: List[Segment] = []
    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()
        speaker = "A"
        for turn in diarization.itertracks(yield_label=True):
            if start >= turn[0].start and end <= turn[0].end:
                speaker = "A" if turn[2] == "SPEAKER_00" else "B"
                break
        segments.append(Segment(start, end, text, speaker))
    return segments


def format_dialog(segments: List[Segment]) -> str:
    lines = []
    for seg in segments:
        lines.append(f"{seg.speaker}: {seg.text}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="转写语音并标记AB对话")
    parser.add_argument("audio", help="音频文件路径")
    parser.add_argument("--output", help="输出文本文件", default="output.txt")
    args = parser.parse_args()

    segments = transcribe(args.audio)
    dialog = format_dialog(segments)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(dialog)
    print(f"结果已保存到 {args.output}")


if __name__ == "__main__":
    main()
