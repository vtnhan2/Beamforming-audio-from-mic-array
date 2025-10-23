# GIAI THICH CACH HOAT DONG CUA BO LOC AM THANH

## Tong quan

Trong project nay, chung ta su dung **Butterworth Digital Filter** de loc am thanh. Day la mot trong nhung bo loc tot nhat cho audio processing.

---

## 1. BUTTERWORTH FILTER LA GI?

### Dinh nghia
**Butterworth filter** la mot loai bo loc dien tu co:
- **Dap ung tan so phang** (flat frequency response) trong passband
- **Khong ripple** (song song) trong passband
- **Attenuation don dieu** (smooth rolloff) ngoai passband

### Tai sao chon Butterworth?
```
So sanh cac loai filter:

┌─────────────┬──────────┬──────────┬──────────┐
│ Loai filter │ Passband │ Rolloff  │ Phase    │
├─────────────┼──────────┼──────────┼──────────┤
│ Butterworth │ ⭐⭐⭐     │ ⭐⭐      │ ⭐⭐⭐     │ ← CHON
│ Chebyshev   │ ⭐⭐      │ ⭐⭐⭐     │ ⭐        │
│ Elliptic    │ ⭐        │ ⭐⭐⭐     │ ⭐        │
│ Bessel      │ ⭐⭐⭐     │ ⭐        │ ⭐⭐⭐     │
└─────────────┴──────────┴──────────┴──────────┘

✓ Butterworth: Can bang tot nhat cho audio
```

---

## 2. BANDPASS FILTER 600-3000 Hz

### Code thuc te da su dung:

```python
from scipy import signal

def apply_bandpass_600_3000(audio_data, sample_rate=16000, order=5):
    # Buoc 1: Tinh Nyquist frequency
    nyquist = sample_rate / 2  # = 8000 Hz
    
    # Buoc 2: Normalize cutoff frequencies
    low = 600 / nyquist   # = 600/8000 = 0.075
    high = 3000 / nyquist # = 3000/8000 = 0.375
    
    # Buoc 3: Thiet ke bo loc Butterworth
    b, a = signal.butter(order, [low, high], btype='band')
    
    # Buoc 4: Ap dung bo loc (zero-phase)
    filtered_data = signal.filtfilt(b, a, audio_data)
    
    return filtered_data
```

### Giai thich tung buoc:

#### **Buoc 1: Tinh Nyquist Frequency**
```
Nyquist Frequency = Sample Rate / 2

Vi du voi file cua ban:
Sample Rate = 16,000 Hz
Nyquist = 16,000 / 2 = 8,000 Hz
```

**Tai sao chia 2?**
- Theo **Nyquist-Shannon Theorem**: De ghi am tan so f, can sample rate >= 2f
- Tan so max co the bieu dien = Sample Rate / 2

#### **Buoc 2: Normalize Cutoff Frequencies**
```
Normalized Frequency = Cutoff / Nyquist

Low cutoff:  600 / 8000 = 0.075  (7.5%)
High cutoff: 3000 / 8000 = 0.375 (37.5%)
```

**Tai sao normalize?**
- Digital filter can tan so trong khoang [0, 1]
- 0 = DC (0 Hz)
- 1 = Nyquist (8000 Hz)

#### **Buoc 3: Thiet ke Filter (butter)**
```python
b, a = signal.butter(5, [0.075, 0.375], btype='band')
```

**Parameters:**
- `order=5`: Do bac cua filter (cao hon = sac hon)
- `[0.075, 0.375]`: Dai tan so mong muon
- `btype='band'`: Bandpass filter

**Output:**
- `b`: Numerator coefficients (tu so)
- `a`: Denominator coefficients (mau so)

**Transfer function:**
```
         b[0] + b[1]*z^-1 + b[2]*z^-2 + ...
H(z) = ────────────────────────────────────
         a[0] + a[1]*z^-1 + a[2]*z^-2 + ...
```

#### **Buoc 4: Ap dung Filter (filtfilt)**
```python
filtered = signal.filtfilt(b, a, audio)
```

**Tai sao dung filtfilt?**
```
filter():   Forward pass only
           → Phase distortion ✗

filtfilt(): Forward + Backward pass
           → Zero phase distortion ✓
```

**Cach hoat dong filtfilt:**
```
1. Filter forward  →  [audio] → [filtered_forward]
2. Reverse         →  [filtered_forward] → [reversed]
3. Filter again    →  [reversed] → [filtered_backward]
4. Reverse again   →  [filtered_backward] → [final]

Ket qua: Phase shift = 0!
```

---

## 3. CACH FILTER HOAT DONG

### Frequency Response cua Bandpass 600-3000 Hz:

```
Magnitude (dB)
    0 ├─────────────────┬───────────────┬─────────────
      │                 │               │
  -10 │                 │               │
      │                ╱│╲              │
  -20 │              ╱  │  ╲            │
      │            ╱    │    ╲          │
  -30 │          ╱      │      ╲        │
      │        ╱        │        ╲      │
  -40 │      ╱          │          ╲    │
      │    ╱            │            ╲  │
  -50 │  ╱              │              ╲│
      │╱                │                ╲
  -60 ├─────────────────┴───────────────┴──────────
      0     300    600     1500    3000    5000   8000
                    ↑  Passband  ↑
                    
Giai thich:
- < 600 Hz:  Bi loai bo (attenuated)
- 600-3000 Hz: Duoc giu lai (passed)
- > 3000 Hz: Bi loai bo (attenuated)
```

### Vi du cu the:

**Input signal co nhieu tan so:**
```
Tan so    | Amplitude | Sau khi loc
----------|-----------|-------------
50 Hz     | 1000      | ~0        (Hum dien - loai bo)
100 Hz    | 500       | ~0        (Nhieu thap - loai bo)
800 Hz    | 2000      | 2000      (Giong noi - giu lai)
1500 Hz   | 3000      | 3000      (Giong noi - giu lai)
2500 Hz   | 2500      | 2500      (Giong noi - giu lai)
5000 Hz   | 800       | ~0        (Nhieu cao - loai bo)
8000 Hz   | 300       | ~0        (Nhieu cao - loai bo)
```

---

## 4. FILTER ORDER (DO BAC)

### Order = 5 nghia la gi?

**Order** xac dinh do sac cua filter:

```
Order 2:  Rolloff = 12 dB/octave (nhe)
Order 3:  Rolloff = 18 dB/octave
Order 5:  Rolloff = 30 dB/octave ← CHON
Order 10: Rolloff = 60 dB/octave (sac)
```

### So sanh cac order:

```
Magnitude (dB)
    0 ├──────────────────────────────
      │        Order 2 (nhe)
  -20 │         ╲
      │          ╲   Order 5 (trung binh)
  -40 │           ╲   ╲
      │            ╲   ╲  Order 10 (sac)
  -60 │             ╲   ╲  ╲
      │              ╲   ╲  ╲
  -80 │               ╲   ╲  ╲
      └────────────────────────────► Frequency
                    600 Hz (cutoff)

Order cao → Rolloff sac → Loai bo tot hon
Nhung: Order qua cao → Computational cost cao
       Order = 5 → Can bang tot!
```

---

## 5. CAC LOAI FILTER KHAC

### A. HIGHPASS FILTER (> 300 Hz)

```python
def apply_highpass_300(audio_data, sample_rate=16000, order=5):
    nyquist = sample_rate / 2
    cutoff = 300 / nyquist  # = 0.0375
    
    b, a = signal.butter(order, cutoff, btype='high')
    filtered = signal.filtfilt(b, a, audio_data)
    
    return filtered
```

**Frequency Response:**
```
Magnitude
    0 ├──────────────────┬─────────────────
      │                  │
  -20 │                ╱ │
      │              ╱   │
  -40 │            ╱     │  Passband
      │          ╱       │  (giu lai)
  -60 │        ╱         │
      │      ╱           │
  -80 │    ╱ Stopband    │
      │  ╱  (loai bo)    │
      ├──────────────────┴─────────────────
      0       300               8000 Hz
              ↑ Cutoff
```

### B. LOWPASS FILTER (< 5000 Hz)

```python
def apply_lowpass_5000(audio_data, sample_rate=16000, order=5):
    nyquist = sample_rate / 2
    cutoff = 5000 / nyquist  # = 0.625
    
    b, a = signal.butter(order, cutoff, btype='low')
    filtered = signal.filtfilt(b, a, audio_data)
    
    return filtered
```

**Frequency Response:**
```
Magnitude
    0 ├─────────────┬────────────────────
      │  Passband   │
      │  (giu lai)  │
  -20 │             │╲
      │             │ ╲
  -40 │             │  ╲
      │             │   ╲  Stopband
  -60 │             │    ╲ (loai bo)
      │             │     ╲
  -80 │             │      ╲
      │             │       ╲
      ├─────────────┴────────────────────
      0           5000            8000 Hz
                   ↑ Cutoff
```

### C. NOTCH FILTER (50 Hz)

```python
def apply_notch_50hz(audio_data, sample_rate=16000):
    freq = 50.0  # Hz
    Q = 30.0     # Quality factor
    
    nyquist = sample_rate / 2
    normalized_freq = freq / nyquist
    
    b, a = signal.iirnotch(normalized_freq, Q)
    filtered = signal.filtfilt(b, a, audio_data)
    
    return filtered
```

**Frequency Response:**
```
Magnitude
    0 ├────────────────────────────────
      │           ╲│╱  ← Notch (rat hep)
  -20 │            │
      │            │
  -40 │            │   Q = 30
      │            │   (cuc hep, cuc sau)
  -60 │            │
      │            │
      ├────────────┴───────────────────
      0    50                  8000 Hz
           ↑ Target frequency
```

**Q Factor:**
- Q cao (30) → Notch hep, chi loai bo 50 Hz
- Q thap (5) → Notch rong, loai bo ca 40-60 Hz

---

## 6. PHASE RESPONSE (DAP UNG PHA)

### Tai sao phase quan trong?

**Linear phase** = Tat ca tan so bi delay giong nhau
**Non-linear phase** = Cac tan so bi delay khac nhau → Bien dang

### filtfilt() vs filter():

```
Original signal:
    ╱╲    ╱╲    ╱╲
   ╱  ╲  ╱  ╲  ╱  ╲

filter() - Forward only:
      ╱╲    ╱╲    ╱╲
     ╱  ╲  ╱  ╲  ╱  ╲
    → Shifted! (Phase distortion)

filtfilt() - Forward + Backward:
    ╱╲    ╱╲    ╱╲
   ╱  ╲  ╱  ╲  ╱  ╲
    → Not shifted! (Zero phase)
```

**Ket luan:** filtfilt() quan trong cho audio de tranh bien dang!

---

## 7. IMPLEMENTATION DETAILS

### Normalization sau khi loc:

```python
def normalize_audio(audio_data, target_level=0.9):
    """Normalize ve muc am thanh mong muon"""
    max_val = np.max(np.abs(audio_data))
    
    if max_val > 0:
        # 16-bit range: -32768 to +32767
        normalized = audio_data * (target_level * 32767 / max_val)
        return normalized.astype(np.int16)
    
    return audio_data.astype(np.int16)
```

**Giai thich:**
```
1. Tim max amplitude:     max_val = 25000
2. Tinh scale factor:     scale = 0.9 * 32767 / 25000 = 1.18
3. Scale audio:           audio * 1.18
4. Convert to int16:      astype(np.int16)

Ket qua: Max amplitude = 0.9 * 32767 = 29490 (90%)
         → Con 10% headroom, tranh clipping
```

---

## 8. PROCESSING PIPELINE

### Toan bo quy trinh loc am thanh:

```
┌─────────────────┐
│ Original Audio  │
│ -32768 to 32767 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Read PCM File   │ ← Buoc 1: Doc file
│ Skip 2 bytes    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Convert to      │ ← Buoc 2: Chuyen sang float
│ Float64 array   │    (de tinh toan chinh xac)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Design Filter   │ ← Buoc 3: Thiet ke filter
│ butter(5, ...)  │    - Order = 5
└────────┬────────┘    - Cutoffs = 600, 3000 Hz
         │
         ▼
┌─────────────────┐
│ Apply Filter    │ ← Buoc 4: Ap dung filter
│ filtfilt(b,a,..)│    - Zero-phase
└────────┬────────┘    - Forward + Backward
         │
         ▼
┌─────────────────┐
│ Normalize       │ ← Buoc 5: Normalize
│ to 90% max      │    - Tranh clipping
└────────┬────────┘    - Target = 0.9 * 32767
         │
         ▼
┌─────────────────┐
│ Convert to      │ ← Buoc 6: Chuyen ve int16
│ Int16 array     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save to WAV     │ ← Buoc 7: Luu file
│ 16-bit PCM      │
└─────────────────┘
```

---

## 9. PERFORMANCE & QUALITY

### Computational Complexity:

```
Time complexity: O(n * order)
n = so luong samples
order = do bac filter (5)

Vi du voi file cua ban:
n = 295,423 samples
order = 5
Thoi gian xu ly: ~0.5 giay / channel (tren may trung binh)
```

### Quality Metrics:

```
Passband ripple:   < 0.1 dB    (rat phang)
Stopband attenuation: > 40 dB  (loai bo tot)
Phase distortion:  0°          (zero-phase)
Group delay:       0 samples   (no delay)
```

---

## 10. SO SANH KET QUA

### Truoc khi loc (Original):

```
Frequency Content:
┌─────────────────────────────────────┐
│ 0-300 Hz:   Hum, noise  ████░░░░░  │
│ 300-600 Hz: Bass, noise ██████░░░  │
│ 600-3000 Hz: Voice     ██████████  │ ← Giong noi
│ 3000-8000 Hz: Noise    ████░░░░░░  │
└─────────────────────────────────────┘
```

### Sau khi loc (Bandpass 600-3000 Hz):

```
Frequency Content:
┌─────────────────────────────────────┐
│ 0-300 Hz:   Removed    ░░░░░░░░░░  │ ← Loai bo
│ 300-600 Hz: Removed    ░░░░░░░░░░  │ ← Loai bo
│ 600-3000 Hz: Voice     ██████████  │ ← GIU LAI
│ 3000-8000 Hz: Removed  ░░░░░░░░░░  │ ← Loai bo
└─────────────────────────────────────┘

Ket qua: Giong noi ro rang hon, it nhieu hon!
```

---

## 11. CODE EXAMPLE - DAY DU

```python
import numpy as np
from scipy import signal
import wave

def complete_filter_pipeline(input_file, output_file):
    """Pipeline day du de loc audio"""
    
    # 1. Doc file PCM
    with open(input_file, 'rb') as f:
        f.seek(2)  # Skip 2 bytes
        raw_data = f.read()
    
    # 2. Convert to numpy array
    samples = np.frombuffer(raw_data, dtype=np.int16)
    audio_float = samples.astype(np.float64)
    
    # 3. Thiet ke Butterworth bandpass filter
    sample_rate = 16000
    nyquist = sample_rate / 2
    low = 600 / nyquist
    high = 3000 / nyquist
    order = 5
    
    b, a = signal.butter(order, [low, high], btype='band')
    
    # 4. Ap dung filter (zero-phase)
    filtered = signal.filtfilt(b, a, audio_float)
    
    # 5. Normalize
    max_val = np.max(np.abs(filtered))
    if max_val > 0:
        normalized = filtered * (0.9 * 32767 / max_val)
    else:
        normalized = filtered
    
    # 6. Convert to int16
    audio_int16 = normalized.astype(np.int16)
    
    # 7. Save to WAV
    with wave.open(output_file, 'wb') as wav:
        wav.setnchannels(1)      # Mono
        wav.setsampwidth(2)       # 16-bit
        wav.setframerate(16000)   # 16 kHz
        wav.writeframes(audio_int16.tobytes())
    
    print(f"Filtered audio saved to {output_file}")
    
    return audio_int16

# Su dung:
filtered_audio = complete_filter_pipeline(
    'audio/original_8channels.pcm',
    'audio/filtered_output.wav'
)
```

---

## 12. TOM TAT

### Cac thanh phan chinh:

1. **Butterworth Filter**: Loai filter duoc chon
   - Passband phang
   - Rolloff don dieu
   - Phu hop cho audio

2. **Order = 5**: Do sac vua phai
   - Rolloff 30 dB/octave
   - Can bang giua hieu qua va computational cost

3. **Bandpass 600-3000 Hz**: Dai tan so toi uu
   - Loai bo hum (< 600 Hz)
   - Giu giong noi (600-3000 Hz)
   - Loai bo nhieu cao (> 3000 Hz)

4. **filtfilt()**: Zero-phase filtering
   - Forward + Backward pass
   - Khong lam sai pha
   - Quan trong cho audio

5. **Normalization**: Tranh clipping
   - Target = 90% max
   - Con 10% headroom

---

## KET LUAN

Bo loc am thanh hoat dong qua **5 buoc chinh**:

1. ✅ **Doc audio** → Convert sang float
2. ✅ **Thiet ke filter** → Butterworth coefficients
3. ✅ **Ap dung filter** → filtfilt (zero-phase)
4. ✅ **Normalize** → 90% max amplitude
5. ✅ **Luu ket qua** → Int16 WAV file

**Ket qua:** Audio sach hon, giong noi ro rang hon, phu hop cho speech recognition!

