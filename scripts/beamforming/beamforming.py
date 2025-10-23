#!/usr/bin/env python3
"""
Delay-and-Sum Beamforming cho Microphone Array
"""

import numpy as np
import struct
import wave
import os
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal
import time
from datetime import timedelta

class DelayAndSumBeamformer:
    """
    Delay-and-Sum Beamforming implementation
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
        
        print(f"Beamformer initialized:")
        print(f"  - {self.n_mics} microphones")
        print(f"  - Sample rate: {sample_rate} Hz")
        print(f"  - Speed of sound: {speed_of_sound} m/s")
    
    def steer_vector(self, azimuth_deg, elevation_deg=0):
        """
        Tinh steering vector cho huong mong muon
        
        Parameters:
        -----------
        azimuth_deg : float
            Goc phuong vi (do), 0° = truoc mat, 90° = phai, -90° = trai
        elevation_deg : float
            Goc nang (do), 0° = ngang, 90° = tren, -90° = duoi
        
        Returns:
        --------
        delays : array
            Delay (giay) cho moi microphone
        """
        # Chuyen do sang radian
        azimuth = np.deg2rad(azimuth_deg)
        elevation = np.deg2rad(elevation_deg)
        
        # Huong den nguon am thanh (unit vector)
        direction = np.array([
            np.cos(elevation) * np.cos(azimuth),
            np.cos(elevation) * np.sin(azimuth),
            np.sin(elevation)
        ])
        
        # Tinh delay cho moi mic (Time Difference of Arrival)
        # delay[i] = (position[i] dot direction) / speed_of_sound
        delays = np.dot(self.mic_positions, direction) / self.speed_of_sound
        
        # Normalize delays (mic gan nhat co delay = 0)
        delays = delays - np.min(delays)
        
        return delays
    
    def apply_beamforming(self, audio_data, azimuth_deg, elevation_deg=0):
        """
        Ap dung Delay-and-Sum beamforming
        
        Parameters:
        -----------
        audio_data : array (n_samples, n_mics)
            Audio multi-channel
        azimuth_deg : float
            Huong beam (goc phuong vi)
        elevation_deg : float
            Huong beam (goc nang)
        
        Returns:
        --------
        beamformed : array (n_samples,)
            Audio da beamform (mono)
        """
        n_samples = audio_data.shape[0]
        
        # Tinh delays cho huong mong muon
        delays = self.steer_vector(azimuth_deg, elevation_deg)
        
        # Chuyen delay tu giay sang samples
        delay_samples = delays * self.sample_rate
        
        # Ap dung fractional delay cho moi channel
        beamformed = np.zeros(n_samples)
        
        for i in range(self.n_mics):
            # Su dung linear interpolation cho fractional delay
            delayed_signal = self._fractional_delay(
                audio_data[:, i], 
                delay_samples[i]
            )
            beamformed += delayed_signal
        
        # Normalize
        beamformed = beamformed / self.n_mics
        
        return beamformed
    
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
    
    def scan_directions(self, audio_data, azimuth_range=(-180, 180), n_directions=72):
        """
        Scan nhieu huong de tim nguon am thanh
        
        Parameters:
        -----------
        audio_data : array (n_samples, n_mics)
            Audio multi-channel
        azimuth_range : tuple
            Range goc phuong vi (min, max) degree
        n_directions : int
            So huong de scan
        
        Returns:
        --------
        azimuths : array
            Cac goc phuong vi da scan
        powers : array
            Cong suat tai moi huong
        """
        azimuths = np.linspace(azimuth_range[0], azimuth_range[1], n_directions)
        powers = np.zeros(n_directions)
        
        print(f"\nScanning {n_directions} directions...")
        
        for i, azimuth in enumerate(azimuths):
            # Beamform theo huong nay
            beamformed = self.apply_beamforming(audio_data, azimuth, elevation_deg=0)
            
            # Tinh power (energy)
            powers[i] = np.sum(beamformed ** 2)
            
            if (i + 1) % 10 == 0:
                print(f"  Scanned {i+1}/{n_directions} directions...")
        
        return azimuths, powers
    
    def find_peak_direction(self, azimuths, powers):
        """
        Tim huong co power cao nhat
        """
        peak_idx = np.argmax(powers)
        peak_azimuth = azimuths[peak_idx]
        peak_power = powers[peak_idx]
        
        return peak_azimuth, peak_power

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
    
    print(f"Saved: {filepath}")

def plot_polar_pattern(azimuths, powers, output_file):
    """Ve polar pattern (beam pattern)"""
    
    # Chuyen sang radian
    azimuths_rad = np.deg2rad(azimuths)
    
    # Normalize powers
    powers_db = 10 * np.log10(powers / np.max(powers) + 1e-10)
    
    # Tao polar plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    # Ve beam pattern
    ax.plot(azimuths_rad, powers_db, 'b-', linewidth=2)
    ax.fill(azimuths_rad, powers_db, alpha=0.3)
    
    # Danh dau peak
    peak_idx = np.argmax(powers)
    ax.plot(azimuths_rad[peak_idx], powers_db[peak_idx], 'ro', markersize=15, label=f'Peak: {azimuths[peak_idx]:.1f}°')
    
    # Cau hinh
    ax.set_theta_zero_location('N')  # 0° o phia tren
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_title('Beamforming Spatial Response (Polar Pattern)', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Power (dB)', fontsize=12)
    ax.set_ylim([np.min(powers_db), 0])
    ax.legend(loc='upper right')
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved polar plot: {output_file}")
    plt.close()

def plot_cartesian_pattern(azimuths, powers, output_file):
    """Ve Cartesian plot"""
    
    # Normalize powers
    powers_db = 10 * np.log10(powers / np.max(powers) + 1e-10)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(azimuths, powers_db, 'b-', linewidth=2)
    ax.fill_between(azimuths, powers_db, alpha=0.3)
    
    # Danh dau peak
    peak_idx = np.argmax(powers)
    ax.plot(azimuths[peak_idx], powers_db[peak_idx], 'ro', markersize=12, 
            label=f'Peak Direction: {azimuths[peak_idx]:.1f}°')
    
    ax.set_xlabel('Azimuth (degrees)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Power (dB)', fontsize=12, fontweight='bold')
    ax.set_title('Beamforming Spatial Response (Cartesian)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    ax.set_xlim([azimuths[0], azimuths[-1]])
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved Cartesian plot: {output_file}")
    plt.close()

def main():
    # ========================================================================
    # TIMING: Bắt đầu đo thời gian
    # ========================================================================
    start_time_total = time.time()
    
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/beamforming"
    
    print("="*60)
    print("DELAY-AND-SUM BEAMFORMING")
    print("="*60)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Tao thu muc output
    os.makedirs(output_dir, exist_ok=True)
    
    # Doc file audio
    audio_data = read_pcm_file(input_file)
    
    # Chi lay channels co audio (1, 2, 3, 4, 5, 8)
    active_channels = [0, 1, 2, 3, 4, 7]  # 0-indexed
    audio_active = audio_data[:, active_channels]
    
    # Setup microphone array (8 mics trong, ban kinh 5cm)
    radius = 0.05  # 5cm
    mic_positions = []
    for i in [0, 1, 2, 3, 4, 7]:  # Chi lay active channels
        angle = 2 * np.pi * i / 8
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.0
        mic_positions.append([x, y, z])
    
    # Tao beamformer
    beamformer = DelayAndSumBeamformer(mic_positions)
    
    # 1. Scan de tim huong nguon am thanh
    print("\n" + "="*60)
    print("BUOC 1: SCAN DE TIM HUONG NGUON AM THANH")
    print("="*60)
    
    azimuths, powers = beamformer.scan_directions(audio_active, n_directions=72)
    peak_azimuth, peak_power = beamformer.find_peak_direction(azimuths, powers)
    
    print(f"\n>>> Peak direction found: {peak_azimuth:.1f}°")
    print(f">>> Peak power: {peak_power:.2e}")
    
    # Ve polar pattern
    plot_polar_pattern(azimuths, powers, os.path.join(output_dir, 'beam_pattern_polar.png'))
    plot_cartesian_pattern(azimuths, powers, os.path.join(output_dir, 'beam_pattern_cartesian.png'))
    
    # 2. Beamform theo cac huong khac nhau
    print("\n" + "="*60)
    print("BUOC 2: TAO BEAMFORMED AUDIO THEO CAC HUONG")
    print("="*60)
    
    directions = [0, 45, 90, 135, 180, -135, -90, -45, peak_azimuth]
    
    for azimuth in directions:
        print(f"\nBeamforming huong {azimuth}°...")
        beamformed = beamformer.apply_beamforming(audio_active, azimuth)
        
        # Luu file
        filename = f'beamformed_{azimuth:.0f}deg.wav'
        filepath = os.path.join(output_dir, filename)
        save_wav(beamformed, filepath)
    
    # 3. So sanh: original vs beamformed
    print("\n" + "="*60)
    print("BUOC 3: SO SANH ORIGINAL VS BEAMFORMED")
    print("="*60)
    
    # Tao omnidirectional (trung binh tat ca channels)
    omnidirectional = np.mean(audio_active, axis=1)
    save_wav(omnidirectional, os.path.join(output_dir, 'omnidirectional.wav'))
    print("Saved omnidirectional audio (trung binh tat ca mics)")
    
    # Beamformed theo peak direction
    beamformed_peak = beamformer.apply_beamforming(audio_active, peak_azimuth)
    save_wav(beamformed_peak, os.path.join(output_dir, 'beamformed_peak.wav'))
    print(f"Saved beamformed audio (huong {peak_azimuth:.1f}°)")
    
    # Tong ket
    print("\n" + "="*60)
    print("HOAN THANH!")
    print("="*60)
    
    print(f"\nCac file da tao:")
    print(f"  - beam_pattern_polar.png - Polar pattern")
    print(f"  - beam_pattern_cartesian.png - Cartesian plot")
    print(f"  - beamformed_X_deg.wav - Audio beamformed theo huong X")
    print(f"  - omnidirectional.wav - Audio tron (khong beamforming)")
    print(f"  - beamformed_peak.wav - Audio beamformed theo peak direction")
    
    print(f"\nThu muc output: {output_dir}")
    print(f"\nPeak direction: {peak_azimuth:.1f}°")
    print(f"  - 0° = Truoc mat (North)")
    print(f"  - 90° = Ben phai (East)")
    print(f"  - 180° / -180° = Phia sau (South)")
    print(f"  - -90° = Ben trai (West)")
    
    print(f"\nBeamforming benefits:")
    print(f"  - Tang SNR (Signal-to-Noise Ratio)")
    print(f"  - Giam nhieu tu cac huong khong mong muon")
    print(f"  - Nhan manh tin hieu tu huong mong muon")
    print(f"  - Directional selectivity")
    
    # ========================================================================
    # TIMING: Thời gian tổng kết
    # ========================================================================
    total_elapsed = time.time() - start_time_total
    
    print("\n" + "="*60)
    print("TIMING SUMMARY")
    print("="*60)
    print(f"Total processing time: {total_elapsed:.3f}s ({timedelta(seconds=int(total_elapsed))})")
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

if __name__ == "__main__":
    main()

