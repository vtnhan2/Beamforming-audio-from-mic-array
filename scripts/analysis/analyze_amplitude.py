#!/usr/bin/env python3
"""
Phan tich dai Amplitude cua audio trong tung channel
"""

import numpy as np
import struct
import matplotlib.pyplot as plt
import os

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

def analyze_amplitude_range(audio_data):
    """Phan tich dai amplitude cua tung channel"""
    
    print("\n" + "="*80)
    print("PHAN TICH DAI AMPLITUDE")
    print("="*80)
    
    results = []
    
    for ch in range(audio_data.shape[1]):
        channel_data = audio_data[:, ch]
        
        # Tinh cac thong so
        min_val = np.min(channel_data)
        max_val = np.max(channel_data)
        mean_val = np.mean(channel_data)
        median_val = np.median(channel_data)
        std_val = np.std(channel_data)
        
        # Tinh RMS (Root Mean Square)
        rms = np.sqrt(np.mean(channel_data**2))
        
        # Tinh peak-to-peak
        peak_to_peak = max_val - min_val
        
        # Tinh dynamic range (dB)
        # DR = 20 * log10(max_signal / noise_floor)
        noise_floor = std_val
        if noise_floor > 0:
            dynamic_range_db = 20 * np.log10(max_val / noise_floor)
        else:
            dynamic_range_db = 0
        
        # Tinh percentiles
        p01 = np.percentile(np.abs(channel_data), 1)
        p05 = np.percentile(np.abs(channel_data), 5)
        p25 = np.percentile(np.abs(channel_data), 25)
        p50 = np.percentile(np.abs(channel_data), 50)
        p75 = np.percentile(np.abs(channel_data), 75)
        p95 = np.percentile(np.abs(channel_data), 95)
        p99 = np.percentile(np.abs(channel_data), 99)
        
        # Xac dinh neu co audio
        has_audio = rms > 100
        
        result = {
            'channel': ch + 1,
            'min': min_val,
            'max': max_val,
            'mean': mean_val,
            'median': median_val,
            'std': std_val,
            'rms': rms,
            'peak_to_peak': peak_to_peak,
            'dynamic_range_db': dynamic_range_db,
            'percentiles': {
                '1%': p01,
                '5%': p05,
                '25%': p25,
                '50%': p50,
                '75%': p75,
                '95%': p95,
                '99%': p99
            },
            'has_audio': has_audio
        }
        
        results.append(result)
        
        # In ket qua
        print(f"\nChannel {ch+1}:")
        print(f"  Status: {'CO AUDIO' if has_audio else 'KHONG CO AUDIO'}")
        print(f"  Amplitude Range:")
        print(f"    Min:           {min_val:10.2f}")
        print(f"    Max:           {max_val:10.2f}")
        print(f"    Peak-to-Peak:  {peak_to_peak:10.2f}")
        print(f"  Central Tendency:")
        print(f"    Mean:          {mean_val:10.2f}")
        print(f"    Median:        {median_val:10.2f}")
        print(f"    RMS:           {rms:10.2f}")
        print(f"  Variability:")
        print(f"    Std Dev:       {std_val:10.2f}")
        print(f"    Dynamic Range: {dynamic_range_db:10.2f} dB")
        print(f"  Percentiles (Absolute Values):")
        print(f"    1%:            {p01:10.2f}")
        print(f"    5%:            {p05:10.2f}")
        print(f"    25%:           {p25:10.2f}")
        print(f"    50% (Median):  {p50:10.2f}")
        print(f"    75%:           {p75:10.2f}")
        print(f"    95%:           {p95:10.2f}")
        print(f"    99%:           {p99:10.2f}")
    
    return results

def plot_amplitude_distribution(audio_data, output_dir):
    """
    Plot amplitude distribution for each channel
    
    Functionality:
    - Create histogram and box plot for each channel
    - Display important statistics (mean, std, RMS, percentiles)
    - Save image to amplitude_distribution.png file
    
    Parameters:
    - audio_data: numpy array containing audio data (samples x channels)
    - output_dir: output directory for saving files
    """
    
    print("\nTao bieu do phan bo amplitude...")
    
    # Get number of channels
    n_channels = audio_data.shape[1]
    
    # Create large figure with 2-column layout for each channel
    # - Left column: Histogram
    # - Right column: Box plot
    fig, axes = plt.subplots(n_channels, 2, figsize=(16, 3*n_channels))
    
    # Iterate through each channel to create plots
    for ch in range(n_channels):
        channel_data = audio_data[:, ch]
        
        # === HISTOGRAM (Left column) ===
        ax = axes[ch, 0]
        
        # Create histogram with 100 bins to display amplitude distribution
        ax.hist(channel_data, bins=100, alpha=0.7, color='blue', edgecolor='black')
        ax.set_title(f'Channel {ch+1} - Amplitude Histogram', fontweight='bold')
        ax.set_xlabel('Amplitude')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        
        # Calculate important statistics
        mean_val = np.mean(channel_data)      # Mean value
        std_val = np.std(channel_data)        # Standard deviation
        rms = np.sqrt(np.mean(channel_data**2))  # Root Mean Square
        
        # Draw vertical lines to mark statistical values
        ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.1f}')
        ax.axvline(mean_val + std_val, color='green', linestyle='--', alpha=0.5, label=f'+1 Std: {std_val:.1f}')
        ax.axvline(mean_val - std_val, color='green', linestyle='--', alpha=0.5)
        ax.legend()
        
        # === BOX PLOT (Right column) ===
        ax = axes[ch, 1]
        
        # Create box plot to display statistical distribution
        # - Box: Q1 to Q3 (25% to 75%)
        # - Middle line: Median (50%)
        # - Whiskers: Min and Max
        # - Outliers: Unusual points
        bp = ax.boxplot([channel_data], vert=True, patch_artist=True, 
                        labels=[f'Channel {ch+1}'],
                        boxprops=dict(facecolor='lightblue'),      # Light blue color for box
                        medianprops=dict(color='red', linewidth=2)) # Red median line
        ax.set_title(f'Channel {ch+1} - Amplitude Box Plot', fontweight='bold')
        ax.set_ylabel('Amplitude')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Calculate percentiles for box plot
        min_val = np.min(channel_data)
        q1 = np.percentile(channel_data, 25)    # Quartile 1 (25%)
        median = np.median(channel_data)        # Median (50%)
        q3 = np.percentile(channel_data, 75)    # Quartile 3 (75%)
        max_val = np.max(channel_data)
        
        # Display important statistics next to box plot
        stats_text = f'Min: {min_val:.1f}\n'
        stats_text += f'Q1: {q1:.1f}\n'
        stats_text += f'Median: {median:.1f}\n'
        stats_text += f'Q3: {q3:.1f}\n'
        stats_text += f'Max: {max_val:.1f}\n'
        stats_text += f'RMS: {rms:.1f}'
        
        # Place text box to the right of box plot
        ax.text(1.15, 0.5, stats_text, transform=ax.transAxes,
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    # Save image to file
    plot_file = os.path.join(output_dir, 'amplitude_distribution.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {plot_file}")
    plt.close()

def plot_amplitude_comparison(audio_data, output_dir):
    """
    Plot amplitude comparison between channels
    
    Functionality:
    - Create bar chart comparing RMS amplitude between channels
    - Create box plot comparing amplitude distribution
    - Classify channels with/without audio (threshold = 100)
    - Save image to amplitude_comparison.png file
    
    Parameters:
    - audio_data: numpy array containing audio data (samples x channels)
    - output_dir: output directory for saving files
    """
    
    print("Tao bieu do so sanh amplitude...")
    
    # Get number of channels
    n_channels = audio_data.shape[1]
    
    # Create figure with 2 subplots: bar chart and box plot
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # === BAR CHART - RMS COMPARISON (Top subplot) ===
    ax = axes[0]
    
    # Create channel names list and calculate RMS for each channel
    channels = [f'Ch{i+1}' for i in range(n_channels)]
    rms_values = [np.sqrt(np.mean(audio_data[:, i]**2)) for i in range(n_channels)]
    
    # Color classification: green if has audio (RMS > 100), red if no audio
    colors = ['green' if rms > 100 else 'red' for rms in rms_values]
    
    # Create bar chart
    bars = ax.bar(channels, rms_values, color=colors, alpha=0.7, edgecolor='black')
    ax.set_title('RMS Amplitude Comparison Across Channels', fontsize=14, fontweight='bold')
    ax.set_xlabel('Channel')
    ax.set_ylabel('RMS Amplitude')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Display RMS values on each bar
    for i, (bar, val) in enumerate(zip(bars, rms_values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Draw threshold line to distinguish audio/no audio
    ax.axhline(y=100, color='orange', linestyle='--', linewidth=2, label='Audio Threshold (100)')
    ax.legend()
    
    # === BOX PLOT - DISTRIBUTION COMPARISON (Bottom subplot) ===
    ax = axes[1]
    
    # Prepare data for box plot: each channel as separate list
    data_for_boxplot = [audio_data[:, i] for i in range(n_channels)]
    
    # Create box plot for all channels
    bp = ax.boxplot(data_for_boxplot, labels=channels, patch_artist=True)
    
    # Color boxes based on RMS values
    # - Light green: channels with audio (RMS > 100)
    # - Light coral: channels without audio (RMS <= 100)
    for i, patch in enumerate(bp['boxes']):
        if rms_values[i] > 100:
            patch.set_facecolor('lightgreen')  # Light green for channels with audio
        else:
            patch.set_facecolor('lightcoral')   # Light coral for channels without audio
    
    ax.set_title('Amplitude Distribution Comparison (Box Plot)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Channel')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adjust layout to prevent clipping
    plt.tight_layout()
    
    # Save image to file
    plot_file = os.path.join(output_dir, 'amplitude_comparison.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {plot_file}")
    plt.close()

def create_summary_table(results, output_dir):
    """
    Create summary table of amplitude statistics for all channels
    
    Functionality:
    - Create detailed statistics table for each channel
    - Color classification based on audio status (with/without audio)
    - Display important statistics: Min, Max, Peak-to-Peak, Mean, RMS, Std Dev, Dynamic Range
    - Save image to amplitude_summary_table.png file
    
    Parameters:
    - results: list containing amplitude analysis results for each channel
    - output_dir: output directory for saving files
    """
    
    print("\nTao bang tom tat...")
    
    # Create figure for table with large size to display full information
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.axis('tight')  # Auto-adjust size
    ax.axis('off')    # Turn off all axes
    
    # Define table columns
    headers = ['Channel', 'Status', 'Min', 'Max', 'Peak-to-Peak', 'Mean', 'RMS', 'Std Dev', 'Dynamic Range (dB)']
    data = []
    
    # Iterate through results of each channel to create table data
    for r in results:
        # Determine status: AUDIO if has audio, SILENT if no audio
        status = 'AUDIO' if r['has_audio'] else 'SILENT'
        
        # Create a data row for current channel
        row = [
            f"Ch {r['channel']}",                    # Channel number
            status,                                  # Audio status
            f"{r['min']:.1f}",                       # Minimum value
            f"{r['max']:.1f}",                       # Maximum value
            f"{r['peak_to_peak']:.1f}",             # Peak-to-peak range
            f"{r['mean']:.1f}",                      # Mean value
            f"{r['rms']:.1f}",                       # Root Mean Square
            f"{r['std']:.1f}",                       # Standard deviation
            f"{r['dynamic_range_db']:.1f}"          # Dynamic range (dB)
        ]
        data.append(row)
    
    # Create table with matplotlib table
    table = ax.table(cellText=data, colLabels=headers, cellLoc='center', loc='center')
    table.auto_set_font_size(False)  # Turn off auto font size adjustment
    table.set_fontsize(10)           # Set fixed font size
    table.scale(1, 2)                # Adjust size: width=1, height=2
    
    # === COLOR HEADER ===
    # Header has green color (#4CAF50) with white text
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4CAF50')        # Green background
        table[(0, i)].set_text_props(weight='bold', color='white')  # Bold white text
    
    # === COLOR DATA ROWS ===
    # Color classification based on audio status of each channel
    for i, r in enumerate(results):
        if r['has_audio']:
            color = '#E8F5E9'  # Light green for channels with audio
        else:
            color = '#FFEBEE'  # Light red for channels without audio
        
        # Color all cells in the row
        for j in range(len(headers)):
            table[(i+1, j)].set_facecolor(color)
    
    # Set title for table
    plt.title('Amplitude Statistics Summary', fontsize=16, fontweight='bold', pad=20)
    
    # Save image to file
    plot_file = os.path.join(output_dir, 'amplitude_summary_table.png')
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {plot_file}")
    plt.close()

def save_results_to_file(results, output_dir):
    """Luu ket qua vao file text"""
    
    filename = os.path.join(output_dir, 'amplitude_analysis.txt')
    
    with open(filename, 'w') as f:
        f.write("="*80 + "\n")
        f.write("AMPLITUDE ANALYSIS REPORT\n")
        f.write("="*80 + "\n\n")
        
        for r in results:
            f.write(f"Channel {r['channel']}:\n")
            f.write(f"  Status: {'CO AUDIO' if r['has_audio'] else 'KHONG CO AUDIO'}\n")
            f.write(f"  Amplitude Range:\n")
            f.write(f"    Min:           {r['min']:10.2f}\n")
            f.write(f"    Max:           {r['max']:10.2f}\n")
            f.write(f"    Peak-to-Peak:  {r['peak_to_peak']:10.2f}\n")
            f.write(f"  Central Tendency:\n")
            f.write(f"    Mean:          {r['mean']:10.2f}\n")
            f.write(f"    Median:        {r['median']:10.2f}\n")
            f.write(f"    RMS:           {r['rms']:10.2f}\n")
            f.write(f"  Variability:\n")
            f.write(f"    Std Dev:       {r['std']:10.2f}\n")
            f.write(f"    Dynamic Range: {r['dynamic_range_db']:10.2f} dB\n")
            f.write(f"  Percentiles:\n")
            for k, v in r['percentiles'].items():
                f.write(f"    {k:10s}  {v:10.2f}\n")
            f.write("\n")
    
    print(f"Saved: {filename}")

def main():
    input_file = "../../output/audio/original_8channels.pcm"
    output_dir = "../../output/audio/amplitude_analysis"
    
    print("="*80)
    print("PHAN TICH DAI AMPLITUDE TRONG AUDIO")
    print("="*80)
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print("="*80)
    
    # Tao thu muc output
    os.makedirs(output_dir, exist_ok=True)
    
    # Doc file audio
    audio_data = read_pcm_file(input_file)
    
    # Phan tich amplitude
    results = analyze_amplitude_range(audio_data)
    
    # Tao cac bieu do
    print("\n" + "="*80)
    print("TAO BIEU DO")
    print("="*80)
    
    plot_amplitude_distribution(audio_data, output_dir)
    plot_amplitude_comparison(audio_data, output_dir)
    create_summary_table(results, output_dir)
    
    # Luu ket qua
    save_results_to_file(results, output_dir)
    
    # Tong ket
    print("\n" + "="*80)
    print("TONG KET")
    print("="*80)
    
    active_channels = [r for r in results if r['has_audio']]
    silent_channels = [r for r in results if not r['has_audio']]
    
    print(f"\nChannels co audio: {len(active_channels)}")
    for r in active_channels:
        print(f"  - Channel {r['channel']}: RMS = {r['rms']:.1f}, Range = [{r['min']:.1f}, {r['max']:.1f}]")
    
    print(f"\nChannels khong co audio: {len(silent_channels)}")
    for r in silent_channels:
        print(f"  - Channel {r['channel']}: RMS = {r['rms']:.1f}, Range = [{r['min']:.1f}, {r['max']:.1f}]")
    
    print(f"\nCac file output da tao:")
    print(f"  - amplitude_distribution.png - Histogram va box plot tung channel")
    print(f"  - amplitude_comparison.png - So sanh amplitude giua cac channels")
    print(f"  - amplitude_summary_table.png - Bang tom tat")
    print(f"  - amplitude_analysis.txt - Bao cao chi tiet")
    
    print(f"\nThu muc output: {output_dir}")

if __name__ == "__main__":
    try:
        import matplotlib.pyplot
    except ImportError:
        print("Cai dat matplotlib:")
        print("pip install matplotlib")
        exit(1)
    
    main()

