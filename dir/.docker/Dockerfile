# Base image
FROM nvidia/cuda:12.0.0-devel-ubuntu20.04

ARG UID
ARG GID

# Environment
# ENV http_proxy http://133.44.62.221:8080
# ENV https_proxy http://133.44.62.221:8080
# ENV no_proxy localhost,192.168.*,127.0.*

ENV PASSWORD="notebook"
ENV USER=nb-user
ENV GROUP=nb-user
ENV HOME /home/${USER}

WORKDIR /tmp

# timezone setting
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y tzdata

# Install Commands
# now removing "tk-dev rust-all"
RUN apt-get install -y \
  python3 \
  make \
  cmake \
  build-essential \
  libssl-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  llvm \
  libncurses5-dev \
  libncursesw5-dev \
  libffi-dev \
  liblzma-dev \
  python3-openssl \
  xz-utils \
  zlib1g-dev \
  curl \
  dpkg \
  git \
  iputils-ping \
  rsync \
  sudo \
  wget \
  vim \
  nano \
  tmux \
  python3-distutils \
  python3-pip \
  libboost-dev \
  locales \
  && locale-gen ja_JP.UTF-8 \
  && apt-get autoremove -y && apt-get clean

# sudo setting
RUN groupadd -g ${GID} ${GROUP} && \
  useradd -u ${UID} -g ${GROUP} -G sudo -m -s /bin/bash ${USER} && \
  echo ${USER}:${PASSWORD} | chpasswd \
  && echo "${USER} ALL=NOPASSWD: ALL" >> /etc/sudoers.d/${USER}

USER ${USER}:${GROUP}

ENV PATH $PATH:${HOME}/.local/bin
# RUN echo $PATH
# RUN pip3 --version

# Other settings
RUN echo 'export LANG=ja_JP.UTF-8' >> /home/nb-user/.bashrc \
  && echo 'export PS1="${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$ "' >> /home/nb-user/.bashrc


# Install python modules
COPY .docker/requirements.txt requirements.txt
# RUN python3 --version | cat
RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --user \
  && sudo rm requirements.txt

# Install JUMAN++ (v2)
RUN wget "https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz" \
  && tar xvf jumanpp-2.0.0-rc3.tar.xz \
  && cd jumanpp-2.0.0-rc3 \
  && mkdir bld && cd bld \
  && curl -LO https://github.com/catchorg/Catch2/releases/download/v2.13.8/catch.hpp \
  && mv catch.hpp ../libs/ \
  && cmake .. -DCMAKE_BUILD_TYPE=Release \
  && sudo make install -j "$(nproc)" \
  && sudo make install

# # [deprecated] Install JUMAN++ (v1) 
# RUN wget http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.02.tar.xz \
#   && tar xJvf jumanpp-1.02.tar.xz \
#   && cd jumanpp-1.02 \
#   && ./configure \
#   && make \
#   && sudo make install \
#   && cd ..

# Install KNP
RUN wget https://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.20.tar.bz2 \
  && tar jxvf knp-4.20.tar.bz2 \
  && cd knp-4.20 \
  && ./configure \
  && make \
  && sudo make install 
  # \
  # && cd ..

# # Install transformers
# RUN wget -O transformers.tar.gz https://github.com/huggingface/transformers/archive/refs/tags/v4.25.1.tar.gz \
#   && pip3 install --user transformers.tar.gz \
#   && sudo rm *.tar.*

# # [old] Install transformers
# WORKDIR ${HOME}
# RUN git clone https://github.com/huggingface/transformers.git -b v3.1.0 --depth 1
# WORKDIR ${HOME}/transformers
# RUN pip3 install .


# # Install Ginza
# # pipでインストールする
# pip3 install ginza
# # Install for tar.gz from github
# RUN sudo -E curl -L -O https://github.com/megagonlabs/ginza/releases/download/v5.1.2/ginza-5.1.2.tar.gz \
#   -O https://github.com/megagonlabs/ginza/releases/download/v5.1.2/ja_ginza-5.1.2.tar.gz \
#   -O https://github.com/megagonlabs/ginza/releases/download/v2.2.0/SudachiDict_core-20190927.tar.gz \
#   && pip3 install --user ginza-2.2.1.tar.gz \
#   && pip3 install --user ja_ginza-2.2.0.tar.gz \
#   && pip3 install --user SudachiDict_core-20190927.tar.gz \
#   && sudo rm *.tar.*

# Init WORKDIR
WORKDIR ${HOME}
COPY .docker/ ${HOME}/.docker/
RUN cp -r ${HOME} /tmp/${USER}

# START
ENTRYPOINT ["/bin/bash", ".docker/startup.sh"]
