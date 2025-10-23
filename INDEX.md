# 📚 ODAS Audio Processing - Documentation Index

## 🎯 Quick Navigation

### 🚀 Start Here
- **[README_COMPLETE.md](README_COMPLETE.md)** - 📖 Complete guide (RECOMMENDED START)

### 🎵 Processing Scripts

#### Best Quality (Recommended) ⭐
- **[combined_processing.py](combined_processing.py)** - Beamforming + Filtering
  - Output: `audio/combined_processing/step2_filtered.wav` 🎵

#### Individual Techniques
- **[beamforming.py](beamforming.py)** - Spatial filtering (direction-based)
- **[reference_beamforming.py](reference_beamforming.py)** - 🎯 Vocal extraction (reference-based)
- **[filter_bandpass_600_3000.py](filter_bandpass_600_3000.py)** - Frequency filtering
- **[audio_source_localization.py](audio_source_localization.py)** - 3D localization

#### Analysis Tools
- **[analyze_audio.py](analyze_audio.py)** - Channel analysis
- **[analyze_amplitude.py](analyze_amplitude.py)** - Amplitude/clipping detection
- **[visualize_filter_response.py](visualize_filter_response.py)** - Filter visualization

---

## 📚 Documentation

### Main Guides
| Document | Topic | When to Read |
|----------|-------|-------------|
| **[README_COMPLETE.md](README_COMPLETE.md)** | Complete overview | 🔰 Start here |
| **[BEAMFORMING_GUIDE.md](BEAMFORMING_GUIDE.md)** | Beamforming chi tiết | When using beamforming |
| **[REFERENCE_BEAMFORMING_GUIDE.md](REFERENCE_BEAMFORMING_GUIDE.md)** | 🎯 Vocal extraction | Tách 1 vocal cụ thể |
| **[FILTER_EXPLANATION.md](FILTER_EXPLANATION.md)** | Filtering principles | When using filtering |
| **[AUDIO_PROCESSING_COMPARISON.md](AUDIO_PROCESSING_COMPARISON.md)** | So sánh kỹ thuật | Understanding tradeoffs |

### Specific Topics
| Document | Topic | When to Read |
|----------|-------|-------------|
| **[README_localization.md](README_localization.md)** | TDOA localization | Finding sound sources |
| **[README_audio_filtering.md](README_audio_filtering.md)** | Filter types | Choosing filters |
| **[QUICK_START_FILTERING.md](QUICK_START_FILTERING.md)** | Quick reference | Fast lookup |
| **[GIAI_THICH_REFERENCE_BEAMFORMING.md](GIAI_THICH_REFERENCE_BEAMFORMING.md)** | 🇻🇳 Giải thích chi tiết (Tiếng Việt) | Hiểu algorithm từng bước |

---

## 🎵 Output Files

### Best Audio Quality

**For general speech enhancement:**
```
audio/combined_processing/
└── step2_filtered.wav ⭐⭐⭐⭐⭐
    (Beamforming + Bandpass 600-3000 Hz)
```

**For extracting specific vocal (e.g., Channel 5):**
```
audio/reference_beamforming/
└── vocal_extracted_combined.wav 🎯⭐⭐⭐⭐⭐
    (Reference-based Beamforming + Masking + Filtering)
```

### Comparison Files
```
audio/combined_processing/
├── comparison_omnidirectional.wav        (Baseline)
├── comparison_omnidirectional_filtered.wav  (Filter only)
├── step1_beamformed.wav                 (Beamforming only)
└── step2_filtered.wav                   (Combined ⭐)
```

### Visualizations
```
audio/combined_processing/
├── processing_comparison.png            (3-step comparison)
└── filter_comparison.png                (Filter effects)
```

---

## 🔍 Quick Reference

### Run Scripts

```bash
# Best Quality (Recommended)
python combined_processing.py

# Vocal Extraction (from specific channel)
python reference_beamforming.py  # 🎯 Extract vocal from Channel 5

# Individual Techniques
python beamforming.py
python filter_bandpass_600_3000.py
python audio_source_localization.py

# Analysis
python analyze_audio.py
python analyze_amplitude.py
```

### Key Results

| Analysis | Result |
|----------|--------|
| **Peak Direction** | 53.2° (beamforming) |
| **Active Channels** | 1, 2, 3, 4, 5, 8 |
| **Silent Channels** | 6, 7 |
| **Clipping** | Channel 4 (min: -32768) |
| **Best Filter** | Bandpass 600-3000 Hz |
| **Duration** | 18.46 seconds |

---

## 📊 Visualizations

### Beamforming
- `audio/beamforming/beam_pattern_polar.png` - Polar pattern
- `audio/beamforming/beam_pattern_cartesian.png` - Cartesian plot

### Combined Processing
- `audio/combined_processing/processing_comparison.png` - Processing steps
- `audio/combined_processing/filter_comparison.png` - Filter comparison

### Filter Response
- `filter_frequency_response.png` - Frequency responses
- `filter_order_comparison.png` - Order effects
- `filtfilt_vs_filter_comparison.png` - Phase comparison
- `filter_effect_on_signal.png` - Time/frequency effects

### Amplitude Analysis
- `audio/amplitude_analysis/amplitude_distribution.png` - Histograms
- `audio/amplitude_analysis/amplitude_comparison.png` - Box plots
- `audio/amplitude_analysis/amplitude_summary_table.png` - Summary table

---

## 🎓 Learning Path

### Beginner
1. Read [README_COMPLETE.md](README_COMPLETE.md)
2. Run `python analyze_audio.py`
3. Run `python combined_processing.py`
4. Listen to output files
5. Compare visualizations

### Intermediate
1. Read [BEAMFORMING_GUIDE.md](BEAMFORMING_GUIDE.md)
2. Read [FILTER_EXPLANATION.md](FILTER_EXPLANATION.md)
3. Experiment with parameters
4. Try individual scripts
5. Read [AUDIO_PROCESSING_COMPARISON.md](AUDIO_PROCESSING_COMPARISON.md)

### Advanced
1. Study ODAS C implementation
2. Implement MVDR beamforming
3. Add adaptive filtering
4. Optimize for real-time
5. Multi-source separation

---

## 🔧 Technical Details

### Input
- **File:** `audio/original_8channels.pcm`
- **Format:** 16-bit signed PCM, 16 kHz, 8 channels
- **Duration:** 18.46 seconds

### Microphone Array
- **Type:** Circular array (6 active mics)
- **Radius:** 5 cm
- **Channels:** 1, 2, 3, 4, 5, 8

### Algorithms
- **Beamforming:** Delay-and-Sum (time domain)
- **Filtering:** Butterworth bandpass, order 4
- **Localization:** TDOA + Least Squares

---

## 🎯 Use Cases

| Application | Recommended Script | Output File |
|-------------|-------------------|-------------|
| **Speech Recognition** | `combined_processing.py` | `step2_filtered.wav` |
| **Voice Commands** | `beamforming.py` | `beamformed_peak.wav` |
| **Noise Reduction** | `combined_processing.py` | `step2_filtered.wav` |
| **Speaker Localization** | `audio_source_localization.py` | Console output |
| **Audio Analysis** | `analyze_audio.py` | `audio_analysis_result.json` |

---

## ❓ FAQ

### Q: Tôi nên bắt đầu từ đâu?
**A:** Đọc [README_COMPLETE.md](README_COMPLETE.md) và chạy `python combined_processing.py`

### Q: File audio tốt nhất là gì?
**A:** `audio/combined_processing/step2_filtered.wav` ⭐

### Q: Tài liệu nào giải thích beamforming?
**A:** [BEAMFORMING_GUIDE.md](BEAMFORMING_GUIDE.md)

### Q: Tài liệu nào giải thích filtering?
**A:** [FILTER_EXPLANATION.md](FILTER_EXPLANATION.md)

### Q: So sánh các kỹ thuật ở đâu?
**A:** [AUDIO_PROCESSING_COMPARISON.md](AUDIO_PROCESSING_COMPARISON.md)

---

## 📋 Checklist

### Have you...?
- [ ] Read [README_COMPLETE.md](README_COMPLETE.md)?
- [ ] Run `python analyze_audio.py`?
- [ ] Run `python combined_processing.py`?
- [ ] Listened to `step2_filtered.wav`?
- [ ] Compared with `comparison_omnidirectional.wav`?
- [ ] Viewed visualization plots?
- [ ] Understood the processing pipeline?

---

## 🎉 Summary

**You have:**
✅ Complete audio processing pipeline  
✅ Beamforming (spatial filtering)  
✅ Frequency filtering (bandpass, highpass, lowpass, notch)  
✅ Sound source localization (3D)  
✅ Combined processing (best quality)  
✅ Analysis tools  
✅ Comprehensive documentation  

**Best audio:**
🎵 `audio/combined_processing/step2_filtered.wav`

**Start here:**
📖 [README_COMPLETE.md](README_COMPLETE.md)

---

## 📞 Contact

For questions or support:
- 📧 Email: [your-email]
- 🔗 GitHub: [your-github]
- 📚 Docs: This repository

---

**Version:** 1.0  
**Last Updated:** October 21, 2025  
**Author:** AI Assistant

---

## Quick Links

### 📖 Documentation
- [README_COMPLETE.md](README_COMPLETE.md) - Main guide
- [BEAMFORMING_GUIDE.md](BEAMFORMING_GUIDE.md) - Beamforming
- [FILTER_EXPLANATION.md](FILTER_EXPLANATION.md) - Filtering
- [AUDIO_PROCESSING_COMPARISON.md](AUDIO_PROCESSING_COMPARISON.md) - Comparison

### 🐍 Scripts
- [combined_processing.py](combined_processing.py) - ⭐ Best quality
- [beamforming.py](beamforming.py) - Beamforming
- [filter_bandpass_600_3000.py](filter_bandpass_600_3000.py) - Filtering
- [audio_source_localization.py](audio_source_localization.py) - Localization

### 🎵 Best Output
- `audio/combined_processing/step2_filtered.wav` - ⭐⭐⭐⭐⭐

---

**Happy Audio Processing! 🎶**

