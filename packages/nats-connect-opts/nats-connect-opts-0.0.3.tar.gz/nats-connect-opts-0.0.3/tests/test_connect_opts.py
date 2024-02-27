from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import Iterator

import pytest
import trustme
from nats.aio.client import Client as NATS

from nats_contrib.connect_opts import connect, option
from nats_contrib.test_server import NATSD


@pytest.mark.asyncio
class ConnectOptsTestSetup:
    @pytest.fixture(autouse=True)
    def setup(self, nats_server: NATSD) -> None:
        self.nats_server = nats_server


class TestConnectOpts(ConnectOptsTestSetup):

    async def test_default_connect_opts(self, nats_client: NATS) -> None:
        nc = await connect(client=nats_client)
        assert nc.is_connected
        assert nc.options == {
            "allow_reconnect": True,
            "connect_timeout": 2,
            "dont_randomize": False,
            "drain_timeout": 30,
            "max_outstanding_pings": 2,
            "max_reconnect_attempts": -1,
            "name": None,
            "no_echo": False,
            "password": None,
            "pedantic": False,
            "ping_interval": 60,
            "reconnect_time_wait": 2,
            "tls_handshake_first": False,
            "token": None,
            "user": None,
            "verbose": False,
        }

    async def test_allow_reconnect_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithAllowReconnect(
                max_attempts=2,
                delay_seconds=5,
            ),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options == {
            "allow_reconnect": True,
            "connect_timeout": 2,
            "dont_randomize": False,
            "drain_timeout": 30,
            "max_outstanding_pings": 2,
            "max_reconnect_attempts": 2,
            "name": None,
            "no_echo": False,
            "password": None,
            "pedantic": False,
            "ping_interval": 60,
            "reconnect_time_wait": 5,
            "tls_handshake_first": False,
            "token": None,
            "user": None,
            "verbose": False,
        }

    async def test_callbacks_connect_option(self, nats_client: NATS) -> None:

        class Spy:
            events: list[object] = []

        async def error_cb(e: Exception) -> None:
            Spy.events.append(["error", str(e)])

        async def closed_cb() -> None:
            Spy.events.append(["closed"])

        async def disconnected_cb() -> None:
            Spy.events.append(["disconnected"])

        async def reconnected_cb() -> None:
            Spy.events.append(["reconnected"])

        nc = await connect(
            option.WithCallbacks(
                on_error=error_cb,
                on_disconnection=disconnected_cb,
                on_connection_closed=closed_cb,
                on_reconnection=reconnected_cb,
            ),
            client=nats_client,
        )
        assert nc.is_connected
        # Stop NATS server
        self.nats_server.stop()
        # Restart NATS server
        self.nats_server.start()
        # Wait for reconnection
        await asyncio.sleep(1e-3)
        assert nc._reconnection_task
        await nc._reconnection_task
        # Close NATS client
        await nc.close()
        assert nc._error_cb == error_cb
        assert nc._disconnected_cb == disconnected_cb
        assert nc._reconnected_cb == reconnected_cb
        assert nc._closed_cb == closed_cb
        assert Spy.events == [
            ["error", "nats: unexpected EOF"],
            ["disconnected"],
            ["reconnected"],
            ["disconnected"],
            ["closed"],
        ]

    async def test_connection_closed_callback_connect_option(
        self, nats_client: NATS
    ) -> None:

        class Spy:
            events: list[object] = []

        async def closed_cb() -> None:
            Spy.events.append(["closed"])

        nc = await connect(
            option.WithConnectionClosedCallback(closed_cb),
            client=nats_client,
        )
        assert nc.is_connected
        # Close NATS client
        await nc.close()
        assert nc._closed_cb == closed_cb
        assert Spy.events == [["closed"]]

    async def test_connection_name_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithConnectionName("test-connection"),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["name"] == "test-connection"

    async def test_connect_timeout_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithConnectTimeout(5),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["connect_timeout"] == 5

    async def test_deterministic_servers_connect_option(
        self, nats_client: NATS
    ) -> None:
        nc = await connect(
            option.WithDeterministicServers(),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["dont_randomize"] is True

    async def test_disallow_reconnect_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithDisallowReconnect(),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["allow_reconnect"] is False

    async def test_disconnected_callback_connect_option(
        self, nats_client: NATS
    ) -> None:

        class Spy:
            events: list[object] = []

        async def disconnected_cb() -> None:
            Spy.events.append(["disconnected"])

        nc = await connect(
            option.WithDisconnectedCallback(disconnected_cb),
            client=nats_client,
        )
        assert nc.is_connected
        # Stop NATS server
        self.nats_server.stop()
        # Wait for disconnection
        await asyncio.sleep(1e-1)
        assert nc._disconnected_cb == disconnected_cb
        assert Spy.events == [["disconnected"]]

    async def test_drain_timeout_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithDrainTimeout(60),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["drain_timeout"] == 60

    async def test_error_callback_connect_option(self, nats_client: NATS) -> None:

        class Spy:
            events: list[object] = []

        async def error_cb(e: Exception) -> None:
            Spy.events.append(["error", str(e)])

        nc = await connect(
            option.WithErrorCallback(error_cb),
            client=nats_client,
        )
        assert nc.is_connected
        # Stop NATS server
        self.nats_server.stop()
        # Wait for error
        await asyncio.sleep(1e-1)
        assert nc._error_cb == error_cb
        assert Spy.events == [["error", "nats: unexpected EOF"]]

    async def test_flusher_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithFlusher(
                queue_size=2048,
                timeout_seconds=5,
            ),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc._flush_queue
        assert nc._flush_queue.maxsize == 2048
        assert nc._flush_timeout == 5

    async def test_inbox_prefix_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithInboxPrefix("test-inbox"),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc._inbox_prefix == bytearray(b"test-inbox")

    async def test_no_echo_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithNoEcho(),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["no_echo"] is True

    async def test_pedantic_mode_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithPedanticMode(),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["pedantic"] is True

    async def test_pending_queue_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithPendingQueue(
                max_bytes=2048,
            ),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc._max_pending_size == 2048

    async def test_ping_pong_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithPingPong(
                interval=10,
                max_outstanding=4,
            ),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["ping_interval"] == 10
        assert nc.options["max_outstanding_pings"] == 4

    async def test_reconnected_callback_connect_option(self, nats_client: NATS) -> None:

        class Spy:
            events: list[object] = []

        async def reconnected_cb() -> None:
            Spy.events.append(["reconnected"])

        nc = await connect(
            option.WithReconnectedCallback(reconnected_cb),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc._reconnected_cb == reconnected_cb
        # Stop NATS server
        self.nats_server.stop()
        # Restart NATS server
        self.nats_server.start()
        # Wait for reconnection
        await asyncio.sleep(1e-3)
        assert nc._reconnection_task
        await nc._reconnection_task
        assert Spy.events == [["reconnected"]]

    async def test_server_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithServer("nats://127.0.0.1:4222"),
            client=nats_client,
        )
        assert nc.is_connected
        assert [srv.geturl() for srv in nc.servers] == ["nats://127.0.0.1:4222"]

    @pytest.mark.skip(reason="Need to start another server during test case to test")
    async def test_server_discovered_callback_connect_option(self) -> None:
        async def server_discovered_cb() -> None:
            pass

        nc = await connect(
            option.WithServerDiscoveredCallback(server_discovered_cb),
        )
        assert nc.is_connected
        assert nc._discovered_server_cb == server_discovered_cb

    async def test_servers_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithServers(
                urls=[
                    "nats://localhost:4222",
                    "nats://localhost:4223",
                ]
            ),
            option.WithDeterministicServers(),
            client=nats_client,
        )
        assert nc.is_connected
        assert set([srv.geturl() for srv in nc.servers]) == set(
            [
                "nats://localhost:4222",
                "nats://localhost:4223",
            ]
        )

    async def test_verbose_logging_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithVerboseLogging(),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["verbose"] is True


class TestTokenConnectOpts(ConnectOptsTestSetup):
    @pytest.fixture
    def natsd(self) -> NATSD:
        return NATSD(
            port=4222,
            address="localhost",
            debug=True,
            trace=True,
            trace_verbose=False,
            token="test-token",
        )

    async def test_token_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithConnectTimeout(1),
            option.WithDisallowReconnect(),
            option.WithToken("test-token"),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["token"] == "test-token"


class TestPasswordConnectOpts(ConnectOptsTestSetup):
    @pytest.fixture
    def natsd(self) -> NATSD:
        return NATSD(
            port=4222,
            address="localhost",
            debug=True,
            trace=True,
            trace_verbose=False,
            user="test-user",
            password="test-password",
        )

    async def test_username_and_password_distinct_connect_option(
        self, nats_client: NATS
    ) -> None:
        nc = await connect(
            option.WithUsername("test-user"),
            option.WithPassword("test-password"),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["user"] == "test-user"
        assert nc.options["password"] == "test-password"

    async def test_username_and_password_connect_option(
        self, nats_client: NATS
    ) -> None:
        nc = await connect(
            option.WithUserPassword(
                user="test-user",
                password="test-password",
            ),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["user"] == "test-user"
        assert nc.options["password"] == "test-password"


class TestTLSConnectOpts(ConnectOptsTestSetup):
    @pytest.fixture
    def tls_ca(self) -> trustme.CA:
        return trustme.CA()

    @pytest.fixture
    def temporary_directory(self) -> Iterator[Path]:

        path = tempfile.TemporaryDirectory()
        with path:
            yield Path(path.name)

    @pytest.fixture
    def natsd(self, tls_ca: trustme.CA, temporary_directory: Path) -> NATSD:
        cert = tls_ca.issue_cert("localhost")
        # Write server pem
        cert.private_key_and_cert_chain_pem.write_to_path(
            temporary_directory / "server.pem"
        )
        # Write server key pem
        cert.private_key_pem.write_to_path(temporary_directory / "server-key.pem")
        # Write CA pem
        tls_ca.cert_pem.write_to_path(temporary_directory / "ca.pem")
        return NATSD(
            port=4222,
            address="localhost",
            debug=True,
            trace=True,
            trace_verbose=False,
            tls_cert=temporary_directory.joinpath("server.pem"),
            tls_key=temporary_directory.joinpath("server-key.pem"),
            tls_ca_cert=temporary_directory.joinpath("ca.pem"),
        )

    async def test_tls_certificate_connect_option(
        self, nats_client: NATS, temporary_directory: Path
    ) -> None:
        nc = await connect(
            option.WithServer("tls://localhost:4222"),
            option.WithConnectTimeout(1),
            option.WithDisallowReconnect(),
            option.WithTLSCertificate(
                cert_file=temporary_directory.joinpath("server.pem").as_posix(),
                key_file=temporary_directory.joinpath("server-key.pem").as_posix(),
                ca_file=temporary_directory.joinpath("ca.pem").as_posix(),
            ),
            client=nats_client,
        )
        assert nc.is_connected


class TestConnectOptsNkey(ConnectOptsTestSetup):

    @pytest.mark.skip(reason="Need a valid nkey file to test")
    async def test_nkey_file_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithNKeyFile("path/to/nkey"),
            client=nats_client,
        )
        assert nc.is_connected

    @pytest.mark.skip(reason="Need a valid nkey seed to test")
    async def test_nkey_seed_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithNKeySeed("seed"),
            client=nats_client,
        )
        assert nc.is_connected


class TestConnectOptsJwt(ConnectOptsTestSetup):

    @pytest.mark.skip(reason="Need a valid credentials file to test")
    async def test_credentials_file_connect_option(self, nats_client: NATS) -> None:
        nc = await connect(
            option.WithCredentialsFile("path/to/credentials"),
            client=nats_client,
        )
        assert nc.is_connected
        assert nc.options["user_credential"] == "path/to/credentials"

    @pytest.mark.skip(reason="Need a valid nkey file and jwt file to test")
    async def test_nkey_file_and_jwt_file_connect_option(
        self, nats_client: NATS
    ) -> None:
        nc = await connect(
            option.WithNkeyFileAndJwtFile(
                "path/to/nkey",
                "path/to/jwt",
            ),
            client=nats_client,
        )
        assert nc.is_connected

    @pytest.mark.skip(reason="Need a valid nkey seed and jwt to test")
    async def test_with_signature_callback_connect_option(
        self, nats_client: NATS
    ) -> None:
        nc = await connect(
            option.WithSignatureCallback(
                lambda nonce: b"signature",
            ),
            client=nats_client,
        )
        assert nc.is_connected

    @pytest.mark.skip(reason="Need valid user JWT")
    async def test_with_user_jwt_callback_connect_option(
        self, nats_client: NATS
    ) -> None:
        nc = await connect(
            option.WithUserJwtCallback(
                lambda: b"jwt",
            ),
            client=nats_client,
        )
        assert nc.is_connected
