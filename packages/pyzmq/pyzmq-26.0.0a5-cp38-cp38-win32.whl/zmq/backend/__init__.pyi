from typing import Any, Callable, List, Optional, Set, Tuple, TypeVar, Union, overload

from typing_extensions import Literal

import zmq

from .select import select_backend

# avoid collision in Frame.bytes
_bytestr = bytes

T = TypeVar("T")

class Frame:
    buffer: Any
    bytes: bytes
    more: bool
    tracker: Any
    def __init__(
        self,
        data: Any = None,
        track: bool = False,
        copy: Optional[bool] = None,
        copy_threshold: Optional[int] = None,
    ): ...
    def copy_fast(self: T) -> T: ...
    def get(self, option: int) -> Union[int, _bytestr, str]: ...
    def set(self, option: int, value: Union[int, _bytestr, str]) -> None: ...

class Socket:
    underlying: int
    context: "zmq.Context"
    copy_threshold: int

    # specific option types
    FD: int

    def __init__(
        self,
        context: Optional[Context] = None,
        socket_type: int = 0,
        shadow: int = 0,
        copy_threshold: Optional[int] = zmq.COPY_THRESHOLD,
    ) -> None: ...
    def close(self, linger: Optional[int] = ...) -> None: ...
    def get(self, option: int) -> Union[int, bytes, str]: ...
    def set(self, option: int, value: Union[int, bytes, str]) -> None: ...
    def connect(self, url: str): ...
    def disconnect(self, url: str) -> None: ...
    def bind(self, url: str): ...
    def unbind(self, url: str) -> None: ...
    def send(
        self,
        data: Any,
        flags: int = ...,
        copy: bool = ...,
        track: bool = ...,
    ) -> Optional["zmq.MessageTracker"]: ...
    @overload
    def recv(
        self,
        flags: int = ...,
        *,
        copy: Literal[False],
        track: bool = ...,
    ) -> "zmq.Frame": ...
    @overload
    def recv(
        self,
        flags: int = ...,
        *,
        copy: Literal[True],
        track: bool = ...,
    ) -> bytes: ...
    @overload
    def recv(
        self,
        flags: int = ...,
        track: bool = False,
    ) -> bytes: ...
    @overload
    def recv(
        self,
        flags: Optional[int] = ...,
        copy: bool = ...,
        track: Optional[bool] = False,
    ) -> Union["zmq.Frame", bytes]: ...
    def monitor(self, addr: Optional[str], events: int) -> None: ...
    # draft methods
    def join(self, group: str) -> None: ...
    def leave(self, group: str) -> None: ...

class Context:
    underlying: int
    def __init__(self, io_threads: int = 1, shadow: int = 0): ...
    def get(self, option: int) -> Union[int, bytes, str]: ...
    def set(self, option: int, value: Union[int, bytes, str]) -> None: ...
    def socket(self, socket_type: int) -> Socket: ...
    def term(self) -> None: ...

IPC_PATH_MAX_LEN: int

def has(capability: str) -> bool: ...
def curve_keypair() -> Tuple[bytes, bytes]: ...
def curve_public(secret_key: bytes) -> bytes: ...
def strerror(errno: Optional[int] = ...) -> str: ...
def zmq_errno() -> int: ...
def zmq_version() -> str: ...
def zmq_version_info() -> Tuple[int, int, int]: ...
def zmq_poll(
    sockets: List[Any], timeout: Optional[int] = ...
) -> List[Tuple[Socket, int]]: ...
def device(
    device_type: int, frontend: Socket, backend: Optional[Socket] = ...
) -> int: ...
def proxy(
    frontend: Socket, backend: Socket, capture: Optional[Socket] = None
) -> int: ...
def proxy_steerable(
    frontend: Socket,
    backend: Socket,
    capture: Optional[Socket] = ...,
    control: Optional[Socket] = ...,
) -> int: ...

monitored_queue = Optional[Callable]
