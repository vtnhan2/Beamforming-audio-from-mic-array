#!/usr/bin/env python3
"""
Minh hoa cach hoat dong cua Butterworth filter
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def plot_filter_frequency_response():
    """Ve frequency response cua cac bo loc"""
    
    sample_rate = 16000
    nyquist = sample_rate / 2
    
    # Tao cac bo loc
    filters = []
    
    # 1. Bandpass 600-3000 Hz
    low = 600 / nyquist
    high = 3000 / nyquist
    b, a = signal.butter(5, [low, high], btype='band')
    filters.append(('Bandpass 600-3000 Hz', b, a, 'blue'))
    
    # 2. Bandpass 300-3000 Hz
    low = 300 / nyquist
    high = 3000 / nyquist
    b, a = signal.butter(5, [low, high], btype='band')
    filters.append(('Bandpass 300-3000 Hz', b, a, 'green'))
    
    # 3. Highpass 300 Hz
    cutoff = 300 / nyquist
    b, a = signal.butter(5, cutoff, btype='high')
    filters.append(('Highpass 300 Hz', b, a, 'red'))
    
    # 4. Lowpass 5000 Hz
    cutoff = 5000 / nyquist
    b, a = signal.butter(5, cutoff, btype='low')
    filters.append(('Lowpass 5000 Hz', b, a, 'purple'))
    
    # 5. Notch 50 Hz
    freq = 50.0
    Q = 30.0
    b, a = signal.iirnotch(freq / nyquist, Q)
    filters.append(('Notch 50 Hz (Q=30)', b, a, 'orange'))
    
    # Tao figure
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    # Ve tung filter
    for idx, (name, b, a, color) in enumerate(filters):
        ax = axes[idx]
        
        # Tinh frequency response
        w, h = signal.freqz(b, a, worN=8000, fs=sample_rate)
        
        # Ve magnitude response
        ax.plot(w, 20 * np.log10(abs(h)), color=color, linewidth=2)
        ax.set_title(name, fontsize=14, fontweight='bold')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude (dB)')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, sample_rate/2])
        ax.set_ylim([-80, 5])
        
        # Danh dau cutoff frequencies
        if 'Bandpass 600-3000' in name:
            ax.axvline(600, color='green', linestyle='--', alpha=0.5, label='600 Hz')
            ax.axvline(3000, color='green', linestyle='--', alpha=0.5, label='3000 Hz')
            ax.legend()
        elif 'Bandpass 300-3000' in name:
            ax.axvline(300, color='green', linestyle='--', alpha=0.5, label='300 Hz')
            ax.axvline(3000, color='green', linestyle='--', alpha=0.5, label='3000 Hz')
            ax.legend()
        elif 'Highpass' in name:
            ax.axvline(300, color='green', linestyle='--', alpha=0.5, label='300 Hz cutoff')
            ax.legend()
        elif 'Lowpass' in name:
            ax.axvline(5000, color='green', linestyle='--', alpha=0.5, label='5000 Hz cutoff')
            ax.legend()
        elif 'Notch' in name:
            ax.axvline(50, color='green', linestyle='--', alpha=0.5, label='50 Hz notch')
            ax.legend()
            ax.set_xlim([0, 200])  # Zoom in cho notch
    
    # Hide last subplot
    axes[-1].axis('off')
    
    plt.tight_layout()
    plt.savefig('filter_frequency_response.png', dpi=150, bbox_inches='tight')
    print("Saved: filter_frequency_response.png")
    plt.close()

def plot_filter_order_comparison():
    """So sanh cac order khac nhau"""
    
    sample_rate = 16000
    nyquist = sample_rate / 2
    low = 600 / nyquist
    high = 3000 / nyquist
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    orders = [2, 3, 5, 7, 10]
    colors = ['blue', 'green', 'orange', 'red', 'purple']
    
    for order, color in zip(orders, colors):
        b, a = signal.butter(order, [low, high], btype='band')
        w, h = signal.freqz(b, a, worN=8000, fs=sample_rate)
        
        # Magnitude
        ax1.plot(w, 20 * np.log10(abs(h)), color=color, linewidth=2, 
                label=f'Order {order}', alpha=0.7)
        
        # Phase
        angles = np.unwrap(np.angle(h))
        ax2.plot(w, angles, color=color, linewidth=2, 
                label=f'Order {order}', alpha=0.7)
    
    # Magnitude plot
    ax1.set_title('Magnitude Response - Different Orders', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.axvline(600, color='black', linestyle='--', alpha=0.3)
    ax1.axvline(3000, color='black', linestyle='--', alpha=0.3)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlim([0, sample_rate/2])
    ax1.set_ylim([-100, 5])
    
    # Phase plot
    ax2.set_title('Phase Response - Different Orders', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (radians)')
    ax2.axvline(600, color='black', linestyle='--', alpha=0.3)
    ax2.axvline(3000, color='black', linestyle='--', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlim([0, sample_rate/2])
    
    plt.tight_layout()
    plt.savefig('filter_order_comparison.png', dpi=150, bbox_inches='tight')
    print("Saved: filter_order_comparison.png")
    plt.close()

def plot_filtfilt_vs_filter():
    """So sanh filtfilt vs filter (zero-phase vs regular)"""
    
    # Tao test signal
    fs = 16000
    t = np.linspace(0, 1, fs, endpoint=False)
    
    # Tao signal voi nhieu tan so
    signal_test = (np.sin(2 * np.pi * 100 * t) +  # 100 Hz
                   np.sin(2 * np.pi * 1000 * t) +  # 1000 Hz
                   np.sin(2 * np.pi * 5000 * t))   # 5000 Hz
    
    # Thiet ke bandpass filter 600-3000 Hz
    nyquist = fs / 2
    low = 600 / nyquist
    high = 3000 / nyquist
    b, a = signal.butter(5, [low, high], btype='band')
    
    # Ap dung filter theo 2 cach
    filtered_regular = signal.lfilter(b, a, signal_test)
    filtered_zerophase = signal.filtfilt(b, a, signal_test)
    
    # Ve ket qua
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Original
    ax = axes[0]
    ax.plot(t[:1000], signal_test[:1000], 'b-', linewidth=1)
    ax.set_title('Original Signal (100Hz + 1000Hz + 5000Hz)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    
    # Regular filter
    ax = axes[1]
    ax.plot(t[:1000], filtered_regular[:1000], 'r-', linewidth=1)
    ax.set_title('After lfilter() - Forward only (Phase Distortion)', 
                fontsize=12, fontweight='bold', color='red')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    
    # filtfilt
    ax = axes[2]
    ax.plot(t[:1000], filtered_zerophase[:1000], 'g-', linewidth=1)
    ax.set_title('After filtfilt() - Forward + Backward (Zero Phase)', 
                fontsize=12, fontweight='bold', color='green')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('filtfilt_vs_filter_comparison.png', dpi=150, bbox_inches='tight')
    print("Saved: filtfilt_vs_filter_comparison.png")
    plt.close()

def plot_filter_effect_on_signal():
    """Minh hoa hieu qua cua filter len tin hieu thuc te"""
    
    fs = 16000
    t = np.linspace(0, 2, 2*fs, endpoint=False)
    
    # Tao signal gia lap giong noi + nhieu
    voice = np.sin(2 * np.pi * 800 * t) + 0.5 * np.sin(2 * np.pi * 1500 * t)
    hum = 0.8 * np.sin(2 * np.pi * 50 * t)  # Hum 50Hz
    noise_low = 0.3 * np.sin(2 * np.pi * 150 * t)  # Nhieu thap
    noise_high = 0.2 * np.sin(2 * np.pi * 6000 * t)  # Nhieu cao
    
    signal_noisy = voice + hum + noise_low + noise_high
    
    # Ap dung bandpass 600-3000 Hz
    nyquist = fs / 2
    low = 600 / nyquist
    high = 3000 / nyquist
    b, a = signal.butter(5, [low, high], btype='band')
    signal_filtered = signal.filtfilt(b, a, signal_noisy)
    
    # Ve ket qua
    fig, axes = plt.subplots(6, 2, figsize=(16, 16))
    
    # Time domain - Noisy
    ax = axes[0, 0]
    ax.plot(t[:500], signal_noisy[:500], 'b-', linewidth=1)
    ax.set_title('Noisy Signal (Time Domain)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    
    # Frequency domain - Noisy
    ax = axes[0, 1]
    fft_noisy = np.fft.fft(signal_noisy)
    freqs = np.fft.fftfreq(len(signal_noisy), 1/fs)
    positive_freqs = freqs[:len(freqs)//2]
    positive_fft = np.abs(fft_noisy[:len(fft_noisy)//2])
    ax.plot(positive_freqs, positive_fft, 'b-', linewidth=1)
    ax.set_title('Noisy Signal (Frequency Domain)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 8000])
    ax.axvspan(0, 600, alpha=0.2, color='red', label='Removed')
    ax.axvspan(3000, 8000, alpha=0.2, color='red')
    ax.axvspan(600, 3000, alpha=0.2, color='green', label='Kept')
    ax.legend()
    
    # Time domain - Filtered
    ax = axes[1, 0]
    ax.plot(t[:500], signal_filtered[:500], 'g-', linewidth=1)
    ax.set_title('Filtered Signal (Time Domain)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)
    
    # Frequency domain - Filtered
    ax = axes[1, 1]
    fft_filtered = np.fft.fft(signal_filtered)
    positive_fft_filtered = np.abs(fft_filtered[:len(fft_filtered)//2])
    ax.plot(positive_freqs, positive_fft_filtered, 'g-', linewidth=1)
    ax.set_title('Filtered Signal (Frequency Domain)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 8000])
    ax.axvspan(600, 3000, alpha=0.2, color='green', label='Passband')
    ax.legend()
    
    # Components
    components = [
        ('Voice (800Hz + 1500Hz)', voice, 'green'),
        ('Hum (50Hz)', hum, 'red'),
        ('Low Noise (150Hz)', noise_low, 'orange'),
        ('High Noise (6000Hz)', noise_high, 'purple')
    ]
    
    for idx, (name, comp, color) in enumerate(components):
        ax = axes[idx+2, 0]
        ax.plot(t[:500], comp[:500], color=color, linewidth=1)
        ax.set_title(name, fontsize=11, fontweight='bold')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3)
        
        ax = axes[idx+2, 1]
        fft_comp = np.fft.fft(comp)
        positive_fft_comp = np.abs(fft_comp[:len(fft_comp)//2])
        ax.plot(positive_freqs, positive_fft_comp, color=color, linewidth=1)
        ax.set_title(f'{name} - Frequency', fontsize=11, fontweight='bold')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 8000])
    
    plt.tight_layout()
    plt.savefig('filter_effect_on_signal.png', dpi=150, bbox_inches='tight')
    print("Saved: filter_effect_on_signal.png")
    plt.close()

def main():
    print("="*60)
    print("TAO BIEU DO MINH HOA CACH HOAT DONG CUA FILTER")
    print("="*60)
    
    print("\n1. Ve frequency response cua cac bo loc...")
    plot_filter_frequency_response()
    
    print("\n2. So sanh cac order khac nhau...")
    plot_filter_order_comparison()
    
    print("\n3. So sanh filtfilt() vs filter()...")
    plot_filtfilt_vs_filter()
    
    print("\n4. Minh hoa hieu qua filter len tin hieu...")
    plot_filter_effect_on_signal()
    
    print("\n" + "="*60)
    print("HOAN THANH!")
    print("="*60)
    print("\nCac file da tao:")
    print("  - filter_frequency_response.png")
    print("  - filter_order_comparison.png")
    print("  - filtfilt_vs_filter_comparison.png")
    print("  - filter_effect_on_signal.png")
    print("\nCac bieu do nay minh hoa cach hoat dong cua filter!")

if __name__ == "__main__":
    try:
        import scipy.signal
        import matplotlib.pyplot
    except ImportError:
        print("Cai dat thu vien:")
        print("pip install scipy matplotlib")
        exit(1)
    
    main()

