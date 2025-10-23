#!/usr/bin/env python3
"""
Demo cac loai bo loc audio khac nhau
"""

import numpy as np
import struct
import wave
import os
from scipy import signal as scipy_signal
import matplotlib.pyplot as plt

def read_pcm_file(filename, sample_rate=16000, n_channels=8):
    """Doc file PCM"""
    with open(filename, 'rb') as f:
        f.seek(2)
        raw_data = f.read()
    
    n_samples_total = len(raw_data) // 2
    n_samples = n_samples_total // n_channels
    
    if n_samples_total % n_channels != 0:
        n_samples = n_samples_total // n_channels
        raw_data = raw_data[:n_samples * n_channels * 2]
    
    samples = struct.unpack(f'<{len(raw_data)//2}h', raw_data)
    audio_data = np.array(samples).reshape(n_samples, n_channels)
    
    return audio_data

def apply_filters_comparison(audio_data, channel_idx, sample_rate=16000):
    """So sanh cac loai bo loc khac nhau"""
    
    channel_data = audio_data[:, channel_idx].copy().astype(float)
    
    results = {
        'original': channel_data,
        'bandpass_100_7000': None,
        'bandpass_300_3000': None,
        'highpass_300': None,
        'lowpass_5000': None,
        'notch_50hz': None  # Loai bo hum 50Hz
    }
    
    # Bandpass 100-7000 Hz (loai bo nhieu thap va cao)
    nyquist = sample_rate / 2
    low = 100 / nyquist
    high = 7000 / nyquist
    b, a = scipy_signal.butter(5, [low, high], btype='band')
    results['bandpass_100_7000'] = scipy_signal.filtfilt(b, a, channel_data)
    
    # Bandpass 300-3000 Hz (giong dien thoai, ro giong noi)
    low = 300 / nyquist
    high = 3000 / nyquist
    b, a = scipy_signal.butter(5, [low, high], btype='band')
    results['bandpass_300_3000'] = scipy_signal.filtfilt(b, a, channel_data)
    
    # Highpass 300 Hz (loai bo nhieu tan so thap)
    normal_cutoff = 300 / nyquist
    b, a = scipy_signal.butter(5, normal_cutoff, btype='high')
    results['highpass_300'] = scipy_signal.filtfilt(b, a, channel_data)
    
    # Lowpass 5000 Hz (loai bo nhieu tan so cao)
    normal_cutoff = 5000 / nyquist
    b, a = scipy_signal.butter(5, normal_cutoff, btype='low')
    results['lowpass_5000'] = scipy_signal.filtfilt(b, a, channel_data)
    
    # Notch filter 50 Hz (loai bo hum dien)
    freq = 50.0
    Q = 30.0
    b, a = scipy_signal.iirnotch(freq / nyquist, Q)
    results['notch_50hz'] = scipy_signal.filtfilt(b, a, channel_data)
    
    return results

def save_filtered_audio(audio_data, output_dir, filename, sample_rate=16000):
    """Luu audio da loc"""
    
    # Normalize
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        normalized = audio_data * (0.9 * 32767 / max_val)
        audio_int16 = normalized.astype(np.int16)
    else:
        audio_int16 = audio_data.astype(np.int16)
    
    filepath = os.path.join(output_dir, filename)
    
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())
    
    return filepath

def plot_filter_comparison(results, channel_idx, output_dir, sample_rate=16000):
    """Ve bieu do so sanh cac bo loc"""
    
    fig, axes = plt.subplots(len(results), 1, figsize=(12, 2*len(results)))
    
    for i, (filter_name, audio_data) in enumerate(results.items()):
        ax = axes[i]
        
        # Chi hien thi 1 giay dau
        n_samples = min(sample_rate, len(audio_data))
        time_axis = np.linspace(0, n_samples/sample_rate, n_samples)
        
        ax.plot(time_axis, audio_data[:n_samples], linewidth=0.5)
        ax.set_title(f'{filter_name}')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f'filter_comparison_channel_{channel_idx+1}.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Da luu bieu do: {plot_file}")
    plt.close()

def plot_frequency_spectrum(results, channel_idx, output_dir, sample_rate=16000):
    """Ve bieu do pho tan so"""
    
    fig, axes = plt.subplots(len(results), 1, figsize=(12, 2*len(results)))
    
    for i, (filter_name, audio_data) in enumerate(results.items()):
        ax = axes[i]
        
        # Tinh FFT
        fft_data = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        
        # Chi hien thi phan duong cua pho
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft_data[:len(fft_data)//2])
        
        ax.plot(positive_freqs, 20*np.log10(positive_fft + 1e-10), linewidth=0.5)
        ax.set_title(f'{filter_name} - Frequency Spectrum')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude (dB)')
        ax.set_xlim([0, sample_rate/2])
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f'frequency_spectrum_channel_{channel_idx+1}.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Da luu bieu do pho: {plot_file}")
    plt.close()

def main():
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/filtered"
    
    print("=== DEMO CAC LOAI BO LOC AUDIO ===")
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print("=" * 50)
    
    # Tao thu muc output
    os.makedirs(output_dir, exist_ok=True)
    
    # Doc file audio
    print("\nDoc file audio...")
    audio_data = read_pcm_file(input_file)
    
    # Chon channel co audio manh nhat (channel 5)
    channel_idx = 4  # Channel 5 (0-indexed)
    
    print(f"\nAp dung cac bo loc len Channel {channel_idx+1}...")
    
    # Ap dung cac bo loc
    results = apply_filters_comparison(audio_data, channel_idx)
    
    # Luu cac file audio da loc
    print("\nLuu cac file audio da loc...")
    for filter_name, audio_filtered in results.items():
        if audio_filtered is not None:
            filename = f'channel_{channel_idx+1}_{filter_name}.wav'
            filepath = save_filtered_audio(audio_filtered, output_dir, filename)
            print(f"  - {filename}")
    
    # Ve bieu do so sanh
    print("\nTao bieu do so sanh...")
    plot_filter_comparison(results, channel_idx, output_dir)
    plot_frequency_spectrum(results, channel_idx, output_dir)
    
    print(f"\n=== HOAN THANH ===")
    print(f"Cac file audio da loc va bieu do duoc luu tai: {output_dir}")
    print("\nCac loai bo loc:")
    print("  1. original - Audio goc khong loc")
    print("  2. bandpass_100_7000 - Loc dải 100-7000 Hz (loai bo nhieu thap va cao)")
    print("  3. bandpass_300_3000 - Loc dải 300-3000 Hz (ro giong noi)")
    print("  4. highpass_300 - Loc thong cao 300 Hz (loai bo nhieu tan so thap)")
    print("  5. lowpass_5000 - Loc thong thap 5000 Hz (loai bo nhieu tan so cao)")
    print("  6. notch_50hz - Loc notch 50 Hz (loai bo hum dien)")

if __name__ == "__main__":
    try:
        import scipy.signal
        import matplotlib.pyplot
    except ImportError as e:
        print(f"Cai dat thu vien can thiet:")
        print("pip install scipy matplotlib")
        exit(1)
    
    main()

