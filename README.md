# Installation

Install CMake from here: https://cmake.org/download/

Install Python 3.11.9 from here: https://www.python.org/downloads/release/python-3119/

Install OpenCV 4.10 from here: https://opencv.org/releases/

Install pybind11 using the following command:

```bash
pip install pybind11
```

Make sure you set OpenCV_DIR like so: D:\opencv\build (this can depend on where you have installed the OpenCV release)

You also need to add the OpenCV binary and library directories to the system PATH:

```
D:\opencv\build\x64\vc16\bin
D:\opencv\build\x64\vc16\lib
```

# Build

## Configure the build

```bash
cmake -DCMAKE_PREFIX_PATH="<pybind_path>\share\cmake\pybind11" -B .\build
```

## Build for Debug

```
cmake --build .\build
```

## Compile for Release

```
cmake --build .\build --config Release
```

You can find out your specific `pybind_python_installation_path` by using command python -m pybind11 --includes it will be something like this: `-ID:\programs\Python311\Lib\site-packages\pybind11\include`.
You need to copy the path without the -I flag

# Environment

This project has been tested with following setup:

- OpenCV 4.10 (currently latest)
- Python 3.11.9
- VS2022 Compiler (MSVC 19.41.34120.0)
