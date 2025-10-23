# HƯỚNG DẪN SỬ DỤNG PROJECT ODAS

## Cấu Trúc Mới

Project đã được tổ chức lại thành cấu trúc folder sạch sẽ:

```
odas/
├── scripts/                    # Python scripts
│   ├── analysis/              # Phân tích audio
│   ├── beamforming/           # Beamforming algorithms
│   ├── filtering/             # Frequency filtering
│   ├── localization/          # Sound source localization
│   └── utilities/             # Utilities & configs
├── docs/                      # Tài liệu
│   ├── guides/               # Hướng dẫn chi tiết
│   ├── explanations/         # Giải thích kỹ thuật
│   └── quickstart/           # Hướng dẫn nhanh
├── output/                    # Kết quả xử lý
│   ├── audio/                # Audio files
│   ├── visualizations/       # Plots & charts
│   └── results/               # Data results
└── audio/                     # Input audio (giữ nguyên)
```

## Cách Sử Dụng

### 1. **Phân Tích Audio**

```bash
# Phân tích biên độ
cd scripts/analysis
python analyze_amplitude.py

# Phân tích channels
python analyze_audio.py
```

**Output:**
- `../../output/audio/amplitude_analysis/` - Biên độ analysis
- `../../output/visualizations/audio_channels_analysis.png` - Channel analysis plot
- `../../output/results/audio_analysis_result.json` - Analysis results

### 2. **Beamforming**

```bash
# Reference-based beamforming (khuyến nghị)
cd scripts/beamforming
python reference_beamforming.py

# Direction-based beamforming
python beamforming.py

# Combined processing (beamforming + filtering)
python combined_processing.py
```

**Output:**
- `../../output/audio/reference_beamforming/` - Reference beamforming results
- `../../output/audio/beamforming/` - Direction beamforming results
- `../../output/audio/combined_processing/` - Combined processing results

### 3. **Frequency Filtering**

```bash
# Bandpass filtering (tối ưu cho speech)
cd scripts/filtering
python filter_bandpass_600_3000.py

# Filter tất cả channels
python filter_all_active_channels.py

# Demo các loại filter
python filter_audio_demo.py

# Extract channels riêng lẻ
python extract_channels.py
```

**Output:**
- `../../output/audio/filtered/` - Filtered audio
- `../../output/audio/filtered_all/` - All channels filtered
- `../../output/audio/channels/` - Individual channels

### 4. **Sound Source Localization**

```bash
# Full localization
cd scripts/localization
python audio_source_localization.py

# Simple localization
python simple_localization.py
```

**Output:**
- `../../output/results/localization_result.json` - Localization results

### 5. **Utilities**

```bash
# Tạo ODAS config
cd scripts/utilities
python create_odas_config.py

# Visualize filter response
python visualize_filter_response.py

# Fix paths (nếu cần)
python fix_paths.py
```

## Pipeline Khuyến Nghị

### **Cho Chất Lượng Tốt Nhất:**

1. **Phân tích audio:**
   ```bash
   cd scripts/analysis
   python analyze_audio.py
   ```

2. **Reference-based beamforming:**
   ```bash
   cd scripts/beamforming
   python reference_beamforming.py
   ```

3. **Kết quả tốt nhất:**
   - File: `output/audio/reference_beamforming/vocal_extracted_combined_ampli.wav`
   - SNR improvement: +6 dB
   - Clean vocal với 4x amplification

### **Cho Localization:**

1. **Phân tích channels:**
   ```bash
   cd scripts/analysis
   python analyze_audio.py
   ```

2. **Localization:**
   ```bash
   cd scripts/localization
   python audio_source_localization.py
   ```

3. **Kết quả:**
   - Peak direction: 53.2°
   - 3D coordinates và spherical coordinates

## Output Files Quan Trọng

### **Audio Files:**
- **`output/audio/reference_beamforming/vocal_extracted_combined_ampli.wav`** ⭐ **BEST**
- `output/audio/beamforming/beamformed_peak.wav` - Direction beamforming
- `output/audio/combined_processing/step2_filtered.wav` - Combined processing

### **Visualizations:**
- `output/visualizations/audio_channels_analysis.png` - Channel analysis
- `output/audio/reference_beamforming/vocal_extraction_comparison.png` - Processing comparison
- `output/audio/reference_beamforming/channel_coherences.png` - Coherence analysis

### **Results:**
- `output/results/audio_analysis_result.json` - Channel analysis data
- `output/results/localization_result.json` - Localization data

## Troubleshooting

### **Lỗi "File not found":**
- Đảm bảo chạy script từ đúng thư mục
- Kiểm tra file input: `output/audio/original_8channels.pcm`

### **Lỗi Unicode:**
- Scripts đã được sửa để tránh lỗi Unicode
- Nếu vẫn gặp lỗi, chạy: `python fix_paths.py`

### **Output không tạo:**
- Kiểm tra quyền ghi file
- Đảm bảo thư mục output tồn tại

## Performance

### **Timing (trên máy trung bình):**
- Analysis: ~0.2s
- Reference beamforming: ~0.4s
- Direction beamforming: ~2s
- Filtering: ~0.1s
- **Total pipeline: ~3s**

### **Memory Usage:**
- Input file: 4.7MB
- Peak memory: ~50MB
- Output files: ~10MB total

## Dependencies

```bash
pip install numpy scipy matplotlib
```

## Cấu Trúc Input/Output

### **Input:**
- `output/audio/original_8channels.pcm` - 8-channel PCM file

### **Output:**
- `output/audio/` - Processed audio files
- `output/visualizations/` - PNG plots
- `output/results/` - JSON data files

## Best Practices

1. **Luôn chạy analysis trước** để hiểu audio characteristics
2. **Sử dụng reference beamforming** cho vocal extraction
3. **Kết hợp beamforming + filtering** cho chất lượng tốt nhất
4. **Kiểm tra output files** sau mỗi bước
5. **Sử dụng visualization** để hiểu kết quả

---

**Project giờ đây có cấu trúc sạch sẽ, dễ sử dụng và professional!** 🎯
