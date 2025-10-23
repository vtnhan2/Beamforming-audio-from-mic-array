#!/usr/bin/env python3
"""
Script phân tích file original_8channels.pcm
Kiểm tra các channel có audio và không có audio
"""

import numpy as np
import struct
import matplotlib.pyplot as plt
import os
import sys

def analyze_pcm_file(filename, sample_rate=16000, n_channels=8, bit_depth=16):
    """Phân tích file PCM và hiển thị thông tin chi tiết"""
    
    print(f"Phân tích file: {filename}")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Channels: {n_channels}")
    print(f"Bit depth: {bit_depth} bits")
    print("=" * 50)
    
    # Đọc file
    with open(filename, 'rb') as f:
        # Skip 2 bytes offset
        f.seek(2)
        raw_data = f.read()
    
    # Convert bytes to numpy array
    n_samples_total = len(raw_data) // 2  # 16-bit = 2 bytes per sample
    n_samples = n_samples_total // n_channels
    
    # Đảm bảo số samples chia hết cho số channels
    if n_samples_total % n_channels != 0:
        print(f"Warning: File size {len(raw_data)} bytes, expected multiple of {n_channels * 2}")
        n_samples = n_samples_total // n_channels
        # Cắt bỏ phần dư
        raw_data = raw_data[:n_samples * n_channels * 2]
    
    samples = struct.unpack(f'<{len(raw_data)//2}h', raw_data)
    audio_data = np.array(samples).reshape(n_samples, n_channels)
    
    print(f"Tong so samples: {n_samples}")
    print(f"Thoi luong: {n_samples / sample_rate:.2f} giay")
    print(f"Kich thuoc file: {len(raw_data) + 2} bytes")
    print("")
    
    # Phan tich tung channel
    print("PHAN TICH CAC CHANNEL:")
    print("-" * 50)
    
    channel_stats = []
    
    for ch in range(n_channels):
        channel_data = audio_data[:, ch]
        
        # Tính các thống kê
        rms = np.sqrt(np.mean(channel_data**2))
        max_amp = np.max(np.abs(channel_data))
        mean_amp = np.mean(np.abs(channel_data))
        
        # Zero crossing rate
        zcr = np.sum(np.diff(np.sign(channel_data)) != 0) / len(channel_data)
        
        # Phân loại channel
        has_audio = rms > 100 and zcr > 0.01
        
        stats = {
            'channel': ch + 1,
            'rms': rms,
            'max_amplitude': max_amp,
            'mean_amplitude': mean_amp,
            'zcr': zcr,
            'has_audio': has_audio
        }
        
        channel_stats.append(stats)
        
        status = "CO AUDIO" if has_audio else "KHONG CO AUDIO"
        print(f"Channel {ch+1:2d}: {status:15s} | RMS: {rms:8.1f} | Max: {max_amp:8.1f} | ZCR: {zcr:.4f}")
    
    print("")
    
    # Tom tat
    active_channels = [ch for ch in channel_stats if ch['has_audio']]
    silent_channels = [ch for ch in channel_stats if not ch['has_audio']]
    
    print("TOM TAT:")
    print("-" * 50)
    print(f"Channels co audio: {[ch['channel'] for ch in active_channels]}")
    print(f"Channels khong co audio: {[ch['channel'] for ch in silent_channels]}")
    print(f"Tong so channels co audio: {len(active_channels)}/{n_channels}")
    
    return channel_stats, audio_data

def plot_audio_channels(audio_data, channel_stats, sample_rate=16000):
    """Vẽ biểu đồ audio của các channels"""
    
    n_channels = audio_data.shape[1]
    n_samples = audio_data.shape[0]
    duration = n_samples / sample_rate
    
    # Tạo subplot cho mỗi channel
    fig, axes = plt.subplots(n_channels, 1, figsize=(12, 2*n_channels))
    if n_channels == 1:
        axes = [axes]
    
    for ch in range(n_channels):
        ax = axes[ch]
        channel_data = audio_data[:, ch]
        time_axis = np.linspace(0, duration, n_samples)
        
        # Ve waveform
        ax.plot(time_axis, channel_data, linewidth=0.5)
        ax.set_title(f'Channel {ch+1} - {"CO AUDIO" if channel_stats[ch]["has_audio"] else "KHONG CO AUDIO"}')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3)
        
        # Highlight neu co audio
        if channel_stats[ch]['has_audio']:
            ax.set_facecolor('lightgreen')
        else:
            ax.set_facecolor('lightcoral')
    
    plt.tight_layout()
    plt.savefig('../../output/visualizations/audio_channels_analysis.png', dpi=150, bbox_inches='tight')
    print("Da luu bieu do: audio_channels_analysis.png")
    
    return fig

def main():
    filename = "../../output/audio/original_8channels.pcm"
    
    # Kiểm tra file
    if not os.path.exists(filename):
        print(f"Loi: Khong tim thay file {filename}")
        print("Vui long dat file original_8channels.pcm vao thu muc hien tai")
        return 1
    
    try:
        # Phan tich file
        channel_stats, audio_data = analyze_pcm_file(filename)
        
        # Ve bieu do
        print("\nTao bieu do...")
        plot_audio_channels(audio_data, channel_stats)
        
        # Luu ket qua phan tich
        import json
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.bool_):
                return bool(obj)
            return obj
        
        # Convert channel_stats to JSON-serializable format
        json_channel_stats = []
        for ch in channel_stats:
            json_ch = {}
            for key, value in ch.items():
                json_ch[key] = convert_numpy(value)
            json_channel_stats.append(json_ch)
        
        result = {
            'filename': filename,
            'sample_rate': 16000,
            'n_channels': 8,
            'duration': float(len(audio_data) / 16000),
            'channel_analysis': json_channel_stats,
            'active_channels': [int(ch['channel']) for ch in channel_stats if ch['has_audio']],
            'silent_channels': [int(ch['channel']) for ch in channel_stats if not ch['has_audio']]
        }
        
        with open('../../output/results/audio_analysis_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print("\nKet qua phan tich da luu: audio_analysis_result.json")
        
    except Exception as e:
        print(f"Loi: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
