#pragma once

#include <vector>

namespace rb {

class FractionalDelay {
public:
    std::vector<double> applyDelay(const std::vector<double>& signal,
                                   double delaySamples) const;
};

} // namespace rb


