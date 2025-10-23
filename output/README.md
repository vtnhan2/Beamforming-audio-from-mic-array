# Output Directory

## Tổng Quan

Thư mục `output/` chứa tất cả kết quả xử lý được phân loại theo loại file:

## Cấu Trúc

```
output/
├── audio/            # Audio files
├── visualizations/   # Plots & charts
└── results/          # Data results
```

## Phân Loại

### 1. **Audio** - Audio files
- `original_8channels.pcm` - Input file gốc
- `amplitude_analysis/` - Kết quả phân tích biên độ
- `beamforming/` - Kết quả beamforming
- `channels/` - Channels riêng lẻ
- `combined_processing/` - Kết quả xử lý kết hợp
- `filtered/` - Audio đã lọc
- `reference_beamforming/` - Kết quả reference beamforming

### 2. **Visualizations** - Plots & charts
- `filter_frequency_response.png` - Frequency response
- `filter_order_comparison.png` - So sánh filter orders
- `filtfilt_vs_filter_comparison.png` - So sánh filtfilt vs filter
- `filter_effect_on_signal.png` - Tác động filter
- `audio_channels_analysis.png` - Phân tích channels

### 3. **Results** - Data results
- `audio_analysis_result.json` - Kết quả phân tích audio
- `localization_result.json` - Kết quả localization

## Cách Sử Dụng

### Nghe audio:
```bash
# Windows
start output/audio/reference_beamforming/vocal_extracted_combined_ampli.wav

# VLC
vlc output/audio/reference_beamforming/vocal_extracted_combined_ampli.wav
```

### Xem visualizations:
```bash
# Windows
start output/visualizations/filter_frequency_response.png
```

### Đọc results:
```bash
# JSON files
cat output/results/audio_analysis_result.json
```

## File Quan Trọng

### Best Audio Output:
- **`audio/reference_beamforming/vocal_extracted_combined_ampli.wav`** ⭐
  - Final output từ reference beamforming
  - Clean vocal với 4x amplification

### Key Visualizations:
- **`visualizations/filter_frequency_response.png`** - Filter characteristics
- **`audio/reference_beamforming/vocal_extraction_comparison.png`** - Processing comparison

### Analysis Results:
- **`results/audio_analysis_result.json`** - Channel analysis
- **`results/localization_result.json`** - Source localization
