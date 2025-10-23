#!/usr/bin/env python3
"""
Extract and Filter Individual Audio Channels
Tach va loc audio cua tung channel
"""

import numpy as np
import struct
import wave
import os
from scipy import signal as scipy_signal

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

def apply_bandpass_filter(audio_data, lowcut=100, highcut=7000, sample_rate=16000, order=5):
    """Ap dung bo loc bandpass de loai bo nhieu"""
    nyquist = sample_rate / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    
    b, a = scipy_signal.butter(order, [low, high], btype='band')
    filtered_data = scipy_signal.filtfilt(b, a, audio_data)
    
    return filtered_data

def apply_highpass_filter(audio_data, cutoff=100, sample_rate=16000, order=5):
    """Ap dung bo loc highpass de loai bo tan so thap"""
    nyquist = sample_rate / 2
    normal_cutoff = cutoff / nyquist
    
    b, a = scipy_signal.butter(order, normal_cutoff, btype='high')
    filtered_data = scipy_signal.filtfilt(b, a, audio_data)
    
    return filtered_data

def apply_lowpass_filter(audio_data, cutoff=7000, sample_rate=16000, order=5):
    """Ap dung bo loc lowpass de loai bo tan so cao"""
    nyquist = sample_rate / 2
    normal_cutoff = cutoff / nyquist
    
    b, a = scipy_signal.butter(order, normal_cutoff, btype='low')
    filtered_data = scipy_signal.filtfilt(b, a, audio_data)
    
    return filtered_data

def normalize_audio(audio_data, target_level=0.9):
    """Normalize audio ve muc am thanh mong muon"""
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        normalized = audio_data * (target_level * 32767 / max_val)
        return normalized.astype(np.int16)
    return audio_data.astype(np.int16)

def save_channel_as_wav(audio_data, channel_idx, output_dir, sample_rate=16000, 
                        apply_filter=True, filter_type='bandpass'):
    """Luu 1 channel thanh file WAV"""
    
    # Lay data cua channel
    channel_data = audio_data[:, channel_idx].copy()
    
    # Ap dung bo loc neu can
    if apply_filter:
        print(f"  - Ap dung bo loc {filter_type}...")
        if filter_type == 'bandpass':
            channel_data = apply_bandpass_filter(channel_data, sample_rate=sample_rate)
        elif filter_type == 'highpass':
            channel_data = apply_highpass_filter(channel_data, sample_rate=sample_rate)
        elif filter_type == 'lowpass':
            channel_data = apply_lowpass_filter(channel_data, sample_rate=sample_rate)
    
    # Normalize
    channel_data = normalize_audio(channel_data)
    
    # Luu file WAV
    filename = os.path.join(output_dir, f'channel_{channel_idx+1}.wav')
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(channel_data.tobytes())
    
    print(f"  - Da luu: {filename}")
    
    return filename

def save_channel_as_pcm(audio_data, channel_idx, output_dir, sample_rate=16000,
                        apply_filter=True, filter_type='bandpass'):
    """Luu 1 channel thanh file PCM"""
    
    # Lay data cua channel
    channel_data = audio_data[:, channel_idx].copy()
    
    # Ap dung bo loc neu can
    if apply_filter:
        print(f"  - Ap dung bo loc {filter_type}...")
        if filter_type == 'bandpass':
            channel_data = apply_bandpass_filter(channel_data, sample_rate=sample_rate)
        elif filter_type == 'highpass':
            channel_data = apply_highpass_filter(channel_data, sample_rate=sample_rate)
        elif filter_type == 'lowpass':
            channel_data = apply_lowpass_filter(channel_data, sample_rate=sample_rate)
    
    # Normalize
    channel_data = normalize_audio(channel_data)
    
    # Luu file PCM
    filename = os.path.join(output_dir, f'channel_{channel_idx+1}.pcm')
    
    with open(filename, 'wb') as pcm_file:
        pcm_file.write(channel_data.tobytes())
    
    print(f"  - Da luu: {filename}")
    
    return filename

def extract_active_channels_only(audio_data, output_dir, sample_rate=16000,
                                 output_format='wav', apply_filter=True, filter_type='bandpass'):
    """Chi trich xuat cac channels co audio"""
    
    print("\nKiem tra cac channels co audio...")
    active_channels = []
    
    for ch in range(audio_data.shape[1]):
        channel_data = audio_data[:, ch]
        rms = np.sqrt(np.mean(channel_data**2))
        zcr = np.sum(np.diff(np.sign(channel_data)) != 0) / len(channel_data)
        
        has_audio = rms > 100 and zcr > 0.01
        
        if has_audio:
            active_channels.append(ch)
            print(f"Channel {ch+1}: CO AUDIO (RMS: {rms:.1f})")
        else:
            print(f"Channel {ch+1}: KHONG CO AUDIO (RMS: {rms:.1f})")
    
    print(f"\nTim thay {len(active_channels)} channels co audio: {[ch+1 for ch in active_channels]}")
    
    # Trich xuat cac channels co audio
    extracted_files = []
    for ch_idx in active_channels:
        print(f"\nTrich xuat Channel {ch_idx+1}...")
        
        if output_format == 'wav':
            filename = save_channel_as_wav(audio_data, ch_idx, output_dir, sample_rate,
                                          apply_filter, filter_type)
        else:
            filename = save_channel_as_pcm(audio_data, ch_idx, output_dir, sample_rate,
                                          apply_filter, filter_type)
        
        extracted_files.append(filename)
    
    return extracted_files, active_channels

def extract_all_channels(audio_data, output_dir, sample_rate=16000,
                        output_format='wav', apply_filter=True, filter_type='bandpass'):
    """Trich xuat tat ca cac channels"""
    
    n_channels = audio_data.shape[1]
    extracted_files = []
    
    print(f"\nTrich xuat tat ca {n_channels} channels...")
    
    for ch_idx in range(n_channels):
        print(f"\nTrich xuat Channel {ch_idx+1}...")
        
        if output_format == 'wav':
            filename = save_channel_as_wav(audio_data, ch_idx, output_dir, sample_rate,
                                          apply_filter, filter_type)
        else:
            filename = save_channel_as_pcm(audio_data, ch_idx, output_dir, sample_rate,
                                          apply_filter, filter_type)
        
        extracted_files.append(filename)
    
    return extracted_files

def create_mixed_audio(audio_data, active_channels, output_dir, sample_rate=16000,
                      apply_filter=True, filter_type='bandpass'):
    """Tron cac channels co audio thanh 1 file"""
    
    print("\nTao file audio tron tu cac channels co audio...")
    
    # Lay data cua cac channels co audio
    mixed_data = np.zeros(audio_data.shape[0])
    
    for ch_idx in active_channels:
        channel_data = audio_data[:, ch_idx].copy()
        
        # Ap dung bo loc
        if apply_filter:
            if filter_type == 'bandpass':
                channel_data = apply_bandpass_filter(channel_data, sample_rate=sample_rate)
            elif filter_type == 'highpass':
                channel_data = apply_highpass_filter(channel_data, sample_rate=sample_rate)
            elif filter_type == 'lowpass':
                channel_data = apply_lowpass_filter(channel_data, sample_rate=sample_rate)
        
        mixed_data += channel_data
    
    # Normalize
    mixed_data = normalize_audio(mixed_data / len(active_channels))
    
    # Luu file WAV
    filename = os.path.join(output_dir, 'mixed_audio.wav')
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(mixed_data.tobytes())
    
    print(f"Da luu file audio tron: {filename}")
    
    return filename

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract and Filter Audio Channels')
    parser.add_argument('--input', '-i', default='../../output/audio/original_8channels.pcm',
                       help='Input PCM file')
    parser.add_argument('--output-dir', '-o', default='../../output/audio/channels',
                       help='Output directory')
    parser.add_argument('--format', '-f', choices=['wav', 'pcm'], default='wav',
                       help='Output format (wav or pcm)')
    parser.add_argument('--filter', choices=['none', 'bandpass', 'highpass', 'lowpass'],
                       default='bandpass', help='Filter type')
    parser.add_argument('--all', action='store_true',
                       help='Extract all channels (default: only active channels)')
    parser.add_argument('--mixed', action='store_true',
                       help='Create mixed audio from active channels')
    
    args = parser.parse_args()
    
    print("=== AUDIO CHANNEL EXTRACTION ===")
    print(f"Input file: {args.input}")
    print(f"Output directory: {args.output_dir}")
    print(f"Output format: {args.format}")
    print(f"Filter type: {args.filter}")
    print("=" * 50)
    
    # Tao thu muc output
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Doc file audio
    audio_data = read_pcm_file(args.input)
    
    # Trich xuat channels
    apply_filter = args.filter != 'none'
    
    if args.all:
        # Trich xuat tat ca channels
        extracted_files = extract_all_channels(audio_data, args.output_dir,
                                               output_format=args.format,
                                               apply_filter=apply_filter,
                                               filter_type=args.filter)
    else:
        # Chi trich xuat channels co audio
        extracted_files, active_channels = extract_active_channels_only(
            audio_data, args.output_dir,
            output_format=args.format,
            apply_filter=apply_filter,
            filter_type=args.filter)
        
        # Tao file audio tron neu can
        if args.mixed:
            mixed_file = create_mixed_audio(audio_data, active_channels, args.output_dir,
                                           apply_filter=apply_filter,
                                           filter_type=args.filter)
    
    print(f"\n=== HOAN THANH ===")
    print(f"Da trich xuat {len(extracted_files)} files")
    print(f"Thu muc output: {args.output_dir}")
    
    return extracted_files

if __name__ == "__main__":
    try:
        import scipy.signal
    except ImportError:
        print("Cai dat scipy de su dung bo loc:")
        print("pip install scipy")
        exit(1)
    
    main()

