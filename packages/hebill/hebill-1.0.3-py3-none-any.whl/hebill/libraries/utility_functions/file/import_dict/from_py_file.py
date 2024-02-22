import sys
import importlib.machinery
"""
    注意，被导入的文件里不要有相对路径import
    """


def from_py_file(file: str, name: str) -> dict | None:
    result = None
    from .....libraries.hebill_system.system.__configs__ import configs
    try:
        loader = importlib.machinery.SourceFileLoader(name, file)
        loaded_module = loader.load_module()
        loaded_attr = getattr(loaded_module, name)
        if isinstance(loaded_attr, dict):
            result = loaded_attr
    except (FileNotFoundError, ImportError, AttributeError, Exception):
        pass
    return result
