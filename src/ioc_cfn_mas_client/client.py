# src/ioc_cfn_mas_client/client.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from generated.api.shared_memories_api import SharedMemoriesApi
from generated.api_client import ApiClient
from generated.configuration import Configuration


@dataclass(frozen=True)
class ClientConfig:
  base_url: str
  api_key: Optional[str] = None
  api_key_name: str = "Authorization"
  api_key_prefix: Optional[str] = "Bearer"
  timeout: Optional[float] = None
  debug: bool = False


class Client:
  """Thin wrapper around the generated OpenAPI client.

  Centralizes configuration/auth and exposes generated API groups.
  """

  def __init__(
          self,
          base_url: str,
          api_key: Optional[str] = None,
          *,
          api_key_name: str = "Authorization",
          api_key_prefix: Optional[str] = "Bearer",
          timeout: Optional[float] = None,
          debug: bool = False,
          configuration: Optional[Configuration] = None,
          api_client: Optional[ApiClient] = None,
  ) -> None:
    if api_client is not None and configuration is not None:
      raise ValueError("Provide only one of api_client or configuration")

    cfg = configuration or (api_client.configuration if api_client else None) or Configuration()
    cfg.host = base_url
    cfg.debug = bool(debug)

    if api_key:
      cfg.api_key[api_key_name] = api_key
      if api_key_prefix:
        cfg.api_key_prefix[api_key_name] = api_key_prefix

    self._configuration = cfg
    self._api_client = api_client or ApiClient(configuration=cfg)
    self._timeout = timeout

    self._shared_memories = SharedMemoriesApi(api_client=self._api_client)

  @property
  def configuration(self) -> Configuration:
    return self._configuration

  @property
  def api_client(self) -> ApiClient:
    return self._api_client

  @property
  def shared_memories(self) -> SharedMemoriesApi:
    return self._shared_memories

  def request(
          self,
          method: str,
          path: str,
          *,
          headers: Optional[Dict[str, str]] = None,
          body: Optional[Any] = None,
          timeout: Optional[float] = None,
  ) -> bytes:
    if not path.startswith("/"):
      raise ValueError("path must start with '/'")

    resp = self._api_client.call_api(
      method.upper(),
      path,
      header_params=headers or {},
      body=body,
      _request_timeout=self._timeout if timeout is None else timeout,
    )
    resp.read()
    return resp.data


