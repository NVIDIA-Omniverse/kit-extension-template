# syntax=docker/dockerfile:1


# Use the official Omniverse Kit container image available from NGC.

#

# Note that while we expect the Service we created to be stable across multiple versions of the Omniverse Kit

# application, it may be advisable to specify a version number nonetheless in order to ensure that our container will

# be built against a known good version of the application. Otherwise, it is also possible to use the `:latest` tag to

# rely on the most recent version available at the time of building.

#

# This can additionally be beneficial if building multiple containers for various different projects, as Docker layers

# can be cached and reused, thus limiting storage requirements.

FROM nvcr.io/nvidia/omniverse/kit:104.0.0



# Include labels from the "Open Container Initiative" (OCI) to document the features of the container. This is useful

# when distributing the container, especially once the number of Services you have available start increasing as you

# author more of them over time:

LABEL \
    org.opencontainers.image.base.name="nvcr.io/nvidia/omniverse/kit:104.0.0" \
    org.opencontainers.image.title="Viewport Capture Service" \
    org.opencontainers.image.description="Example of an Omniverse viewport capture Service"



# Let's copy our extension in a location where we can easily collect any extensions we may wish to bundle with our

# container:

COPY ./exts/omni.services.example.viewport_capture.core /opt/nvidia/omniverse/services/


# Launch an instance of Omniverse Kit, mapping the folder where we copied our extension before enabling it:

ENTRYPOINT [ \
    "/opt/nvidia/omniverse/kit-sdk-launcher/kit", \
        "--ext-folder", "/opt/nvidia/omniverse/services/", \
        "--enable", "omni.services.example.viewport_capture.core", \
        "--allow-root", \
        "--no-window", \
]


# Expose ports used by the HTTP server bundled in Omniverse Kit and used for the Services stack:

EXPOSE 8011/tcp


# Perform health-check on the container at regular interval, ignoring any false-negative results that may arise within

# the first 10 minutes due to the application potentially not being responsive because of application launch sequence,

# during which the warm-up and shader cache generation may cause it to miss check-ins:

HEALTHCHECK \
    --start-period=10m \
    --interval=5m \
    --timeout=30s \
    --retries=3 \
    CMD curl --fail http://localhost:8011/docs || exit 1
