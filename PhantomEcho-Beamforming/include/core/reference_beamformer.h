#pragma once

#include <vector>

namespace rb {

struct BeamformingResult {
    std::vector<double> extractedVocal;
    std::vector<double> delays;
    std::vector<double> coherences;
    std::vector<double> weights;
};

class ReferenceBeamformer {
public:
    ReferenceBeamformer(double sampleRate = 16000.0);

    BeamformingResult extractVocalFromReference(
        const std::vector<std::vector<double>>& audioData,
        int referenceChannelIdx = 4,
        double coherenceThreshold = 0.3) const;

private:
    double sampleRate;
};

} // namespace rb


