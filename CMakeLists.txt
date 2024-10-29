cmake_minimum_required(VERSION 3.15)
project(myocr)

# Find packages
find_package(OpenCV REQUIRED)
find_package(pybind11 REQUIRED)
# Include directories
include_directories(${OpenCV_INCLUDE_DIRS} ${pybind11_INCLUDE_DIRS})

# Add Pybind11 module
pybind11_add_module(myocr main.cpp)

# Link libraries
target_link_libraries(myocr PRIVATE ${OpenCV_LIBS})