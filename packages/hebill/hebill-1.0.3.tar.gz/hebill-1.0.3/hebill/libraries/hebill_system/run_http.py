from hebill.libraries.hebill_system.core import x
from flask import Flask, session
import secrets
from .__constants__ import SN_ID

app = Flask(__name__)
if 'SECRET_KEY' not in app.config or not app.config['SECRET_KEY']:
    app.config['SECRET_KEY'] = secrets.token_hex(24)


@app.route('/')
def root():
    if SN_ID not in session:
        session[SN_ID] = secrets.token_hex(32)

    # 返回客户端语言偏好的第一个语言名称
    return x.client(session[SN_ID]).http()
