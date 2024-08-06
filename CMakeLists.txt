project(ortools-rte)
message("PLOP")
include(FetchContent)
include(ExternalProject)
FetchContent_Declare(ortools
        GIT_REPOSITORY https://github.com/google/or-tools.git
        GIT_TAG v9.10
        PATCH_COMMAND cp -r patch/* . && python patch.py
        FETCHCONTENT_QUIET FALSE
        LOG_DOWNLOAD ON
        LOG_PATCH ON
        LOG_CONFIGURE ON
        LOB_BUILD ON
)
FetchContent_MakeAvailable(ortools)
message("PLOP4")