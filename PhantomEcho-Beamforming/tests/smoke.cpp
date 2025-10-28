#include "core/reference_beamformer.h"

#include <iostream>

int main() {
    rb::ReferenceBeamformer bf(16000.0);
    std::vector<std::vector<double>> audio(3, std::vector<double>(512, 0.0));
    // Simple impulse on reference channel
    audio[1][100] = 1.0;
    // Shifted versions
    audio[0][98] = 0.7;
    audio[2][103] = 0.5;

    auto res = bf.extractVocalFromReference(audio, 1, 0.1);
    std::cout << "delays: ";
    for (double d : res.delays) std::cout << d << " ";
    std::cout << "\nweights: ";
    for (double w : res.weights) std::cout << w << " ";
    std::cout << "\nDone." << std::endl;
    return 0;
}


