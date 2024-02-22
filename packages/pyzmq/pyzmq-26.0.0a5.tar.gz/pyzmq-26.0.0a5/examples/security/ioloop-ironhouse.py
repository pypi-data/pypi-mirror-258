#!/usr/bin/env python

'''
Ironhouse extends Stonehouse with client public key authentication.

This is the strongest security model we have today, protecting against every
attack we know about, except end-point attacks (where an attacker plants
spyware on a machine to capture data before it's encrypted, or after it's
decrypted).

This example demonstrates using the IOLoopAuthenticator.

Author: Chris Laws
'''

import asyncio
import logging
import os
import sys
from typing import List

from tornado import ioloop

import zmq
import zmq.auth
from zmq.auth.asyncio import AsyncioAuthenticator
from zmq.eventloop import zmqstream


def echo(server: zmqstream.ZMQStream, msg: List[bytes]) -> None:
    logging.debug("server recvd %s", msg)
    reply = msg + [b'World']
    logging.debug("server sending %s", reply)
    server.send_multipart(reply)


def setup_server(server_secret_file: str, endpoint: str = 'tcp://127.0.0.1:9000'):
    """setup a simple echo server with CURVE auth"""
    server = zmq.Context.instance().socket(zmq.ROUTER)

    server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
    server.curve_secretkey = server_secret
    server.curve_publickey = server_public
    server.curve_server = True  # must come before bind
    server.bind(endpoint)

    server_stream = zmqstream.ZMQStream(server)
    # simple echo
    server_stream.on_recv_stream(echo)
    return server_stream


def client_msg_recvd(msg: List[bytes]):
    logging.debug("client recvd %s", msg)
    logging.info("Ironhouse test OK")
    # stop the loop when we get the reply
    ioloop.IOLoop.current().stop()


def setup_client(
    client_secret_file: str,
    server_public_file: str,
    endpoint: str = 'tcp://127.0.0.1:9000',
):
    """setup a simple client with CURVE auth"""

    client = zmq.Context.instance().socket(zmq.DEALER)

    # We need two certificates, one for the client and one for
    # the server. The client must know the server's public key
    # to make a CURVE connection.
    client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
    client.curve_secretkey = client_secret
    client.curve_publickey = client_public

    server_public, _ = zmq.auth.load_certificate(server_public_file)
    # The client must know the server's public key to make a CURVE connection.
    client.curve_serverkey = server_public
    client.connect(endpoint)

    client_stream = zmqstream.ZMQStream(client)
    client_stream.on_recv(client_msg_recvd)
    return client_stream


async def run() -> None:
    '''Run Ironhouse example'''

    # These directories are generated by the generate_certificates script
    base_dir = os.path.dirname(__file__)
    keys_dir = os.path.join(base_dir, 'certificates')
    public_keys_dir = os.path.join(base_dir, 'public_keys')
    secret_keys_dir = os.path.join(base_dir, 'private_keys')

    if not (
        os.path.exists(keys_dir)
        and os.path.exists(public_keys_dir)
        and os.path.exists(secret_keys_dir)
    ):
        logging.critical(
            "Certificates are missing - run generate_certificates script first"
        )
        sys.exit(1)

    # Start an authenticator for this context.
    auth = AsyncioAuthenticator()
    auth.allow('127.0.0.1')
    # Tell authenticator to use the certificate in a directory
    auth.configure_curve(domain='*', location=public_keys_dir)

    server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
    server = setup_server(server_secret_file)
    server_public_file = os.path.join(public_keys_dir, "server.key")
    client_secret_file = os.path.join(secret_keys_dir, "client.key_secret")
    client = setup_client(client_secret_file, server_public_file)
    client.send(b'Hello')

    auth.start()


if __name__ == '__main__':
    if zmq.zmq_version_info() < (4, 0):
        raise RuntimeError(
            "Security is not supported in libzmq version < 4.0. libzmq version {}".format(
                zmq.zmq_version()
            )
        )

    if '-v' in sys.argv:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")

    loop = asyncio.new_event_loop()
    loop.create_task(run())
    loop.run_forever()
