FROM docker/sandbox-templates:claude-code

USER root
RUN apt-get update && apt-get install -y vim

USER agent

# Install OpenTofu
RUN curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh && \
    chmod +x install-opentofu.sh && \
    ./install-opentofu.sh --install-method deb && \
    rm -f install-opentofu.sh

# Install AWS CLI
RUN curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash
