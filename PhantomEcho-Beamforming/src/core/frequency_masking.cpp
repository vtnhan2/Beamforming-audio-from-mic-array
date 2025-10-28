#include "core/frequency_masking.h"

#include <algorithm>
#include <cmath>
#include <complex>

namespace rb {

// --------------------------
// Minimal fallback STFT/ISTFT
// --------------------------
static void hannWindow(size_t N, std::vector<double>& w) {
    w.resize(N);
    for (size_t n = 0; n < N; ++n) {
        w[n] = 0.5 * (1.0 - std::cos(2.0 * M_PI * static_cast<double>(n) / static_cast<double>(N - 1)));
    }
}

static void dftRealToComplex(const std::vector<double>& x,
                             std::vector<std::complex<double>>& X) {
    const size_t N = x.size();
    X.assign(N, {});
    for (size_t k = 0; k < N; ++k) {
        std::complex<double> sum(0.0, 0.0);
        for (size_t n = 0; n < N; ++n) {
            double ang = -2.0 * M_PI * static_cast<double>(k) * static_cast<double>(n) / static_cast<double>(N);
            std::complex<double> w(std::cos(ang), std::sin(ang));
            sum += x[n] * w;
        }
        X[k] = sum;
    }
}

static void idftComplexToReal(const std::vector<std::complex<double>>& X,
                              std::vector<double>& x) {
    const size_t N = X.size();
    x.assign(N, 0.0);
    for (size_t n = 0; n < N; ++n) {
        std::complex<double> sum(0.0, 0.0);
        for (size_t k = 0; k < N; ++k) {
            double ang = 2.0 * M_PI * static_cast<double>(k) * static_cast<double>(n) / static_cast<double>(N);
            std::complex<double> w(std::cos(ang), std::sin(ang));
            sum += X[k] * w;
        }
        x[n] = (sum.real()) / static_cast<double>(N);
    }
}

static size_t hzToBin(double hz, double sampleRate, size_t fftSize) {
    double bin = hz * static_cast<double>(fftSize) / sampleRate;
    if (bin < 0.0) bin = 0.0;
    size_t b = static_cast<size_t>(std::floor(bin + 0.5));
    if (b >= fftSize) b = fftSize - 1;
    return b;
}

// Fallback masking implementation (O(N*M)) intended for correctness over speed.
static std::vector<double> maskWithFallbackSTFT(const std::vector<double>& signal,
                                                const std::vector<double>& reference,
                                                double sampleRate,
                                                double lowFreq,
                                                double highFreq) {
    const size_t nperseg = 512;
    const size_t hop = nperseg / 2; // 50% overlap
    const size_t N = signal.size();
    if (N == 0) return {};

    // Prepare window
    std::vector<double> win;
    hannWindow(nperseg, win);

    // Output buffer (overlap-add)
    std::vector<double> out(N, 0.0);
    std::vector<double> norm(N, 0.0);

    // Frequency range bins
    const size_t binLow = hzToBin(lowFreq, sampleRate, nperseg);
    const size_t binHigh = hzToBin(highFreq, sampleRate, nperseg);

    // Process frames
    for (size_t start = 0; start + nperseg <= N; start += hop) {
        // Windowed frames
        std::vector<double> frameS(nperseg), frameR(nperseg);
        for (size_t i = 0; i < nperseg; ++i) {
            frameS[i] = signal[start + i] * win[i];
            frameR[i] = reference[start + i] * win[i];
        }

        // DFT
        std::vector<std::complex<double>> XS, XR;
        dftRealToComplex(frameS, XS);
        dftRealToComplex(frameR, XR);

        // Create mask from reference magnitude
        double maxMag = 0.0;
        for (size_t k = 0; k < nperseg; ++k) {
            double m = std::abs(XR[k]);
            if (m > maxMag) maxMag = m;
        }
        const double eps = 1e-10;

        for (size_t k = 0; k < nperseg; ++k) {
            double mask = 0.0;
            if (k >= binLow && k <= binHigh) {
                mask = (maxMag > eps) ? (std::abs(XR[k]) / (maxMag + eps)) : 0.0;
            }
            XS[k] *= mask; // apply mask
        }

        // Inverse DFT and overlap-add
        std::vector<double> y;
        idftComplexToReal(XS, y);
        for (size_t i = 0; i < nperseg; ++i) {
            out[start + i] += y[i] * win[i];
            norm[start + i] += win[i] * win[i];
        }
    }

    // Normalize overlap-add
    for (size_t i = 0; i < N; ++i) {
        if (norm[i] > 1e-12) out[i] /= norm[i];
    }
    return out;
}

std::vector<double> FrequencyMasking::applyMasking(const std::vector<double>& signal,
                                                   const std::vector<double>& reference,
                                                   double sampleRate,
                                                   double lowFreq,
                                                   double highFreq) const {
    // Optional backends can be wired here when available.
#ifdef HAS_ESSENTIA
    // TODO: Integrate Essentia STFT/ISTFT here.
    return maskWithFallbackSTFT(signal, reference, sampleRate, lowFreq, highFreq);
#elif defined(HAS_AQUILA)
    // TODO: Integrate Aquila STFT/ISTFT here.
    return maskWithFallbackSTFT(signal, reference, sampleRate, lowFreq, highFreq);
#else
    // Fallback portable STFT/ISTFT implementation
    return maskWithFallbackSTFT(signal, reference, sampleRate, lowFreq, highFreq);
#endif
}

} // namespace rb


