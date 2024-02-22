import os.path

from hebill import he
from hebill.he.hs.templates import front_module, back_junior_core, back_senior_core
from flask import request, session


class index(front_module):
    def http(self):
        htm = he.hd.document()

        def server_info():
            htm.html.body.create.tag.h3('服务端信息')
            table = htm.html.body.create.component.table()
            table.attributes['border'] = 1
            table.attributes['cellspacing'] = 0

            table.body.add_row()
            table.body.row.add_cell(f'连接数量：')
            table.body.row.add_cell(f'{len(self.x.clients)}')
            table.body.add_row()
            table.body.row.add_cell(f'连接标识：')
            r = table.body.row.add_cell()
            for k, v in self.x.clients.items():
                r.create.tag.div(f'{k}')

        server_info()

        def client_info():
            htm.html.body.create.tag.h3('客户端信息')
            table = htm.html.body.create.component.table()
            table.attributes['border'] = 1
            table.attributes['cellspacing'] = 0
            table.head.row.add_cell('名称')
            table.head.row.add_cell('取值')

            def row(name, value):
                table.body.add_row()
                table.body.row.add_cell(f'{name}')
                table.body.row.add_cell(f'{value}')

            row("session_id", self.x.client().session_id)
            row("session_time_start", self.x.client().session_time_start.strftime("%Y-%m-%d %H:%M:%S"))
            row("session_time_start", self.x.client().session_time_start.astimezone().tzinfo)
            row("request_method", request.method)
            row("request_host", request.host)
            row("request_url", request.url)
            row("request_args", request.args)
            row("request_method", request.method)
            row("accept_languages", request.accept_languages)
            row("root_path", request.root_path)
            row("remote_addr", request.remote_addr)
            row("abspath(root_path)", os.path.abspath(request.root_path))
            row("permanent", session.permanent)

        client_info()

        def system_configs_info():
            htm.html.body.create.tag.h3('系统设置')
            table = htm.html.body.create.component.table()
            table.attributes['border'] = 1
            table.attributes['cellspacing'] = 0
            table.head.row.add_cell('名称')
            table.head.row.add_cell('系统取值')
            table.head.row.add_cell('实例取值')
            table.head.row.add_cell('最后取值')
            for k, v in self.x.sir_system_core.configs.system.all.items():
                table.body.add_row()
                table.body.row.add_cell(f'{k}')
                table.body.row.add_cell(f'{self.x.sir_system_core.configs.system.get(k)}')
                table.body.row.add_cell(f'{self.x.sir_system_core.configs.default.get(k)}')
                table.body.row.add_cell(f'{self.x.sir_system_core.configs.get(k)}')

        system_configs_info()

        def info(x: back_junior_core | back_senior_core):
            htm.html.body.create.tag.h3('/' + '/'.join(x.tree))
            table = htm.html.body.create.component.table()
            table.attributes['border'] = 1
            table.attributes['cellspacing'] = 0
            table.head.row.add_cell('名称')
            table.head.row.add_cell('取值')
            table.head.row.add_cell('备注')

            def row(name, value, refer='-'):
                table.body.add_row()
                table.body.row.add_cell(f'{name}')
                table.body.row.add_cell(f'{value}')
                table.body.row.add_cell(f'{refer}')

            is_junior = isinstance(x, back_junior_core)
            row('系统目录路径', x.x_path)
            if is_junior:
                row('系统设置文件', x.x_configs_file_path)
                row('系统语言目录', x.x_translations_dir_path)
            row('实例目录路径', x.path)
            if is_junior:
                row('实例设置文件', x.configs_file_path)
                row('实例语言目录', x.translations_dir_path)
            row('实例空间路径', x.namespace)

        info(self.x.sir_system_core)
        info(self.x.sir_projects_core)
        info(self.x.sir_project_core)
        info(self.x.sir_applications_core)
        info(self.x.sir_application_core)
        info(self.x.sir_modules_core)
        info(self.x)

        return htm.output()
