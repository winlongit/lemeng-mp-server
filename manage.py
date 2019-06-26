# Set the path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_script import Manager, Server
from app import app

manager = Manager(app)
# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    # use_reloader=True 这个配置用到了Werkzeug库，它会生成一个子进程，当代码有变动的时候它会自动重启如果在run（）里加入参数
    # use_reloader=False，就会取消这个功能，当然，在以后的代码改动后也不会自动更新了。
    use_reloader=True,
    host='0.0.0.0',
    # host='localhost',
    port=5000,
    threaded=True)
                    )

if __name__ == "__main__":
    manager.run()
