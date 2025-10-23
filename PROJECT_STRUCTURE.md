# CẤU TRÚC PROJECT ODAS

## Tổng Quan

Project đã được tổ chức lại thành cấu trúc folder sạch sẽ và logic:

```
odas/
├── scripts/                    # Tất cả Python scripts
│   ├── analysis/              # Phân tích audio
│   │   ├── analyze_amplitude.py
│   │   └── analyze_audio.py
│   ├── beamforming/           # Beamforming algorithms
│   │   ├── beamforming.py
│   │   ├── reference_beamforming.py
│   │   └── combined_processing.py
│   ├── filtering/             # Frequency filtering
│   │   ├── filter_audio_demo.py
│   │   ├── filter_bandpass_600_3000.py
│   │   ├── filter_all_active_channels.py
│   │   └── extract_channels.py
│   ├── localization/          # Sound source localization
│   │   ├── audio_source_localization.py
│   │   └── simple_localization.py
│   └── utilities/             # Utilities & configs
│       ├── create_odas_config.py
│       ├── visualize_filter_response.py
│       ├── odas_loop.sh
│       ├── run_odas_localization.sh
│       ├── re6_sockets.cfg
│       ├── re6_vr.cfg
│       ├── sca.c
│       ├── CMakeLists.txt
│       └── ProcesserLib/
├── docs/                      # Tài liệu
│   ├── guides/               # Hướng dẫn chi tiết
│   │   ├── BEAMFORMING_GUIDE.md
│   │   ├── REFERENCE_BEAMFORMING_GUIDE.md
│   │   ├── README_localization.md
│   │   └── README_audio_filtering.md
│   ├── explanations/          # Giải thích kỹ thuật
│   │   ├── FILTER_EXPLANATION.md
│   │   ├── GIAI_THICH_REFERENCE_BEAMFORMING.md
│   │   └── AUDIO_PROCESSING_COMPARISON.md
│   └── quickstart/           # Hướng dẫn nhanh
│       └── QUICK_START_FILTERING.md
├── output/                    # Kết quả xử lý
│   ├── audio/                # Audio files
│   │   ├── original_8channels.pcm
│   │   ├── amplitude_analysis/
│   │   ├── beamforming/
│   │   ├── channels/
│   │   ├── combined_processing/
│   │   ├── filtered/
│   │   └── reference_beamforming/
│   ├── visualizations/       # Plots & charts
│   │   ├── filter_frequency_response.png
│   │   ├── filter_order_comparison.png
│   │   ├── filtfilt_vs_filter_comparison.png
│   │   ├── filter_effect_on_signal.png
│   │   └── audio_channels_analysis.png
│   └── results/              # JSON results
│       ├── audio_analysis_result.json
│       └── localization_result.json
├── audio/                     # Input audio (giữ nguyên)
│   └── original_8channels.pcm
├── README_COMPLETE.md         # Tài liệu chính
├── INDEX.md                   # Mục lục
├── LICENSE                    # License
└── PROJECT_STRUCTURE.md       # File này
```

## Phân Loại Theo Chức Năng

### 1. **Scripts/Analysis** - Phân tích audio
- `analyze_amplitude.py`: Phân tích biên độ, phát hiện clipping
- `analyze_audio.py`: Phân tích nhanh channels, xác định active/silent

### 2. **Scripts/Beamforming** - Lọc không gian
- `beamforming.py`: Delay-and-Sum beamforming
- `reference_beamforming.py`: Reference-based vocal extraction
- `combined_processing.py`: Beamforming + Filtering pipeline

### 3. **Scripts/Filtering** - Lọc tần số
- `filter_audio_demo.py`: Demo các loại filter
- `filter_bandpass_600_3000.py`: Bandpass tối ưu cho speech
- `filter_all_active_channels.py`: Lọc tất cả channels
- `extract_channels.py`: Trích xuất channels riêng lẻ

### 4. **Scripts/Localization** - Định vị nguồn âm
- `audio_source_localization.py`: TDOA + Least squares
- `simple_localization.py`: Phiên bản đơn giản

### 5. **Scripts/Utilities** - Tiện ích
- `create_odas_config.py`: Tạo config cho ODAS C
- `visualize_filter_response.py`: Minh họa filter response
- Shell scripts, config files, C code

## Phân Loại Theo Tài Liệu

### 1. **Docs/Guides** - Hướng dẫn chi tiết
- Hướng dẫn sử dụng từng kỹ thuật
- Examples và use cases
- Troubleshooting

### 2. **Docs/Explanations** - Giải thích kỹ thuật
- Lý thuyết thuật toán
- Mathematical formulas
- So sánh phương pháp

### 3. **Docs/Quickstart** - Hướng dẫn nhanh
- Commands cơ bản
- Quick reference
- Getting started

## Phân Loại Theo Output

### 1. **Output/Audio** - Audio files
- Processed audio files
- Organized by processing type
- Maintains original structure

### 2. **Output/Visualizations** - Plots & charts
- PNG files từ matplotlib
- Frequency responses
- Comparison plots

### 3. **Output/Results** - Data results
- JSON files với analysis results
- Metrics và measurements
- Localization data

## Lợi Ích Của Cấu Trúc Mới

### ✅ **Tổ chức rõ ràng**
- Scripts được phân loại theo chức năng
- Docs được phân loại theo mục đích
- Output được phân loại theo loại file

### ✅ **Dễ tìm kiếm**
- Biết chức năng → Vào folder tương ứng
- Biết loại tài liệu → Vào docs phù hợp
- Biết loại output → Vào output tương ứng

### ✅ **Dễ bảo trì**
- Thêm script mới → Vào folder chức năng
- Thêm docs mới → Vào folder mục đích
- Clean separation of concerns

### ✅ **Professional structure**
- Giống các open source projects
- Dễ hiểu cho người mới
- Scalable cho tương lai

## Cách Sử Dụng

### 1. **Chạy Analysis**
```bash
cd scripts/analysis
python analyze_amplitude.py
python analyze_audio.py
```

### 2. **Chạy Beamforming**
```bash
cd scripts/beamforming
python reference_beamforming.py
python beamforming.py
```

### 3. **Chạy Filtering**
```bash
cd scripts/filtering
python filter_bandpass_600_3000.py
```

### 4. **Chạy Localization**
```bash
cd scripts/localization
python audio_source_localization.py
```

### 5. **Xem Output**
```bash
# Audio files
ls output/audio/

# Visualizations
ls output/visualizations/

# Results
ls output/results/
```

## Migration Notes

### Files đã được di chuyển:
- ✅ Tất cả Python scripts → `scripts/`
- ✅ Tất cả markdown docs → `docs/`
- ✅ Tất cả audio files → `output/audio/`
- ✅ Tất cả PNG files → `output/visualizations/`
- ✅ Tất cả JSON files → `output/results/`
- ✅ Utilities → `scripts/utilities/`

### Files giữ nguyên:
- ✅ `audio/original_8channels.pcm` (input file)
- ✅ `README_COMPLETE.md` (main documentation)
- ✅ `INDEX.md` (index)
- ✅ `LICENSE` (license)

## Next Steps

1. **Update import paths** trong các scripts nếu cần
2. **Update documentation** để reflect new structure
3. **Test all scripts** để đảm bảo hoạt động
4. **Update README** với new structure

---

**Cấu trúc mới giúp project sạch sẽ, dễ hiểu và professional hơn!** 🎯
