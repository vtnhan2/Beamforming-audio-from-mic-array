# Scripts Directory

## Tổng Quan

Thư mục `scripts/` chứa tất cả Python scripts được phân loại theo chức năng:

## Cấu Trúc

```
scripts/
├── analysis/          # Phân tích audio
├── beamforming/       # Beamforming algorithms  
├── filtering/         # Frequency filtering
├── localization/      # Sound source localization
└── utilities/         # Utilities & configs
```

## Cách Sử Dụng

### 1. Analysis Scripts
```bash
cd scripts/analysis
python analyze_amplitude.py    # Phân tích biên độ
python analyze_audio.py        # Phân tích channels
```

### 2. Beamforming Scripts
```bash
cd scripts/beamforming
python reference_beamforming.py  # Reference-based vocal extraction
python beamforming.py            # Direction-based beamforming
python combined_processing.py    # Combined pipeline
```

### 3. Filtering Scripts
```bash
cd scripts/filtering
python filter_bandpass_600_3000.py  # Bandpass filtering
python filter_all_active_channels.py # Filter all channels
python extract_channels.py           # Extract individual channels
```

### 4. Localization Scripts
```bash
cd scripts/localization
python audio_source_localization.py  # Full localization
python simple_localization.py        # Simple localization
```

### 5. Utilities
```bash
cd scripts/utilities
python create_odas_config.py         # Create ODAS config
python visualize_filter_response.py  # Visualize filters
```

## Input/Output

- **Input**: `../audio/original_8channels.pcm`
- **Output**: `../output/` (audio, visualizations, results)

## Dependencies

Tất cả scripts sử dụng các thư viện Python chuẩn:
- numpy
- scipy
- matplotlib
- wave
- struct
- os
- time
