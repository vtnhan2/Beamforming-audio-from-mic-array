#pragma once

#include <vector>

namespace rb {

class GCCPHAT {
public:
    explicit GCCPHAT();
    double findDelay(const std::vector<double>& signal1,
                     const std::vector<double>& signal2,
                     int maxDelaySamples = 100) const;
};

} // namespace rb


