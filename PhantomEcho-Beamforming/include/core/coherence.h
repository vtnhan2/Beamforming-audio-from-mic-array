#pragma once

#include <vector>

namespace rb {

class CoherenceCalculator {
public:
    double computeCoherence(const std::vector<double>& signal1,
                            const std::vector<double>& signal2) const;
};

} // namespace rb


