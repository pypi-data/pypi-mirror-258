import os
from spike.utils import run_cmd, echo, run_cmd_inactivate

pkg_current_path = os.path.dirname(os.path.abspath(__file__))

def show_choice_list(choice_list):
    echo(f"0. 退出", "blue")
    for i, c in enumerate(choice_list):
        echo(f"{i+1}. {c.title}", "blue")
    echo ("\n请输入序号：", "blue")
    

class PipSetter:
    def __init__(self):
        self.title = "设置 pip 源"
        
    def run(self):
        # ---------------------------------------------------------------------------- #
        #                         设置 pip 源                                     
        # ---------------------------------------------------------------------------- #
        pip_source = [
            "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/",
            "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/",
            "conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/",
            "conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/",
            "conda config --set show_channel_urls yes",
            "pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple",
            "pip config set global.extra-index-url https://pypi.org/simple"
        ]
        run_cmd(pip_source)
        
class RangerInstaller:
    def __init__(self):
        self.title = "安装 ranger"
        
    def run(self):
        # ---------------------------------------------------------------------------- #
        #                             安装 ranger                                 
        # ---------------------------------------------------------------------------- #
        ranger = [
            "python -m pip install ranger-fm",
            "mv {}/ranger ~/.config/".format(pkg_current_path),
        ]
        run_cmd(ranger)
        
class RedisInstaller:
    def __init__(self):
        self.title = "安装 redis"
        
    def run(self):
        # ---------------------------------------------------------------------------- #
        #                             安装 redis                                 
        # ---------------------------------------------------------------------------- #
        echo("安装 Redis 时间可能较长（大约五分钟），请耐心等待！")
        run_cmd([
            "sh {}/redis.sh".format(pkg_current_path),
            "cp {}/redis.conf ~/redis/bin/".format(pkg_current_path),
            "~/redis/bin/redis-server ~/redis/bin/redis.conf",
        ])
    

class CondaInstaller:
    def __init__(self):
        self.title = "安装 Miniconda"
        
    def run(self):
        # ---------------------------------------------------------------------------- #
        #                             安装 conda                                 
        # ---------------------------------------------------------------------------- #
        run_cmd_inactivate([
            "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh",
            "sh Miniconda3-latest-Linux-x86_64.sh",
        ])
 
class RedisStarter:
    def __init__(self):
        self.title = "启动 redis"
        
    def run(self):
        # ---------------------------------------------------------------------------- #
        #                             启动 redis                                 
        # ---------------------------------------------------------------------------- #
        run_cmd_inactivate("~/redis/bin/redis-server ~/redis/bin/redis.conf")
        echo("redis 启动成功！", "green")
        
class RedisMaintainer:
    def __init__(self):
        self.title = "redis 数据维护"
        
    def run(self):
        run_cmd_inactivate(f"nohup python {pkg_current_path}/redis_maintainer.py > ~/redis_maintainer.log 2>&1 &")
        echo("Redis 数据维护已启动！", "yellow")
        echo("查看维护日志：tail -f ~/redis_maintainer.log", "yellow")
        
                



choice_list = [
    PipSetter(), 
    RangerInstaller(), 
    CondaInstaller(), 
    RedisStarter(), 
    RedisMaintainer()
]

def main():
    if "bash" not in run_cmd("echo $SHELL", show_cmd=False):
        if "bash" not in run_cmd("cat /etc/shells", show_cmd=False):
            echo("未找到 bash 环境，请先安装 bash 环境！", "red")
        else:        
            echo("请在 bash 环境下运行本工具！")
        echo("您可以通过以下命令查看所支持的 Shell 类型：\ncat /etc/shells", "red")
        echo("您可以通过以下命令切换 Shell 类型：\nchsh -s /bin/bash", "red")
        exit()

    # 读取 ~/.bashrc 文件内容
    if not os.path.exists("~/.bashrc"):
        run_cmd("touch ~/.bashrc", show_cmd=False)
    bashrc = run_cmd("cat ~/.bashrc", show_cmd=False)
    if "lazyinit" not in bashrc:
        print("未找到 lazyinit 配置，即将注入配置到 ~/.bashrc（完成后可能需要重启初始化工具）")
        # ---------------------------------------------------------------------------- #
        #                         配置 Bash 环境变量                                     
        # ---------------------------------------------------------------------------- #
        bash = [
            "cd ~/",
            "cat {}/bash_config.txt >> ~/.bashrc".format(pkg_current_path),
        ]
        run_cmd(bash, show_cmd=False)
        echo("运行 {} 以完成配置（运行后需要重启工具）".format("source ~/.bashrc"), "yellow")
        exit(0)
        
    echo("")
    echo("")
    echo("")
    echo("")
    echo("")
    echo("         __                         __  ___      __                ____")
    echo("        / /   ____ _____  __  __   /  |/  /___ _/ /_____  _____   / __ )__  _________  __")
    echo("       / /   / __ `/_  / / / / /  / /|_/ / __ `/ //_/ _ \\/ ___/  / __  / / / / ___/ / / /")
    echo("      / /___/ /_/ / / /_/ /_/ /  / /  / / /_/ / ,< /  __(__  )  / /_/ / /_/ (__  ) /_/ /")
    echo("     /_____/\\__,_/ /___/\\__, /  /_/  /_/\\__,_/_/|_|\\___/____/  /_____/\\__,_/____/\\__, /")
    echo("                       /____/                                                   /____/")
    echo("")
    echo("")
    echo("")
    echo("")

 
    step = "-1"
    while step != "0":
        if step != "-1":
            echo("\n是否继续配置？（y/n）", "yellow")
            conti = input()
            if conti != "y":
                echo("\n\n再见咯👋🏻👋🏻👋🏻")
                break
        show_choice_list(choice_list)
        step = int(input())
        
        if step == 0:
            break
    
        choice_list[step-1].run()
        
    