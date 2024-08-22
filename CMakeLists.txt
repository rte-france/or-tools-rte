CMAKE_MINIMUM_REQUIRED(VERSION 3.11)
project(ortools-rte)
include(FetchContent)
function(set_if_not_defined var default_value)
    if(NOT DEFINED ${var})
        set(${var} ${default_value} CACHE INTERNAL "")
    endif()
endfunction()
if (NOT DEFINED ortools_REPO)
    message(FATAL_ERROR "ortools_REPO is not defined")
endif ()
if (NOT DEFINED ortools_REF)
    message(FATAL_ERROR "ortools_REF is not defined")
endif ()
find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
message("found PYTHON interpreter ${Python_EXECUTABLE} = " ${Python_EXECUTABLE})
FetchContent_Declare(ortools
        GIT_REPOSITORY ${ortools_REPO}
        GIT_TAG ${ortools_REF}
        PATCH_COMMAND cp -rf
            ${CMAKE_CURRENT_SOURCE_DIR}/patch.py
            ${CMAKE_CURRENT_SOURCE_DIR}/patch_utils.py
            ${CMAKE_CURRENT_SOURCE_DIR}/ortools
            ${CMAKE_CURRENT_SOURCE_DIR}/cmake_patches
            . && ${Python3_EXECUTABLE} patch.py
        OVERRIDE_FIND_PACKAGE ON
)
message("BUILD_DEPS: " ${BUILD_DEPS})
set_if_not_defined(BUILD_DEPS "ON" CACHE INTERNAL "")
set_if_not_defined(BUILD_SAMPLES "OFF" CACHE INTERNAL "")
set_if_not_defined(BUILD_FLATZINC "OFF" CACHE INTERNAL "")
set_if_not_defined(BUILD_EXAMPLES "OFF" CACHE INTERNAL "")
set_if_not_defined(USE_SCIP "ON" CACHE INTERNAL "")
set_if_not_defined(USE_GLPK "ON" CACHE INTERNAL "")
# We build OR-Tools as a static lib. Cyclic dependencies are detected
# without this flag.
set_if_not_defined(BUILD_SHARED_LIBS "OFF" CACHE INTERNAL "")
# In mode optimization error analysis, we call Sirius through or-tools
# So we need to activate Sirius in or-tools configuration (OFF by default)
set_if_not_defined(USE_SIRIUS "OFF" CACHE INTERNAL "")
FetchContent_MakeAvailable(ortools)
find_package(ortools REQUIRED)

add_custom_target(ortools-rte
        DEPENDS ortools
)