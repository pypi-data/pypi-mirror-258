import os
import sys
import bcrypt
from ..templates.back_junior_core import back_junior_core
from ..__constants__ import (ROOT_DIR_NAME, PASSWORD_FILE_NAME, PASSWORD_DEFAULT, INSTANCE_RUN_HTTP_FILE_NAME,
                             INSTANCE_REQUIREMENTS_FILE_NAME, BACK_INITIALIZE_DIR_NAME)


class core(back_junior_core):
    def __init__(self):
        root_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ROOT_DIR_NAME)
        super().__init__(__file__, None, ROOT_DIR_NAME, root_path)
        self._jun_projects_core = None
        self._x_password_file_path = None
        self._x_password = None

    ####################################################################################################
    @property
    def x_password_file_path(self):
        if self._x_password_file_path is None:
            self._x_password_file_path = os.path.join(self.x_path, PASSWORD_FILE_NAME)
        return self._x_password_file_path

    @property
    def x_password(self):
        if self._x_password is None:
            from ...utility_functions.file.is_exists import is_exists
            from ...utility_functions.file.read import read
            if not is_exists(self.x_password_file_path):
                self.set_x_password(PASSWORD_DEFAULT)
            else:
                self._x_password = read(self.x_password_file_path)
        return self._x_password

    def set_x_password(self, password) -> bool:
        if password is not str or password == "":
            return False
        from ...utility_functions.file.write import write
        if not write(self.x_password_file_path, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())):
            return False
        return True

    def x_password_verify(self, password):
        if password is not str or password == "":
            return False
        if bcrypt.checkpw(password.encode('utf-8'), self.x_password):
            return True
        return False

    ####################################################################################################
    @property
    def jun_projects_core(self):
        if self._jun_projects_core is None:
            from .projects.core import core
            self._jun_projects_core = core(self)
        return self._jun_projects_core

    def jun_project_core(self, name):
        return self.jun_projects_core.jun_project_core(name)

    ####################################################################################################
    @property
    def configs(self):
        if self._configs is None:
            from .configs.multiple_configs import multiple_configs
            self._configs = multiple_configs(self.x_configs_file_path, self.configs_file_path)
        return self._configs

    ####################################################################################################
    def http(self):
        return "Welcome to hews"

    def console(self, langauge='zh-CN'):
        ln = self.x_translations.package(langauge)
        self._cmd.print_success(ln.get('console_welcome_message'))
        self._console_help(ln)
        self._cmd.print_success(ln.get('console_current_node').format(node=self.namespace))
        loop = True
        while loop:
            cs = self._cmd.input("").split()
            if len(cs) < 1 or cs[0] == "":
                continue
            match cs[0]:
                case "help":
                    self._console_help(ln)
                case "install":
                    self._console_install(ln, cs)
                case "projects":
                    self._console_install(ln, cs)
                case "exit":
                    self._console_exit(ln)
                    return

    def _console_help(self, ln):
        self._cmd.print_info(ln.get('console_help_help'))
        self._cmd.print_info(ln.get('console_help_install'))
        self._cmd.print_info(ln.get('console_help_projects'))
        self._cmd.print_info(ln.get('console_help_exit'))

    def _console_install(self, ln, cs):
        path = None
        terminal_path = os.getcwd()
        if len(cs) > 1:
            path = cs[1]
        else:
            self._cmd.print_warning(ln.get('console_sys_init_input_path_none').format(path=terminal_path))
            c = self._cmd.input(ln.get('console_sys_init_input_path_none_crt_path_confirm'))
            if c.lower() == "y":
                path = terminal_path
        if path is None:
            self._cmd.print_danger(ln.get('console_sys_init_path_none_canceled'))
            return
        if not os.path.isdir(path):
            self._cmd.print_danger(ln.get('console_sys_init_path_un_exists').format(path=path))
            self._cmd.print_danger(ln.get('console_sys_init_failed'))
            return
        if not os.access(path, os.W_OK):
            self._cmd.print_danger(ln.get('console_sys_init_path_un_writable').format(path=path))
            self._cmd.print_danger(ln.get('console_sys_init_failed'))
            return
        from ...utility_functions.dir.sub_path import sub_path
        from ...utility_functions.dir.sir_dir_path import sir_dir_path
        from ...utility_functions.file.is_exists import is_exists as is_file_exists
        from ...utility_functions.dir.is_exists import is_exists as is_dir_exists
        from ...utility_functions.dir.copy import copy as dir_copy
        from ...utility_functions.file.copy import copy as file_copy
        files = [
            INSTANCE_RUN_HTTP_FILE_NAME,
            INSTANCE_REQUIREMENTS_FILE_NAME,
        ]
        dirs = [
            ROOT_DIR_NAME
        ]
        files_existed = []
        dirs_existed = []
        for i in files:
            f = sub_path(path, i)
            if is_file_exists(f):
                files_existed.append(f)
        for i in dirs:
            f = sub_path(path, i)
            if is_dir_exists(f):
                dirs_existed.append(f)
        if len(files_existed) > 0 or len(dirs_existed) > 0:
            if len(files_existed) > 0:
                self._cmd.print_danger(ln.get('console_sys_init_some_files_existed'))
                for i in files_existed:
                    self._cmd.print_danger(' - ' + i)
            if len(dirs_existed) > 0:
                self._cmd.print_danger(ln.get('console_sys_init_some_dirs_existed'))
                for i in dirs_existed:
                    self._cmd.print_danger(' - ' + i)
            self._cmd.print_danger(ln.get('console_sys_init_failed'))
            return
        initialize_path = sub_path(sir_dir_path(sir_dir_path(__file__)), BACK_INITIALIZE_DIR_NAME)
        for i in files:
            ft = sub_path(path, i)
            ff = sub_path(initialize_path, i)
            if not file_copy(ff, ft):
                self._cmd.print_danger(ln.get('console_sys_init_copy_file_failed').format(path=ft))
                self._cmd.print_danger(ln.get('console_sys_init_failed'))
                return
            else:
                self._cmd.print_success(ln.get('console_sys_init_copy_file_success').format(path=ft))
        for i in dirs:
            ft = sub_path(path, i)
            ff = sub_path(initialize_path, i)
            if not dir_copy(ff, ft):
                self._cmd.print_danger(ln.get('console_sys_init_copy_dir_failed').format(path=ft))
                self._cmd.print_danger(ln.get('console_sys_init_failed'))
                return
            else:
                self._cmd.print_success(ln.get('console_sys_init_copy_dir_success').format(path=ft))
        self._cmd.print_success(ln.get('console_sys_init_success'))

    def _console_projects(self):
        self.jun_projects_core.console()

    def _console_exit(self, ln):
        self._cmd.print_warning(ln.get('console_exited_info'))
