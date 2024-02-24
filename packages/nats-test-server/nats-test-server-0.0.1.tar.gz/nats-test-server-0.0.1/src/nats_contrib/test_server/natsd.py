from __future__ import annotations

import os
import shutil
import signal
import socket
import subprocess
import tempfile
import time
import types
import weakref
from pathlib import Path
from typing import Any

from .config import ConfigGenerator

DEFAULT_BIN_DIR = Path.home().joinpath("nats-server").absolute()


class NATSD:
    def __init__(
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
        logtime: bool | None = None,
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
        config_file: str | Path | None = None,
        max_cpus: float | None = None,
        start_timeout: float = 2,
        output_colorized: bool = True,
        clean_log_file_on_exit: bool = False,
        clean_pid_file_on_exit: bool = False,
    ) -> None:
        """Create a new instance of nats-server daemon.

        Arguments:
            address: host address nats-server should listen to. Default is 127.0.0.1 (localhost).
            port: tcp port nats-server should listen to. Clients can connect to this port. Default is 4222.
            server_name: the server name. Default to auto-generated name.
            user: username required for connections. Omitted by default.
            password: password required for connections. Omitted by default.
            token: authorization token required for connections. Omitted by default.
            http_port: port for http monitoring. Default is 8222.
            debug: enable debugging output. Default is False.
            trace: enable raw traces. Default is False.
            pid_file: file to write process ID to. Omitted by default.
            log_file: file to redirect log output to. Omitted by default.
            tls_cert: server certificate file (TLS is enabled when both cert and key are provided)
            tls_key: server key file (TLS is enabled when both cert and key are provided)
            tls_ca_cert: client certificate for CA verification (mutual TLS is enabled when ca cert is provided)
            cluster_name: the cluster name. Default to auto-generated name when clustering is enabled.
            cluster_url: cluster URL for sollicited routes.
            cluster_listen: cluster URL from which members can solicite routes. Enable cluster mode when set.
            routes: routes to solicit and connect.
            no_advertise: do not advertise known cluster information to clients.
            with_jetstream: enable jetstream engine when True. Disabled by default.
            store_directory: path to jetstream store directory. Default to a temporary directory.
            config_file: path to a configuration file. None by default.
            max_cpus: maximum number of CPU configured using GOMAXPROCS environment variable. By default all CPUs can be used.
            start_timeout: amount of time to wait before raising an error when starting the daemon with wait=True.
            output_colorized: enable colorized output. Default is True.
        """
        self.output_writer = OutputWriter(colorized=output_colorized)
        if config_file is None:
            config_file = Path(tempfile.mkdtemp()).joinpath("nats.conf")
            generator = ConfigGenerator()
            config_str = generator.render(
                address=address,
                port=port,
                client_advertise=client_advertise,
                server_name=server_name,
                server_tags=server_tags,
                user=user,
                password=password,
                users=users,
                token=token,
                http_port=http_port,
                debug=debug,
                trace=trace,
                trace_verbose=trace_verbose,
                log_time=logtime,
                pid_file=pid_file,
                ports_file_dir=ports_file_dir,
                log_file=log_file,
                log_size_limit=log_size_limit,
                tls_cert=tls_cert,
                tls_key=tls_key,
                tls_ca_cert=tls_ca_cert,
                cluster_name=cluster_name,
                cluster_url=cluster_url,
                cluster_listen=cluster_listen,
                routes=routes,
                no_advertise=no_advertise,
                with_jetstream=with_jetstream,
                jetstream_domain=jetstream_domain,
                store_directory=store_directory,
                max_memory_store=max_memory_store,
                max_file_store=max_file_store,
                max_outstanding_catchup=max_outstanding_catchup,
                leafnodes_listen_address=leafnodes_listen_address,
                leafnodes_listen_port=leafnodes_listen_port,
                leafnode_remotes=leafnode_remotes,
                websocket_listen_address=websocket_listen_address,
                websocket_listen_port=websocket_listen_port,
                websocket_advertise_url=websocket_advertise_url,
                websocket_tls_cert=websocket_tls_cert,
                websocket_tls_key=websocket_tls_key,
                websocket_same_origin=websocket_same_origin,
                websocket_allowed_origins=websocket_allowed_origins,
                websocket_compression=websocket_compression,
                jwt_path=jwt_path,
                operator=operator,
                system_account=system_account,
                system_account_jwt=system_account_jwt,
                allow_delete_jwt=allow_delete_jwt,
                resolver_preload=resolver_preload,
            )
            config_file.write_text(config_str)
            weakref.finalize(self, shutil.rmtree, config_file.parent, True)
        self.server_name = server_name
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.timeout = start_timeout
        self.http_port = http_port
        self.token = token
        self.bin_name = "nats-server"
        self.bin_path: str | None = None
        self.config_file = Path(config_file)
        self.debug = debug or os.environ.get("DEBUG_NATS_TEST", "") in (
            "true",
            "1",
            "y",
            "yes",
            "on",
        )
        self.trace = trace or os.environ.get("DEBUG_NATS_TEST", "") in (
            "true",
            "1",
            "y",
            "yes",
            "on",
        )
        self.pid_file = Path(pid_file).absolute().as_posix() if pid_file else None
        self.log_file = Path(log_file).absolute().as_posix() if log_file else None
        self.max_cpus = max_cpus
        self.clean_log_file_on_exit = clean_log_file_on_exit
        self.clean_pid_file_on_exit = clean_pid_file_on_exit
        self.tls_cert = tls_cert
        self.tls_key = tls_key
        self.tls_ca_cert = tls_ca_cert
        if self.tls_ca_cert and self.tls_cert and self.tls_key:
            self.tls_verify = True
            self.tls = False
        elif self.tls_cert and self.tls_key:
            self.tls_verify = False
            self.tls = True
        elif self.tls_ca_cert:
            raise ValueError(
                "Both certificate and key files must be provided with a CA certificate"
            )
        elif self.tls_cert or self.tls_key:
            raise ValueError("Both certificate and key files must be provided")
        else:
            self.tls = False
            self.tls_verify = False

        self.cluster_name = cluster_name
        self.cluster_url = cluster_url
        self.cluster_listen = cluster_listen
        self.routes = routes
        self.no_advertise = no_advertise

        self.jetstream_enabled = with_jetstream
        if store_directory:
            self.store_dir = Path(store_directory)
            self._store_dir_is_temporary = False
        else:
            self.store_dir = Path(tempfile.mkdtemp()).resolve(True)
            self._store_dir_is_temporary = True
            weakref.finalize(self, shutil.rmtree, self.store_dir.as_posix(), True)

        self.proc: subprocess.Popen[bytes] | None = None

    def is_alive(self) -> bool:
        """Check if the server is still running."""
        if self.proc is None:
            return False
        return self.proc.poll() is None

    def _cleanup_on_exit(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.output_writer.warning(
                "Stopping server listening on port %d." % self.port
            )
            self.kill()
        if self.clean_log_file_on_exit and self.log_file:
            if Path(self.log_file).exists():
                self.output_writer.warning(
                    "Removing log file {log_file}.".format(log_file=self.log_file)
                )
                Path(self.log_file).unlink()
        if self.clean_pid_file_on_exit and self.pid_file:
            if Path(self.pid_file).exists():
                self.output_writer.warning(
                    "Removing pid file {pid_file}.".format(pid_file=self.pid_file)
                )
                Path(self.pid_file).unlink()

    def start(self, wait: bool = False) -> "NATSD":
        """Start the server listening on the given port.

        By default this method will not wait for the server to be up and running.
        If you want to wait for the server to be up and running, set the `wait` parameter to `True`.
        """
        # Check if there is an nats-server binary in the current working directory
        if Path(self.bin_name).is_file():
            self.bin_path = Path(self.bin_name).resolve(True).as_posix()
        # Path in `../scripts/install_nats.sh`
        elif DEFAULT_BIN_DIR.joinpath(self.bin_name).is_file():
            self.bin_path = DEFAULT_BIN_DIR.joinpath(self.bin_name).as_posix()
        # This directory contains binary
        else:
            self.bin_path = shutil.which(self.bin_name)
            if self.bin_path is None:
                raise FileNotFoundError("nats-server executable not found")
        if self.debug:
            self.output_writer.debug(f"Using nats-server executable at {self.bin_path}")
        cmd = [
            self.bin_path,
        ]

        if not self.config_file.exists():
            raise FileNotFoundError(self.config_file)
        else:
            config_file = self.config_file.absolute().as_posix()
        cmd.append("--config")
        cmd.append(config_file)

        env = os.environ.copy()

        if self.max_cpus:
            env["GOMAXPROCS"] = format(self.max_cpus, ".2f")

        if self.debug:
            self.proc = subprocess.Popen(cmd, env=env)
        else:
            self.proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
            )

        if self.debug:
            self.output_writer.debug("Server listening on port %d started." % self.port)
        if wait:
            deadline = time.time() + self.timeout or float("inf")
            while True:
                status = self.proc.poll()
                if status is not None:
                    if self.debug:
                        self.output_writer.warning(
                            "Server listening on port {port} already finished running with exit {ret}".format(
                                port=self.port, ret=self.proc.returncode
                            )
                        )
                    raise subprocess.CalledProcessError(
                        returncode=self.proc.returncode, cmd=self.proc.args
                    )
                if time.time() > deadline:
                    self.stop()
                    raise TimeoutError(
                        f"nats-server failed to start before timeout ({self.timeout:.3f}s)"
                    )
                try:
                    if try_open_port(self.address or "localhost", self.port):
                        self.output_writer.debug(
                            f"Server listening on port {self.port} is up."
                        )
                        break
                    else:
                        self.output_writer.debug(
                            f"Waiting for server listening on port {self.port} to be up."
                        )
                except Exception as exc:
                    self.output_writer.debug(
                        f"Waiting for server listening on port {self.port} to be up. Last error: {type(exc).__name__} - {repr(exc)}."
                    )
                time.sleep(0.1)
                continue

        weakref.finalize(self, self._cleanup_on_exit)
        return self

    def stop(self, timeout: float | None = 10) -> None:
        """Stop the server listening on the given port.

        This will first send a `SIGINT` signal to the process and wait for it to finish.
        If the process does not finish within the given timeout, a `SIGKILL` signal will be sent.
        """
        if self.debug:
            self.output_writer.debug(f"Server listening on port {self.port} will stop.")

        if self.proc is None:
            if self.debug:
                self.output_writer.warning(
                    "Failed terminating server listening on port %d" % self.port
                )

        elif self.proc.returncode is not None and self.proc.returncode != 0:
            if self.debug:
                self.output_writer.warning(
                    "Server listening on port {port} already finished running with exit {ret}".format(
                        port=self.port, ret=self.proc.returncode
                    )
                )
        else:
            try:
                self.cancel(timeout=timeout)
            except TimeoutError:
                self.kill()
            if self.debug:
                self.output_writer.debug(
                    "Server listening on %d was stopped." % self.port
                )
        if self.proc and self.proc.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=self.proc.returncode, cmd=self.proc.args
            )

    def wait(self, timeout: float | None = None) -> int:
        """Wait for process to finish and return status code.

        Possible status codes (non-exhaustive):

        - -1: process is not started yet.
        - 0: process has been stopped after entering lame duck mode or SIGINT signal.
        - 15: process has been stopped due to TERM signal.
        - 2: process has been stopped due to QUIT signal.
        - -9: process has been stopped due to KILL signal.
        """
        if self.proc is None:
            return 0
        status = self.proc.poll()
        if status is not None:
            return status
        return self.proc.wait(timeout=timeout)

    def quit(self, timeout: float | None = None) -> None:
        """Send a `SIGQUIT` signal and wait for process to finish.

        Note:
            This method is only supported on Unix platforms.
        """
        if not self.proc:
            raise ProcessLookupError("Process is not started yet")
        self.proc.send_signal(signal.SIGQUIT)
        self.wait(timeout=timeout)

    def kill(self, timeout: float | None = None) -> None:
        """Send a `SIGKILL` signal and wait for process to finish."""
        if not self.proc:
            raise ProcessLookupError("Process is not started yet")
        self.proc.send_signal(signal.SIGKILL)
        self.wait(timeout=timeout)

    def cancel(self, timeout: float | None = 10) -> None:
        """Send a `SIGINT` signal and wait for process to finish."""
        if not self.proc:
            raise ProcessLookupError("Process is not started yet")
        self.proc.send_signal(signal.SIGINT)
        self.wait(timeout=timeout)

    def reopen_log_file(self) -> None:
        """Send a `SIGUSR1` signal to reopen log file.

        Note:
            This method is only supported on Unix platforms.
        """
        if not self.proc:
            raise ProcessLookupError("Process is not started yet")
        self.proc.send_signal(signal.SIGUSR1)

    def enter_lame_duck_mode(self) -> None:
        """Send a `SIGUSR2` signal to enter lame duck mode.

        Note:
            This method is only supported on Unix platforms.
        """
        if not self.proc:
            raise ProcessLookupError("Process is not started yet")
        self.proc.send_signal(signal.SIGUSR2)

    def reload_config(self) -> None:
        """Send a `SIGHUP` signal to reload configuration file.

        Note:
            This method is only supported on Unix platforms.
        """
        if not self.proc:
            raise ProcessLookupError("Process is not started yet")
        self.proc.send_signal(signal.SIGHUP)

    def __enter__(self) -> "NATSD":
        return self.start(wait=True)

    def __exit__(
        self,
        error_type: type[BaseException] | None = None,
        error: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ) -> None:
        self.stop()


def try_open_port(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if sock.connect_ex((host, port)) == 0:
            return True
        return False
    finally:
        sock.close()


class OutputWriter:
    def __init__(self, colorized: bool = True) -> None:
        self.colorized = colorized

    def debug(self, message: str) -> None:
        if self.colorized:
            print(f"[\033[0;33mDEBUG\033[0;0m] {message}")
        else:
            print(f"[DEBUG] {message}")

    def warning(self, message: str) -> None:
        if self.colorized:
            print(f"[\033[0;31mWARNING\033[0;0m] {message}")
        else:
            print(f"[WARNING] {message}")
