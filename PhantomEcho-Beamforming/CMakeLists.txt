cmake_minimum_required(VERSION 3.16)

project(PhantomEchoBeamforming LANGUAGES CXX)

option(USE_FFTW "Use FFTW3 for FFT operations" ON)
option(USE_ESSENTIA "Enable Essentia for STFT/ISTFT masking" OFF)
option(USE_AQUILA "Enable Aquila DSP (optional)" OFF)
option(BUILD_PYBIND11 "Build Python bindings via pybind11" ON)
option(BUILD_TESTS "Build tests" ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(Eigen3 REQUIRED)

if(USE_FFTW)
  find_package(FFTW3 COMPONENTS FFTW3 FFTW3F QUIET)
endif()

if(BUILD_PYBIND11)
  find_package(pybind11 QUIET)
endif()

if(USE_ESSENTIA)
  find_package(Essentia QUIET)
endif()

if(USE_AQUILA)
  find_package(Aquila QUIET)
endif()

add_library(reference_beamforming
  src/core/gcc_phat.cpp
  src/core/coherence.cpp
  src/core/fractional_delay.cpp
  src/core/butterworth_filter.cpp
  src/core/frequency_masking.cpp
  src/core/PhantomEcho.cpp
)

target_include_directories(reference_beamforming
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
  PRIVATE ${EIGEN3_INCLUDE_DIR}
)

if(FFTW3_FOUND)
  target_compile_definitions(reference_beamforming PRIVATE HAS_FFTW)
  target_link_libraries(reference_beamforming PRIVATE FFTW3::FFTW3)
endif()

if(Essentia_FOUND)
  target_compile_definitions(reference_beamforming PRIVATE HAS_ESSENTIA)
  target_link_libraries(reference_beamforming PRIVATE Essentia::essentia)
endif()

if(Aquila_FOUND)
  target_compile_definitions(reference_beamforming PRIVATE HAS_AQUILA)
  target_link_libraries(reference_beamforming PRIVATE Aquila::Aquila)
endif()

target_link_libraries(reference_beamforming PUBLIC Eigen3::Eigen)

if(BUILD_PYBIND11 AND pybind11_FOUND)
  pybind11_add_module(reference_beamforming_py src/python_bindings/bindings.cpp)
  target_link_libraries(reference_beamforming_py PRIVATE reference_beamforming)
endif()

if(BUILD_TESTS)
  enable_testing()
  add_executable(rb_smoke tests/smoke.cpp)
  target_link_libraries(rb_smoke PRIVATE reference_beamforming)
  add_test(NAME rb_smoke COMMAND rb_smoke)
endif()


