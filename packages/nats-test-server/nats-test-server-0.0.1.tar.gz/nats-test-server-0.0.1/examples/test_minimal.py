from __future__ import annotations

from typing import Iterator

import pytest
from nats.aio.client import Client

from nats_contrib.test_server import NATSD


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
