FROM centos:centos7 as base

RUN mkdir /applis

# Install requirements : update repo
RUN sed -i s/mirror.centos.org/vault.centos.org/g /etc/yum.repos.d/*.repo &&\
    sed -i s/^#.*baseurl=http/baseurl=http/g /etc/yum.repos.d/*.repo &&\
    sed -i s/^mirrorlist=http/#mirrorlist=http/g /etc/yum.repos.d/*.repo &&\
    yum install -y epel-release &&\
    yum install -y git redhat-lsb-core make wget centos-release-scl scl-utils python3 &&\
    sed -i s/mirror.centos.org/vault.centos.org/g /etc/yum.repos.d/*.repo &&\
    sed -i s/^#.*baseurl=http/baseurl=http/g /etc/yum.repos.d/*.repo &&\
    sed -i s/^mirrorlist=http/#mirrorlist=http/g /etc/yum.repos.d/*.repo &&\
    yum install -y devtoolset-11 python3-devel python3-pip python3-numpy &&\
    python3 -m pip install --upgrade pip &&\
    python3 -m pip install dataclasses

# Install requirements
RUN rm -rf /var/cache/yum

RUN echo "source /opt/rh/devtoolset-11/enable" >> /etc/bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Install CMake 3.28.3
RUN wget -q "https://cmake.org/files/v3.28/cmake-3.28.3-linux-x86_64.sh" \
&& chmod a+x cmake-3.28.3-linux-x86_64.sh \
&& ./cmake-3.28.3-linux-x86_64.sh --prefix=/usr/local/ --skip-license \
&& rm cmake-3.28.3-linux-x86_64.sh
CMD [ "/usr/bin/bash" ]

ARG SIRIUS_RELEASE_TAG=antares-integration-v1.8

# Download Sirius
RUN cd /applis &&\
    zipfile=centos-7_sirius-solver.zip &&\
    wget https://github.com/rte-france/sirius-solver/releases/download/${SIRIUS_RELEASE_TAG}/$zipfile &&\
    unzip $zipfile && rm $zipfile &&\
    mv install sirius_install &&\
    echo "export LD_LIBRARY_PATH=$PWD/sirius_install/lib::$LD_LIBRARY_PATH" >> /etc/bashrc &&\
    echo "SIRIUS_CMAKE_DIR=$PWD/sirius_install/cmake" >> /etc/bashrc

# Download xpress
RUN cd /applis &&\
    python3 -m pip install --upgrade pip &&\
    mkdir xpress &&\
    cd xpress &&\
    python3 -m pip download --only-binary=:all: --python-version 310  "xpress==9.2.7" &&\
    unzip xpr*.whl &&\
    XPRESS_DIR=$PWD/xpress &&\
    echo "export XPRESSDIR=$XPRESS_DIR" >> /etc/bashrc &&\
    echo "XPAUTH_PATH=$XPRESS_DIR/license/community-xpauth.xpr" >> /etc/bashrc &&\
    ln -s $XPRESS_DIR/lib/libxprs.so.42 $XPRESS_DIR/lib/libxprs.so

FROM base AS devel
ARG SIRIUS=OFF
ARG SHARED=ON
ARG BUILD_EXAMPLES=OFF
ARG OR_REPO="https://github.com/google/or-tools.git"
ARG OR_REF="stable"
WORKDIR /home/project
COPY . .
FROM devel AS build
RUN cmake -S. -Bbuild \
    -Dortools_REPO=${OR_REPO} \
    -Dortools_REF=${OR_REF} \
    -DBUILD_DEPS=ON \
    -DBUILD_SHARED_LIBS=${SHARED} \
    -DUSE_SIRIUS=${SIRIUS}\
    -DBUILD_EXAMPLES=${BUILD_EXAMPLES}\
    -DCMAKE_INSTALL_PREFIX=install \
    -DBUILD_SAMPLES=OFF \
    -DBUILD_FLATZINC=OFF \
    -Dsirius_solver_DIR="$SIRIUS_CMAKE_DIR" \
    -DUSE_HIGHS=ON \
    -DUSE_PDLP=ON

RUN cmake --build build --target all -j4
RUN cmake --build build --target install

FROM build AS test
RUN cd build &&\
    ctest -V -C Release --output-on-failure


