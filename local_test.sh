!#/bin/bash
SANDBOX_DIR_NAME="or-tools-rte-sandbox"
BRANCH_NAME="stable"

git clone  https://github.com/google/or-tools.git --branch $BRANCH_NAME --single-branch $SANDBOX_DIR_NAME
cd $SANDBOX_DIR_NAME
cp ../*.py .
cp -r ../ortools .
python3 patch.py
# the content of the directory $SANDBOX_DIR_NAME is the patched ortools
SIRIUS_ZIPFILE=ubuntu-20.04_sirius-solver.zip
SIRIUS_RELEASE_TAG="antares-integration-v1.8"
wget https://github.com/rte-france/sirius-solver/releases/download/$SIRIUS_RELEASE_TAG/$SIRIUS_ZIPFILE
unzip $SIRIUS_ZIPFILE
mv ubuntu-20.04_sirius-solver-install sirius_install
export LD_LIBRARY_PATH=$PWD/sirius_install/lib
export SIRIUS_CMAKE_DIR=$PWD/sirius_install/cmake

cmake -S . -B build &\
  -DCMAKE_BUILD_TYPE=Release  &\
  -DBUILD_DEPS=ON  &\
  -DBUILD_EXAMPLES=OFF  &\
  -DUSE_SIRIUS=ON  &\
  -Dsirius_solver_DIR=$SIRIUS_CMAKE_DIR  &\
  -DBUILD_SAMPLES=OFF  &\
  -DCMAKE_INSTALL_PREFIX="build/install"

cmake --build build --config Release --target all install -j4
