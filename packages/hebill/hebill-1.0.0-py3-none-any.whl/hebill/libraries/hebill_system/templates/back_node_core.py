import os
from ..system.clients.core import core as client_core
from flask import session
from ..__constants__ import SN_ID


class back_node_core:
    def __init__(self, x_file, senior, name, path=None):
        self._x_file = x_file
        self._x_path = os.path.dirname(os.path.abspath(x_file))
        self._senior = senior
        self._name = name
        self._tree = None
        self._path = path
        self._namespace = None
        self.__cmd = None
        self._clients = {}
        pass

    @property
    def x_path(self):
        return self._x_path

    @property
    def senior(self):
        return self._senior

    @property
    def name(self):
        return self._name

    @property
    def tree(self) -> list:
        if self._tree is None:
            if self.senior is None:
                self._tree = [self.name]
            else:
                self._tree = [*self.senior.tree, self.name]
        return self._tree

    @property
    def path(self) -> str:
        if self._path is None:
            if self.senior is not None:
                self._path = os.path.join(self.senior.path, self.name)
        return self._path

    @property
    def namespace(self) -> str:
        if self._namespace is None:
            if self.senior is None:
                self._namespace = self.name
            else:
                self._namespace = ".".join([self.senior.namespace, self.name])
        return self._namespace

    @property
    def clients(self):
        if self.senior is not None:
            return self.senior.clients
        return self._clients

    def client(self, session_id=None) -> client_core:
        if self.senior is not None:
            return self.senior.client(session_id)
        if session_id is None:
            session_id = session[SN_ID]
        if session_id not in self._clients:
            self._clients[session_id] = client_core(session_id)
        return self._clients[session_id]

    ####################################################################################################
    # 命令对话
    ####################################################################################################
    @property
    def _cmd(self):
        if self.__cmd is None:
            from ....libraries.terminal_command.main import terminal_command
            self.__cmd = terminal_command()
            self.__cmd.prompt = "/".join(self.tree)
        return self.__cmd
