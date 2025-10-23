#!/usr/bin/env python3
"""
Simple Audio Source Localization Script
"""

import numpy as np
import struct
import json
import os

def read_pcm_file(filename, sample_rate=16000, n_channels=8):
    """Doc file PCM"""
    print(f"Doc file: {filename}")
    
    with open(filename, 'rb') as f:
        f.seek(2)  # Skip 2 bytes offset
        raw_data = f.read()
    
    # Convert bytes to numpy array
    n_samples_total = len(raw_data) // 2
    n_samples = n_samples_total // n_channels
    
    if n_samples_total % n_channels != 0:
        n_samples = n_samples_total // n_channels
        raw_data = raw_data[:n_samples * n_channels * 2]
    
    samples = struct.unpack(f'<{len(raw_data)//2}h', raw_data)
    audio_data = np.array(samples).reshape(n_samples, n_channels)
    
    print(f"Da doc {n_samples} samples, {n_channels} channels")
    print(f"Duration: {n_samples / sample_rate:.2f} seconds")
    
    return audio_data

def analyze_channels(audio_data):
    """Phan tich cac channels"""
    print("\nPhan tich channels:")
    print("-" * 50)
    
    channel_stats = []
    
    for ch in range(audio_data.shape[1]):
        channel_data = audio_data[:, ch]
        
        # Tinh cac thong ke
        rms = np.sqrt(np.mean(channel_data**2))
        max_amp = np.max(np.abs(channel_data))
        zcr = np.sum(np.diff(np.sign(channel_data)) != 0) / len(channel_data)
        
        # Phan loai channel
        has_audio = rms > 100 and zcr > 0.01
        
        stats = {
            'channel': ch + 1,
            'rms': float(rms),
            'max_amplitude': int(max_amp),
            'zcr': float(zcr),
            'has_audio': bool(has_audio)
        }
        
        channel_stats.append(stats)
        
        status = "CO AUDIO" if has_audio else "KHONG CO AUDIO"
        print(f"Channel {ch+1:2d}: {status:15s} | RMS: {rms:8.1f} | Max: {max_amp:8.1f} | ZCR: {zcr:.4f}")
    
    return channel_stats

def calculate_tdoa(audio_data, ref_channel=0):
    """Tinh Time Difference of Arrival"""
    print("\nTinh TDOA...")
    
    tdoas = []
    sample_rate = 16000
    
    for ch in range(audio_data.shape[1]):
        if ch == ref_channel:
            tdoas.append(0.0)
            continue
            
        # Cross-correlation de tim delay
        correlation = np.correlate(audio_data[:, ref_channel], audio_data[:, ch], mode='full')
        delay = np.argmax(correlation) - len(audio_data) + 1
        
        # Convert delay to time
        tdoa = delay / sample_rate
        tdoas.append(tdoa)
    
    print("TDOAs (seconds):", [f"{t:.6f}" for t in tdoas])
    return tdoas

def localize_source(tdoas):
    """Xac dinh vi tri nguon am thanh"""
    print("\nXac dinh vi tri nguon am thanh...")
    
    # Microphone array configuration (8 microphones in circle)
    radius = 0.05  # 5cm radius
    mic_positions = []
    
    for i in range(8):
        angle = 2 * np.pi * i / 8
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.0
        mic_positions.append([x, y, z])
    
    mic_positions = np.array(mic_positions)
    speed_of_sound = 343.0  # m/s
    
    # Simplified localization using least squares
    n_mics = len(tdoas)
    A = np.zeros((n_mics-1, 3))
    b = np.zeros(n_mics-1)
    
    for i in range(1, n_mics):
        A[i-1, 0] = 2 * (mic_positions[i, 0] - mic_positions[0, 0])
        A[i-1, 1] = 2 * (mic_positions[i, 1] - mic_positions[0, 1])
        A[i-1, 2] = 2 * (mic_positions[i, 2] - mic_positions[0, 2])
        
        distance_diff = tdoas[i] * speed_of_sound
        b[i-1] = distance_diff
    
    # Solve least squares
    try:
        position = np.linalg.lstsq(A, b, rcond=None)[0]
        x, y, z = position[0], position[1], position[2]
        
        # Convert to spherical coordinates
        r = np.sqrt(x**2 + y**2 + z**2)
        azimuth = np.arctan2(y, x) * 180 / np.pi
        elevation = np.arcsin(z / r) * 180 / np.pi if r > 0 else 0
        
        return {
            'position_cartesian': [float(x), float(y), float(z)],
            'position_spherical': {
                'distance': float(r),
                'azimuth': float(azimuth),
                'elevation': float(elevation)
            }
        }
    except:
        return {
            'position_cartesian': [0.0, 0.0, 0.0],
            'position_spherical': {
                'distance': 0.0,
                'azimuth': 0.0,
                'elevation': 0.0
            }
        }

def main():
    filename = "../../output/audio/original_8channels.pcm"
    output_file = "audio/localization_result.json"
    
    print("=== SIMPLE AUDIO SOURCE LOCALIZATION ===")
    print(f"Input file: {filename}")
    print(f"Output file: {output_file}")
    print("=" * 50)
    
    # Doc file audio
    audio_data = read_pcm_file(filename)
    
    # Phan tich channels
    channel_stats = analyze_channels(audio_data)
    
    # Tinh TDOA
    tdoas = calculate_tdoa(audio_data)
    
    # Localization
    localization_result = localize_source(tdoas)
    
    # Tao ket qua cuoi cung
    result = {
        'filename': filename,
        'sample_rate': 16000,
        'n_channels': 8,
        'duration': len(audio_data) / 16000,
        'channel_analysis': channel_stats,
        'tdoas': [float(t) for t in tdoas],
        'localization': localization_result,
        'active_channels': [ch['channel'] for ch in channel_stats if ch['has_audio']],
        'silent_channels': [ch['channel'] for ch in channel_stats if not ch['has_audio']]
    }
    
    # Luu ket qua
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n=== KET QUA LOCALIZATION ===")
    print(f"Vi tri Cartesian (x, y, z): {localization_result['position_cartesian']}")
    print(f"Vi tri Spherical:")
    print(f"  - Khoang cach: {localization_result['position_spherical']['distance']:.3f} m")
    print(f"  - Goc phuong vi: {localization_result['position_spherical']['azimuth']:.1f}°")
    print(f"  - Goc nang: {localization_result['position_spherical']['elevation']:.1f}°")
    print(f"\nKet qua da luu vao: {output_file}")
    
    return result

if __name__ == "__main__":
    main()
