# Base image
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

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

# Install Commands
RUN apt-get update && apt-get install -y sudo python3 python3-pip 
RUN pip3 install torch torchvision







# # ここから下は過去のコマンド
# RUN apt-get update && apt-get install -y tzdata
# RUN apt-get install -y   make \
#   build-essential \
#   tk-dev \
#   libssl-dev \
#   libbz2-dev \
#   libreadline-dev \
#   libsqlite3-dev \
#   llvm \
#   libncurses5-dev \
#   libncursesw5-dev \
#   libffi-dev \
#   liblzma-dev \
#   python3-openssl \
#   xz-utils \
#   zlib1g-dev \
#   curl \
#   dpkg \
#   git \
#   iputils-ping \
#   rsync \
#   sudo \
#   wget \
#   vim \
#   nano \
#   tmux \
#   python3-distutils \
#   python3-pip \
#   libboost-dev \
#   locales \
#   rust-all \
#   && locale-gen ja_JP.UTF-8 \
#   && apt-get autoremove -y && apt-get clean

# # sudo setting
# RUN groupadd -g ${GID} ${GROUP} && \
#   useradd -u ${UID} -g ${GROUP} -G sudo -m -s /bin/bash ${USER} && \
#   echo ${USER}:${PASSWORD} | chpasswd \
#   && echo "${USER} ALL=NOPASSWD: ALL" >> /etc/sudoers.d/${USER}

# USER ${USER}:${GROUP}

# ENV PATH $PATH:${HOME}/.local/bin
# RUN echo $PATH
# RUN pip3 --version

# # Other settings
# RUN echo 'export LANG=ja_JP.UTF-8' >> ~/.bashrc \
#   && echo 'export PS1="${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$ "' >> ~/.bashrc

# COPY .docker/requirements.txt requirements.txt

# RUN python3 --version | cat

# # Install python modules
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt --user \
#   && sudo rm requirements.txt
# # RUN pip3 install tensorflow==2.4.2 --user

# # Install JUMAN++
# # RUN wget http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.02.tar.xz \
# #   && tar xJvf jumanpp-1.02.tar.xz \
# #   && cd jumanpp-1.02 \
# #   && ./configure \
# #   && make \
# #   && sudo make install \
# #   && cd ..

# # Install KNP
# # RUN wget https://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.20.tar.bz2 \
# #   && tar jxvf knp-4.20.tar.bz2 \
# #   && cd knp-4.20 \
# #   && ./configure \
# #   && make \
# #   && sudo make install \
# #   && cd ..

# # Install transformers
# # RUN wget https://github.com/huggingface/transformers/archive/refs/tags/v4.23.1.tar.gz \
# #   && pip3 install --user transformers-4.23.1.tar.gz \
# #   && sudo rm *.tar.*

# # WORKDIR ${HOME}
# # RUN git clone https://github.com/huggingface/transformers.git -b v3.1.0 --depth 1
# # WORKDIR ${HOME}/transformers
# # RUN pip3 install .

# # # Install for tar.gz from github
# # # pipでインストールする
# # RUN sudo -E curl -L -O https://github.com/megagonlabs/ginza/releases/download/v5.1.2/ginza-5.1.2.tar.gz \
# #   -O https://github.com/megagonlabs/ginza/releases/download/v5.1.2/ja_ginza-5.1.2.tar.gz \
# #   -O https://github.com/megagonlabs/ginza/releases/download/v2.2.0/SudachiDict_core-20190927.tar.gz \
# #   && pip3 install --user ginza-2.2.1.tar.gz \
# #   && pip3 install --user ja_ginza-2.2.0.tar.gz \
# #   && pip3 install --user SudachiDict_core-20190927.tar.gz \
# #   && sudo rm *.tar.*

# Init WORKDIR
WORKDIR ${HOME}
COPY .docker/ ${HOME}/.docker/
RUN cp -r ${HOME} /tmp/${USER}

# START
ENTRYPOINT ["/bin/bash", ".docker/startup.sh"]
