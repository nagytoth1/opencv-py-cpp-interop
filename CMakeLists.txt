cmake_minimum_required(VERSION 3.15)
project(myocr)

# Set CMAKE_PREFIX_PATH for pybind11 (change to your specific Pybind11 installation path)
set(CMAKE_PREFIX_PATH "C:/programming/Python311/Lib/site-packages/pybind11/share/cmake/pybind11" ${CMAKE_PREFIX_PATH})

# Find packages
find_package(OpenCV REQUIRED)
find_package(pybind11 REQUIRED)
# Include directories
include_directories(${OpenCV_INCLUDE_DIRS} ${pybind11_INCLUDE_DIRS})

# Add Pybind11 module
pybind11_add_module(myocr main.cpp)

# Link libraries
target_link_libraries(myocr PRIVATE ${OpenCV_LIBS})