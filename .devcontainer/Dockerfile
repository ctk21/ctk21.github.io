FROM ubuntu:26.04

ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

ENV DEBIAN_FRONTEND=noninteractive

RUN chown root:root /tmp \
    && chmod 1777 /tmp

# Base development tools + Ruby.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        bubblewrap \
        build-essential \
        ca-certificates \
        curl \
        file \
        git \
        git-lfs \
        gnupg \
        jq \
        less \
        locales \
        openssh-client \
        pkg-config \
        procps \
        rsync \
        ruby \
        ruby-dev \
        shellcheck \
        sudo \
        tar \
        tig \
        tzdata \
        unzip \
        vim \
        wget \
        xz-utils \
        zip \
        zsh \
        zstd \
    && gem install bundler \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN usermod --shell /bin/bash "${USERNAME}" \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${USERNAME}" \
    && chmod 0440 "/etc/sudoers.d/${USERNAME}"

# Node.js + Codex.
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @openai/codex@latest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER ${USERNAME}
