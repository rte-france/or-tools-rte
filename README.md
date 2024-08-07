# OR-Tools-RTE - RTE specific additions to Google's OR-Tools

This repository contains RTE-specific developments for [OR-Tools](https://github.com/google/or-tools):  
- Support for [SIRIUS](https://github.com/rte-france/sirius-solver) solver
- Customized CI & releases
- Scripting tool for XPRESS, used to update the XPRESS MPsolver implementation
- A simple bash script (not tested by the CI) that allows to test the patch on a linux machine (doc inside)

## Technical overview
This repository aims to build a code with the same structure as the [original code of OR-Tools](https://github.com/google/or-tools-rte), 
only by adding extra files and applying some patches.  
- Extra files are found in the root directory, especially in the [ortools](./ortools) folder.
- Patches are applied using [patch.py](./patch.py), in order to add new features to Cmake files, among others.
- The CI chain applies these patches on [RTE's fork of OR-Tools](https://github.com/rte-france/or-tools) instead of 
  Google's, allowing us to build and test features before merging them into Google's code.

## Support for SIRIUS solver
- Two extra files contain the SIRIUS implementation of MPSolver: [sirius_interface.cc](ortools/linear_solver/sirius_interface.cc)
  and [sirius_interface_test.cc](ortools/linear_solver/sirius_interface_test.cc)
- These files have to be added to different CMake files, thanks to [patch.py](patch.py)
- Also, [patch.py](patch.py) creates the `USE_SIRIUS` flag that can be used to build OR-Tools with SIRIUS support.

## Customized CI
The CI runs after applying patches on [RTE's fork of OR-Tools](https://github.com/rte-france/or-tools).  
Assets are built for different operating systems and development languages.  
Stable versions are published in the [Releases](https://github.com/rte-france/or-tools-rte/releases) section.  
Moreover, you can run the workflows manually on your desired branch of [rte-france/or-tools](https://github.com/rte-france/or-tools) 
in the [actions](https://github.com/rte-france/or-tools-rte/actions) section. This will allow you to test the assets.

# Scripting tool for XPRESS
The script file [parse_header_xpress.py](ortools/xpress/parse_header_xpress.py) allows maintainers of the XPRESS MPSolver 
implementation to easily update the implementation for new versions of XPRESS.

# Developing as a CMake project
This project can be used as a CMake project. It will fetch ortools and apply the patches.
Two variables must be set at configure time:
- `ortools_REPO` url of ortools repository
- `ortools_REF` commit hash to use

Sirius dependency can be provided through CMAKE_PREFIX_PATH otherwise it will be fetched automatically

Fetching the dependencies the first time can be long, but it will be cached for the next builds.

A target `ortools-rte` is created and can be used to build the project. However, it will rebuild ortools.