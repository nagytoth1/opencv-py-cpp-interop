#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>
#include <iostream>

namespace py = pybind11;

// Function to invert image colors
cv::Mat invert_image(const cv::Mat &image)
{
    cv::Mat inverted_img;
    cv::bitwise_not(image, inverted_img);
    return inverted_img;
}

// Function to apply binary threshold
cv::Mat threshold_image(const cv::Mat &gray_image, int threshold_value, int max_value)
{
    cv::Mat black_white_image;
    cv::threshold(gray_image, black_white_image, threshold_value, max_value, cv::THRESH_BINARY);
    return black_white_image;
}

// Function for noise removal
cv::Mat noise_removal(const cv::Mat &image)
{
    cv::Mat clean_image;
    cv::Mat kernel = cv::Mat::ones(1, 1, CV_8U);
    cv::dilate(image, clean_image, kernel, cv::Point(-1, -1), 1);
    cv::erode(clean_image, clean_image, kernel, cv::Point(-1, -1), 1);
    cv::morphologyEx(clean_image, clean_image, cv::MORPH_CLOSE, kernel);
    cv::medianBlur(clean_image, clean_image, 3);
    return clean_image;
}

// Function to thin font
cv::Mat thin_font(const cv::Mat &image)
{
    cv::Mat thin_img;
    cv::bitwise_not(image, thin_img);
    cv::Mat kernel = cv::Mat::ones(2, 2, CV_8U);
    cv::erode(thin_img, thin_img, kernel, cv::Point(-1, -1), 1);
    cv::bitwise_not(thin_img, thin_img);
    return thin_img;
}

// Function to thicken font
cv::Mat thicken_font(const cv::Mat &image)
{
    cv::Mat thick_img;
    cv::bitwise_not(image, thick_img);
    cv::Mat kernel = cv::Mat::ones(2, 2, CV_8U);
    cv::dilate(thick_img, thick_img, kernel, cv::Point(-1, -1), 1);
    cv::bitwise_not(thick_img, thick_img);
    return thick_img;
}

// Function to remove borders from an image
cv::Mat remove_borders(const cv::Mat &image)
{
    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(image, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

    if (contours.empty())
        return image;

    std::sort(contours.begin(), contours.end(), [](const std::vector<cv::Point> &a, const std::vector<cv::Point> &b)
              { return cv::contourArea(a) < cv::contourArea(b); });

    cv::Rect bounding_rect = cv::boundingRect(contours.back());
    return image(bounding_rect);
}

py::array_t<uint8_t> mat_to_numpy(const cv::Mat &mat)
{
    // Ensure the mat is of the correct type
    if (mat.type() != CV_8UC1)
    {
        throw std::invalid_argument("Unsupported cv::Mat type");
    }

    // Create the correct numpy array
    return py::array_t<uint8_t>({mat.rows, mat.cols}, mat.data);
}

py::array_t<uint8_t> process_image(const std::string &imagePath, const std::string &outputDirectory = "temp")
{
    cv::Mat original_image = cv::imread(imagePath, cv::IMREAD_COLOR);
    if (original_image.empty())
    {
        throw std::runtime_error("Could not open or find the image!");
    }

    std::stringstream path_stream;

    std::cout << "1. grayscaling image" << std::endl;
    cv::Mat gray_image;
    cv::cvtColor(original_image, gray_image, cv::COLOR_BGR2GRAY);
    path_stream << outputDirectory << "/gray.jpg";
    cv::imwrite(path_stream.str(), gray_image);
    path_stream.str("");

    std::cout << "2. making black and white image" << std::endl;
    cv::Mat binarized_image = threshold_image(gray_image, 210, 230);
    path_stream << outputDirectory << "/bw_image.jpg";
    cv::imwrite(path_stream.str(), binarized_image);
    path_stream.str("");

    std::cout << "3. removing noise from image" << std::endl;
    cv::Mat nonoise_image = noise_removal(binarized_image);
    path_stream << outputDirectory << "/no_noise.jpg";
    cv::imwrite(path_stream.str(), nonoise_image);
    path_stream.str("");

    std::cout << "4. thickening texts" << std::endl;
    cv::Mat dilated_image = thicken_font(nonoise_image);
    path_stream << outputDirectory << "/thick.jpg";
    cv::imwrite(path_stream.str(), dilated_image);
    path_stream.str("");
    return mat_to_numpy(dilated_image); // return the input of the OCR model
}

py::array_t<uint8_t> process_image_v2(const std::string &imagePath, const std::string &outputDirectory = "temp1")
{
    cv::Mat original_image = cv::imread(imagePath, cv::IMREAD_COLOR);
    if (original_image.empty())
    {
        throw std::runtime_error("Could not open or find the image!");
    }
    std::stringstream path_stream;

    std::cout << "0. upscaling image" << std::endl;
    // Define new dimensions (e.g., 3x original size)
    cv::Size new_dimensions(original_image.cols * 3, original_image.rows * 3);
    // Resize the image
    cv::Mat upscaled_image;
    cv::resize(original_image, upscaled_image, new_dimensions, 0, 0, cv::INTER_CUBIC);

    std::cout << "1. grayscaling image" << std::endl;
    cv::Mat gray_image;
    path_stream << outputDirectory << "/gray.jpg";
    cv::cvtColor(upscaled_image, gray_image, cv::COLOR_RGB2GRAY);
    cv::imwrite(path_stream.str(), gray_image);
    path_stream.str("");

    std::cout << "2. applying gaussian blur" << std::endl;
    cv::Mat blurred_image;
    cv::GaussianBlur(gray_image, blurred_image, cv::Point(3, 3), 0);
    path_stream << outputDirectory << "/blurred.jpg";
    cv::imwrite(path_stream.str(), blurred_image);
    path_stream.str("");

    std::cout << "3. making black and white image" << std::endl;
    cv::Mat binarized_image;
    path_stream << outputDirectory << "/bw_image.jpg";
    cv::adaptiveThreshold(blurred_image, binarized_image, 255, cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY, 35, 5);
    cv::imwrite(path_stream.str(), binarized_image);
    path_stream.str("");

    std::cout << "4. thickening texts" << std::endl;
    cv::Mat thickened_image = thicken_font(binarized_image);
    path_stream << outputDirectory << "/thick.jpg";
    cv::imwrite(path_stream.str(), thickened_image);
    // path_stream.str("");

    return mat_to_numpy(binarized_image); // return the input of the OCR model
}

PYBIND11_MODULE(myocr, m)
{
    cv::utils::logging::setLogLevel(cv::utils::logging::LOG_LEVEL_ERROR);
    m.doc() = "Pybind11 module for image processing";
    m.def("process_image", &process_image, "A function to load and process an image")
        .def("process_image_v2",
             &process_image_v2,
             py::arg("imagePath"),
             py::arg("output_directory") = "temp1",
             "Alternative function to load and process a more homogenic image with less contrast.");
}
