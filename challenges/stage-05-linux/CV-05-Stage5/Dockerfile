FROM ubuntu:24.04

LABEL org.opencontainers.image.title="CyberVault CV-05"
LABEL org.opencontainers.image.description="Standalone Linux investigation challenge"

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-server \
        sudo \
        bash \
        coreutils \
        findutils \
        grep \
        sed \
        gawk \
        procps \
        iproute2 \
        less \
        nano \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash player \
    && echo 'player:CV05-Lab-Only!' | chpasswd \
    && chmod 0750 /home/player \
    && passwd --lock root \
    && rm -f /etc/ssh/ssh_host_* \
    && install -d -m 0755 /run/sshd

WORKDIR /home/player

# SSH configuration, startup, maintenance weakness and evidence
# will be added in subsequent steps.

COPY --chown=root:root container/sshd_config /etc/ssh/sshd_config
COPY --chown=root:root container/entrypoint.sh /usr/local/bin/cv05-entrypoint.sh

RUN chmod 0644 /etc/ssh/sshd_config \
    && chmod 0755 /usr/local/bin/cv05-entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/usr/local/bin/cv05-entrypoint.sh"]

RUN groupadd cvmaint \
    && usermod -aG cvmaint player \
    && install -d -o root -g cvmaint -m 0755 /opt/cybervault/maintenance \
    && install -d -o root -g root -m 0700 /root/evidence

COPY --chown=root:root container/maintenance/run-maintenance.sh /usr/local/sbin/cv05-maintenance
COPY --chown=root:cvmaint container/maintenance/collect-evidence.sh /opt/cybervault/maintenance/collect-evidence.sh
COPY --chown=root:root container/sudoers-cv05 /etc/sudoers.d/cv05
COPY --chown=root:root container/evidence/incident-report.txt /root/evidence/incident-report.txt

RUN chmod 0755 /usr/local/sbin/cv05-maintenance \
    && chmod 0775 /opt/cybervault/maintenance/collect-evidence.sh \
    && chmod 0440 /etc/sudoers.d/cv05 \
    && chmod 0600 /root/evidence/incident-report.txt \
    && visudo -cf /etc/sudoers.d/cv05
