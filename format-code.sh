#!/bin/bash

if [ $# -eq 0 ]
then
    # No arguments: format all
    SOURCE_DIRS="ortools/"
    SOURCE_FILES=$(find $SOURCE_DIRS -regextype egrep -regex ".*/*\.(c|cxx|cpp|cc|h|hxx|hpp)$")
else
    # Format files provided as arguments
    SOURCE_FILES="$@"
fi

# Remove ^M, etc.
if ! [ -x "$(command -v dos2unix)" ]; then
    echo 'Warning: dos2unix is not installed. Skipping' >&2
else
    echo "$SOURCE_FILES" | xargs dos2unix
fi

if ! [ -x "$(command -v clang-format)" ]; then
    echo 'Warning: clang-format is not installed. Skipping' >&2
else
    echo "$SOURCE_FILES" | xargs clang-format  -style=file:.clang-format -i --verbose
fi
