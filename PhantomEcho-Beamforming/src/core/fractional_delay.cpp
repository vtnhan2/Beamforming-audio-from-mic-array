#include "core/fractional_delay.h"

#include <algorithm>

namespace rb {

std::vector<double> FractionalDelay::applyDelay(const std::vector<double>& signal,
                                                double delaySamples) const {
    const size_t N = signal.size();
    std::vector<double> out(N, 0.0);
    if (N == 0) return out;

    for (size_t i = 0; i < N; ++i) {
        double srcIdx = static_cast<double>(i) - delaySamples;
        if (srcIdx <= 0.0) {
            out[i] = signal.front();
        } else if (srcIdx >= static_cast<double>(N - 1)) {
            out[i] = signal.back();
        } else {
            size_t idx0 = static_cast<size_t>(srcIdx);
            size_t idx1 = idx0 + 1;
            double frac = srcIdx - static_cast<double>(idx0);
            out[i] = (1.0 - frac) * signal[idx0] + frac * signal[idx1];
        }
    }

    return out;
}

} // namespace rb


