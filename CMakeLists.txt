project(Ortools-RTE)
message("PLOP")
externalproject_add(Ortools
    GIT_REPOSITORY https://github.com/google/or-tools.git
    GIT_TAG v9.10
    PATCH_COMMAND "cp -r patch/* . && python patch.py"
)
message("PLOP2")