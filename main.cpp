#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>
#include <iostream>

namespace py = pybind11;

py::array_t<uint8_t> mat_to_numpy(const cv::Mat &mat)
{
    // Ensure the mat is of the correct type
    if (mat.type() != CV_8UC1 && mat.type() != CV_8UC3)
    {
        throw std::invalid_argument("Unsupported cv::Mat type");
    }

    // Get the total size of the matrix
    size_t height = mat.rows;
    size_t width = mat.cols;
    size_t channels = mat.channels();

    // Create the correct numpy array based on the number of channels
    py::array_t<uint8_t> result({height, width, channels}, mat.data);

    return result;
}

py::array_t<uint8_t> process_image(const std::string &imagePath)
{
    cv::Mat image = cv::imread(imagePath, cv::IMREAD_COLOR);
    if (image.empty())
    {
        throw std::runtime_error("Could not open or find the image!");
    }

    return mat_to_numpy(image);
}

PYBIND11_MODULE(myocr, m)
{
    m.def("process_image", &process_image, "A function to load and process an image");
}
