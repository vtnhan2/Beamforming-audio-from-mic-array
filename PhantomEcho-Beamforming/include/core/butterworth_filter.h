#pragma once

#include <vector>

namespace rb {

class ButterworthFilter {
public:
    void designBandpass(double lowcutHz, double highcutHz, double sampleRate, int order = 4);
    std::vector<double> filtfilt(const std::vector<double>& signal) const;

private:
    std::vector<double> bCoeffs;
    std::vector<double> aCoeffs;
};

} // namespace rb


