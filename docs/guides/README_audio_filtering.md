# Huong dan loc audio tung channel

## Tong quan
Project cung cap cac cong cu de tach va loc audio cua tung channel tu file multi-channel PCM.

## Cac chuc nang chinh

### 1. Trich xuat va loc audio tung channel

**Script:** `extract_channels.py`

#### Cach su dung co ban:

```bash
# Trich xuat chi cac channels co audio (mac dinh)
python extract_channels.py --input audio/original_8channels.pcm --output-dir audio/channels

# Trich xuat tat ca cac channels
python extract_channels.py --input audio/original_8channels.pcm --output-dir audio/channels --all

# Tao file audio tron tu cac channels co audio
python extract_channels.py --input audio/original_8channels.pcm --output-dir audio/channels --mixed

# Luu dinh dang PCM thay vi WAV
python extract_channels.py --input audio/original_8channels.pcm --output-dir audio/channels --format pcm
```

#### Cac tuy chon bo loc:

```bash
# Khong ap dung bo loc
python extract_channels.py --filter none

# Bo loc bandpass (100-7000 Hz) - Loai bo nhieu thap va cao
python extract_channels.py --filter bandpass

# Bo loc highpass (> 100 Hz) - Loai bo nhieu tan so thap
python extract_channels.py --filter highpass

# Bo loc lowpass (< 7000 Hz) - Loai bo nhieu tan so cao
python extract_channels.py --filter lowpass
```

#### Vi du day du:

```bash
# Trich xuat tat ca channels, ap dung bo loc bandpass, dinh dang WAV, va tao file tron
python extract_channels.py \
    --input audio/original_8channels.pcm \
    --output-dir audio/channels \
    --format wav \
    --filter bandpass \
    --all \
    --mixed
```

### 2. Demo cac loai bo loc

**Script:** `filter_audio_demo.py`

Script nay tao cac file audio voi cac loai bo loc khac nhau de so sanh:

```bash
python filter_audio_demo.py
```

**Output:**
- `channel_5_original.wav` - Audio goc khong loc
- `channel_5_bandpass_100_7000.wav` - Loc dai 100-7000 Hz
- `channel_5_bandpass_300_3000.wav` - Loc dai 300-3000 Hz (ro giong noi)
- `channel_5_highpass_300.wav` - Loc thong cao 300 Hz
- `channel_5_lowpass_5000.wav` - Loc thong thap 5000 Hz
- `channel_5_notch_50hz.wav` - Loc notch 50 Hz (loai bo hum dien)
- `filter_comparison_channel_5.png` - Bieu do so sanh
- `frequency_spectrum_channel_5.png` - Bieu do pho tan so

## Cac loai bo loc

### 1. Bandpass Filter (Bo loc dai)
- **Cong dung:** Giu lai am thanh trong mot dai tan so nhat dinh, loai bo cac tan so ben ngoai
- **Su dung:** Loai bo nhieu tan so thap (hum) va nhieu tan so cao
- **Tham so:**
  - `100-7000 Hz`: Dai rong, giu hau het giong noi va nhac
  - `300-3000 Hz`: Dai hep, toi uu cho giong noi (giong dien thoai)

### 2. Highpass Filter (Bo loc thong cao)
- **Cong dung:** Chi cho phep cac tan so cao hon nguong cat truyen qua
- **Su dung:** Loai bo hum dien, nhieu tan so thap
- **Tham so:** 
  - `100 Hz`: Loai bo hum nhe
  - `300 Hz`: Loai bo hum manh va nhieu background

### 3. Lowpass Filter (Bo loc thong thap)
- **Cong dung:** Chi cho phep cac tan so thap hon nguong cat truyen qua
- **Su dung:** Loai bo nhieu tan so cao, tieng sit
- **Tham so:**
  - `5000 Hz`: Loai bo nhieu cao
  - `7000 Hz`: Loai bo nhieu cao nhe

### 4. Notch Filter (Bo loc notch)
- **Cong dung:** Loai bo mot tan so cu the
- **Su dung:** Loai bo hum dien 50Hz/60Hz
- **Tham so:**
  - `50 Hz`: Loai bo hum dien (chau Au, chau A)
  - `60 Hz`: Loai bo hum dien (chau My)

## Ket qua da tao

### Thu muc audio/channels/
- `channel_1.wav` - Audio cua channel 1 (da loc)
- `channel_2.wav` - Audio cua channel 2 (da loc)
- `channel_3.wav` - Audio cua channel 3 (da loc)
- `channel_4.wav` - Audio cua channel 4 (da loc)
- `channel_5.wav` - Audio cua channel 5 (da loc)
- `channel_8.wav` - Audio cua channel 8 (da loc)
- `mixed_audio.wav` - Audio tron tu cac channels co audio

### Thu muc audio/filtered/
- Cac file audio voi cac loai bo loc khac nhau
- Bieu do so sanh cac bo loc
- Bieu do pho tan so

## Thong so ky thuat

### Cau hinh audio
- **Sample rate:** 16000 Hz
- **Bit depth:** 16-bit
- **Format output:** WAV (mono) hoac PCM
- **Channels:** 8 (chi channels 1-5 va 8 co audio)

### Bo loc
- **Loai bo loc:** Butterworth filter (order 5)
- **Xu ly:** Zero-phase filtering (filtfilt)
- **Normalization:** 90% max amplitude

## Yeu cau he thong

### Python packages:
```bash
pip install numpy scipy wave
```

### Cac packages tuy chon:
```bash
pip install matplotlib  # De tao bieu do
```

## Troubleshooting

### 1. Loi "scipy not found"
```bash
pip install scipy
```

### 2. Loi "matplotlib not found"
```bash
pip install matplotlib
```

### 3. Khong nghe duoc file WAV
- Kiem tra audio player ho tro 16000 Hz sample rate
- Thu VLC Media Player hoac Audacity

### 4. File output qua nho hoac qua lon
- Dieu chinh normalization level trong code
- Thay doi `target_level` tu 0.9 sang gia tri khac (0.5 - 0.95)

## Vi du ung dung

### 1. Tach giong noi ro rang
```bash
python extract_channels.py \
    --filter bandpass \
    --format wav \
    --mixed
```

### 2. Loai bo hum dien
```bash
# Chinh sua filter_audio_demo.py de su dung notch filter 50Hz
```

### 3. Tao audio cho machine learning
```bash
python extract_channels.py \
    --all \
    --format pcm \
    --filter none
```

## Luu y

1. **Channels 6 va 7** khong co audio (chi co nhieu nho) nen se khong duoc trich xuat mac dinh
2. **Bo loc bandpass** tot nhat cho ung dung giong noi
3. **File mixed_audio.wav** la trung binh cua tat ca cac channels co audio
4. **Sample rate 16000 Hz** phu hop cho speech recognition
5. **Dinh dang WAV** tien loi cho playback, **PCM** tot cho xu ly sau

## Tham khao

- **Butterworth filter:** Bo loc co dap ung tan so phang nhat
- **Zero-phase filtering:** Khong lam sai pha, quan trong cho audio
- **Normalization:** Dam bao volume nhat quan giua cac file

## Lien he

Neu gap van de, kiem tra:
1. File input co dung dinh dang (16-bit PCM, 8 channels, 16000 Hz)
2. Python packages da cai dat day du
3. Quyen ghi file vao thu muc output

