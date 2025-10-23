# Audio Source Localization với ODAS

## Mô tả
Dự án này xử lý file `original_8channels.pcm` để xác định vị trí nguồn âm thanh trong không gian 3D sử dụng thư viện ODAS.

## Thông tin file audio
- **File**: `original_8channels.pcm`
- **Format**: Signed 16-bit PCM, Little-endian
- **Sample rate**: 16000 Hz
- **Channels**: 8
- **Channels có audio**: 1, 2, 3, 4, 5, 8
- **Channels không có audio**: 6, 7
- **Start offset**: 2 bytes

## Cấu trúc dự án

```
├── audio_source_localization.py    # Script chính xử lý audio
├── create_odas_config.py           # Tạo file cấu hình ODAS
├── analyze_audio.py                # Phân tích file audio
├── run_odas_localization.sh       # Script chạy ODAS
├── odas_8ch_config.cfg            # File cấu hình ODAS (tự tạo)
└── README_localization.md         # File hướng dẫn này
```

## Cài đặt

### 1. Cài đặt dependencies

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip python3-numpy python3-matplotlib
sudo apt-get install cmake build-essential
sudo apt-get install libfftw3-dev libasound2-dev libconfig-dev libpulse-dev

# CentOS/RHEL
sudo yum install python3 python3-pip python3-numpy python3-matplotlib
sudo yum install cmake gcc gcc-c++ make
sudo yum install fftw-devel alsa-lib-devel libconfig-devel pulseaudio-libs-devel
```

### 2. Build ODAS

```bash
# Trong thư mục ODAS
mkdir build && cd build
cmake ..
make -j4

# Copy executable
cp odaslive ../
cd ..
```

## Sử dụng

### 1. Phân tích file audio

```bash
# Phân tích file original_8channels.pcm
python3 analyze_audio.py

# Kết quả:
# - audio_channels_analysis.png: Biểu đồ các channels
# - audio_analysis_result.json: Kết quả phân tích chi tiết
```

### 2. Tạo file cấu hình ODAS

```bash
# Tạo file cấu hình cho 8-channel microphone array
python3 create_odas_config.py

# Tạo file: odas_8ch_config.cfg
```

### 3. Chạy localization với ODAS

```bash
# Chạy ODAS với file cấu hình
./run_odas_localization.sh

# Hoặc chạy trực tiếp
./odaslive -c odas_8ch_config.cfg -v
```

### 4. Sử dụng script Python (không cần ODAS)

```bash
# Chạy localization bằng Python
python3 audio_source_localization.py --input original_8channels.pcm --output result.json

# Tạo file cấu hình ODAS
python3 audio_source_localization.py --create-config
```

## Kết quả

### 1. Output từ ODAS
- **Socket port 9000**: Tracked sources (JSON)
- **Socket port 9001**: Potential sources (JSON)
- **File**: `separated.raw`, `postfiltered.raw`

### 2. Output từ Python script
- **JSON file**: Vị trí nguồn âm thanh (Cartesian và Spherical)
- **Channel analysis**: Phân tích chi tiết các channels
- **TDOA**: Time Difference of Arrival

### 3. Lắng nghe kết quả

```bash
# Lắng nghe tracked sources
netcat -l 9000

# Lắng nghe potential sources  
netcat -l 9001

# Xem kết quả JSON
cat result.json | jq .
```

## Cấu hình microphone array

### Vị trí microphones (8 microphones dạng tròn)
- **Bán kính**: 5cm
- **Vị trí**: 
  - Mic 1: (0.05, 0.00, 0.00)
  - Mic 2: (0.035, 0.035, 0.00)
  - Mic 3: (0.00, 0.05, 0.00)
  - Mic 4: (-0.035, 0.035, 0.00)
  - Mic 5: (-0.05, 0.00, 0.00)
  - Mic 6: (-0.035, -0.035, 0.00) [KHÔNG SỬ DỤNG]
  - Mic 7: (0.00, -0.05, 0.00) [KHÔNG SỬ DỤNG]
  - Mic 8: (0.035, -0.035, 0.00)

### Channels mapping
- **Sử dụng**: Channels 1, 2, 3, 4, 5, 8
- **Bỏ qua**: Channels 6, 7

## Troubleshooting

### 1. Lỗi dependencies
```bash
# Kiểm tra Python packages
pip3 install numpy matplotlib

# Kiểm tra ODAS dependencies
pkg-config --cflags --libs fftw3f
pkg-config --cflags --libs alsa
```

### 2. Lỗi file không tìm thấy
```bash
# Kiểm tra file input
ls -la original_8channels.pcm

# Kiểm tra quyền truy cập
chmod +x run_odas_localization.sh
```

### 3. Lỗi socket
```bash
# Kiểm tra port đã sử dụng
netstat -tulpn | grep 9000
netstat -tulpn | grep 9001

# Thay đổi port trong config nếu cần
```

## Kết quả mẫu

### JSON output
```json
{
  "position_cartesian": [0.123, -0.045, 0.012],
  "position_spherical": {
    "distance": 0.131,
    "azimuth": -20.1,
    "elevation": 5.2
  },
  "tdoas": [0.0, 0.0001, -0.0002, 0.0003, -0.0001, 0.0002],
  "channel_analysis": {
    "0": {"has_audio": true, "rms": 1250.5},
    "1": {"has_audio": true, "rms": 1180.2},
    ...
  }
}
```

### Ý nghĩa kết quả
- **position_cartesian**: Vị trí (x, y, z) trong mét
- **position_spherical**: 
  - **distance**: Khoảng cách từ microphone array
  - **azimuth**: Góc phương vị (-180° đến +180°)
  - **elevation**: Góc nâng (-90° đến +90°)
- **tdoas**: Thời gian trễ giữa các microphone (giây)

## Tùy chỉnh

### 1. Thay đổi microphone array
Chỉnh sửa `mic_positions` trong `audio_source_localization.py`:

```python
def _setup_microphone_array(self) -> np.ndarray:
    # Thay đổi vị trí microphones
    positions = [
        [0.05, 0.00, 0.00],    # Mic 1
        [0.035, 0.035, 0.00],  # Mic 2
        # ... thêm vị trí khác
    ]
    return np.array(positions)
```

### 2. Thay đổi thuật toán localization
Chỉnh sửa hàm `localize_sound_source()` để sử dụng thuật toán khác:
- MUSIC
- SRP-PHAT  
- GCC-PHAT
- Beamforming

### 3. Thay đổi cấu hình ODAS
Chỉnh sửa file `odas_8ch_config.cfg`:
- `nPots`: Số potential sources
- `probMin`: Xác suất tối thiểu
- `interpRate`: Tỷ lệ nội suy
- `scans`: Cấu hình quét

## Liên hệ
Nếu có vấn đề, vui lòng kiểm tra:
1. File `original_8channels.pcm` có đúng format không
2. Dependencies đã cài đặt đầy đủ chưa
3. ODAS đã build thành công chưa
4. Port 9000, 9001 có bị chiếm dụng không
