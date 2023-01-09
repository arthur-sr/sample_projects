from datetime import datetime
import asyncio

dt_format = "%Y-%m-%d %H:%M:%S"

def ts():
    return datetime.now().strftime(dt_format)

def write_log_func(logfile_path: str, write_to_logs_flag=True):
    def write_log(*args):
        if not write_to_logs_flag:
            return
        with open(logfile_path, 'a') as f:
            f.write(ts() + ' :: ' + ' :: '.join(args) + '\n')
    return write_log


def aexec(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))
        loop.close()
    return wrapper

write_log = write_log_func('./Logs/logfile.log')
write_error = write_log_func('./Logs/errors.log')
