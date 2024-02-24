from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import jinja2

TEMPLATES_DIR = Path(__file__).parent.joinpath("templates")
TEMPLATE_NAME = "nats.conf.j2"


def taglist(input: dict[str, str]):
    """Custom filter"""
    return json.dumps([f"{k}:{v}" for k, v in input.items()])


def asposix(path: str | Path) -> str:
    if isinstance(path, Path):
        return path.resolve().as_posix()
    return path


@dataclass
class ServerConfig:
    port: int = -1
    host: str | None = None
    client_advertise: str | None = None
    server_name: str | None = None
    server_tags: dict[str, str] | None = None
    debug: bool | None = None
    trace: bool | None = None
    trace_verbose: bool | None = None
    http_port: int | None = None
    pid_file: str | Path | None = None
    ports_file_dir: str | Path | None = None
    log_file: str | Path | None = None
    log_time: bool | None = None
    log_size_limit: int | None = None
    tls_cert_file: str | Path | None = None
    tls_key_file: str | Path | None = None
    tls_ca_file: str | Path | None = None
    cluster_name: str | None = None
    cluster_listen: str | None = None
    cluster_url: str | None = None
    cluster_no_advertise: bool | None = None
    cluster_routes: list[str] | None = None
    websocket_listen_address: str | None = None
    websocket_listen_port: int | None = None
    websocket_advertise_url: str | None = None
    websocket_tls_cert_file: str | Path | None = None
    websocket_tls_key_file: str | Path | None = None
    websocket_same_origin: bool | None = None
    websocket_allowed_origins: list[str] | None = None
    websocket_compression: bool | None = None
    enable_jetstream: bool = False
    jetstream_domain: str | None = None
    jetstream_store_dir: str | Path | None = None
    max_memory_store: int | None = None
    max_file_store: int | None = None
    max_outstanding_catchup: int | None = None
    leafnodes_listen_address: str | None = None
    leafnodes_listen_port: int | None = None
    leafnode_remotes: dict[str, Any] | None = None
    user: str | None = None
    password: str | None = None
    token: str | None = None
    users: list[dict[str, Any]] | None = None
    accounts: dict[str, Any] | None = None
    operator: str | None = None
    system_account: str | None = None
    jwt_path: str | Path | None = None
    allow_delete_jwt: bool | None = None
    resolver_preload: dict[str, str] | None = None


class ConfigGenerator:

    def __init__(self) -> None:
        loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
        environment = jinja2.Environment(loader=loader)
        environment.filters["taglist"] = taglist  # type: ignore
        environment.filters["asposix"] = asposix  # type: ignore
        self.template = environment.get_template(TEMPLATE_NAME)

    def render(
        self,
        port: int = -1,
        address: str | None = None,
        client_advertise: str | None = None,
        server_name: str | None = None,
        server_tags: dict[str, str] | None = None,
        user: str | None = None,
        password: str | None = None,
        users: list[dict[str, Any]] | None = None,
        token: str | None = None,
        http_port: int | None = None,
        debug: bool | None = None,
        trace: bool | None = None,
        trace_verbose: bool | None = None,
        log_time: bool | None = None,
        pid_file: str | Path | None = None,
        ports_file_dir: str | Path | None = None,
        log_file: str | Path | None = None,
        log_size_limit: int | None = None,
        tls_cert: str | Path | None = None,
        tls_key: str | Path | None = None,
        tls_ca_cert: str | Path | None = None,
        cluster_name: str | None = None,
        cluster_url: str | None = None,
        cluster_listen: str | None = None,
        routes: list[str] | None = None,
        no_advertise: bool | None = None,
        with_jetstream: bool = False,
        jetstream_domain: str | None = None,
        store_directory: str | Path | None = None,
        max_memory_store: int | None = None,
        max_file_store: int | None = None,
        max_outstanding_catchup: int | None = None,
        leafnodes_listen_address: str | None = None,
        leafnodes_listen_port: int | None = None,
        leafnode_remotes: dict[str, Any] | None = None,
        websocket_listen_address: str | None = None,
        websocket_listen_port: int | None = None,
        websocket_advertise_url: str | None = None,
        websocket_tls_cert: str | Path | None = None,
        websocket_tls_key: str | Path | None = None,
        websocket_same_origin: bool | None = None,
        websocket_allowed_origins: list[str] | None = None,
        websocket_compression: bool | None = None,
        jwt_path: str | Path | None = None,
        operator: str | None = None,
        system_account: str | None = None,
        system_account_jwt: str | None = None,
        allow_delete_jwt: bool | None = None,
        resolver_preload: dict[str, str] | None = None,
    ) -> str:
        cfg = ServerConfig(
            port=port,
            host=address,
            client_advertise=client_advertise,
            server_name=server_name,
            server_tags=server_tags,
            debug=debug,
            trace=trace,
            trace_verbose=trace_verbose,
            http_port=http_port,
            pid_file=pid_file,
            ports_file_dir=ports_file_dir,
            log_file=log_file,
            log_time=log_time,
            log_size_limit=log_size_limit,
            tls_cert_file=tls_cert,
            tls_key_file=tls_key,
            tls_ca_file=tls_ca_cert,
            cluster_name=cluster_name,
            cluster_listen=cluster_listen,
            cluster_url=cluster_url,
            cluster_no_advertise=no_advertise,
            cluster_routes=routes,
            websocket_listen_address=websocket_listen_address,
            websocket_listen_port=websocket_listen_port,
            websocket_advertise_url=websocket_advertise_url,
            websocket_tls_cert_file=websocket_tls_cert,
            websocket_tls_key_file=websocket_tls_key,
            websocket_same_origin=websocket_same_origin,
            websocket_allowed_origins=websocket_allowed_origins,
            websocket_compression=websocket_compression,
            enable_jetstream=with_jetstream,
            jetstream_domain=jetstream_domain,
            jetstream_store_dir=store_directory,
            max_memory_store=max_memory_store,
            max_file_store=max_file_store,
            max_outstanding_catchup=max_outstanding_catchup,
            leafnodes_listen_address=leafnodes_listen_address,
            leafnodes_listen_port=leafnodes_listen_port,
            leafnode_remotes=leafnode_remotes,
            user=user,
            password=password,
            token=token,
            users=users,
            operator=operator,
            system_account=system_account,
            jwt_path=jwt_path,
            allow_delete_jwt=allow_delete_jwt,
            resolver_preload=resolver_preload,
        )

        if user or password:
            if not (user and password):
                raise ValueError(
                    "Both user and password argument must be provided together"
                )

        if token:
            if user:
                raise ValueError(
                    "token argument cannot be used together with user and password"
                )

        if users:
            if token or user:
                raise ValueError(
                    "users argument cannot be used with token or user and password"
                )

        if operator:
            if users or token or user:
                raise ValueError(
                    "operator argument cannot be used with any of users, token, user and password arguments"
                )
            if system_account is None:
                raise ValueError("system_account argument must be provided")
            if system_account_jwt is None:
                raise ValueError("system_account_jwt argument must be provided")
            if jwt_path is None:
                raise ValueError("jwt_path argument must be provided")

        if system_account and system_account_jwt:
            if not resolver_preload:
                resolver_preload = {}
            resolver_preload[system_account] = system_account_jwt

        if websocket_tls_cert and websocket_tls_key:
            if not websocket_tls_cert and websocket_tls_key:
                raise ValueError(
                    "websocket_tls_cert and websocket_tls_key must be provided to enable websocket TLS"
                )
        return self.template.render(asdict(cfg))
