include(FetchContent)
find_package(sirius_solver QUIET)
if (NOT sirius_solver_FOUND)
    message("SIRIUS not found, fetching it from github")
FetchContent_Declare(sirius_solver
        GIT_REPOSITORY https://github.com/rte-france/sirius-solver
        GIT_TAG antares-integration-v1.5
        SOURCE_SUBDIR src
        FETCHCONTENT_QUIET OFF
        LOG_DOWNLOAD ON
        LOG_PATCH ON
        LOG_CONFIGURE ON
        LOB_BUILD ON
        OVERRIDE_FIND_PACKAGE ON
)
FetchContent_MakeAvailable(sirius_solver)
find_package(sirius_solver REQUIRED)
endif ()