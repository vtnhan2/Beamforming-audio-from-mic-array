#pragma once

#include <vector>

namespace rb {

class FrequencyMasking {
public:
    // Apply simple magnitude mask derived from reference STFT.
    // If no STFT backend available, returns input unchanged.
    std::vector<double> applyMasking(const std::vector<double>& signal,
                                     const std::vector<double>& reference,
                                     double sampleRate,
                                     double lowFreq,
                                     double highFreq) const;
};

} // namespace rb


