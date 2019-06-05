# coding: utf8 
import time
import argparse
import threading
from job_register_log_stream import JobRegisterLogStream
from context import g_ctx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify config file",
            default='/conf/logbus/test.conf')
    args = parser.parse_args()
    g_ctx.init(args.config)

    workers = []
    workers.append(JobRegisterLogStream(interval=500))

    for w in workers:
        w.start()

    while threading.active_count() > 1:
        time.sleep(0.2)


if __name__ == '__main__':
    main()

