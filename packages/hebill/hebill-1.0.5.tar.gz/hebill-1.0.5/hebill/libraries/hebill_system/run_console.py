def run():
    from .core import x
    from ..terminal_command.main import terminal_command
    langauge = 'zh-CN'
    console = terminal_command()
    console.print_info("选择语言，回车默认为中文 | Select your language, press Enter to default to Chinese")
    console.print_info('[1] 中文 # 输入"1"回车选择中文')
    console.print_info('[2] English # Input "2" press Enter to select English')
    cmd = console.input("")
    if cmd == '2':
        langauge = 'en-GB'
    x.console(langauge)
