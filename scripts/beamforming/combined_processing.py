#!/usr/bin/env python3
"""
Combined Audio Processing: Beamforming + Bandpass Filtering
"""

import numpy as np
import struct
import wave
import os
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal
import time
from datetime import timedelta

# ============================================================================
# BEAMFORMING
# ============================================================================

class DelayAndSumBeamformer:
    """Delay-and-Sum Beamforming"""
    
    def __init__(self, mic_positions, sample_rate=16000, speed_of_sound=343.0):
        self.mic_positions = np.array(mic_positions)
        self.n_mics = len(mic_positions)
        self.sample_rate = sample_rate
        self.speed_of_sound = speed_of_sound
    
    def steer_vector(self, azimuth_deg, elevation_deg=0):
        """Tinh steering vector cho huong mong muon"""
        azimuth = np.deg2rad(azimuth_deg)
        elevation = np.deg2rad(elevation_deg)
        
        direction = np.array([
            np.cos(elevation) * np.cos(azimuth),
            np.cos(elevation) * np.sin(azimuth),
            np.sin(elevation)
        ])
        
        delays = np.dot(self.mic_positions, direction) / self.speed_of_sound
        delays = delays - np.min(delays)
        
        return delays
    
    def apply_beamforming(self, audio_data, azimuth_deg, elevation_deg=0):
        """Ap dung Delay-and-Sum beamforming"""
        n_samples = audio_data.shape[0]
        delays = self.steer_vector(azimuth_deg, elevation_deg)
        delay_samples = delays * self.sample_rate
        
        beamformed = np.zeros(n_samples)
        
        for i in range(self.n_mics):
            delayed_signal = self._fractional_delay(
                audio_data[:, i], 
                delay_samples[i]
            )
            beamformed += delayed_signal
        
        beamformed = beamformed / self.n_mics
        
        return beamformed
    
    def _fractional_delay(self, signal, delay_samples):
        """Ap dung fractional delay"""
        n_samples = len(signal)
        original_indices = np.arange(n_samples)
        delayed_indices = original_indices - delay_samples
        delayed_indices = np.clip(delayed_indices, 0, n_samples - 1)
        delayed_signal = np.interp(delayed_indices, original_indices, signal)
        
        return delayed_signal
    
    def scan_directions(self, audio_data, azimuth_range=(-180, 180), n_directions=72):
        """Scan nhieu huong de tim nguon am thanh"""
        azimuths = np.linspace(azimuth_range[0], azimuth_range[1], n_directions)
        powers = np.zeros(n_directions)
        
        for i, azimuth in enumerate(azimuths):
            beamformed = self.apply_beamforming(audio_data, azimuth, elevation_deg=0)
            powers[i] = np.sum(beamformed ** 2)
        
        return azimuths, powers

# ============================================================================
# FILTERING
# ============================================================================

class BandpassFilter:
    """Butterworth Bandpass Filter"""
    
    def __init__(self, lowcut, highcut, sample_rate=16000, order=4):
        self.lowcut = lowcut
        self.highcut = highcut
        self.sample_rate = sample_rate
        self.order = order
        
        # Design filter
        nyquist = sample_rate / 2
        low = lowcut / nyquist
        high = highcut / nyquist
        self.b, self.a = scipy_signal.butter(order, [low, high], btype='band')
    
    def apply(self, signal):
        """Ap dung filter"""
        return scipy_signal.filtfilt(self.b, self.a, signal)

# ============================================================================
# UTILITIES
# ============================================================================

def read_pcm_file(filename, sample_rate=16000, n_channels=8):
    """Doc file PCM"""
    print(f"\nDoc file: {filename}")
    
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

def save_wav(audio_data, filepath, sample_rate=16000):
    """Luu file WAV"""
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
    
    print(f"Saved: {filepath}")

def calculate_snr(signal, noise):
    """Tinh SNR (dB)"""
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    
    if noise_power > 0:
        snr_db = 10 * np.log10(signal_power / noise_power)
    else:
        snr_db = float('inf')
    
    return snr_db

def plot_comparison(signals, labels, titles, output_file, sample_rate=16000):
    """Ve bieu do so sanh"""
    n_signals = len(signals)
    
    fig, axes = plt.subplots(n_signals, 2, figsize=(16, 4*n_signals))
    
    if n_signals == 1:
        axes = axes.reshape(1, -1)
    
    for i, (signal, label, title) in enumerate(zip(signals, labels, titles)):
        # Waveform
        time = np.arange(len(signal)) / sample_rate
        axes[i, 0].plot(time, signal, linewidth=0.5)
        axes[i, 0].set_title(f'{title} - Waveform', fontweight='bold')
        axes[i, 0].set_xlabel('Time (s)')
        axes[i, 0].set_ylabel('Amplitude')
        axes[i, 0].grid(True, alpha=0.3)
        
        # Frequency spectrum
        freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
        spectrum = np.abs(np.fft.rfft(signal))
        spectrum_db = 20 * np.log10(spectrum + 1e-10)
        
        axes[i, 1].plot(freqs, spectrum_db, linewidth=0.5)
        axes[i, 1].set_title(f'{title} - Frequency Spectrum', fontweight='bold')
        axes[i, 1].set_xlabel('Frequency (Hz)')
        axes[i, 1].set_ylabel('Magnitude (dB)')
        axes[i, 1].set_xlim([0, 8000])
        axes[i, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved comparison plot: {output_file}")
    plt.close()

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    # ========================================================================
    # TIMING: Bắt đầu đo thời gian
    # ========================================================================
    start_time_total = time.time()
    
    # Configuration
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/combined_processing"
    
    # Parameters
    beamforming_azimuth = None  # None = auto-detect, or specify angle (e.g., 53.2)
    bandpass_lowcut = 600
    bandpass_highcut = 3000
    
    print("="*70)
    print("COMBINED AUDIO PROCESSING")
    print("Beamforming + Bandpass Filtering")
    print("="*70)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Bandpass: {bandpass_lowcut}-{bandpass_highcut} Hz")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read audio
    audio_data = read_pcm_file(input_file)
    
    # Use active channels only (1, 2, 3, 4, 5, 8)
    active_channels = [0, 1, 2, 3, 4, 7]  # 0-indexed
    audio_active = audio_data[:, active_channels]
    
    # Setup microphone array
    radius = 0.05  # 5cm
    mic_positions = []
    for i in [0, 1, 2, 3, 4, 7]:
        angle = 2 * np.pi * i / 8
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.0
        mic_positions.append([x, y, z])
    
    # Create beamformer
    print("\n" + "-"*70)
    print("STEP 1: BEAMFORMING")
    print("-"*70)
    
    beamformer = DelayAndSumBeamformer(mic_positions)
    
    # Auto-detect direction if not specified
    if beamforming_azimuth is None:
        print("\nAuto-detecting peak direction...")
        azimuths, powers = beamformer.scan_directions(audio_active, n_directions=72)
        peak_idx = np.argmax(powers)
        beamforming_azimuth = azimuths[peak_idx]
        print(f"Peak direction detected: {beamforming_azimuth:.1f} degrees")
    else:
        print(f"\nUsing specified direction: {beamforming_azimuth:.1f} degrees")
    
    # Apply beamforming
    print(f"\nApplying beamforming (direction: {beamforming_azimuth:.1f} degrees)...")
    beamformed = beamformer.apply_beamforming(audio_active, beamforming_azimuth)
    
    # Save beamformed audio
    beamformed_file = os.path.join(output_dir, 'step1_beamformed.wav')
    save_wav(beamformed, beamformed_file)
    
    # Create bandpass filter
    print("\n" + "-"*70)
    print("STEP 2: BANDPASS FILTERING")
    print("-"*70)
    
    print(f"\nApplying bandpass filter ({bandpass_lowcut}-{bandpass_highcut} Hz)...")
    bandpass = BandpassFilter(bandpass_lowcut, bandpass_highcut)
    filtered = bandpass.apply(beamformed)
    
    # Save filtered audio
    filtered_file = os.path.join(output_dir, 'step2_filtered.wav')
    save_wav(filtered, filtered_file)
    
    # Create comparison: omnidirectional
    print("\n" + "-"*70)
    print("STEP 3: COMPARISON")
    print("-"*70)
    
    print("\nCreating comparison signals...")
    
    # Omnidirectional (average all mics)
    omnidirectional = np.mean(audio_active, axis=1)
    omnidirectional_file = os.path.join(output_dir, 'comparison_omnidirectional.wav')
    save_wav(omnidirectional, omnidirectional_file)
    
    # Omnidirectional + bandpass
    omnidirectional_filtered = bandpass.apply(omnidirectional)
    omnidirectional_filtered_file = os.path.join(output_dir, 'comparison_omnidirectional_filtered.wav')
    save_wav(omnidirectional_filtered, omnidirectional_filtered_file)
    
    # Calculate SNR improvements (using silent segment as noise estimate)
    # For simplicity, we'll compare RMS values
    rms_original = np.sqrt(np.mean(omnidirectional ** 2))
    rms_beamformed = np.sqrt(np.mean(beamformed ** 2))
    rms_filtered = np.sqrt(np.mean(filtered ** 2))
    
    print(f"\nRMS Levels:")
    print(f"  Original (omnidirectional): {rms_original:.2f}")
    print(f"  After beamforming: {rms_beamformed:.2f}")
    print(f"  After filtering: {rms_filtered:.2f}")
    
    # Plot comparison
    print("\n" + "-"*70)
    print("STEP 4: VISUALIZATION")
    print("-"*70)
    
    print("\nCreating comparison plots...")
    
    # Main comparison plot
    signals = [
        omnidirectional,
        beamformed,
        filtered
    ]
    labels = [
        'Omnidirectional',
        f'Beamformed ({beamforming_azimuth:.1f}°)',
        f'Beamformed + Filtered ({bandpass_lowcut}-{bandpass_highcut} Hz)'
    ]
    titles = [
        '1. Original (Omnidirectional)',
        '2. After Beamforming',
        '3. After Beamforming + Filtering'
    ]
    
    comparison_file = os.path.join(output_dir, 'processing_comparison.png')
    plot_comparison(signals, labels, titles, comparison_file)
    
    # Filter comparison plot
    signals2 = [
        omnidirectional,
        omnidirectional_filtered,
        filtered
    ]
    labels2 = [
        'Original',
        'Filtered only',
        'Beamformed + Filtered'
    ]
    titles2 = [
        '1. Original',
        f'2. Bandpass {bandpass_lowcut}-{bandpass_highcut} Hz only',
        f'3. Beamformed ({beamforming_azimuth:.1f}°) + Bandpass'
    ]
    
    filter_comparison_file = os.path.join(output_dir, 'filter_comparison.png')
    plot_comparison(signals2, labels2, titles2, filter_comparison_file)
    
    # Summary
    print("\n" + "="*70)
    print("PROCESSING COMPLETE!")
    print("="*70)
    
    print(f"\nOutput files in: {output_dir}")
    print("\nProcessing Steps:")
    print(f"  1. Beamforming: Direction {beamforming_azimuth:.1f}°")
    print(f"     -> step1_beamformed.wav")
    print(f"  2. Bandpass Filter: {bandpass_lowcut}-{bandpass_highcut} Hz")
    print(f"     -> step2_filtered.wav")
    print(f"  3. Comparison signals:")
    print(f"     -> comparison_omnidirectional.wav")
    print(f"     -> comparison_omnidirectional_filtered.wav")
    print(f"  4. Visualizations:")
    print(f"     -> processing_comparison.png")
    print(f"     -> filter_comparison.png")
    
    print("\nRecommendations:")
    print("  - Listen to step2_filtered.wav for best quality")
    print("  - Compare with comparison_omnidirectional.wav to hear improvement")
    print("  - Check processing_comparison.png to see frequency content")
    
    print("\nBenefits of Combined Processing:")
    print("  + Beamforming: Removes spatial noise (from unwanted directions)")
    print("  + Bandpass: Removes frequency noise (outside speech range)")
    print("  + Result: Cleaner speech with better SNR")
    
    # ========================================================================
    # TIMING: Thời gian tổng kết
    # ========================================================================
    total_elapsed = time.time() - start_time_total
    
    print("\n" + "="*70)
    print("TIMING SUMMARY")
    print("="*70)
    print(f"Total processing time: {total_elapsed:.3f}s ({timedelta(seconds=int(total_elapsed))})")
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()

