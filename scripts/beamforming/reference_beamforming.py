#!/usr/bin/env python3
"""
Reference-Based Beamforming - Tách vocal dựa trên reference signal
Sử dụng channel 5 làm reference để tách vocal cụ thể
"""

import numpy as np
import struct
import wave
import os
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal
from scipy.fft import fft, fftfreq
import time
from datetime import timedelta

class ReferenceBeamformer:
    """
    Beamforming dựa trên reference signal (channel 5)
    """
    
    def __init__(self, mic_positions, sample_rate=16000, speed_of_sound=343.0):
        """
        Parameters:
        -----------
        mic_positions : array (N, 3)
            Vi tri cua N microphones (x, y, z) tinh bang met
        sample_rate : int
            Sample rate (Hz)
        speed_of_sound : float
            Toc do am thanh (m/s)
        """
        self.mic_positions = np.array(mic_positions)
        self.n_mics = len(mic_positions)
        self.sample_rate = sample_rate
        self.speed_of_sound = speed_of_sound
        
        print(f"Reference Beamformer initialized:")
        print(f"  - {self.n_mics} microphones")
        print(f"  - Sample rate: {sample_rate} Hz")
        print(f"  - Speed of sound: {speed_of_sound} m/s")
    
    def extract_vocal_from_reference(self, audio_data, reference_channel_idx=4):
        """
        Tach vocal dua tren reference channel (channel 5 = index 4)
        
        Strategy:
        1. Su dung cross-correlation de tim delay giua reference va cac channels khac
        2. Align cac channels theo delays
        3. Coherence-based weighting (channels co tuong quan cao voi reference)
        4. Sum aligned signals voi weights
        
        Parameters:
        -----------
        audio_data : array (n_samples, n_mics)
            Audio multi-channel
        reference_channel_idx : int
            Index cua reference channel (default: 4 = channel 5)
        
        Returns:
        --------
        vocal_extracted : array (n_samples,)
            Vocal da tach (mono)
        delays : array
            Delays tim duoc (samples)
        coherences : array
            Coherence scores voi reference
        """
        n_samples = audio_data.shape[0]
        
        # Reference signal (channel 5)
        reference = audio_data[:, reference_channel_idx]
        
        print(f"\nUsing reference: Channel {reference_channel_idx + 1}")
        
        # Tinh delays va coherences
        delays = np.zeros(self.n_mics)
        coherences = np.zeros(self.n_mics)
        
        for i in range(self.n_mics):
            if i == reference_channel_idx:
                delays[i] = 0
                coherences[i] = 1.0
            else:
                # Cross-correlation de tim delay
                delay = self._find_delay_gcc_phat(reference, audio_data[:, i])
                delays[i] = delay
                
                # Tinh coherence (correlation coefficient)
                aligned = self._fractional_delay(audio_data[:, i], -delay)
                coherences[i] = self._compute_coherence(reference, aligned)
        
        print(f"\nDelays (samples): {delays}")
        print(f"Coherences: {coherences}")
        
        # Normalize weights (chi lay channels co coherence cao)
        # Threshold: coherence > 0.3
        threshold = 0.3
        weights = np.where(coherences > threshold, coherences, 0)
        
        # Normalize weights
        if np.sum(weights) > 0:
            weights = weights / np.sum(weights)
        else:
            print("Warning: No channels with high coherence, using reference only")
            weights = np.zeros(self.n_mics)
            weights[reference_channel_idx] = 1.0
        
        print(f"Weights (normalized): {weights}")
        print(f"Active channels (coherence > {threshold}): {np.where(weights > 0)[0] + 1}")
        
        # Apply delays and weights
        vocal_extracted = np.zeros(n_samples)
        
        for i in range(self.n_mics):
            if weights[i] > 0:
                # Align signal
                aligned = self._fractional_delay(audio_data[:, i], -delays[i])
                
                # Apply weight
                vocal_extracted += weights[i] * aligned
        
        return vocal_extracted, delays, coherences, weights
    
    def _find_delay_gcc_phat(self, signal1, signal2, max_delay=100):
        """
        Find delay between 2 signals using GCC-PHAT
        
        Returns:
        --------
        delay : float
            Delay in samples (signal2 is delayed by this amount)
        """
        # FFT
        n = len(signal1)
        S1 = fft(signal1)
        S2 = fft(signal2)
        
        # GCC-PHAT
        R = S1 * np.conj(S2)
        R = R / (np.abs(R) + 1e-10)
        
        # IFFT
        r = np.fft.ifft(R)
        r = np.abs(r)
        
        # Find peak trong range [-max_delay, max_delay]
        r_centered = np.concatenate([r[-max_delay:], r[:max_delay+1]])
        peak_idx = np.argmax(r_centered)
        delay = peak_idx - max_delay
        
        return delay
    
    def _compute_coherence(self, signal1, signal2):
        """
        Tinh coherence (correlation coefficient) giua 2 signals
        """
        # Normalize
        s1 = signal1 - np.mean(signal1)
        s2 = signal2 - np.mean(signal2)
        
        # Correlation coefficient
        numerator = np.sum(s1 * s2)
        denominator = np.sqrt(np.sum(s1**2) * np.sum(s2**2))
        
        if denominator > 0:
            coherence = numerator / denominator
        else:
            coherence = 0
        
        return np.abs(coherence)
    
    def _fractional_delay(self, signal, delay_samples):
        """
        Ap dung fractional delay su dung linear interpolation
        """
        n_samples = len(signal)
        
        # Tao time indices
        original_indices = np.arange(n_samples)
        delayed_indices = original_indices - delay_samples
        
        # Linear interpolation
        # Xu ly out-of-bound indices
        delayed_indices = np.clip(delayed_indices, 0, n_samples - 1)
        
        # Interpolate
        delayed_signal = np.interp(delayed_indices, original_indices, signal)
        
        return delayed_signal
    
    def apply_frequency_masking(self, signal, reference, freq_range=(300, 3000)):
        """
        Apply frequency masking dua tren reference
        Chi giu lai cac frequency components co trong reference
        
        Parameters:
        -----------
        signal : array
            Signal can filter
        reference : array
            Reference signal
        freq_range : tuple
            Frequency range de focus (Hz)
        
        Returns:
        --------
        masked_signal : array
            Signal sau khi mask
        """
        # STFT
        f, t, Zxx_signal = scipy_signal.stft(signal, fs=self.sample_rate, nperseg=512)
        f, t, Zxx_ref = scipy_signal.stft(reference, fs=self.sample_rate, nperseg=512)
        
        # Create mask dua tren reference
        # Mask = 1 neu reference co energy cao, 0 neu thap
        mask = np.abs(Zxx_ref) / (np.max(np.abs(Zxx_ref)) + 1e-10)
        
        # Apply frequency range
        freq_mask = (f >= freq_range[0]) & (f <= freq_range[1])
        mask[~freq_mask, :] = 0
        
        # Apply mask
        Zxx_masked = Zxx_signal * mask
        
        # ISTFT
        _, masked_signal = scipy_signal.istft(Zxx_masked, fs=self.sample_rate, nperseg=512)
        
        # Ensure same length
        if len(masked_signal) < len(signal):
            masked_signal = np.pad(masked_signal, (0, len(signal) - len(masked_signal)))
        elif len(masked_signal) > len(signal):
            masked_signal = masked_signal[:len(signal)]
        
        return masked_signal

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
        axes[i, 0].set_title(f'{title} - Waveform', fontweight='bold', fontsize=12)
        axes[i, 0].set_xlabel('Time (s)')
        axes[i, 0].set_ylabel('Amplitude')
        axes[i, 0].grid(True, alpha=0.3)
        
        # Frequency spectrum
        freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
        spectrum = np.abs(np.fft.rfft(signal))
        spectrum_db = 20 * np.log10(spectrum + 1e-10)
        
        axes[i, 1].plot(freqs, spectrum_db, linewidth=0.5)
        axes[i, 1].set_title(f'{title} - Frequency Spectrum', fontweight='bold', fontsize=12)
        axes[i, 1].set_xlabel('Frequency (Hz)')
        axes[i, 1].set_ylabel('Magnitude (dB)')
        axes[i, 1].set_xlim([0, 8000])
        axes[i, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved comparison plot: {output_file}")
    plt.close()

def plot_channel_coherences(coherences, weights, output_file):
    """Ve bieu do coherences va weights"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    channels = np.arange(len(coherences)) + 1
    
    # Coherences
    colors = ['green' if c > 0.3 else 'red' for c in coherences]
    ax1.bar(channels, coherences, color=colors, alpha=0.7, edgecolor='black')
    ax1.axhline(y=0.3, color='orange', linestyle='--', linewidth=2, label='Threshold (0.3)')
    ax1.set_xlabel('Channel', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Coherence with Reference (Ch 5)', fontweight='bold', fontsize=12)
    ax1.set_title('Channel Coherences', fontweight='bold', fontsize=14)
    ax1.set_xticks(channels)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.legend()
    
    # Weights
    colors_weights = ['green' if w > 0 else 'gray' for w in weights]
    ax2.bar(channels, weights, color=colors_weights, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Channel', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Weight (Normalized)', fontweight='bold', fontsize=12)
    ax2.set_title('Beamforming Weights', fontweight='bold', fontsize=14)
    ax2.set_xticks(channels)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved coherences plot: {output_file}")
    plt.close()

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    # ========================================================================
    # TIMING: Bắt đầu đo thời gian
    # ========================================================================
    start_time_total = time.time()
    
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/reference_beamforming"
    
    print("="*70)
    print("REFERENCE-BASED BEAMFORMING")
    print("Tach vocal dua tren reference (Channel 5)")
    print("="*70)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Reference channel: 5")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Tao thu muc output
    os.makedirs(output_dir, exist_ok=True)
    
    # Doc file audio
    start_time_step = time.time()
    audio_data = read_pcm_file(input_file)
    elapsed_step = time.time() - start_time_step
    print(f"[TIMING] Doc file: {elapsed_step:.3f}s")
    
    # Chi lay channels co audio (1, 2, 3, 4, 5, 8)
    active_channels = [0, 1, 2, 3, 4, 7]  # 0-indexed
    audio_active = audio_data[:, active_channels]
    
    # Setup microphone array (circular, no center)
    radius = 0.05  # 5cm
    mic_positions = []
    for i in [0, 1, 2, 3, 4, 7]:  # Chi lay active channels
        angle = 2 * np.pi * i / 8
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.0
        mic_positions.append([x, y, z])
    
    # Tao beamformer
    beamformer = ReferenceBeamformer(mic_positions)
    
    # Extract reference signal (channel 5 = index 4 trong audio_active)
    # Mapping: [ch1, ch2, ch3, ch4, ch5, ch8] = [0, 1, 2, 3, 4, 5]
    reference_idx_in_active = 4  # Channel 5
    reference_signal = audio_active[:, reference_idx_in_active]
    
    print("\n" + "="*70)
    print("STEP 1: SAVE REFERENCE SIGNAL (CHANNEL 5)")
    print("="*70)
    
    start_time_step = time.time()
    reference_file = os.path.join(output_dir, 'reference_channel5.wav')
    save_wav(reference_signal, reference_file)
    elapsed_step = time.time() - start_time_step
    print(f"[TIMING] Step 1: {elapsed_step:.3f}s")
    
    # Tach vocal dua tren reference
    print("\n" + "="*70)
    print("STEP 2: REFERENCE-BASED BEAMFORMING")
    print("="*70)
    
    start_time_step = time.time()
    vocal_extracted, delays, coherences, weights = beamformer.extract_vocal_from_reference(
        audio_active, 
        reference_channel_idx=reference_idx_in_active
    )
    
    # Save vocal extracted
    vocal_file = os.path.join(output_dir, 'vocal_extracted_beamforming.wav')
    save_wav(vocal_extracted, vocal_file)
    elapsed_step = time.time() - start_time_step
    print(f"[TIMING] Step 2 (Beamforming): {elapsed_step:.3f}s")
    
    # Apply frequency masking (optional)
    print("\n" + "="*70)
    print("STEP 3: FREQUENCY MASKING")
    print("="*70)
    
    start_time_step = time.time()
    print("\nApplying frequency masking (300-3000 Hz)...")
    vocal_masked = beamformer.apply_frequency_masking(
        vocal_extracted, 
        reference_signal, 
        freq_range=(300, 3000)
    )
    
    vocal_masked_file = os.path.join(output_dir, 'vocal_extracted_masked.wav')
    save_wav(vocal_masked, vocal_masked_file)
    elapsed_step = time.time() - start_time_step
    print(f"[TIMING] Step 3 (Frequency Masking): {elapsed_step:.3f}s")
    
    # Apply bandpass filter
    print("\n" + "="*70)
    print("STEP 4: BANDPASS FILTERING")
    print("="*70)
    
    start_time_step = time.time()
    print("\nApplying bandpass filter (600-3000 Hz)...")
    nyquist = 16000 / 2
    b, a = scipy_signal.butter(4, [600/nyquist, 3000/nyquist], btype='band')
    vocal_filtered = scipy_signal.filtfilt(b, a, vocal_extracted)
    
    vocal_filtered_file = os.path.join(output_dir, 'vocal_extracted_filtered.wav')
    save_wav(vocal_filtered, vocal_filtered_file)
    
    # Combined: masking + filtering
    vocal_combined = scipy_signal.filtfilt(b, a, vocal_masked)
    vocal_combined_file = os.path.join(output_dir, 'vocal_extracted_combined.wav')
    save_wav(vocal_combined, vocal_combined_file)
    
    # Amplify combined audio by 4x
    print("\nApplying 4x amplification...")
    vocal_amplified = vocal_combined * 4.0
    
    # Check for clipping and normalize if necessary
    max_val = np.max(np.abs(vocal_amplified))
    if max_val > 32767:  # 16-bit limit
        print(f"Warning: Amplification caused clipping (max: {max_val:.0f})")
        print("Normalizing to prevent clipping...")
        vocal_amplified = vocal_amplified * (32767 / max_val)
        print(f"Normalized to max: {np.max(np.abs(vocal_amplified)):.0f}")
    
    vocal_amplified_file = os.path.join(output_dir, 'vocal_extracted_combined_ampli.wav')
    save_wav(vocal_amplified, vocal_amplified_file)
    elapsed_step = time.time() - start_time_step
    print(f"[TIMING] Step 4 (Bandpass Filtering + Amplification): {elapsed_step:.3f}s")
    
    # Visualizations
    print("\n" + "="*70)
    print("STEP 5: VISUALIZATION")
    print("="*70)
    
    start_time_step = time.time()
    # Plot coherences and weights
    coherences_plot = os.path.join(output_dir, 'channel_coherences.png')
    
    # Map coherences/weights back to original channels (1-8)
    coherences_full = np.zeros(8)
    weights_full = np.zeros(8)
    for i, ch_idx in enumerate(active_channels):
        coherences_full[ch_idx] = coherences[i]
        weights_full[ch_idx] = weights[i]
    
    plot_channel_coherences(coherences_full, weights_full, coherences_plot)
    
    # Plot comparison
    signals = [
        reference_signal,
        vocal_extracted,
        vocal_masked,
        vocal_filtered,
        vocal_combined,
        vocal_amplified
    ]
    labels = [
        'Reference (Ch 5)',
        'Beamformed',
        'Beamformed + Masked',
        'Beamformed + Filtered',
        'Beamformed + Masked + Filtered',
        'Beamformed + Masked + Filtered + 4x Amplified'
    ]
    titles = [
        '1. Reference Signal (Channel 5)',
        '2. After Reference-Based Beamforming',
        '3. After Frequency Masking',
        '4. After Bandpass Filtering',
        '5. Combined (Masked + Filtered)',
        '6. Amplified (4x) - Final Output'
    ]
    
    comparison_file = os.path.join(output_dir, 'vocal_extraction_comparison.png')
    plot_comparison(signals, labels, titles, comparison_file)
    elapsed_step = time.time() - start_time_step
    print(f"[TIMING] Step 5 (Visualization): {elapsed_step:.3f}s")
    
    # Calculate RMS levels
    print("\n" + "="*70)
    print("STEP 6: QUALITY METRICS")
    print("="*70)
    
    rms_reference = np.sqrt(np.mean(reference_signal ** 2))
    rms_beamformed = np.sqrt(np.mean(vocal_extracted ** 2))
    rms_masked = np.sqrt(np.mean(vocal_masked ** 2))
    rms_filtered = np.sqrt(np.mean(vocal_filtered ** 2))
    rms_combined = np.sqrt(np.mean(vocal_combined ** 2))
    rms_amplified = np.sqrt(np.mean(vocal_amplified ** 2))
    
    print(f"\nRMS Levels:")
    print(f"  Reference (Ch 5):              {rms_reference:.2f}")
    print(f"  After beamforming:             {rms_beamformed:.2f}")
    print(f"  After masking:                 {rms_masked:.2f}")
    print(f"  After filtering:               {rms_filtered:.2f}")
    print(f"  Combined (masked + filtered):  {rms_combined:.2f}")
    print(f"  Amplified (4x):               {rms_amplified:.2f}")
    
    # Summary
    print("\n" + "="*70)
    print("PROCESSING COMPLETE!")
    print("="*70)
    
    print(f"\nOutput files in: {output_dir}")
    
    print("\nProcessed Audio:")
    print(f"  1. reference_channel5.wav           - Original Ch 5")
    print(f"  2. vocal_extracted_beamforming.wav  - After beamforming")
    print(f"  3. vocal_extracted_masked.wav       - Beamformed + Masked")
    print(f"  4. vocal_extracted_filtered.wav     - Beamformed + Filtered")
    print(f"  5. vocal_extracted_combined.wav     - Beamformed + Masked + Filtered")
    print(f"  6. vocal_extracted_combined_ampli.wav - Amplified 4x (FINAL OUTPUT) [BEST]")
    
    print("\nVisualizations:")
    print(f"  - channel_coherences.png            - Coherences & weights")
    print(f"  - vocal_extraction_comparison.png   - Processing comparison")
    
    print("\nChannel Analysis:")
    active_ch_indices = np.where(weights_full > 0)[0] + 1
    print(f"  Active channels (used): {list(active_ch_indices)}")
    print(f"  Coherence threshold: 0.3")
    
    print("\nAlgorithm:")
    print(f"  1. Use Channel 5 as reference")
    print(f"  2. Find delays using GCC-PHAT cross-correlation")
    print(f"  3. Calculate coherence between reference and other channels")
    print(f"  4. Weight channels by coherence (threshold: 0.3)")
    print(f"  5. Align and sum weighted signals")
    print(f"  6. Apply frequency masking (300-3000 Hz)")
    print(f"  7. Apply bandpass filter (600-3000 Hz)")
    print(f"  8. Amplify signal by 4x (with clipping protection)")
    
    print("\nBest Output:")
    print(f"  >>> {vocal_amplified_file}")
    print(f"  This file contains the cleanest vocal extraction with 4x amplification")
    
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

