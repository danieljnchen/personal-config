FROM docker/sandbox-templates:claude-code

USER root
RUN apt-get update && apt-get install -y vim tmux zip unzip

USER agent

# Install OpenTofu
RUN curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh && \
    chmod +x install-opentofu.sh && \
    ./install-opentofu.sh --install-method deb && \
    rm -f install-opentofu.sh

# Install AWS CLI
RUN curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash

# Install fnm (Fast Node Manager) and Node.js
ARG NODE_VERSION=24
ENV FNM_DIR=/home/agent/.local/share/fnm
RUN curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir "$FNM_DIR" --skip-shell && \
    "$FNM_DIR/fnm" install "$NODE_VERSION" && \
    "$FNM_DIR/fnm" default "$NODE_VERSION"
# Default node on PATH for non-interactive shells (e.g. the agent's tool calls);
# interactive shells also run `fnm env` from bashrc_ext for version switching.
ENV PATH=$FNM_DIR/aliases/default/bin:$FNM_DIR:$PATH

# Home directory config (v2 kit files/home), then one-time setup at build
# instead of on every boot.
COPY --chown=agent:agent files/home/ /home/agent/
RUN bash /home/agent/setup_sbx.sh

ENTRYPOINT ["bash", "-c", "cd /home/agent && exec bash"]
