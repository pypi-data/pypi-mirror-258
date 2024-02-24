# NATS Connect Opts

!!! warning "This is not an official NATS project"
    This is a personal project and is not endorsed by the NATS.io community. It is not guaranteed to be maintained or supported.

!!! bug "This is an experimental project"
    This project is a prototype and should not be used for anything serious. It is not tested, nor is it guaranteed to be correct.


## References

- The [test fixture from nats-py](https://nats-io.github.io/nats.py/modules.html#nats.aio.client.Client.connect).


## How to install

<!-- termynal -->

```bash
$ pip install git+https://github.com/charbonnierg/nats-test-server.git
```

## Example usage

``` py linenums="1" title="examples/minimal.py"
from __future__ import annotations
from typing import Iterator

import pytest

from nats_contrib.test_server import NATSD
from nats.aio.client import Client


@pytest.fixture
def nats_server() -> Iterator[NATSD]:
    with NATSD(
        port=4222,
        address="localhost",
        client_advertise="localhost:4222",
        server_name="test-server-01",
        server_tags={"region": "test01"},
        debug=True,
        trace=True,
        trace_verbose=False,
        http_port=8222,
        websocket_listen_address="localhost",
        websocket_listen_port=10080,
        leafnodes_listen_port=7422,
        pid_file="server/nats-server.pid",
        ports_file_dir="server",
    ) as server:
        yield server


@pytest.mark.asyncio
async def test_something(nats_server: NATSD) -> None:
    """You can use nats_server fixture in your tests."""
    # Do something with NATS server
    assert nats_server.is_alive()
    # Create a client
    client = Client()
    # Connect to the server
    await client.connect("nats://localhost:4222")
    # Do something with the client
    async with client:
        await client.publish("foo")
```

Run the tests using `pytest` with the `-s` option to capture the standard output and standard error:

<!-- termynal -->

```bash
$ pytest examples/ -s
========================== test session starts ==========================
platform linux -- Python 3.10.12, pytest-8.0.1, pluggy-1.4.0
rootdir: ~/github/charbonats/nats-test-server
configfile: setup.cfg
plugins: cov-4.1.0, asyncio-0.23.5
asyncio: mode=strict
collected 1 item                                                        

examples/test_minimal.py [DEBUG] Using nats-server executable at /usr/local/bin/nats-server
[DEBUG] Server listening on port 4222 started.
[DEBUG] Waiting for server listening on port 4222 to be up.
[191036] 2024/02/21 08:05:24.735483 [INF] Starting nats-server
[191036] 2024/02/21 08:05:24.735746 [INF]   Version:  2.10.10
[191036] 2024/02/21 08:05:24.735755 [INF]   Git:      [983a1d2]
[191036] 2024/02/21 08:05:24.735764 [DBG]   Go build: go1.21.6
[191036] 2024/02/21 08:05:24.735773 [INF]   Name:     test-server-01
[191036] 2024/02/21 08:05:24.735779 [INF]   ID:       NDW35OXDBEEFAAF5NZGU56WU3K5KXAGI4RNHDF6L5ZVDXIA4UON76UQX
[191036] 2024/02/21 08:05:24.735828 [INF] Using configuration file: /tmp/tmprm9ln40r/nats.conf
[191036] 2024/02/21 08:05:24.736046 [DBG] Created system account: "$SYS"
[191036] 2024/02/21 08:05:24.737235 [INF] Listening for websocket clients on ws://localhost:10080
[191036] 2024/02/21 08:05:24.737437 [WRN] Websocket not configured with TLS. DO NOT USE IN PRODUCTION!
[191036] 2024/02/21 08:05:24.737653 [INF] Listening for leafnode connections on 0.0.0.0:7422
[191036] 2024/02/21 08:05:24.737911 [DBG] Get non local IPs for "0.0.0.0"
[191036] 2024/02/21 08:05:24.738215 [DBG]   ip=172.31.93.60
[191036] 2024/02/21 08:05:24.738282 [DBG]   ip=172.17.0.1
[191036] 2024/02/21 08:05:24.739004 [INF] Listening for client connections on localhost:4222
[191036] 2024/02/21 08:05:24.739132 [INF] Server is ready
[191036] 2024/02/21 08:05:24.739986 [DBG] maxprocs: Leaving GOMAXPROCS=4: CPU quota undefined
[DEBUG] Server listening on port 4222 is up.
[191036] 2024/02/21 08:05:24.832027 [DBG] 127.0.0.1:51680 - cid:5 - Client connection created
[191036] 2024/02/21 08:05:24.833198 [DBG] 127.0.0.1:51680 - cid:5 - Client connection closed: Client Closed
[191036] 2024/02/21 08:05:24.881211 [DBG] 127.0.0.1:51694 - cid:6 - Client connection created
[191036] 2024/02/21 08:05:24.883853 [DBG] 127.0.0.1:51694 - cid:6 - Client connection closed: Client Closed
.[DEBUG] Server listening on port 4222 will stop.
[191036] 2024/02/21 08:05:24.886733 [DBG] Trapped "interrupt" signal
[191036] 2024/02/21 08:05:24.887181 [INF] Initiating Shutdown...
[191036] 2024/02/21 08:05:24.887399 [DBG] Leafnode accept loop exiting..
[191036] 2024/02/21 08:05:24.887673 [DBG] Client accept loop exiting..
[191036] 2024/02/21 08:05:24.887699 [DBG] SYSTEM - System connection closed: Client Closed
[191036] 2024/02/21 08:05:24.887990 [INF] Server Exiting..
[DEBUG] Server listening on 4222 was stopped.


=========================== 1 passed in 0.31s ===========================
```

## Other works

- [NATS Micro](https://charbonats.github.io/nats-micro): An NATS micro framework in Python.

- [NATS Request Many](https://charbonats.github.io/nats-request-many): A Python impementation of the Request Many pattern in NATS.

- [NATS Connect Opts](https://charbonats.github.io/nats-connect-opts): An opinionated way to connect to NATS in Python.
