project(Ortools-RTE)
message("PLOP")
ExternalProject_Add(Ortools
    GIT_REPOSITORY https://github.com/google/or-tools.git
    GIT_TAG v9.10
    PATCH_COMMAND "cp -r patch/* . && python patch.py"
)
message("PLOP2")