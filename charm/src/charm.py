#!/usr/bin/env python3
# Copyright 2025 gschiano
# See LICENSE file for licensing details.

"""Go Charm entrypoint."""

import logging
import typing

import ops
from urllib.parse import urlparse

import paas_charm.go
from paas_charm.charm_state import CharmState
from paas_charm.app import App

logger = logging.getLogger(__name__)

class OllamaCharm(paas_charm.go.Charm):
    """Go Charm service."""

    def __init__(self, *args: typing.Any) -> None:
        """Initialize the instance.

        Args:
            args: passthrough to CharmBase.
        """
        super().__init__(*args)


    def _create_app(self) -> App:
        """Build a App instance.

        Returns:
            A new App instance.
        """
        charm_state = self._create_charm_state()
        return App(
            container=self._container,
            charm_state=charm_state,
            workload_config=self._workload_config,
            database_migration=self._database_migration,
            configuration_prefix="",
        )

    def _create_charm_state(self) -> CharmState:
        charm_state = super()._create_charm_state()
        port = charm_state.framework_config["port"]
        charm_state._user_defined_config["ollama_origins"] = self._base_url
        charm_state._user_defined_config["ollama_host"] = f"0.0.0.0:{port}"
        if self._ingress.url:
            parsed_url = urlparse(self._base_url)
            charm_state._user_defined_config["ollama_host"] = f"{parsed_url.scheme}://0.0.0.0:{port}"
        return charm_state

if __name__ == "__main__":
    ops.main(OllamaCharm)
