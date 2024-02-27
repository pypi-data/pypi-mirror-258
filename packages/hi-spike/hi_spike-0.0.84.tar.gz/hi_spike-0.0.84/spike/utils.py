import os
from rich.console import Console
import subprocess
from rich.progress import track
import time
import logging
import inspect
import re
from importlib import import_module
import sys
import traceback


log = Logger(__name__)


def print_error_info(e: Exception):
    """打印错误信息

    Args:
        e (_type_): 异常事件
    """
    print("str(Exception):\t", str(Exception))
    print("str(e):\t\t", str(e))
    print("repr(e):\t", repr(e))
    # Get information about the exception that is currently being handled
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("e.message:\t", exc_value)
    print(
        "Note, object e and exc of Class %s is %s the same."
        % (type(exc_value), ("not", "")[exc_value is e])
    )
    print("traceback.print_exc(): ", traceback.print_exc())
    print("traceback.format_exc():\n%s" % traceback.format_exc())



def load_class(class_path: str) -> type:
    """Load a class from a string.

    Args:
        class_path: The class path.

    Returns:
        The class.

    Raises:
        ImportError: If the class cannot be imported.
        AttributeError: If the class cannot be found.
    """
    try:
        module_path, _, class_name = class_path.rpartition(".")
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        log.error(f"加载类失败: {class_path}")
        print_error_info(e)
        raise e





def delete_between_delimiters(text, delimiter1, delimiter2):
    """删除text中位于delimiter1和delimiter2之间的字符

    Args:
        text (str): 文本
        delimiter1 (str): 前分隔符
        delimiter2 (str): 后分隔符

    Returns:
        result: 处理后的文本
    """
    pattern = re.escape(delimiter1) + ".*?" + re.escape(delimiter2)
    result = re.sub(pattern, '', text)
    return result


console = Console()

class Logger:
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[91m',
        'FILENAME': '\033[95m',
        'LINENO': '\033[95m',
    }
    RESET = '\033[0m'

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.rank = 0

    def get_logger(self):
        return self.logger

    def set_rank(self, rank):
        self.rank = rank

    def format_with_color(self, message, color):
        return f'{color}{message}{self.RESET}'

    def debug(self, message):
        if self.rank == 0:
            frame = inspect.currentframe().f_back
            filename = os.path.basename(frame.f_code.co_filename)
            lineno = frame.f_lineno
            timestamp = time.strftime('%m-%d %H:%M:%S', time.localtime())
            formatted_time = self.format_with_color(timestamp, self.COLORS['DEBUG'])
            formatted_filename = self.format_with_color(filename, self.COLORS['FILENAME'])
            formatted_lineno = self.format_with_color(str(lineno), self.COLORS['LINENO'])
            print(f'\033[1m{self.COLORS["DEBUG"]}[DEBUG] {formatted_time}  {self.RESET} \033[1m[{formatted_filename}:\033[1m{formatted_lineno}] \033[1m{message}')

    def info(self, message):
        if self.rank == 0:
            frame = inspect.currentframe().f_back
            filename = os.path.basename(frame.f_code.co_filename)
            lineno = frame.f_lineno
            timestamp = time.strftime('%m-%d %H:%M:%S', time.localtime())
            formatted_time = self.format_with_color(timestamp, self.COLORS['INFO'])
            formatted_filename = self.format_with_color(filename, self.COLORS['FILENAME'])
            formatted_lineno = self.format_with_color(str(lineno), self.COLORS['LINENO'])
            print(f'\033[2m{formatted_time} {self.COLORS["INFO"]}{self.RESET} \033[2m[{formatted_filename}:\033[2m{formatted_lineno}] {message}')

    def warning(self, message):
        if self.rank == 0:
            frame = inspect.currentframe().f_back
            filename = os.path.basename(frame.f_code.co_filename)
            lineno = frame.f_lineno
            timestamp = time.strftime('%m-%d %H:%M:%S', time.localtime())
            formatted_time = self.format_with_color(timestamp, self.COLORS['WARNING'])
            formatted_filename = self.format_with_color(filename, self.COLORS['FILENAME'])
            formatted_lineno = self.format_with_color(str(lineno), self.COLORS['LINENO'])
            print(f'\033[1m{self.COLORS["WARNING"]}[WARNING] {formatted_time} {self.RESET} \033[1m[{formatted_filename}:\033[1m{formatted_lineno}] \033[1m{message}')

    def error(self, message):
        if self.rank == 0:
            frame = inspect.currentframe().f_back
            filename = os.path.basename(frame.f_code.co_filename)
            lineno = frame.f_lineno
            timestamp = time.strftime('%m-%d %H:%M:%S', time.localtime())
            formatted_time = self.format_with_color(timestamp, self.COLORS['ERROR'])
            formatted_filename = self.format_with_color(filename, self.COLORS['FILENAME'])
            formatted_lineno = self.format_with_color(str(lineno), self.COLORS['LINENO'])
            print(f'\033[1m{self.COLORS["ERROR"]}[ERROR] {formatted_time} {self.RESET} \033[1m[{formatted_filename}:\033[1m{formatted_lineno}] \033[1m{message}')

    def critical(self, message):
        if self.rank == 0:
            frame = inspect.currentframe().f_back
            filename = os.path.basename(frame.f_code.co_filename)
            lineno = frame.f_lineno
            timestamp = time.strftime('%m-%d %H:%M:%S', time.localtime())
            formatted_time = self.format_with_color(timestamp, self.COLORS['CRITICAL'])
            formatted_filename = self.format_with_color(filename, self.COLORS['FILENAME'])
            formatted_lineno = self.format_with_color(str(lineno), self.COLORS['LINENO'])
            print(f'\033[1m{self.COLORS["CRITICAL"]}[CRITICAL] {formatted_time} {self.RESET} \033[1m[{formatted_filename}:\033[1m{formatted_lineno}] \033[1m{message}')




def echo(msg, color="green"):
    console.print(msg, style=color)
    
    
def run_cmd_inactivate(cmd_list):
    if isinstance(cmd_list, str):
        cmd = cmd_list
        print("\n" + cmd)
        while True:
            exitcode = os.system(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":   
                    return exitcode
            else:
                return exitcode
            
    outputs = []
    for cmd in track(cmd_list, description="命令执行中", transient=True):
        print("\n" + cmd)
        while True:
            exitcode = os.system(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":
                    break
            else:
                break

    return outputs   


def run_cmd(cmd_list, show_cmd=True):
    if isinstance(cmd_list, str):
        cmd = cmd_list
        if show_cmd:
            print("\n" + cmd)
        while True:
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("错误信息：\n{}".format(output))
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":
                    return output
            else:
                return output
            
    outputs = []
    for cmd in track(cmd_list, description="命令执行中", transient=True):
        if show_cmd:
            print("\n" + cmd)
        while True:
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("错误信息：\n{}".format(output))
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":
                    outputs.append(output)
                    break
            else:
                outputs.append(output)
                break

    return outputs