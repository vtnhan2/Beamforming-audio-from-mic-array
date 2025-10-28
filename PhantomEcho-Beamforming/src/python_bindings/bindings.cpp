#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "core/PhantomEcho.h"

namespace py = pybind11;

PYBIND11_MODULE(reference_beamforming_py, m) {
    m.doc() = "Reference-based beamforming (C++ core)";

    py::class_<rb::BeamformingResult>(m, "BeamformingResult")
        .def_readonly("extractedVocal", &rb::BeamformingResult::extractedVocal)
        .def_readonly("delays", &rb::BeamformingResult::delays)
        .def_readonly("coherences", &rb::BeamformingResult::coherences)
        .def_readonly("weights", &rb::BeamformingResult::weights);

    py::class_<rb::ReferenceBeamformer>(m, "ReferenceBeamformer")
        .def(py::init<double>(), py::arg("sampleRate") = 16000.0)
        .def("extractVocalFromReference", &rb::ReferenceBeamformer::extractVocalFromReference,
             py::arg("audioData"), py::arg("referenceChannelIdx") = 4, py::arg("coherenceThreshold") = 0.3);
}


