#include "core/PhantomEcho.h"

#include "core/gcc_phat.h"
#include "core/coherence.h"
#include "core/fractional_delay.h"
#include "core/frequency_masking.h"

#include <algorithm>
#include <numeric>

namespace rb {

ReferenceBeamformer::ReferenceBeamformer(double sampleRate)
    : sampleRate(sampleRate) {}

BeamformingResult ReferenceBeamformer::extractVocalFromReference(
    const std::vector<std::vector<double>>& audioData,
    int referenceChannelIdx,
    double coherenceThreshold) const {

    const size_t nMics = audioData.size();
    if (nMics == 0) return {};
    const size_t nSamples = audioData[0].size();

    GCCPHAT gcc;
    CoherenceCalculator coh;
    FractionalDelay delayer;
    FrequencyMasking masker;

    std::vector<double> delays(nMics, 0.0);
    std::vector<double> coherences(nMics, 0.0);

    const std::vector<double>& reference = audioData[referenceChannelIdx];

    for (size_t i = 0; i < nMics; ++i) {
        if (static_cast<int>(i) == referenceChannelIdx) {
            delays[i] = 0.0;
            coherences[i] = 1.0;
        } else {
            double d = gcc.findDelay(reference, audioData[i], 100);
            delays[i] = d;
            auto aligned = delayer.applyDelay(audioData[i], -d);
            coherences[i] = coh.computeCoherence(reference, aligned);
        }
    }

    std::vector<double> weights(nMics, 0.0);
    for (size_t i = 0; i < nMics; ++i) {
        weights[i] = (coherences[i] > coherenceThreshold) ? coherences[i] : 0.0;
    }

    double sumw = std::accumulate(weights.begin(), weights.end(), 0.0);
    if (sumw <= 1e-12) {
        weights.assign(nMics, 0.0);
        weights[referenceChannelIdx] = 1.0;
        sumw = 1.0;
    }
    for (auto& w : weights) w /= sumw;

    std::vector<double> output(nSamples, 0.0);
    for (size_t i = 0; i < nMics; ++i) {
        if (weights[i] <= 0.0) continue;
        auto aligned = delayer.applyDelay(audioData[i], -delays[i]);
        for (size_t n = 0; n < nSamples; ++n) {
            output[n] += weights[i] * aligned[n];
        }
    }

    auto masked = masker.applyMasking(output, reference, sampleRate, 300.0, 3000.0);

    BeamformingResult res;
    res.extractedVocal = std::move(masked);
    res.delays = std::move(delays);
    res.coherences = std::move(coherences);
    res.weights = std::move(weights);
    return res;
}

} // namespace rb


