#include "core/gcc_phat.h"

#include <algorithm>
#include <cmath>

namespace rb {

GCCPHAT::GCCPHAT() = default;

static void naiveDFT(const std::vector<double>& inReal,
                     std::vector<std::complex<double>>& out,
                     bool inverse) {
    const size_t N = inReal.size();
    out.assign(N, {});
    const double sign = inverse ? 1.0 : -1.0;
    for (size_t k = 0; k < N; ++k) {
        std::complex<double> sum(0.0, 0.0);
        for (size_t n = 0; n < N; ++n) {
            double angle = 2.0 * M_PI * k * n / static_cast<double>(N);
            std::complex<double> w(std::cos(angle), sign * std::sin(angle));
            sum += inReal[n] * w;
        }
        out[k] = sum;
    }
    if (inverse) {
        for (auto& v : out) v /= static_cast<double>(N);
    }
}

static void naiveIDFTMag(const std::vector<std::complex<double>>& in,
                         std::vector<double>& out) {
    const size_t N = in.size();
    out.assign(N, 0.0);
    for (size_t n = 0; n < N; ++n) {
        std::complex<double> sum(0.0, 0.0);
        for (size_t k = 0; k < N; ++k) {
            double angle = 2.0 * M_PI * k * n / static_cast<double>(N);
            std::complex<double> w(std::cos(angle), std::sin(angle));
            sum += in[k] * w;
        }
        out[n] = std::abs(sum) / static_cast<double>(N);
    }
}

double GCCPHAT::findDelay(const std::vector<double>& signal1,
                          const std::vector<double>& signal2,
                          int maxDelaySamples) const {
    const size_t N = std::min(signal1.size(), signal2.size());
    if (N == 0) return 0.0;

    std::vector<std::complex<double>> S1, S2;
    naiveDFT(signal1, S1, false);
    naiveDFT(signal2, S2, false);

    std::vector<std::complex<double>> R(S1.size());
    for (size_t i = 0; i < S1.size(); ++i) {
        std::complex<double> val = S1[i] * std::conj(S2[i]);
        double mag = std::abs(val);
        if (mag > 1e-10) val /= mag;
        R[i] = val;
    }

    std::vector<double> r;
    naiveIDFTMag(R, r);

    int center = static_cast<int>(N / 2);
    int bestIdx = center;
    double bestVal = -1.0;
    for (int d = -maxDelaySamples; d <= maxDelaySamples; ++d) {
        int idx = (center + d + static_cast<int>(N)) % static_cast<int>(N);
        double v = r[idx];
        if (v > bestVal) {
            bestVal = v;
            bestIdx = idx;
        }
    }

    int delay = bestIdx - center;
    return static_cast<double>(delay);
}

} // namespace rb


