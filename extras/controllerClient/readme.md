# NVDA Controller Client API 2.0 Documentation

## Introduction

This client API allows an application to communicate with NVDA, in order to do such things as speak text or braille a message.

The client API is implemented as a dll (dynamic link library). The functions in this dll can be called from any programming language that supports looking up and calling of any symbol in a dll (such as ctypes in Python), or by linking to it for languages like C and C++.

## Compatibility notice

Version 2.0 of the controller client was introduced in NVDA 2024.1, offering the following additional functions compared to version 1.0:
- nvdaController_getProcessId
- nvdaController_speakSsml

These functions are supported in NVDA 2024.1 and newer. On older versions, they return error code 1717 (RPC_S_UNKNOWN_IF).

## Security practices

Developers should be aware that NVDA runs on the lock screen and [secure screens](https://download.nvaccess.org/documentation/userGuide.html#SecureScreens).
Before providing information to the end user (e.g. via `nvdaController_speakText`), developers should check if Windows is locked or running on a secure screen to prevent secure data being leaked.

## How to get it?

You can build locally or download pre-built, details:
- **Built with the release:**
  - Download the `*controllerClient.zip` from the releases folder: e.g. [Latest stable](https://download.nvaccess.org/releases/stable/)
- **Latest, in development version:**
  - The libraries are built by Appveyor (our CI).
  - Downloads are available from the artifacts tab.
- **Build them yourself:**
  - Follow the project `readme.txt` for general build requirements/dependencies.
  - Run `scons source client`
  - Build output can be found in `./build/[x86|x64|arm64]/client/`

## What is Included?

* `*.dll` file, which you can distribute with your application.
* `*.lib` and `*.exp`
  - The import and export libraries for `nvdaControllerClient` DLL.
  - Used when linking with C/C++ code.
* `nvdaController.h`
  - A C header file containing declarations for all the provided functions.

The **`extras/controllerClient/examples` directory** also contains example usage:

* `example_python.py`
  - an example Python program that uses the NVDA controller client API.
* `example_c.c`
  - The source code for an example C program that uses the NVDA controller client API.
* `example_csharp`
  - The source code for an example C# project on NET Standard 2.0 that uses the NVDA controller client API.
* `example_rust`
  - The source code for an example Rust crate providing access to the NVDA controller client API, including example code.

Running these examples requires a copy of **`nvdaControllerClient.dll`** in its path that matches the architecture of the example.
For example, if you want to test the Python example on an X64 version of Python, you need the **`x64/nvdaControllerClient.dll`** file.

## Available Functions

All functions in this dll return 0 on success and a non-0 code on failure. Failure could be due to not being able to communicate with NVDA or incorrect usage of the function. The error codes that these functions return are always standard Windows error codes.

For definitions of all the functions available, please see `nvdaController.h`.
The functions are documented with comments.

## License

The NVDA Controller Client API is licensed under the GNU Lesser General Public License (LGPL), version 2.1.
In simple terms, this means you can use this library in any application, but if you modify the library in any way, you must contribute the changes back to the community under the same license.

Please refer to [`license.txt`](./license.txt) for more details.
