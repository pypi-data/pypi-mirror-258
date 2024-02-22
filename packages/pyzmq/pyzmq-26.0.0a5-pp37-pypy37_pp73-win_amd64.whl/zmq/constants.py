"""zmq constants as enums"""

import errno
import sys
from enum import Enum, IntEnum, IntFlag
from typing import List

_HAUSNUMERO = 156384712


class Errno(IntEnum):
    """libzmq error codes

    .. versionadded:: 23
    """

    EAGAIN = errno.EAGAIN
    EFAULT = errno.EFAULT
    EINVAL = errno.EINVAL

    if sys.platform.startswith("win"):
        # Windows: libzmq uses errno.h
        # while Python errno prefers WSA* variants
        # many of these were introduced to errno.h in vs2010
        # ref: https://github.com/python/cpython/blob/3.9/Modules/errnomodule.c#L10-L37
        # source: https://docs.microsoft.com/en-us/cpp/c-runtime-library/errno-constants
        ENOTSUP = 129
        EPROTONOSUPPORT = 135
        ENOBUFS = 119
        ENETDOWN = 116
        EADDRINUSE = 100
        EADDRNOTAVAIL = 101
        ECONNREFUSED = 107
        EINPROGRESS = 112
        ENOTSOCK = 128
        EMSGSIZE = 115
        EAFNOSUPPORT = 102
        ENETUNREACH = 118
        ECONNABORTED = 106
        ECONNRESET = 108
        ENOTCONN = 126
        ETIMEDOUT = 138
        EHOSTUNREACH = 110
        ENETRESET = 117

    else:
        ENOTSUP = getattr(errno, "ENOTSUP", _HAUSNUMERO + 1)
        EPROTONOSUPPORT = getattr(errno, "EPROTONOSUPPORT", _HAUSNUMERO + 2)
        ENOBUFS = getattr(errno, "ENOBUFS", _HAUSNUMERO + 3)
        ENETDOWN = getattr(errno, "ENETDOWN", _HAUSNUMERO + 4)
        EADDRINUSE = getattr(errno, "EADDRINUSE", _HAUSNUMERO + 5)
        EADDRNOTAVAIL = getattr(errno, "EADDRNOTAVAIL", _HAUSNUMERO + 6)
        ECONNREFUSED = getattr(errno, "ECONNREFUSED", _HAUSNUMERO + 7)
        EINPROGRESS = getattr(errno, "EINPROGRESS", _HAUSNUMERO + 8)
        ENOTSOCK = getattr(errno, "ENOTSOCK", _HAUSNUMERO + 9)
        EMSGSIZE = getattr(errno, "EMSGSIZE", _HAUSNUMERO + 10)
        EAFNOSUPPORT = getattr(errno, "EAFNOSUPPORT", _HAUSNUMERO + 11)
        ENETUNREACH = getattr(errno, "ENETUNREACH", _HAUSNUMERO + 12)
        ECONNABORTED = getattr(errno, "ECONNABORTED", _HAUSNUMERO + 13)
        ECONNRESET = getattr(errno, "ECONNRESET", _HAUSNUMERO + 14)
        ENOTCONN = getattr(errno, "ENOTCONN", _HAUSNUMERO + 15)
        ETIMEDOUT = getattr(errno, "ETIMEDOUT", _HAUSNUMERO + 16)
        EHOSTUNREACH = getattr(errno, "EHOSTUNREACH", _HAUSNUMERO + 17)
        ENETRESET = getattr(errno, "ENETRESET", _HAUSNUMERO + 18)

    # Native 0MQ error codes
    EFSM = _HAUSNUMERO + 51
    ENOCOMPATPROTO = _HAUSNUMERO + 52
    ETERM = _HAUSNUMERO + 53
    EMTHREAD = _HAUSNUMERO + 54


class ContextOption(IntEnum):
    """Options for Context.get/set

    .. versionadded:: 23
    """

    IO_THREADS = 1
    MAX_SOCKETS = 2
    SOCKET_LIMIT = 3
    THREAD_PRIORITY = 3
    THREAD_SCHED_POLICY = 4
    MAX_MSGSZ = 5
    MSG_T_SIZE = 6
    THREAD_AFFINITY_CPU_ADD = 7
    THREAD_AFFINITY_CPU_REMOVE = 8
    THREAD_NAME_PREFIX = 9


class SocketType(IntEnum):
    """zmq socket types

    .. versionadded:: 23
    """

    PAIR = 0
    PUB = 1
    SUB = 2
    REQ = 3
    REP = 4
    DEALER = 5
    ROUTER = 6
    PULL = 7
    PUSH = 8
    XPUB = 9
    XSUB = 10
    STREAM = 11

    # deprecated aliases
    XREQ = DEALER
    XREP = ROUTER

    # DRAFT socket types
    SERVER = 12
    CLIENT = 13
    RADIO = 14
    DISH = 15
    GATHER = 16
    SCATTER = 17
    DGRAM = 18
    PEER = 19
    CHANNEL = 20


class _OptType(Enum):
    int = 'int'
    int64 = 'int64'
    bytes = 'bytes'
    fd = 'fd'


class SocketOption(IntEnum):
    """Options for Socket.get/set

    .. versionadded:: 23
    """

    _opt_type: _OptType

    def __new__(cls, value: int, opt_type: _OptType = _OptType.int):
        """Attach option type as `._opt_type`"""
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._opt_type = opt_type
        return obj

    HWM = 1
    AFFINITY = 4, _OptType.int64
    ROUTING_ID = 5, _OptType.bytes
    SUBSCRIBE = 6, _OptType.bytes
    UNSUBSCRIBE = 7, _OptType.bytes
    RATE = 8
    RECOVERY_IVL = 9
    SNDBUF = 11
    RCVBUF = 12
    RCVMORE = 13
    FD = 14, _OptType.fd
    EVENTS = 15
    TYPE = 16
    LINGER = 17
    RECONNECT_IVL = 18
    BACKLOG = 19
    RECONNECT_IVL_MAX = 21
    MAXMSGSIZE = 22, _OptType.int64
    SNDHWM = 23
    RCVHWM = 24
    MULTICAST_HOPS = 25
    RCVTIMEO = 27
    SNDTIMEO = 28
    LAST_ENDPOINT = 32, _OptType.bytes
    ROUTER_MANDATORY = 33
    TCP_KEEPALIVE = 34
    TCP_KEEPALIVE_CNT = 35
    TCP_KEEPALIVE_IDLE = 36
    TCP_KEEPALIVE_INTVL = 37
    IMMEDIATE = 39
    XPUB_VERBOSE = 40
    ROUTER_RAW = 41
    IPV6 = 42
    MECHANISM = 43
    PLAIN_SERVER = 44
    PLAIN_USERNAME = 45, _OptType.bytes
    PLAIN_PASSWORD = 46, _OptType.bytes
    CURVE_SERVER = 47
    CURVE_PUBLICKEY = 48, _OptType.bytes
    CURVE_SECRETKEY = 49, _OptType.bytes
    CURVE_SERVERKEY = 50, _OptType.bytes
    PROBE_ROUTER = 51
    REQ_CORRELATE = 52
    REQ_RELAXED = 53
    CONFLATE = 54
    ZAP_DOMAIN = 55, _OptType.bytes
    ROUTER_HANDOVER = 56
    TOS = 57
    CONNECT_ROUTING_ID = 61, _OptType.bytes
    GSSAPI_SERVER = 62
    GSSAPI_PRINCIPAL = 63, _OptType.bytes
    GSSAPI_SERVICE_PRINCIPAL = 64, _OptType.bytes
    GSSAPI_PLAINTEXT = 65
    HANDSHAKE_IVL = 66
    SOCKS_PROXY = 68, _OptType.bytes
    XPUB_NODROP = 69
    BLOCKY = 70
    XPUB_MANUAL = 71
    XPUB_WELCOME_MSG = 72, _OptType.bytes
    STREAM_NOTIFY = 73
    INVERT_MATCHING = 74
    HEARTBEAT_IVL = 75
    HEARTBEAT_TTL = 76
    HEARTBEAT_TIMEOUT = 77
    XPUB_VERBOSER = 78
    CONNECT_TIMEOUT = 79
    TCP_MAXRT = 80
    THREAD_SAFE = 81
    MULTICAST_MAXTPDU = 84
    VMCI_BUFFER_SIZE = 85, _OptType.int64
    VMCI_BUFFER_MIN_SIZE = 86, _OptType.int64
    VMCI_BUFFER_MAX_SIZE = 87, _OptType.int64
    VMCI_CONNECT_TIMEOUT = 88
    USE_FD = 89
    GSSAPI_PRINCIPAL_NAMETYPE = 90
    GSSAPI_SERVICE_PRINCIPAL_NAMETYPE = 91
    BINDTODEVICE = 92, _OptType.bytes

    # Deprecated options and aliases
    # must not use name-assignment, must have the same value
    IDENTITY = ROUTING_ID
    CONNECT_RID = CONNECT_ROUTING_ID
    TCP_ACCEPT_FILTER = 38, _OptType.bytes
    IPC_FILTER_PID = 58
    IPC_FILTER_UID = 59
    IPC_FILTER_GID = 60
    IPV4ONLY = 31
    DELAY_ATTACH_ON_CONNECT = IMMEDIATE
    FAIL_UNROUTABLE = ROUTER_MANDATORY
    ROUTER_BEHAVIOR = ROUTER_MANDATORY

    # Draft socket options
    ZAP_ENFORCE_DOMAIN = 93
    LOOPBACK_FASTPATH = 94
    METADATA = 95, _OptType.bytes
    MULTICAST_LOOP = 96
    ROUTER_NOTIFY = 97
    XPUB_MANUAL_LAST_VALUE = 98
    SOCKS_USERNAME = 99, _OptType.bytes
    SOCKS_PASSWORD = 100, _OptType.bytes
    IN_BATCH_SIZE = 101
    OUT_BATCH_SIZE = 102
    WSS_KEY_PEM = 103, _OptType.bytes
    WSS_CERT_PEM = 104, _OptType.bytes
    WSS_TRUST_PEM = 105, _OptType.bytes
    WSS_HOSTNAME = 106, _OptType.bytes
    WSS_TRUST_SYSTEM = 107
    ONLY_FIRST_SUBSCRIBE = 108
    RECONNECT_STOP = 109
    HELLO_MSG = 110, _OptType.bytes
    DISCONNECT_MSG = 111, _OptType.bytes
    PRIORITY = 112
    # 4.3.5
    BUSY_POLL = 113
    HICCUP_MSG = 114, _OptType.bytes
    XSUB_VERBOSE_UNSUBSCRIBE = 115
    TOPICS_COUNT = 116
    NORM_MODE = 117
    NORM_UNICAST_NACK = 118
    NORM_BUFFER_SIZE = 119
    NORM_SEGMENT_SIZE = 120
    NORM_BLOCK_SIZE = 121
    NORM_NUM_PARITY = 122
    NORM_NUM_AUTOPARITY = 123
    NORM_PUSH = 124


class MessageOption(IntEnum):
    """Options on zmq.Frame objects

    .. versionadded:: 23
    """

    MORE = 1
    SHARED = 3
    # Deprecated message options
    SRCFD = 2


class Flag(IntFlag):
    """Send/recv flags

    .. versionadded:: 23
    """

    DONTWAIT = 1
    SNDMORE = 2
    NOBLOCK = DONTWAIT


class RouterNotify(IntEnum):
    """Values for zmq.ROUTER_NOTIFY socket option

    .. versionadded:: 26
    .. versionadded:: libzmq-4.3.0 (draft)
    """

    @staticmethod
    def _global_name(name):
        return f"NOTIFY_{name}"

    CONNECT = 1
    DISCONNECT = 2


class NormMode(IntEnum):
    """Values for zmq.NORM_MODE socket option

    .. versionadded:: 26
    .. versionadded:: libzmq-4.3.5 (draft)
    """

    @staticmethod
    def _global_name(name):
        return f"NORM_{name}"

    FIXED = 0
    CC = 1
    CCL = 2
    CCE = 3
    CCE_ECNONLY = 4


class SecurityMechanism(IntEnum):
    """Security mechanisms (as returned by ``socket.get(zmq.MECHANISM)``)

    .. versionadded:: 23
    """

    NULL = 0
    PLAIN = 1
    CURVE = 2
    GSSAPI = 3


class ReconnectStop(IntEnum):
    """Select behavior for socket.reconnect_stop

    .. versionadded:: 25
    """

    @staticmethod
    def _global_name(name):
        return f"RECONNECT_STOP_{name}"

    CONN_REFUSED = 0x1
    HANDSHAKE_FAILED = 0x2
    AFTER_DISCONNECT = 0x4


class Event(IntFlag):
    """Socket monitoring events

    .. versionadded:: 23
    """

    @staticmethod
    def _global_name(name):
        if name.startswith("PROTOCOL_ERROR_"):
            return name
        else:
            # add EVENT_ prefix
            return "EVENT_" + name

    PROTOCOL_ERROR_WS_UNSPECIFIED = 0x30000000
    PROTOCOL_ERROR_ZMTP_UNSPECIFIED = 0x10000000
    PROTOCOL_ERROR_ZMTP_UNEXPECTED_COMMAND = 0x10000001
    PROTOCOL_ERROR_ZMTP_INVALID_SEQUENCE = 0x10000002
    PROTOCOL_ERROR_ZMTP_KEY_EXCHANGE = 0x10000003
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED = 0x10000011
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_MESSAGE = 0x10000012
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_HELLO = 0x10000013
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_INITIATE = 0x10000014
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_ERROR = 0x10000015
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_READY = 0x10000016
    PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_WELCOME = 0x10000017
    PROTOCOL_ERROR_ZMTP_INVALID_METADATA = 0x10000018

    PROTOCOL_ERROR_ZMTP_CRYPTOGRAPHIC = 0x11000001
    PROTOCOL_ERROR_ZMTP_MECHANISM_MISMATCH = 0x11000002
    PROTOCOL_ERROR_ZAP_UNSPECIFIED = 0x20000000
    PROTOCOL_ERROR_ZAP_MALFORMED_REPLY = 0x20000001
    PROTOCOL_ERROR_ZAP_BAD_REQUEST_ID = 0x20000002
    PROTOCOL_ERROR_ZAP_BAD_VERSION = 0x20000003
    PROTOCOL_ERROR_ZAP_INVALID_STATUS_CODE = 0x20000004
    PROTOCOL_ERROR_ZAP_INVALID_METADATA = 0x20000005

    # define event types _after_ overlapping protocol error masks
    CONNECTED = 0x0001
    CONNECT_DELAYED = 0x0002
    CONNECT_RETRIED = 0x0004
    LISTENING = 0x0008
    BIND_FAILED = 0x0010
    ACCEPTED = 0x0020
    ACCEPT_FAILED = 0x0040
    CLOSED = 0x0080
    CLOSE_FAILED = 0x0100
    DISCONNECTED = 0x0200
    MONITOR_STOPPED = 0x0400

    HANDSHAKE_FAILED_NO_DETAIL = 0x0800
    HANDSHAKE_SUCCEEDED = 0x1000
    HANDSHAKE_FAILED_PROTOCOL = 0x2000
    HANDSHAKE_FAILED_AUTH = 0x4000

    ALL_V1 = 0xFFFF
    ALL = ALL_V1

    # DRAFT Socket monitoring events
    PIPES_STATS = 0x10000
    ALL_V2 = ALL_V1 | PIPES_STATS


class PollEvent(IntFlag):
    """Which events to poll for in poll methods

    .. versionadded: 23
    """

    POLLIN = 1
    POLLOUT = 2
    POLLERR = 4
    POLLPRI = 8


class DeviceType(IntEnum):
    """Device type constants for zmq.device

    .. versionadded: 23
    """

    STREAMER = 1
    FORWARDER = 2
    QUEUE = 3


# AUTOGENERATED_BELOW_HERE


IO_THREADS: int = ContextOption.IO_THREADS
MAX_SOCKETS: int = ContextOption.MAX_SOCKETS
SOCKET_LIMIT: int = ContextOption.SOCKET_LIMIT
THREAD_PRIORITY: int = ContextOption.THREAD_PRIORITY
THREAD_SCHED_POLICY: int = ContextOption.THREAD_SCHED_POLICY
MAX_MSGSZ: int = ContextOption.MAX_MSGSZ
MSG_T_SIZE: int = ContextOption.MSG_T_SIZE
THREAD_AFFINITY_CPU_ADD: int = ContextOption.THREAD_AFFINITY_CPU_ADD
THREAD_AFFINITY_CPU_REMOVE: int = ContextOption.THREAD_AFFINITY_CPU_REMOVE
THREAD_NAME_PREFIX: int = ContextOption.THREAD_NAME_PREFIX
STREAMER: int = DeviceType.STREAMER
FORWARDER: int = DeviceType.FORWARDER
QUEUE: int = DeviceType.QUEUE
EAGAIN: int = Errno.EAGAIN
EFAULT: int = Errno.EFAULT
EINVAL: int = Errno.EINVAL
ENOTSUP: int = Errno.ENOTSUP
EPROTONOSUPPORT: int = Errno.EPROTONOSUPPORT
ENOBUFS: int = Errno.ENOBUFS
ENETDOWN: int = Errno.ENETDOWN
EADDRINUSE: int = Errno.EADDRINUSE
EADDRNOTAVAIL: int = Errno.EADDRNOTAVAIL
ECONNREFUSED: int = Errno.ECONNREFUSED
EINPROGRESS: int = Errno.EINPROGRESS
ENOTSOCK: int = Errno.ENOTSOCK
EMSGSIZE: int = Errno.EMSGSIZE
EAFNOSUPPORT: int = Errno.EAFNOSUPPORT
ENETUNREACH: int = Errno.ENETUNREACH
ECONNABORTED: int = Errno.ECONNABORTED
ECONNRESET: int = Errno.ECONNRESET
ENOTCONN: int = Errno.ENOTCONN
ETIMEDOUT: int = Errno.ETIMEDOUT
EHOSTUNREACH: int = Errno.EHOSTUNREACH
ENETRESET: int = Errno.ENETRESET
EFSM: int = Errno.EFSM
ENOCOMPATPROTO: int = Errno.ENOCOMPATPROTO
ETERM: int = Errno.ETERM
EMTHREAD: int = Errno.EMTHREAD
PROTOCOL_ERROR_WS_UNSPECIFIED: int = Event.PROTOCOL_ERROR_WS_UNSPECIFIED
PROTOCOL_ERROR_ZMTP_UNSPECIFIED: int = Event.PROTOCOL_ERROR_ZMTP_UNSPECIFIED
PROTOCOL_ERROR_ZMTP_UNEXPECTED_COMMAND: int = (
    Event.PROTOCOL_ERROR_ZMTP_UNEXPECTED_COMMAND
)
PROTOCOL_ERROR_ZMTP_INVALID_SEQUENCE: int = Event.PROTOCOL_ERROR_ZMTP_INVALID_SEQUENCE
PROTOCOL_ERROR_ZMTP_KEY_EXCHANGE: int = Event.PROTOCOL_ERROR_ZMTP_KEY_EXCHANGE
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED
)
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_MESSAGE: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_MESSAGE
)
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_HELLO: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_HELLO
)
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_INITIATE: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_INITIATE
)
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_ERROR: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_ERROR
)
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_READY: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_READY
)
PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_WELCOME: int = (
    Event.PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_WELCOME
)
PROTOCOL_ERROR_ZMTP_INVALID_METADATA: int = Event.PROTOCOL_ERROR_ZMTP_INVALID_METADATA
PROTOCOL_ERROR_ZMTP_CRYPTOGRAPHIC: int = Event.PROTOCOL_ERROR_ZMTP_CRYPTOGRAPHIC
PROTOCOL_ERROR_ZMTP_MECHANISM_MISMATCH: int = (
    Event.PROTOCOL_ERROR_ZMTP_MECHANISM_MISMATCH
)
PROTOCOL_ERROR_ZAP_UNSPECIFIED: int = Event.PROTOCOL_ERROR_ZAP_UNSPECIFIED
PROTOCOL_ERROR_ZAP_MALFORMED_REPLY: int = Event.PROTOCOL_ERROR_ZAP_MALFORMED_REPLY
PROTOCOL_ERROR_ZAP_BAD_REQUEST_ID: int = Event.PROTOCOL_ERROR_ZAP_BAD_REQUEST_ID
PROTOCOL_ERROR_ZAP_BAD_VERSION: int = Event.PROTOCOL_ERROR_ZAP_BAD_VERSION
PROTOCOL_ERROR_ZAP_INVALID_STATUS_CODE: int = (
    Event.PROTOCOL_ERROR_ZAP_INVALID_STATUS_CODE
)
PROTOCOL_ERROR_ZAP_INVALID_METADATA: int = Event.PROTOCOL_ERROR_ZAP_INVALID_METADATA
EVENT_CONNECTED: int = Event.CONNECTED
EVENT_CONNECT_DELAYED: int = Event.CONNECT_DELAYED
EVENT_CONNECT_RETRIED: int = Event.CONNECT_RETRIED
EVENT_LISTENING: int = Event.LISTENING
EVENT_BIND_FAILED: int = Event.BIND_FAILED
EVENT_ACCEPTED: int = Event.ACCEPTED
EVENT_ACCEPT_FAILED: int = Event.ACCEPT_FAILED
EVENT_CLOSED: int = Event.CLOSED
EVENT_CLOSE_FAILED: int = Event.CLOSE_FAILED
EVENT_DISCONNECTED: int = Event.DISCONNECTED
EVENT_MONITOR_STOPPED: int = Event.MONITOR_STOPPED
EVENT_HANDSHAKE_FAILED_NO_DETAIL: int = Event.HANDSHAKE_FAILED_NO_DETAIL
EVENT_HANDSHAKE_SUCCEEDED: int = Event.HANDSHAKE_SUCCEEDED
EVENT_HANDSHAKE_FAILED_PROTOCOL: int = Event.HANDSHAKE_FAILED_PROTOCOL
EVENT_HANDSHAKE_FAILED_AUTH: int = Event.HANDSHAKE_FAILED_AUTH
EVENT_ALL_V1: int = Event.ALL_V1
EVENT_ALL: int = Event.ALL
EVENT_PIPES_STATS: int = Event.PIPES_STATS
EVENT_ALL_V2: int = Event.ALL_V2
DONTWAIT: int = Flag.DONTWAIT
SNDMORE: int = Flag.SNDMORE
NOBLOCK: int = Flag.NOBLOCK
MORE: int = MessageOption.MORE
SHARED: int = MessageOption.SHARED
SRCFD: int = MessageOption.SRCFD
NORM_FIXED: int = NormMode.FIXED
NORM_CC: int = NormMode.CC
NORM_CCL: int = NormMode.CCL
NORM_CCE: int = NormMode.CCE
NORM_CCE_ECNONLY: int = NormMode.CCE_ECNONLY
POLLIN: int = PollEvent.POLLIN
POLLOUT: int = PollEvent.POLLOUT
POLLERR: int = PollEvent.POLLERR
POLLPRI: int = PollEvent.POLLPRI
RECONNECT_STOP_CONN_REFUSED: int = ReconnectStop.CONN_REFUSED
RECONNECT_STOP_HANDSHAKE_FAILED: int = ReconnectStop.HANDSHAKE_FAILED
RECONNECT_STOP_AFTER_DISCONNECT: int = ReconnectStop.AFTER_DISCONNECT
NOTIFY_CONNECT: int = RouterNotify.CONNECT
NOTIFY_DISCONNECT: int = RouterNotify.DISCONNECT
NULL: int = SecurityMechanism.NULL
PLAIN: int = SecurityMechanism.PLAIN
CURVE: int = SecurityMechanism.CURVE
GSSAPI: int = SecurityMechanism.GSSAPI
HWM: int = SocketOption.HWM
AFFINITY: int = SocketOption.AFFINITY
ROUTING_ID: int = SocketOption.ROUTING_ID
SUBSCRIBE: int = SocketOption.SUBSCRIBE
UNSUBSCRIBE: int = SocketOption.UNSUBSCRIBE
RATE: int = SocketOption.RATE
RECOVERY_IVL: int = SocketOption.RECOVERY_IVL
SNDBUF: int = SocketOption.SNDBUF
RCVBUF: int = SocketOption.RCVBUF
RCVMORE: int = SocketOption.RCVMORE
FD: int = SocketOption.FD
EVENTS: int = SocketOption.EVENTS
TYPE: int = SocketOption.TYPE
LINGER: int = SocketOption.LINGER
RECONNECT_IVL: int = SocketOption.RECONNECT_IVL
BACKLOG: int = SocketOption.BACKLOG
RECONNECT_IVL_MAX: int = SocketOption.RECONNECT_IVL_MAX
MAXMSGSIZE: int = SocketOption.MAXMSGSIZE
SNDHWM: int = SocketOption.SNDHWM
RCVHWM: int = SocketOption.RCVHWM
MULTICAST_HOPS: int = SocketOption.MULTICAST_HOPS
RCVTIMEO: int = SocketOption.RCVTIMEO
SNDTIMEO: int = SocketOption.SNDTIMEO
LAST_ENDPOINT: int = SocketOption.LAST_ENDPOINT
ROUTER_MANDATORY: int = SocketOption.ROUTER_MANDATORY
TCP_KEEPALIVE: int = SocketOption.TCP_KEEPALIVE
TCP_KEEPALIVE_CNT: int = SocketOption.TCP_KEEPALIVE_CNT
TCP_KEEPALIVE_IDLE: int = SocketOption.TCP_KEEPALIVE_IDLE
TCP_KEEPALIVE_INTVL: int = SocketOption.TCP_KEEPALIVE_INTVL
IMMEDIATE: int = SocketOption.IMMEDIATE
XPUB_VERBOSE: int = SocketOption.XPUB_VERBOSE
ROUTER_RAW: int = SocketOption.ROUTER_RAW
IPV6: int = SocketOption.IPV6
MECHANISM: int = SocketOption.MECHANISM
PLAIN_SERVER: int = SocketOption.PLAIN_SERVER
PLAIN_USERNAME: int = SocketOption.PLAIN_USERNAME
PLAIN_PASSWORD: int = SocketOption.PLAIN_PASSWORD
CURVE_SERVER: int = SocketOption.CURVE_SERVER
CURVE_PUBLICKEY: int = SocketOption.CURVE_PUBLICKEY
CURVE_SECRETKEY: int = SocketOption.CURVE_SECRETKEY
CURVE_SERVERKEY: int = SocketOption.CURVE_SERVERKEY
PROBE_ROUTER: int = SocketOption.PROBE_ROUTER
REQ_CORRELATE: int = SocketOption.REQ_CORRELATE
REQ_RELAXED: int = SocketOption.REQ_RELAXED
CONFLATE: int = SocketOption.CONFLATE
ZAP_DOMAIN: int = SocketOption.ZAP_DOMAIN
ROUTER_HANDOVER: int = SocketOption.ROUTER_HANDOVER
TOS: int = SocketOption.TOS
CONNECT_ROUTING_ID: int = SocketOption.CONNECT_ROUTING_ID
GSSAPI_SERVER: int = SocketOption.GSSAPI_SERVER
GSSAPI_PRINCIPAL: int = SocketOption.GSSAPI_PRINCIPAL
GSSAPI_SERVICE_PRINCIPAL: int = SocketOption.GSSAPI_SERVICE_PRINCIPAL
GSSAPI_PLAINTEXT: int = SocketOption.GSSAPI_PLAINTEXT
HANDSHAKE_IVL: int = SocketOption.HANDSHAKE_IVL
SOCKS_PROXY: int = SocketOption.SOCKS_PROXY
XPUB_NODROP: int = SocketOption.XPUB_NODROP
BLOCKY: int = SocketOption.BLOCKY
XPUB_MANUAL: int = SocketOption.XPUB_MANUAL
XPUB_WELCOME_MSG: int = SocketOption.XPUB_WELCOME_MSG
STREAM_NOTIFY: int = SocketOption.STREAM_NOTIFY
INVERT_MATCHING: int = SocketOption.INVERT_MATCHING
HEARTBEAT_IVL: int = SocketOption.HEARTBEAT_IVL
HEARTBEAT_TTL: int = SocketOption.HEARTBEAT_TTL
HEARTBEAT_TIMEOUT: int = SocketOption.HEARTBEAT_TIMEOUT
XPUB_VERBOSER: int = SocketOption.XPUB_VERBOSER
CONNECT_TIMEOUT: int = SocketOption.CONNECT_TIMEOUT
TCP_MAXRT: int = SocketOption.TCP_MAXRT
THREAD_SAFE: int = SocketOption.THREAD_SAFE
MULTICAST_MAXTPDU: int = SocketOption.MULTICAST_MAXTPDU
VMCI_BUFFER_SIZE: int = SocketOption.VMCI_BUFFER_SIZE
VMCI_BUFFER_MIN_SIZE: int = SocketOption.VMCI_BUFFER_MIN_SIZE
VMCI_BUFFER_MAX_SIZE: int = SocketOption.VMCI_BUFFER_MAX_SIZE
VMCI_CONNECT_TIMEOUT: int = SocketOption.VMCI_CONNECT_TIMEOUT
USE_FD: int = SocketOption.USE_FD
GSSAPI_PRINCIPAL_NAMETYPE: int = SocketOption.GSSAPI_PRINCIPAL_NAMETYPE
GSSAPI_SERVICE_PRINCIPAL_NAMETYPE: int = SocketOption.GSSAPI_SERVICE_PRINCIPAL_NAMETYPE
BINDTODEVICE: int = SocketOption.BINDTODEVICE
IDENTITY: int = SocketOption.IDENTITY
CONNECT_RID: int = SocketOption.CONNECT_RID
TCP_ACCEPT_FILTER: int = SocketOption.TCP_ACCEPT_FILTER
IPC_FILTER_PID: int = SocketOption.IPC_FILTER_PID
IPC_FILTER_UID: int = SocketOption.IPC_FILTER_UID
IPC_FILTER_GID: int = SocketOption.IPC_FILTER_GID
IPV4ONLY: int = SocketOption.IPV4ONLY
DELAY_ATTACH_ON_CONNECT: int = SocketOption.DELAY_ATTACH_ON_CONNECT
FAIL_UNROUTABLE: int = SocketOption.FAIL_UNROUTABLE
ROUTER_BEHAVIOR: int = SocketOption.ROUTER_BEHAVIOR
ZAP_ENFORCE_DOMAIN: int = SocketOption.ZAP_ENFORCE_DOMAIN
LOOPBACK_FASTPATH: int = SocketOption.LOOPBACK_FASTPATH
METADATA: int = SocketOption.METADATA
MULTICAST_LOOP: int = SocketOption.MULTICAST_LOOP
ROUTER_NOTIFY: int = SocketOption.ROUTER_NOTIFY
XPUB_MANUAL_LAST_VALUE: int = SocketOption.XPUB_MANUAL_LAST_VALUE
SOCKS_USERNAME: int = SocketOption.SOCKS_USERNAME
SOCKS_PASSWORD: int = SocketOption.SOCKS_PASSWORD
IN_BATCH_SIZE: int = SocketOption.IN_BATCH_SIZE
OUT_BATCH_SIZE: int = SocketOption.OUT_BATCH_SIZE
WSS_KEY_PEM: int = SocketOption.WSS_KEY_PEM
WSS_CERT_PEM: int = SocketOption.WSS_CERT_PEM
WSS_TRUST_PEM: int = SocketOption.WSS_TRUST_PEM
WSS_HOSTNAME: int = SocketOption.WSS_HOSTNAME
WSS_TRUST_SYSTEM: int = SocketOption.WSS_TRUST_SYSTEM
ONLY_FIRST_SUBSCRIBE: int = SocketOption.ONLY_FIRST_SUBSCRIBE
RECONNECT_STOP: int = SocketOption.RECONNECT_STOP
HELLO_MSG: int = SocketOption.HELLO_MSG
DISCONNECT_MSG: int = SocketOption.DISCONNECT_MSG
PRIORITY: int = SocketOption.PRIORITY
BUSY_POLL: int = SocketOption.BUSY_POLL
HICCUP_MSG: int = SocketOption.HICCUP_MSG
XSUB_VERBOSE_UNSUBSCRIBE: int = SocketOption.XSUB_VERBOSE_UNSUBSCRIBE
TOPICS_COUNT: int = SocketOption.TOPICS_COUNT
NORM_MODE: int = SocketOption.NORM_MODE
NORM_UNICAST_NACK: int = SocketOption.NORM_UNICAST_NACK
NORM_BUFFER_SIZE: int = SocketOption.NORM_BUFFER_SIZE
NORM_SEGMENT_SIZE: int = SocketOption.NORM_SEGMENT_SIZE
NORM_BLOCK_SIZE: int = SocketOption.NORM_BLOCK_SIZE
NORM_NUM_PARITY: int = SocketOption.NORM_NUM_PARITY
NORM_NUM_AUTOPARITY: int = SocketOption.NORM_NUM_AUTOPARITY
NORM_PUSH: int = SocketOption.NORM_PUSH
PAIR: int = SocketType.PAIR
PUB: int = SocketType.PUB
SUB: int = SocketType.SUB
REQ: int = SocketType.REQ
REP: int = SocketType.REP
DEALER: int = SocketType.DEALER
ROUTER: int = SocketType.ROUTER
PULL: int = SocketType.PULL
PUSH: int = SocketType.PUSH
XPUB: int = SocketType.XPUB
XSUB: int = SocketType.XSUB
STREAM: int = SocketType.STREAM
XREQ: int = SocketType.XREQ
XREP: int = SocketType.XREP
SERVER: int = SocketType.SERVER
CLIENT: int = SocketType.CLIENT
RADIO: int = SocketType.RADIO
DISH: int = SocketType.DISH
GATHER: int = SocketType.GATHER
SCATTER: int = SocketType.SCATTER
DGRAM: int = SocketType.DGRAM
PEER: int = SocketType.PEER
CHANNEL: int = SocketType.CHANNEL

__all__: List[str] = [
    "ContextOption",
    "IO_THREADS",
    "MAX_SOCKETS",
    "SOCKET_LIMIT",
    "THREAD_PRIORITY",
    "THREAD_SCHED_POLICY",
    "MAX_MSGSZ",
    "MSG_T_SIZE",
    "THREAD_AFFINITY_CPU_ADD",
    "THREAD_AFFINITY_CPU_REMOVE",
    "THREAD_NAME_PREFIX",
    "DeviceType",
    "STREAMER",
    "FORWARDER",
    "QUEUE",
    "Enum",
    "Errno",
    "EAGAIN",
    "EFAULT",
    "EINVAL",
    "ENOTSUP",
    "EPROTONOSUPPORT",
    "ENOBUFS",
    "ENETDOWN",
    "EADDRINUSE",
    "EADDRNOTAVAIL",
    "ECONNREFUSED",
    "EINPROGRESS",
    "ENOTSOCK",
    "EMSGSIZE",
    "EAFNOSUPPORT",
    "ENETUNREACH",
    "ECONNABORTED",
    "ECONNRESET",
    "ENOTCONN",
    "ETIMEDOUT",
    "EHOSTUNREACH",
    "ENETRESET",
    "EFSM",
    "ENOCOMPATPROTO",
    "ETERM",
    "EMTHREAD",
    "Event",
    "PROTOCOL_ERROR_WS_UNSPECIFIED",
    "PROTOCOL_ERROR_ZMTP_UNSPECIFIED",
    "PROTOCOL_ERROR_ZMTP_UNEXPECTED_COMMAND",
    "PROTOCOL_ERROR_ZMTP_INVALID_SEQUENCE",
    "PROTOCOL_ERROR_ZMTP_KEY_EXCHANGE",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_MESSAGE",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_HELLO",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_INITIATE",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_ERROR",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_READY",
    "PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_WELCOME",
    "PROTOCOL_ERROR_ZMTP_INVALID_METADATA",
    "PROTOCOL_ERROR_ZMTP_CRYPTOGRAPHIC",
    "PROTOCOL_ERROR_ZMTP_MECHANISM_MISMATCH",
    "PROTOCOL_ERROR_ZAP_UNSPECIFIED",
    "PROTOCOL_ERROR_ZAP_MALFORMED_REPLY",
    "PROTOCOL_ERROR_ZAP_BAD_REQUEST_ID",
    "PROTOCOL_ERROR_ZAP_BAD_VERSION",
    "PROTOCOL_ERROR_ZAP_INVALID_STATUS_CODE",
    "PROTOCOL_ERROR_ZAP_INVALID_METADATA",
    "EVENT_CONNECTED",
    "EVENT_CONNECT_DELAYED",
    "EVENT_CONNECT_RETRIED",
    "EVENT_LISTENING",
    "EVENT_BIND_FAILED",
    "EVENT_ACCEPTED",
    "EVENT_ACCEPT_FAILED",
    "EVENT_CLOSED",
    "EVENT_CLOSE_FAILED",
    "EVENT_DISCONNECTED",
    "EVENT_MONITOR_STOPPED",
    "EVENT_HANDSHAKE_FAILED_NO_DETAIL",
    "EVENT_HANDSHAKE_SUCCEEDED",
    "EVENT_HANDSHAKE_FAILED_PROTOCOL",
    "EVENT_HANDSHAKE_FAILED_AUTH",
    "EVENT_ALL_V1",
    "EVENT_ALL",
    "EVENT_PIPES_STATS",
    "EVENT_ALL_V2",
    "Flag",
    "DONTWAIT",
    "SNDMORE",
    "NOBLOCK",
    "IntEnum",
    "IntFlag",
    "MessageOption",
    "MORE",
    "SHARED",
    "SRCFD",
    "NormMode",
    "NORM_FIXED",
    "NORM_CC",
    "NORM_CCL",
    "NORM_CCE",
    "NORM_CCE_ECNONLY",
    "PollEvent",
    "POLLIN",
    "POLLOUT",
    "POLLERR",
    "POLLPRI",
    "ReconnectStop",
    "RECONNECT_STOP_CONN_REFUSED",
    "RECONNECT_STOP_HANDSHAKE_FAILED",
    "RECONNECT_STOP_AFTER_DISCONNECT",
    "RouterNotify",
    "NOTIFY_CONNECT",
    "NOTIFY_DISCONNECT",
    "SecurityMechanism",
    "NULL",
    "PLAIN",
    "CURVE",
    "GSSAPI",
    "SocketOption",
    "HWM",
    "AFFINITY",
    "ROUTING_ID",
    "SUBSCRIBE",
    "UNSUBSCRIBE",
    "RATE",
    "RECOVERY_IVL",
    "SNDBUF",
    "RCVBUF",
    "RCVMORE",
    "FD",
    "EVENTS",
    "TYPE",
    "LINGER",
    "RECONNECT_IVL",
    "BACKLOG",
    "RECONNECT_IVL_MAX",
    "MAXMSGSIZE",
    "SNDHWM",
    "RCVHWM",
    "MULTICAST_HOPS",
    "RCVTIMEO",
    "SNDTIMEO",
    "LAST_ENDPOINT",
    "ROUTER_MANDATORY",
    "TCP_KEEPALIVE",
    "TCP_KEEPALIVE_CNT",
    "TCP_KEEPALIVE_IDLE",
    "TCP_KEEPALIVE_INTVL",
    "IMMEDIATE",
    "XPUB_VERBOSE",
    "ROUTER_RAW",
    "IPV6",
    "MECHANISM",
    "PLAIN_SERVER",
    "PLAIN_USERNAME",
    "PLAIN_PASSWORD",
    "CURVE_SERVER",
    "CURVE_PUBLICKEY",
    "CURVE_SECRETKEY",
    "CURVE_SERVERKEY",
    "PROBE_ROUTER",
    "REQ_CORRELATE",
    "REQ_RELAXED",
    "CONFLATE",
    "ZAP_DOMAIN",
    "ROUTER_HANDOVER",
    "TOS",
    "CONNECT_ROUTING_ID",
    "GSSAPI_SERVER",
    "GSSAPI_PRINCIPAL",
    "GSSAPI_SERVICE_PRINCIPAL",
    "GSSAPI_PLAINTEXT",
    "HANDSHAKE_IVL",
    "SOCKS_PROXY",
    "XPUB_NODROP",
    "BLOCKY",
    "XPUB_MANUAL",
    "XPUB_WELCOME_MSG",
    "STREAM_NOTIFY",
    "INVERT_MATCHING",
    "HEARTBEAT_IVL",
    "HEARTBEAT_TTL",
    "HEARTBEAT_TIMEOUT",
    "XPUB_VERBOSER",
    "CONNECT_TIMEOUT",
    "TCP_MAXRT",
    "THREAD_SAFE",
    "MULTICAST_MAXTPDU",
    "VMCI_BUFFER_SIZE",
    "VMCI_BUFFER_MIN_SIZE",
    "VMCI_BUFFER_MAX_SIZE",
    "VMCI_CONNECT_TIMEOUT",
    "USE_FD",
    "GSSAPI_PRINCIPAL_NAMETYPE",
    "GSSAPI_SERVICE_PRINCIPAL_NAMETYPE",
    "BINDTODEVICE",
    "IDENTITY",
    "CONNECT_RID",
    "TCP_ACCEPT_FILTER",
    "IPC_FILTER_PID",
    "IPC_FILTER_UID",
    "IPC_FILTER_GID",
    "IPV4ONLY",
    "DELAY_ATTACH_ON_CONNECT",
    "FAIL_UNROUTABLE",
    "ROUTER_BEHAVIOR",
    "ZAP_ENFORCE_DOMAIN",
    "LOOPBACK_FASTPATH",
    "METADATA",
    "MULTICAST_LOOP",
    "ROUTER_NOTIFY",
    "XPUB_MANUAL_LAST_VALUE",
    "SOCKS_USERNAME",
    "SOCKS_PASSWORD",
    "IN_BATCH_SIZE",
    "OUT_BATCH_SIZE",
    "WSS_KEY_PEM",
    "WSS_CERT_PEM",
    "WSS_TRUST_PEM",
    "WSS_HOSTNAME",
    "WSS_TRUST_SYSTEM",
    "ONLY_FIRST_SUBSCRIBE",
    "RECONNECT_STOP",
    "HELLO_MSG",
    "DISCONNECT_MSG",
    "PRIORITY",
    "BUSY_POLL",
    "HICCUP_MSG",
    "XSUB_VERBOSE_UNSUBSCRIBE",
    "TOPICS_COUNT",
    "NORM_MODE",
    "NORM_UNICAST_NACK",
    "NORM_BUFFER_SIZE",
    "NORM_SEGMENT_SIZE",
    "NORM_BLOCK_SIZE",
    "NORM_NUM_PARITY",
    "NORM_NUM_AUTOPARITY",
    "NORM_PUSH",
    "SocketType",
    "PAIR",
    "PUB",
    "SUB",
    "REQ",
    "REP",
    "DEALER",
    "ROUTER",
    "PULL",
    "PUSH",
    "XPUB",
    "XSUB",
    "STREAM",
    "XREQ",
    "XREP",
    "SERVER",
    "CLIENT",
    "RADIO",
    "DISH",
    "GATHER",
    "SCATTER",
    "DGRAM",
    "PEER",
    "CHANNEL",
]
