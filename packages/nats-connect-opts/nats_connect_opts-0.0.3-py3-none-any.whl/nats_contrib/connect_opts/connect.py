from __future__ import annotations

from typing import TypeVar, overload

from nats.aio.client import Client

from .connect_opts import ConnectOption, ConnectOpts

CT = TypeVar("CT", bound=Client)


@overload
async def connect(
    *opt: ConnectOption,
    client: None = None,
) -> Client: ...


@overload
async def connect(
    *opt: ConnectOption,
    client: CT,
) -> CT: ...


async def connect(
    *opt: ConnectOption,
    client: Client | None = None,
) -> Client:
    """Connect to a NATS server using the provided options.

    Args:
        *opt: Options to use when connecting to the NATS server.

    Returns:
        Client: The connected client.

    Example:

        ```python
        from nats.aio.connect import connect, WithServers, WithUserPassword

        client = await connect(
            WithServer("nats://localhost:4222""),
        )
        ```
    """
    opts = ConnectOpts()
    for o in opt:
        o(opts)
    nc = client or Client()
    await nc.connect(**opts.to_dict())
    return nc
