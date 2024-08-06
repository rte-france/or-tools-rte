project(ortools-rte)
message("PLOP")
include(FetchContent)
include(ExternalProject)
FetchContent_Declare(ortools
        GIT_REPOSITORY https://github.com/google/or-tools.git
        GIT_TAG v9.10
        PATCH_COMMAND "cp -r patch/* . && python patch.py"
)
FetchContent_MakeAvailable(ortools)
message("PLOP4")