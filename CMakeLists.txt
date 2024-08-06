CMAKE_MINIMUM_REQUIRED(VERSION 3.11)
project(ortools-rte)
message("PLOP")
include(FetchContent)
FetchContent_Declare(ortools
        GIT_REPOSITORY https://github.com/google/or-tools.git
        GIT_TAG v9.10
        PATCH_COMMAND cp -rf
            ${CMAKE_SOURCE_DIR}/patch.py
            ${CMAKE_SOURCE_DIR}/patch_utils.py
            ${CMAKE_SOURCE_DIR}/ortools
            ${CMAKE_SOURCE_DIR}/patchs
            . && python patch.py
)
set(BUILD_DEPS "ON" CACHE INTERNAL "")
set(BUILD_SAMPLES "OFF" CACHE INTERNAL "")
set(BUILD_FLATZINC "OFF" CACHE INTERNAL "")
set(BUILD_EXAMPLES "OFF" CACHE INTERNAL "")
set(USE_SCIP "ON" CACHE INTERNAL "")
set(USE_GLPK "ON" CACHE INTERNAL "")
# We build OR-Tools as a static lib. Cyclic dependencies are detected
# without this flag.
set(BUILD_SHARED_LIBS "OFF" CACHE INTERNAL "")
# In mode optimization error analysis, we call Sirius through or-tools
# So we need to activate Sirius in or-tools configuration (OFF by default)
set(USE_SIRIUS "ON" CACHE INTERNAL "")
FetchContent_MakeAvailable(ortools)
message("PLOP4")