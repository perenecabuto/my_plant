# -*- coding: utf-8 -*-

import bluetooth


class BluetoothConn(object):

    MAX_ATTEMPTS = 3

    def __init__(self, addr):
        self._addr = addr

    @property
    def addr(self):
        return self._addr

    @property
    def sock(self):
        cls = type(self)

        if not getattr(cls, '_sock', None):
            cls._sock = self.get_sock()

        return cls._sock

    def get_sock(self, attempt=0):
        if attempt > self.MAX_ATTEMPTS:
            return

        sock = bluetooth.BluetoothSocket()

        try:
            sock.connect((self.addr, 1))
        except bluetooth.BluetoothError:
            sock.close()
            return self.get_sock(attempt + 1)

        return sock

    def close_sock(self):
        cls = type(self)

        if getattr(cls, '_sock', None):
            cls._sock.close()
            cls._sock = None

    def __enter__(self):
        return self.sock

    def __exit__(self, type_, value, traceback):
        if isinstance(value, bluetooth.BluetoothError):
            self.close_sock()

    def __del__(self):
        print "! Closing conn to %s " % self.addr
        self.close_sock()
