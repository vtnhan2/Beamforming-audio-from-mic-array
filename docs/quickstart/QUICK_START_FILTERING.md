# HUONG DAN NHANH: LOC AUDIO TUNG CHANNEL

## Cac lenh da chay thanh cong

### 1. Tach va loc cac channels co audio (6 channels)
```bash
python filter_all_active_channels.py
```

**Ket qua:**
- Thu muc: `audio/filtered_all/`
- 36 file audio WAV (6 channels x 6 loai bo loc)
- 14 bieu do PNG (12 cho tung channel + 2 tong hop)
- 1 file SUMMARY.md chi tiet

## Cau truc thu muc output

```
audio/filtered_all/
├── channel_1/
│   ├── channel_1_original.wav
│   ├── channel_1_bandpass_100_7000.wav
│   ├── channel_1_bandpass_300_3000.wav
│   ├── channel_1_highpass_300.wav
│   ├── channel_1_lowpass_5000.wav
│   ├── channel_1_notch_50hz.wav
│   ├── waveform_channel_1.png
│   └── spectrum_channel_1.png
├── channel_2/ (tuong tu)
├── channel_3/ (tuong tu)
├── channel_4/ (tuong tu)
├── channel_5/ (tuong tu - MANH NHAT)
├── channel_8/ (tuong tu)
├── all_channels_comparison.png
├── all_channels_spectrum.png
└── SUMMARY.md
```

## Cac scripts co san

### 1. `extract_channels.py` - Tach channels don gian
```bash
# Tach chi channels co audio, dinh dang WAV, bo loc bandpass
python extract_channels.py

# Tach tat ca channels
python extract_channels.py --all

# Tao file audio tron
python extract_channels.py --mixed

# Khong ap dung bo loc
python extract_channels.py --filter none
```

### 2. `filter_audio_demo.py` - Demo cac bo loc (1 channel)
```bash
# Demo cac bo loc tren channel 5 (manh nhat)
python filter_audio_demo.py
```
Output: `audio/filtered/`

### 3. `filter_all_active_channels.py` - Loc tat ca channels ⭐
```bash
# Xu ly tat ca channels co audio voi day du cac bo loc
python filter_all_active_channels.py
```
Output: `audio/filtered_all/`

## So sanh RMS cac channels

| Channel | RMS    | Danh gia |
|---------|--------|----------|
| 5       | 9891.0 | ⭐⭐⭐ MANH NHAT |
| 4       | 6410.6 | ⭐⭐ Manh |
| 3       | 5626.7 | ⭐⭐ Manh |
| 8       | 5081.2 | ⭐⭐ Trung binh |
| 2       | 3475.3 | ⭐ Yeu |
| 1       | 2943.2 | ⭐ Yeu nhat |
| 6       | 1.9    | ✗ Silent |
| 7       | 1.8    | ✗ Silent |

## Lua chon bo loc phu hop

### Cho giong noi (Speech Recognition)
```
✅ Dung: channel_X_bandpass_300_3000.wav
   - Dai tan so 300-3000 Hz (giong dien thoai)
   - Ro giong noi nhat
   - Tot nhat cho speech-to-text
```

### Cho audio tong quat
```
✅ Dung: channel_X_bandpass_100_7000.wav
   - Dai tan so 100-7000 Hz
   - Giu hau het thong tin audio
   - Can bang giua chat luong va loai nhieu
```

### Loai bo hum dien
```
✅ Dung: channel_X_notch_50hz.wav
   hoac: channel_X_highpass_300.wav
   - Loai bo hum 50Hz (dien chau Au/A)
   - Highpass 300Hz loai bo tat ca tan so thap
```

### Loai bo nhieu tan so cao
```
✅ Dung: channel_X_lowpass_5000.wav
   - Loai bo tieng xit, nhieu cao
   - Lam muot audio
```

## Xem va phan tich ket qua

### 1. Nghe audio
```bash
# Windows
start audio\filtered_all\channel_5\channel_5_bandpass_300_3000.wav

# VLC
vlc audio/filtered_all/channel_5/channel_5_bandpass_300_3000.wav
```

### 2. Xem bieu do
```bash
# Bieu do tong hop tat ca channels
start audio\filtered_all\all_channels_comparison.png

# Bieu do pho tan so
start audio\filtered_all\all_channels_spectrum.png

# Bieu do chi tiet 1 channel
start audio\filtered_all\channel_5\waveform_channel_5.png
start audio\filtered_all\channel_5\spectrum_channel_5.png
```

### 3. Doc summary
```bash
notepad audio\filtered_all\SUMMARY.md
```

## Goi y su dung

### Use case 1: Speech Recognition
```
Channel nen dung: Channel 5 (manh nhat)
File nen dung: channel_5_bandpass_300_3000.wav
Ly do: Ro giong noi nhat, dai tan so toi uu cho speech
```

### Use case 2: Audio Analysis
```
Channel nen dung: Tat ca channels
File nen dung: channel_X_bandpass_100_7000.wav
Ly do: Giu day du thong tin, loai bo nhieu
```

### Use case 3: Noise Reduction
```
Channel nen dung: Channel co RMS cao (4, 5, 8)
File nen dung: channel_X_highpass_300.wav hoac channel_X_notch_50hz.wav
Ly do: Loai bo nhieu tan so thap va hum dien
```

### Use case 4: Compare Channels
```
File nen xem: all_channels_comparison.png
Ly do: Nhin thay ngay channel nao tot nhat
```

## Thong so ky thuat

- **Sample rate:** 16000 Hz
- **Bit depth:** 16-bit
- **Format:** WAV (Mono)
- **Bo loc:** Butterworth order 5
- **Method:** Zero-phase filtering (filtfilt)
- **Normalization:** 90% max amplitude

## Troubleshooting

### Khong nghe duoc file WAV
```
✅ Kiem tra audio player ho tro 16000 Hz
✅ Thu VLC Media Player
✅ Thu Audacity
```

### Muon doi sample rate
```python
# Chinh sua trong script:
sample_rate = 44100  # thay vi 16000
```

### Muon thay doi bo loc
```python
# Chinh sua tham so trong filter_all_active_channels.py:
# Vi du: Bandpass 200-8000 Hz
low = 200 / nyquist
high = 8000 / nyquist
```

## Tong ket

✅ **36 file audio WAV** - Tat ca channels da loc
✅ **14 bieu do PNG** - Visualization day du
✅ **1 file SUMMARY.md** - Tai lieu chi tiet
✅ **Tong 50 files** - San sang su dung

Channels duoc xu ly:
1. ✅ Channel 1 (RMS: 2943)
2. ✅ Channel 2 (RMS: 3475)
3. ✅ Channel 3 (RMS: 5627)
4. ✅ Channel 4 (RMS: 6411)
5. ✅ Channel 5 (RMS: 9891) ⭐ MANH NHAT
6. ✅ Channel 8 (RMS: 5081)

Channels khong co audio (da bo qua):
- ✗ Channel 6 (RMS: 1.9)
- ✗ Channel 7 (RMS: 1.8)

