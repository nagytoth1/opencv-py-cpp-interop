#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // For using standard containers
#include <opencv2/opencv.hpp>
#include <iostream>

namespace py = pybind11;

cv::Mat load_and_display_image(const std::string &imagePath)
{
    cv::Mat image = cv::imread(imagePath, cv::IMREAD_COLOR);
    if (image.empty())
    {
        throw std::runtime_error("Could not open or find the image!");
    }
    cv::imshow("Display window", image);
    cv::waitKey(0);
    return image;
}

PYBIND11_MODULE(my_image_module, m)
{
    m.def("load_and_display_image", &load_and_display_image, "A function to load and display an image.");
}
