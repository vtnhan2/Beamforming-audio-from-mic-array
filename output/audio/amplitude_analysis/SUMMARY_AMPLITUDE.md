# BAO CAO DAI AMPLITUDE TRONG AUDIO

## Tong quan
Phan tich dai amplitude (bien do) cua audio trong 8 channels cua file `original_8channels.pcm`

**Format:** 16-bit PCM (Signed Integer)  
**Dai gia tri ly thuyet:** -32768 den +32767  
**Duration:** 18.46 giay  

---

## DAI AMPLITUDE CUA TUNG CHANNEL

### Channel 1 (CO AUDIO ✓)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | -20,609 den 22,332 |
| **Peak-to-Peak** | 42,941 |
| **RMS** | 2,943 |
| **Mean** | -1.03 |
| **Median** | -38 |
| **Std Dev** | 2,943 |
| **Dynamic Range** | 17.6 dB |

**Percentiles (|Amplitude|):**
- 50% gia tri < 1,474
- 75% gia tri < 3,003
- 95% gia tri < 6,202
- 99% gia tri < 9,232

---

### Channel 2 (CO AUDIO ✓)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | -25,283 den 27,209 |
| **Peak-to-Peak** | 52,492 |
| **RMS** | 3,475 |
| **Mean** | -1.07 |
| **Median** | -52 |
| **Std Dev** | 3,475 |
| **Dynamic Range** | 17.9 dB |

**Percentiles (|Amplitude|):**
- 50% gia tri < 1,737
- 75% gia tri < 3,538
- 95% gia tri < 7,312
- 99% gia tri < 10,871

---

### Channel 3 (CO AUDIO ✓)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | **-32,768 den 32,767** (FULL RANGE) |
| **Peak-to-Peak** | **65,535** (MAX) |
| **RMS** | 5,627 |
| **Mean** | -1.04 |
| **Median** | -36 |
| **Std Dev** | 5,627 |
| **Dynamic Range** | 15.3 dB |

**Percentiles (|Amplitude|):**
- 50% gia tri < 2,254
- 75% gia tri < 4,971
- 95% gia tri < 12,195
- 99% gia tri < 20,423

⚠️ **Luu y:** Channel nay co clipping (dat gia tri max/min)

---

### Channel 4 (CO AUDIO ✓)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | **-32,768 den 32,767** (FULL RANGE) |
| **Peak-to-Peak** | **65,535** (MAX) |
| **RMS** | 6,411 |
| **Mean** | -0.86 |
| **Median** | -29 |
| **Std Dev** | 6,411 |
| **Dynamic Range** | 14.2 dB |

**Percentiles (|Amplitude|):**
- 50% gia tri < 2,379
- 75% gia tri < 5,428
- 95% gia tri < 14,408
- 99% gia tri < 23,788

⚠️ **Luu y:** Channel nay co clipping (dat gia tri max/min)

---

### Channel 5 (CO AUDIO ✓) ⭐ MANH NHAT
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | **-32,768 den 32,767** (FULL RANGE) |
| **Peak-to-Peak** | **65,535** (MAX) |
| **RMS** | **9,891** (CAO NHAT) |
| **Mean** | 0.45 |
| **Median** | -80 |
| **Std Dev** | 9,891 |
| **Dynamic Range** | 10.4 dB |

**Percentiles (|Amplitude|):**
- 50% gia tri < 3,315
- 75% gia tri < 8,613
- 95% gia tri < 24,438
- 99% gia tri < 32,486

⚠️ **Luu y:** 
- Channel manh nhat (RMS cao nhat)
- Co clipping nghiem trong (99% < 32,486 gan max)
- Bien do lon nhat trong tat ca cac channels

---

### Channel 6 (KHONG CO AUDIO ✗)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | -9 den 9 |
| **Peak-to-Peak** | 18 |
| **RMS** | 1.9 |
| **Mean** | -0.59 |
| **Median** | -1 |
| **Std Dev** | 1.79 |
| **Dynamic Range** | 14.0 dB |

**Nhan xet:** Chi co nhieu nho, khong co tin hieu audio thuc su

---

### Channel 7 (KHONG CO AUDIO ✗)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | -9 den 8 |
| **Peak-to-Peak** | 17 |
| **RMS** | 1.8 |
| **Mean** | -0.59 |
| **Median** | -1 |
| **Std Dev** | 1.71 |
| **Dynamic Range** | 13.4 dB |

**Nhan xet:** Chi co nhieu nho, khong co tin hieu audio thuc su

---

### Channel 8 (CO AUDIO ✓)
| Thong so | Gia tri |
|----------|---------|
| **Dai amplitude** | **-32,768 den 32,767** (FULL RANGE) |
| **Peak-to-Peak** | **65,535** (MAX) |
| **RMS** | 5,081 |
| **Mean** | -1.06 |
| **Median** | -33 |
| **Std Dev** | 5,081 |
| **Dynamic Range** | 16.2 dB |

**Percentiles (|Amplitude|):**
- 50% gia tri < 2,128
- 75% gia tri < 4,581
- 95% gia tri < 11,073
- 99% gia tri < 18,102

⚠️ **Luu y:** Channel nay co clipping (dat gia tri max/min)

---

## SO SANH GIUA CAC CHANNELS

### Xep hang theo RMS (Cong suat)
| Thu hang | Channel | RMS | Chat luong |
|----------|---------|-----|------------|
| 1 🥇 | **Channel 5** | **9,891** | ⭐⭐⭐ Tot nhat |
| 2 🥈 | Channel 4 | 6,411 | ⭐⭐ Manh |
| 3 🥉 | Channel 3 | 5,627 | ⭐⭐ Manh |
| 4 | Channel 8 | 5,081 | ⭐⭐ Trung binh |
| 5 | Channel 2 | 3,475 | ⭐ Yeu |
| 6 | Channel 1 | 2,943 | ⭐ Yeu nhat |
| - | Channel 6 | 1.9 | ✗ Khong co audio |
| - | Channel 7 | 1.8 | ✗ Khong co audio |

### Channels co Clipping
**Channels dat full range (-32768, 32767):**
- ⚠️ Channel 3
- ⚠️ Channel 4
- ⚠️ **Channel 5** (nghiem trong nhat)
- ⚠️ Channel 8

**Y nghia:** Cac channels nay co the bi clip (cat dinh) tai mot so thoi diem, gay mat thong tin va bien dang.

### Channels khong co Clipping
- ✓ Channel 1: Max 22,332 (-31%)
- ✓ Channel 2: Max 27,209 (-17%)

---

## PHAN TICH DYNAMIC RANGE

| Channel | Dynamic Range | Danh gia |
|---------|---------------|----------|
| Channel 2 | 17.9 dB | Tot nhat |
| Channel 1 | 17.6 dB | Tot |
| Channel 8 | 16.2 dB | Trung binh |
| Channel 3 | 15.3 dB | Trung binh |
| Channel 4 | 14.2 dB | Trung binh thap |
| **Channel 5** | **10.4 dB** | **Thap nhat** |

**Giai thich Dynamic Range:**
- Dynamic Range cao = Tin hieu sach, it nhieu
- Dynamic Range thap = Tin hieu manh nhung co nhieu hoac bien dong lon
- Channel 5 co DR thap vi tin hieu qua manh (RMS cao)

---

## PHAN TICH PERCENTILES

### Median Amplitude (50%)
Cho biet 50% cac gia tri nam duoi muc nao:

| Channel | Median (50%) | Y nghia |
|---------|--------------|---------|
| Channel 5 | 3,315 | Bien do trung binh cao nhat |
| Channel 4 | 2,379 | Bien do trung binh cao |
| Channel 3 | 2,254 | Bien do trung binh cao |
| Channel 8 | 2,128 | Bien do trung binh |
| Channel 2 | 1,737 | Bien do trung binh thap |
| Channel 1 | 1,474 | Bien do trung binh thap nhat |

### 95th Percentile (Peaks)
95% gia tri nam duoi muc nao (chi 5% peaks cao hon):

| Channel | 95th % | Y nghia |
|---------|--------|---------|
| Channel 5 | 24,438 | Co nhieu peaks rat cao |
| Channel 4 | 14,408 | Co peaks cao |
| Channel 3 | 12,195 | Co peaks cao |
| Channel 8 | 11,073 | Co peaks trung binh |
| Channel 2 | 7,312 | Peaks thap |
| Channel 1 | 6,202 | Peaks thap nhat |

---

## GOI Y SU DUNG

### Cho Speech Recognition
```
✅ Nen dung: Channel 5
   - RMS cao nhat (9,891)
   - Tin hieu manh nhat
   - Nhung can xu ly clipping

⚠️ Can normalize truoc khi dung
⚠️ Can ap dung bo loc de giam clipping
```

### Cho Audio Analysis
```
✅ Nen dung: Channel 2 hoac Channel 1
   - Khong co clipping
   - Dynamic Range tot
   - Tin hieu sach hon
```

### Cho Multi-channel Processing
```
✅ Nen dung: Tat ca channels co audio (1,2,3,4,5,8)
   - Trung binh de giam clipping
   - Tang SNR
```

---

## CANH BAO VA LUU Y

### ⚠️ Clipping Detection
**Channels co clipping nghiem trong:**
- Channel 5: 99% < 32,486 (gan full range)
- Channel 4: 99% < 23,788
- Channel 3: 99% < 20,423
- Channel 8: 99% < 18,102

**Giai phap:**
1. Giam gain khi recording
2. Su dung compressor/limiter
3. Normalize ve muc thap hon (70-80% thay vi 90%)

### ⚠️ Bit Depth Utilization
**16-bit range:** -32,768 den +32,767

**Channels su dung full range:**
- Channels 3, 4, 5, 8: Dat full range
- Risk: Co the bi clip, mat thong tin

**Channels khong dat full range:**
- Channel 1: Max 22,332 (68% range)
- Channel 2: Max 27,209 (83% range)
- Better: It risk clip hon

---

## KET LUAN

### Channels tot nhat cho cac ung dung:

**Speech Recognition:**
- 🥇 Channel 5 (sau khi normalize)
- 🥈 Channel 4
- 🥉 Channel 3

**Clean Audio (no clipping):**
- 🥇 Channel 2
- 🥈 Channel 1

**Balanced (quality vs power):**
- 🥇 Channel 8
- 🥈 Channel 3

### Tong ket dai amplitude:
- **Channels co audio:** 6/8 (75%)
- **Channels co clipping:** 4/6 (67%)
- **Channel manh nhat:** Channel 5 (RMS: 9,891)
- **Channel sach nhat:** Channel 2 (DR: 17.9 dB)
- **Dai amplitude:** Rat da dang, tu -32,768 den +32,767

---

## FILES DA TAO

1. **amplitude_distribution.png** - Histogram va box plot tung channel
2. **amplitude_comparison.png** - So sanh RMS va phan bo giua cac channels  
3. **amplitude_summary_table.png** - Bang tom tat cac thong so
4. **amplitude_analysis.txt** - Bao cao chi tiet text format
5. **SUMMARY_AMPLITUDE.md** - Tai lieu nay

**Thu muc:** `audio/amplitude_analysis/`

