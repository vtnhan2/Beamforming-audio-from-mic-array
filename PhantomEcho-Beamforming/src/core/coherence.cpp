#include "core/coherence.h"

#include <algorithm>
#include <cmath>

namespace rb {

double CoherenceCalculator::computeCoherence(const std::vector<double>& signal1,
                                             const std::vector<double>& signal2) const {
    const size_t N = std::min(signal1.size(), signal2.size());
    if (N == 0) return 0.0;

    double mean1 = 0.0, mean2 = 0.0;
    for (size_t i = 0; i < N; ++i) {
        mean1 += signal1[i];
        mean2 += signal2[i];
    }
    mean1 /= static_cast<double>(N);
    mean2 /= static_cast<double>(N);

    double num = 0.0, den1 = 0.0, den2 = 0.0;
    for (size_t i = 0; i < N; ++i) {
        const double s1 = signal1[i] - mean1;
        const double s2 = signal2[i] - mean2;
        num += s1 * s2;
        den1 += s1 * s1;
        den2 += s2 * s2;
    }
    const double den = std::sqrt(den1 * den2);
    if (den <= 1e-12) return 0.0;
    return std::abs(num / den);
}

} // namespace rb


