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
cmake -B -DCMAKE_PREFIX_PATH=<pybind_path>  .\build
```

You can find out your specific Pybind11 installation path (`pybind_path`) by using following command:

```bash
python -m pybind11 --includes
```

The output will be something like this: `-ID:\programs\Python311\Lib\site-packages\pybind11\include`.
You need to copy the path without the `-I` prefix and the `include` part at the end.

## Build for Debug

If you want to build the Debug target, you can do it with following command:

```
cmake --build .\build
```

## Compile for Release

If you want to build the Release target, you can do it with following command:

```
cmake --build .\build --config Release
```

## Run the code

I suggest creating a virtual environment to separate this project's dependencies from your local setup:

```bash
python -m venv venv
```

Then you can activate it in Windows with following command: `venv\Scripts\activate.bat` and in Linux like so: `./venv/bin/activate`

When you first try to run the application with `python main.py` you may see the following error coming up, preventing you to launch the application:

```
Failed to import, skipping with error: DLL load failed while importing myocr: The specified module could not be found.
```

This means the myocr module misses the OpenCV DLL files. I have managed to resolve this issue just by copying over the .dll and .pdb files from the bin directory of the OpenCV installation path (<opencv_path>\build\x64\vc16\bin) starting with `opencv_world` to the directory where the `myocr` module is located (in my case it was `build\Debug`).

After doing this you are able to run the main.py script with `python main.py` command.

## Generate stub for the compiled myocr module

By installing the `mypy` Python package with `pip install mypy` we can use the `stubgen` command to make a stub for the module to have the benefits of type hinting and intellisense in Python.

```bash
# generate calculations_cpp.pyi from the myocr module into the build directory
stubgen -m build.Debug.myocr -o .
```

# Environment

This project has been tested with following setup:

- OpenCV 4.10 (currently latest)
- Python 3.11.9
- VS2022 Compiler (MSVC 19.41.34120.0)
