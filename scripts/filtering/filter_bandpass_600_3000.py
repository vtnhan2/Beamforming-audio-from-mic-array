#!/usr/bin/env python3
"""
Ap dung bo loc bandpass 600-3000 Hz cho tat ca channels
Dai tan so toi uu hon cho giong noi
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

def apply_bandpass_600_3000(audio_data, sample_rate=16000, order=5):
    """Ap dung bo loc bandpass 600-3000 Hz"""
    
    nyquist = sample_rate / 2
    low = 600 / nyquist
    high = 3000 / nyquist
    
    b, a = scipy_signal.butter(order, [low, high], btype='band')
    filtered_data = scipy_signal.filtfilt(b, a, audio_data)
    
    return filtered_data

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

def plot_comparison(original, filtered, channel_idx, output_dir, sample_rate=16000):
    """Ve bieu do so sanh truoc va sau khi loc"""
    
    fig, axes = plt.subplots(4, 1, figsize=(14, 10))
    
    # Waveform - Original
    ax = axes[0]
    n_samples = min(sample_rate, len(original))
    time_axis = np.linspace(0, n_samples/sample_rate, n_samples)
    ax.plot(time_axis, original[:n_samples], linewidth=0.5, color='blue')
    ax.set_title(f'Channel {channel_idx+1} - Original (Khong loc)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    
    # Waveform - Filtered
    ax = axes[1]
    ax.plot(time_axis, filtered[:n_samples], linewidth=0.5, color='red')
    ax.set_title(f'Channel {channel_idx+1} - Bandpass 600-3000 Hz', fontsize=12, fontweight='bold')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    
    # Spectrum - Original
    ax = axes[2]
    fft_data = np.fft.fft(original)
    freqs = np.fft.fftfreq(len(original), 1/sample_rate)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft_data[:len(fft_data)//2])
    ax.plot(positive_freqs, 20*np.log10(positive_fft + 1e-10), linewidth=0.5, color='blue')
    ax.set_title(f'Spectrum - Original', fontsize=12, fontweight='bold')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.axvline(x=600, color='green', linestyle='--', alpha=0.5, label='600 Hz')
    ax.axvline(x=3000, color='green', linestyle='--', alpha=0.5, label='3000 Hz')
    ax.set_xlim([0, sample_rate/2])
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Spectrum - Filtered
    ax = axes[3]
    fft_data = np.fft.fft(filtered)
    freqs = np.fft.fftfreq(len(filtered), 1/sample_rate)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft_data[:len(fft_data)//2])
    ax.plot(positive_freqs, 20*np.log10(positive_fft + 1e-10), linewidth=0.5, color='red')
    ax.set_title(f'Spectrum - Bandpass 600-3000 Hz', fontsize=12, fontweight='bold')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.axvline(x=600, color='green', linestyle='--', alpha=0.5, label='600 Hz cutoff')
    ax.axvline(x=3000, color='green', linestyle='--', alpha=0.5, label='3000 Hz cutoff')
    ax.set_xlim([0, sample_rate/2])
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f'comparison_channel_{channel_idx+1}.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"  + Saved comparison plot: {plot_file}")
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
    """Xu ly 1 channel"""
    
    channel_number = channel_idx + 1
    channel_data = audio_data[:, channel_idx].copy().astype(float)
    
    print(f"\nXu ly Channel {channel_number}...")
    
    # Ap dung bo loc bandpass 600-3000 Hz
    print("  - Ap dung bo loc bandpass 600-3000 Hz...")
    filtered_data = apply_bandpass_600_3000(channel_data, sample_rate)
    
    # Luu file audio
    filename = f'channel_{channel_number}_bandpass_600_3000.wav'
    filepath = os.path.join(output_dir, filename)
    save_wav(filtered_data, filepath, sample_rate)
    print(f"  - Saved: {filename}")
    
    # Tao bieu do so sanh
    plot_comparison(channel_data, filtered_data, channel_idx, output_dir, sample_rate)
    
    return filepath

def create_mixed_audio(audio_data, active_channels, output_dir, sample_rate=16000):
    """Tao file audio tron tu cac channels da loc"""
    
    print("\nTao file audio tron...")
    
    mixed_data = np.zeros(audio_data.shape[0])
    
    for ch_info in active_channels:
        ch_idx = ch_info['index']
        channel_data = audio_data[:, ch_idx].copy().astype(float)
        
        # Ap dung bo loc
        filtered_data = apply_bandpass_600_3000(channel_data, sample_rate)
        mixed_data += filtered_data
    
    # Trung binh
    mixed_data = mixed_data / len(active_channels)
    
    # Luu file
    filename = 'mixed_audio_bandpass_600_3000.wav'
    filepath = os.path.join(output_dir, filename)
    save_wav(mixed_data, filepath, sample_rate)
    print(f"  - Saved: {filename}")
    
    return filepath

def create_summary_plot(audio_data, active_channels, output_dir, sample_rate=16000):
    """Tao bieu do tong hop tat ca channels sau khi loc"""
    
    print("\nTao bieu do tong hop...")
    
    fig, axes = plt.subplots(len(active_channels), 1, figsize=(14, 2*len(active_channels)))
    
    if len(active_channels) == 1:
        axes = [axes]
    
    for i, ch_info in enumerate(active_channels):
        ax = axes[i]
        ch_idx = ch_info['index']
        channel_data = audio_data[:, ch_idx].copy().astype(float)
        
        # Ap dung bo loc
        filtered_data = apply_bandpass_600_3000(channel_data, sample_rate)
        
        # Hien thi 1 giay dau
        n_samples = min(sample_rate, len(filtered_data))
        time_axis = np.linspace(0, n_samples/sample_rate, n_samples)
        
        ax.plot(time_axis, filtered_data[:n_samples], linewidth=0.5)
        ax.set_title(f'Channel {ch_info["number"]} - Bandpass 600-3000 Hz (RMS: {ch_info["rms"]:.1f})', 
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 1])
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'all_channels_bandpass_600_3000.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"  - Saved: {plot_file}")
    plt.close()

def main():
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/bandpass_600_3000"
    
    print("="*60)
    print("BO LOC BANDPASS 600-3000 Hz")
    print("Dai tan so toi uu cho giong noi")
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
    print(f"\n{'='*60}")
    print("XU LY TUNG CHANNEL")
    print(f"{'='*60}")
    
    processed_files = []
    for ch_info in active_channels:
        filepath = process_channel(audio_data, ch_info['index'], output_dir)
        processed_files.append(filepath)
    
    # Tao file audio tron
    mixed_file = create_mixed_audio(audio_data, active_channels, output_dir)
    
    # Tao bieu do tong hop
    create_summary_plot(audio_data, active_channels, output_dir)
    
    # Tong ket
    print(f"\n{'='*60}")
    print("HOAN THANH!")
    print(f"{'='*60}")
    print(f"\nDa xu ly {len(active_channels)} channels:")
    for ch_info in active_channels:
        print(f"  - Channel {ch_info['number']}")
    
    print(f"\nCac file output:")
    print(f"  - {len(active_channels)} file audio da loc (bandpass 600-3000 Hz)")
    print(f"  - {len(active_channels)} bieu do so sanh (truoc/sau khi loc)")
    print(f"  - 1 file audio tron (mixed)")
    print(f"  - 1 bieu do tong hop tat ca channels")
    
    print(f"\nThu muc output: {output_dir}")
    
    total_files = len(active_channels) * 2 + 2  # audio + comparison per channel + mixed + summary
    print(f"\nTong cong: {total_files} files")
    
    print(f"\nBo loc bandpass 600-3000 Hz:")
    print(f"  - Loai bo tan so < 600 Hz (hum dien, nhieu thap)")
    print(f"  - Loai bo tan so > 3000 Hz (nhieu cao)")
    print(f"  - Giu lai dai giong noi ro rang nhat")
    print(f"  - Phu hop cho speech recognition, voice analysis")

if __name__ == "__main__":
    try:
        import scipy.signal
        import matplotlib.pyplot
    except ImportError as e:
        print("Cai dat thu vien can thiet:")
        print("pip install scipy matplotlib")
        exit(1)
    
    main()

