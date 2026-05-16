import librosa
import numpy as np
import os
import sys

filePath=sys.argv[1]

def detect_bpm(audio_path):
    try:
        print(f"正在加载音频文件: {os.path.basename(audio_path)}")
        
        # 加载音频
        y, sr = librosa.load(audio_path, sr=22050)

        # 计算节拍起始强度
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)

        # 检测BPM（兼容新版 + 旧版）
        tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

        # 核心修复：取数组平均值，兼容所有版本
        detected_bpm = round(float(np.mean(tempo)), 6)

        print(f"✅ 检测完成！BPM = {detected_bpm}")
        return detected_bpm

    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("    Python BPM检测工具（最终完美版）")
    print("=" * 50)
    MUSIC_FILE = filePath
    
    if os.path.exists(MUSIC_FILE):
        detect_bpm(MUSIC_FILE)
    else:
        print("❌ 错误：文件不存在，请检查路径！")

