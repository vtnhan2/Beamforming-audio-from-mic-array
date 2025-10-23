#!/usr/bin/env python3
"""
Loc tat ca cac channels co audio voi nhieu loai bo loc khac nhau
Tuong tu nhu filter_audio_demo.py nhung ap dung cho tat ca channels
"""

import numpy as np
import struct
import wave
import os
from scipy import signal as scipy_signal
import matplotlib.pyplot as plt

def read_pcm_file(filename, sample_rate=16000, n_channels=8):
    """Doc file PCM"""
    print(f"Doc file: {filename}")
    
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
    
    print(f"Da doc {n_samples} samples, {n_channels} channels")
    print(f"Duration: {n_samples / sample_rate:.2f} seconds")
    
    return audio_data

def apply_filters(audio_data, sample_rate=16000):
    """Ap dung cac loai bo loc"""
    
    results = {
        'original': audio_data,
        'bandpass_100_7000': None,
        'bandpass_300_3000': None,
        'highpass_300': None,
        'lowpass_5000': None,
        'notch_50hz': None
    }
    
    # Bandpass 100-7000 Hz
    nyquist = sample_rate / 2
    low = 100 / nyquist
    high = 7000 / nyquist
    b, a = scipy_signal.butter(5, [low, high], btype='band')
    results['bandpass_100_7000'] = scipy_signal.filtfilt(b, a, audio_data)
    
    # Bandpass 300-3000 Hz
    low = 300 / nyquist
    high = 3000 / nyquist
    b, a = scipy_signal.butter(5, [low, high], btype='band')
    results['bandpass_300_3000'] = scipy_signal.filtfilt(b, a, audio_data)
    
    # Highpass 300 Hz
    normal_cutoff = 300 / nyquist
    b, a = scipy_signal.butter(5, normal_cutoff, btype='high')
    results['highpass_300'] = scipy_signal.filtfilt(b, a, audio_data)
    
    # Lowpass 5000 Hz
    normal_cutoff = 5000 / nyquist
    b, a = scipy_signal.butter(5, normal_cutoff, btype='low')
    results['lowpass_5000'] = scipy_signal.filtfilt(b, a, audio_data)
    
    # Notch filter 50 Hz
    freq = 50.0
    Q = 30.0
    b, a = scipy_signal.iirnotch(freq / nyquist, Q)
    results['notch_50hz'] = scipy_signal.filtfilt(b, a, audio_data)
    
    return results

def save_wav(audio_data, filepath, sample_rate=16000):
    """Luu file WAV"""
    
    # Normalize
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        normalized = audio_data * (0.9 * 32767 / max_val)
        audio_int16 = normalized.astype(np.int16)
    else:
        audio_int16 = audio_data.astype(np.int16)
    
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())

def plot_waveform_comparison(results, channel_idx, output_dir, sample_rate=16000):
    """Ve bieu do so sanh waveform"""
    
    fig, axes = plt.subplots(len(results), 1, figsize=(14, 2.5*len(results)))
    
    for i, (filter_name, audio_data) in enumerate(results.items()):
        ax = axes[i]
        
        # Hien thi 1 giay dau
        n_samples = min(sample_rate, len(audio_data))
        time_axis = np.linspace(0, n_samples/sample_rate, n_samples)
        
        ax.plot(time_axis, audio_data[:n_samples], linewidth=0.5, color='blue')
        ax.set_title(f'Channel {channel_idx+1} - {filter_name}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 1])
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f'waveform_channel_{channel_idx+1}.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"  + Saved waveform plot: {plot_file}")
    plt.close()

def plot_frequency_spectrum(results, channel_idx, output_dir, sample_rate=16000):
    """Ve bieu do pho tan so"""
    
    fig, axes = plt.subplots(len(results), 1, figsize=(14, 2.5*len(results)))
    
    for i, (filter_name, audio_data) in enumerate(results.items()):
        ax = axes[i]
        
        # Tinh FFT
        fft_data = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        
        # Chi hien thi phan duong
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft_data[:len(fft_data)//2])
        
        ax.plot(positive_freqs, 20*np.log10(positive_fft + 1e-10), linewidth=0.5, color='red')
        ax.set_title(f'Channel {channel_idx+1} - {filter_name} - Frequency Spectrum', 
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude (dB)')
        ax.set_xlim([0, sample_rate/2])
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f'spectrum_channel_{channel_idx+1}.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"  + Saved spectrum plot: {plot_file}")
    plt.close()

def get_active_channels(audio_data):
    """Xac dinh cac channels co audio"""
    
    active_channels = []
    
    for ch in range(audio_data.shape[1]):
        channel_data = audio_data[:, ch]
        rms = np.sqrt(np.mean(channel_data**2))
        zcr = np.sum(np.diff(np.sign(channel_data)) != 0) / len(channel_data)
        
        has_audio = rms > 100 and zcr > 0.01
        
        if has_audio:
            active_channels.append({
                'index': ch,
                'number': ch + 1,
                'rms': rms,
                'has_audio': True
            })
    
    return active_channels

def process_channel(audio_data, channel_idx, output_dir, sample_rate=16000):
    """Xu ly 1 channel: ap dung cac bo loc va luu ket qua"""
    
    channel_number = channel_idx + 1
    channel_data = audio_data[:, channel_idx].copy().astype(float)
    
    print(f"\n{'='*60}")
    print(f"Xu ly Channel {channel_number}")
    print(f"{'='*60}")
    
    # Tao thu muc cho channel nay
    channel_dir = os.path.join(output_dir, f'channel_{channel_number}')
    os.makedirs(channel_dir, exist_ok=True)
    
    # Ap dung cac bo loc
    print("Ap dung cac bo loc...")
    results = apply_filters(channel_data, sample_rate)
    
    # Luu cac file audio
    print("\nLuu cac file audio:")
    for filter_name, filtered_data in results.items():
        if filtered_data is not None:
            filename = f'channel_{channel_number}_{filter_name}.wav'
            filepath = os.path.join(channel_dir, filename)
            save_wav(filtered_data, filepath, sample_rate)
            print(f"  + {filename}")
    
    # Tao cac bieu do
    print("\nTao bieu do:")
    plot_waveform_comparison(results, channel_idx, channel_dir, sample_rate)
    plot_frequency_spectrum(results, channel_idx, channel_dir, sample_rate)
    
    return channel_dir

def create_summary_comparison(audio_data, active_channels, output_dir, sample_rate=16000):
    """Tao bieu do so sanh tat ca cac channels"""
    
    print(f"\n{'='*60}")
    print("Tao bieu do tong hop so sanh tat ca channels")
    print(f"{'='*60}")
    
    # So sanh waveform cua tat ca channels (original)
    fig, axes = plt.subplots(len(active_channels), 1, figsize=(14, 2*len(active_channels)))
    
    if len(active_channels) == 1:
        axes = [axes]
    
    for i, ch_info in enumerate(active_channels):
        ax = axes[i]
        ch_idx = ch_info['index']
        channel_data = audio_data[:, ch_idx]
        
        # Hien thi 1 giay dau
        n_samples = min(sample_rate, len(channel_data))
        time_axis = np.linspace(0, n_samples/sample_rate, n_samples)
        
        ax.plot(time_axis, channel_data[:n_samples], linewidth=0.5)
        ax.set_title(f'Channel {ch_info["number"]} (RMS: {ch_info["rms"]:.1f})', 
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 1])
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'all_channels_comparison.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {plot_file}")
    plt.close()
    
    # So sanh pho tan so cua tat ca channels
    fig, axes = plt.subplots(len(active_channels), 1, figsize=(14, 2*len(active_channels)))
    
    if len(active_channels) == 1:
        axes = [axes]
    
    for i, ch_info in enumerate(active_channels):
        ax = axes[i]
        ch_idx = ch_info['index']
        channel_data = audio_data[:, ch_idx]
        
        # Tinh FFT
        fft_data = np.fft.fft(channel_data)
        freqs = np.fft.fftfreq(len(channel_data), 1/sample_rate)
        
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft_data[:len(fft_data)//2])
        
        ax.plot(positive_freqs, 20*np.log10(positive_fft + 1e-10), linewidth=0.5)
        ax.set_title(f'Channel {ch_info["number"]} - Frequency Spectrum', 
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude (dB)')
        ax.set_xlim([0, sample_rate/2])
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'all_channels_spectrum.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {plot_file}")
    plt.close()

def main():
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/filtered_all"
    
    print("="*60)
    print("LOC TAT CA CAC CHANNELS CO AUDIO")
    print("="*60)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print("="*60)
    
    # Tao thu muc output
    os.makedirs(output_dir, exist_ok=True)
    
    # Doc file audio
    audio_data = read_pcm_file(input_file)
    
    # Xac dinh cac channels co audio
    print("\nXac dinh cac channels co audio...")
    active_channels = get_active_channels(audio_data)
    
    print(f"\nTim thay {len(active_channels)} channels co audio:")
    for ch_info in active_channels:
        print(f"  - Channel {ch_info['number']}: RMS = {ch_info['rms']:.1f}")
    
    # Xu ly tung channel
    processed_dirs = []
    for ch_info in active_channels:
        channel_dir = process_channel(audio_data, ch_info['index'], output_dir)
        processed_dirs.append(channel_dir)
    
    # Tao bieu do so sanh tong hop
    create_summary_comparison(audio_data, active_channels, output_dir)
    
    # Tong ket
    print(f"\n{'='*60}")
    print("HOAN THANH!")
    print(f"{'='*60}")
    print(f"\nDa xu ly {len(active_channels)} channels:")
    for ch_info in active_channels:
        print(f"  - Channel {ch_info['number']}")
    
    print(f"\nCac file output:")
    print(f"  - Moi channel co 6 file audio (cac loai bo loc khac nhau)")
    print(f"  - Moi channel co 2 bieu do (waveform va spectrum)")
    print(f"  - Co 2 bieu do tong hop so sanh tat ca channels")
    
    print(f"\nThu muc output: {output_dir}")
    print(f"\nCac loai bo loc:")
    print(f"  1. original          - Goc khong loc")
    print(f"  2. bandpass_100_7000 - Loc dai 100-7000 Hz")
    print(f"  3. bandpass_300_3000 - Loc dai 300-3000 Hz (giong noi)")
    print(f"  4. highpass_300      - Loc thong cao 300 Hz")
    print(f"  5. lowpass_5000      - Loc thong thap 5000 Hz")
    print(f"  6. notch_50hz        - Loai bo hum 50 Hz")
    
    total_files = len(active_channels) * 8 + 2  # 6 audio + 2 plots per channel + 2 summary plots
    print(f"\nTong cong: {total_files} files")

if __name__ == "__main__":
    try:
        import scipy.signal
        import matplotlib.pyplot
    except ImportError as e:
        print("Cai dat thu vien can thiet:")
        print("pip install scipy matplotlib")
        exit(1)
    
    main()

