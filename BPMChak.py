import librosa
import numpy as np
import os
import sys

filePath=sys.argv[1]

def detect_bpm(audio_path):
    try:
        print(f"加载音频文件: {os.path.basename(audio_path)}")
        y, sr = librosa.load(audio_path, sr=22050)

        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        detected_bpm = round(float(np.mean(tempo)), 6)

        print(f"检测完成,BPM = {detected_bpm}")
        return detected_bpm

    except Exception as e:
        print(f"处理失败: {str(e)}")
        return None

if __name__ == "__main__":
    MUSIC_FILE = filePath
    
    if os.path.exists(MUSIC_FILE):
        detect_bpm(MUSIC_FILE)
    else:
        print("文件不存在")

