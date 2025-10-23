# Hướng Dẫn Beamforming - Microphone Array

## Tổng Quan

**Beamforming** là kỹ thuật xử lý tín hiệu không gian (spatial signal processing) sử dụng mảng microphone để:
- **Tập trung vào âm thanh từ một hướng cụ thể** (directional selectivity)
- **Loại bỏ tiếng ồn từ các hướng khác** (noise rejection)
- **Tăng tỷ lệ tín hiệu trên nhiễu** (SNR improvement)
- **Xác định hướng nguồn âm thanh** (sound source localization)

## Kết Quả Beamforming

### Peak Direction Phát Hiện: **53.2°**

Nguồn âm thanh chính nằm ở hướng **53.2°** (về phía đông bắc):
- **0°** = Trước mặt (North)
- **53.2°** = Đông bắc (Northeast)
- **90°** = Bên phải (East)
- **180°/-180°** = Phía sau (South)
- **-90°** = Bên trái (West)

### Files Đã Tạo

```
audio/beamforming/
├── beam_pattern_polar.png          # Polar pattern (hình tròn)
├── beam_pattern_cartesian.png      # Cartesian plot (đồ thị thẳng)
│
├── omnidirectional.wav             # Audio gốc (trung bình tất cả mics)
├── beamformed_peak.wav             # Audio beamformed theo peak direction (53.2°)
│
├── beamformed_0deg.wav             # Beamformed hướng 0° (trước)
├── beamformed_45deg.wav            # Beamformed hướng 45°
├── beamformed_90deg.wav            # Beamformed hướng 90° (phải)
├── beamformed_135deg.wav           # Beamformed hướng 135°
├── beamformed_180deg.wav           # Beamformed hướng 180° (sau)
├── beamformed_-135deg.wav          # Beamformed hướng -135°
├── beamformed_-90deg.wav           # Beamformed hướng -90° (trái)
├── beamformed_-45deg.wav           # Beamformed hướng -45°
└── beamformed_53deg.wav            # Beamformed theo peak direction
```

## Cách Hoạt Động

### 1. Delay-and-Sum Beamforming

**Nguyên lý cơ bản:**

```
Microphone Array (6 mics)
      ↓
Calculate Delays
      ↓
Align Signals
      ↓
Sum Together
      ↓
Beamformed Output
```

**Chi tiết:**

1. **Calculate Steering Vector**
   - Tính delay (độ trễ) cho mỗi microphone dựa trên hướng mong muốn
   - Delay phụ thuộc vào:
     - Vị trí microphone
     - Hướng nguồn âm thanh (azimuth, elevation)
     - Tốc độ âm thanh (343 m/s)

   ```python
   # Công thức tính delay
   delay[i] = (mic_position[i] · direction) / speed_of_sound
   ```

2. **Apply Fractional Delay**
   - Dịch chuyển tín hiệu của mỗi mic theo delay tính được
   - Sử dụng linear interpolation cho fractional delay (độ trễ lẻ)

3. **Sum and Average**
   - Cộng tất cả tín hiệu đã align
   - Chia trung bình

   ```python
   beamformed = sum(delayed_signals) / n_mics
   ```

### 2. Microphone Array Configuration

**Layout:** 6 microphones active (channels 1, 2, 3, 4, 5, 8) trong mảng tròn

```
        Mic 1 (0°)
          ↑
    Mic 8 ↗   ↖ Mic 2 (45°)
          |
Mic 5 ←   ●   → Mic 3 (90°)
          |
          ↓ Mic 4
```

**Thông số:**
- **Radius:** 5 cm (0.05m)
- **Channels active:** 1, 2, 3, 4, 5, 8
- **Sample rate:** 16000 Hz
- **Speed of sound:** 343 m/s

## Hiểu Các Plots

### 1. Polar Pattern (`beam_pattern_polar.png`)

<img src="audio/beamforming/beam_pattern_polar.png" alt="Polar Pattern" width="600"/>

**Cách đọc:**
- **0° ở phía trên** (North)
- **Góc tăng theo chiều kim đồng hồ**
- **Bán kính = Power (dB)**
- **Màu xanh = Beam response**
- **Chấm đỏ = Peak direction (53.2°)**

**Ý nghĩa:**
- Peak càng cao = Nguồn âm thanh càng mạnh từ hướng đó
- Vùng rộng = Beamwidth (độ rộng beam)
- Side lobes = Độ nhạy với các hướng khác

### 2. Cartesian Plot (`beam_pattern_cartesian.png`)

<img src="audio/beamforming/beam_pattern_cartesian.png" alt="Cartesian Plot" width="800"/>

**Cách đọc:**
- **Trục X = Azimuth (góc phương vi)** từ -180° đến 180°
- **Trục Y = Power (dB)** (chuẩn hóa về 0 dB max)
- **Peak = Hướng nguồn âm thanh mạnh nhất**

## So Sánh Audio

### Omnidirectional vs Beamformed

| File | Mô tả | Ứng dụng |
|------|-------|----------|
| `omnidirectional.wav` | Trung bình tất cả mics<br/>Không có directional selectivity | - Ghi âm tổng quan<br/>- Hội nghị với nhiều người |
| `beamformed_peak.wav` | Tập trung vào hướng 53.2°<br/>Tăng SNR, giảm nhiễu | - Ghi âm một người nói<br/>- Speech recognition<br/>- Zoom vào nguồn âm thanh |

### Beamformed Theo Các Hướng

- **`beamformed_0deg.wav`** - Tập trung phía trước
- **`beamformed_90deg.wav`** - Tập trung bên phải
- **`beamformed_180deg.wav`** - Tập trung phía sau
- **`beamformed_-90deg.wav`** - Tập trung bên trái
- **`beamformed_53deg.wav`** - Tập trung theo peak direction

## Ứng Dụng Thực Tế

### 1. Smart Speakers
- **Amazon Echo, Google Home** sử dụng beamforming
- Tập trung vào người đang nói
- Loại bỏ tiếng nhạc, TV

### 2. Hearing Aids
- Tập trung vào người đối diện
- Giảm tiếng ồn phía sau

### 3. Video Conferencing
- **Zoom, Teams** dùng beamforming
- Tập trung vào người đang phát biểu
- Loại bỏ tiếng gõ bàn phím, tiếng điều hòa

### 4. Automotive
- Voice command trong xe
- Loại bỏ tiếng động cơ, tiếng đường

### 5. Robotics
- Robot xác định hướng người nói
- Quay mặt về người đang gọi

## Kỹ Thuật Beamforming Nâng Cao

### 1. Delay-and-Sum (DAS) - Đã implement ✅
**Ưu điểm:**
- Đơn giản, robust
- Không cần training

**Nhược điểm:**
- Beamwidth rộng (độ phân giải hạn chế)
- Side lobes lớn

### 2. Minimum Variance Distortionless Response (MVDR)
**Ưu điểm:**
- Beamwidth hẹp hơn
- Side lobes nhỏ hơn
- Tự động loại bỏ nhiễu

**Nhược điểm:**
- Cần ước lượng covariance matrix
- Tính toán phức tạp hơn

### 3. Generalized Sidelobe Canceller (GSC)
**Ưu điểm:**
- Tối ưu trong môi trường nhiễu
- Adaptive nulling (loại bỏ nhiễu tự động)

### 4. Super-directive Beamforming
**Ưu điểm:**
- Beamwidth rất hẹp
- Độ phân giải cao

**Nhược điểm:**
- Nhạy cảm với lỗi mics
- Yêu cầu calibration chính xác

## Code Implementation

### Cấu Trúc Class

```python
class DelayAndSumBeamformer:
    def __init__(self, mic_positions, sample_rate, speed_of_sound):
        # Khởi tạo với vị trí mics
        
    def steer_vector(self, azimuth_deg, elevation_deg):
        # Tính steering vector (delays) cho hướng mong muốn
        
    def apply_beamforming(self, audio_data, azimuth_deg):
        # Áp dụng beamforming
        
    def scan_directions(self, audio_data, n_directions):
        # Scan nhiều hướng để tìm nguồn âm thanh
        
    def _fractional_delay(self, signal, delay_samples):
        # Áp dụng fractional delay
```

### Sử Dụng

```python
# 1. Tạo beamformer
beamformer = DelayAndSumBeamformer(
    mic_positions=[[x1,y1,z1], [x2,y2,z2], ...],
    sample_rate=16000,
    speed_of_sound=343.0
)

# 2. Scan để tìm hướng
azimuths, powers = beamformer.scan_directions(audio_data, n_directions=72)
peak_azimuth, peak_power = beamformer.find_peak_direction(azimuths, powers)

# 3. Beamform theo hướng cụ thể
beamformed = beamformer.apply_beamforming(audio_data, azimuth_deg=53.2)

# 4. Lưu file
save_wav(beamformed, 'output.wav')
```

## Tham Số Quan Trọng

### 1. Microphone Spacing
- **Spacing nhỏ** (< λ/2):
  - ✅ Tránh spatial aliasing
  - ❌ Beamwidth rộng
  
- **Spacing lớn** (> λ/2):
  - ✅ Beamwidth hẹp
  - ❌ Grating lobes (ambiguity)

**Công thức:**
```
λ = c / f
Spacing optimal ≈ λ/2 ≈ 343 / (2 * f_max)
```

Với `f_max = 3000 Hz`: `spacing ≈ 5.7 cm` ✅ (array hiện tại: radius = 5 cm)

### 2. Number of Microphones
- **Nhiều mics hơn:**
  - ✅ Beamwidth hẹp hơn
  - ✅ Side lobes nhỏ hơn
  - ✅ Directional selectivity tốt hơn
  - ❌ Chi phí cao hơn
  - ❌ Tính toán phức tạp hơn

### 3. Beamwidth
```
Beamwidth (degrees) ≈ 50 * λ / (N * d)
```
- `λ` = wavelength
- `N` = số mics
- `d` = spacing

Với array hiện tại (6 mics, radius 5cm, f=1000Hz):
```
λ = 343 / 1000 = 0.343m
Beamwidth ≈ 50 * 0.343 / (6 * 0.05) ≈ 57°
```

## So Sánh với ODAS

| Feature | Implementation này | ODAS |
|---------|-------------------|------|
| **Algorithm** | Delay-and-Sum | DDS, DGSS, DMVDR |
| **Domain** | Time domain | Frequency domain (STFT) |
| **Tracking** | Static scan | Kalman/Particle filter |
| **Separation** | Single beam | Multiple sources |
| **Real-time** | Batch processing | ✅ Real-time |
| **Language** | Python | C (optimized) |

### Khi Nào Dùng Cái Nào?

**Dùng implementation này khi:**
- ✅ Cần giải pháp đơn giản, dễ hiểu
- ✅ Xử lý offline (không real-time)
- ✅ Prototyping, testing
- ✅ Educational purposes

**Dùng ODAS khi:**
- ✅ Cần real-time processing
- ✅ Multiple sound sources
- ✅ Tracking moving sources
- ✅ Production deployment
- ✅ Tối ưu performance

## Chạy Beamforming

### Cài Đặt Dependencies

```bash
pip install numpy scipy matplotlib wave
```

### Chạy Script

```bash
python beamforming.py
```

### Output

Script sẽ:
1. ✅ Đọc `audio/original_8channels.pcm`
2. ✅ Scan 72 hướng để tìm peak
3. ✅ Tạo beamformed audio theo nhiều hướng
4. ✅ Vẽ polar pattern và Cartesian plot
5. ✅ Lưu tất cả vào `audio/beamforming/`

## Kết Luận

### Beamforming đạt được gì?

1. **Localization** ✅
   - Xác định nguồn âm thanh ở hướng **53.2°**
   
2. **Directional Selectivity** ✅
   - Tập trung vào hướng mong muốn
   - Loại bỏ nhiễu từ các hướng khác
   
3. **SNR Improvement** ✅
   - Tăng tỷ lệ tín hiệu trên nhiễu
   - Audio rõ ràng hơn
   
4. **Spatial Filtering** ✅
   - Lọc không gian (không chỉ tần số)
   - Complement với bandpass filtering

### Kết Hợp với Filtering

**Pipeline đầy đủ:**
```
PCM Input (8 channels)
      ↓
Beamforming (spatial filtering)
      ↓
Bandpass 600-3000 Hz (frequency filtering)
      ↓
Clean Speech Output
```

## Tài Liệu Tham Khảo

1. **Van Veen, B. D., & Buckley, K. M. (1988).** Beamforming: A versatile approach to spatial filtering. *IEEE ASSP Magazine*, 5(2), 4-24.

2. **Benesty, J., Chen, J., & Huang, Y. (2008).** Microphone array signal processing (Vol. 1). Springer Science & Business Media.

3. **ODAS Documentation:** https://github.com/introlab/odas

4. **Johnson, D. H., & Dudgeon, D. E. (1993).** Array signal processing: concepts and techniques. Simon & Schuster.

## Liên Hệ / Support

Nếu có câu hỏi về beamforming hoặc cần customize thêm:
- 📧 Email: [your-email]
- 🔗 GitHub: [your-github]
- 📚 Docs: Xem `FILTER_EXPLANATION.md`, `README_localization.md`

---

**Version:** 1.0  
**Last Updated:** October 21, 2025  
**Author:** AI Assistant

