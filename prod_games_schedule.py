from prod import games_schedule as games_schedule
from settings import settings

import logging
import os
import signal
import threading
import time
from sys import path as pylib  # im naming it as pylib so that we won't get confused between os.path and sys.path

import tornado.autoreload
import tornado.ioloop
import tornado.web
from tornado.options import options, parse_command_line, parse_config_file

pylib += [os.path.abspath('./prod')]


class MainHandler(tornado.web.RequestHandler):
    is_done = False

    def get(self):
        self.write('OK')

    def post(self):
        # global slots, teams

        (slots, teams) = games_schedule.set_data_from_json(self.request.body)

        def breaker():
            # logging.info("At the breaker")
            count = 0
            while True:
                if self.is_done:
                    logging.info("It is done!")
                    break
                if count >= 450:
                    logging.info("We are doomed...")
                    os.kill(os.getpid(), signal.SIGINT)
                time.sleep(0.1)
                count += 1

        t_breaker = threading.Thread(target=breaker)
        t_breaker.start()

        res = games_schedule.solution(slots, teams)

        self.is_done = True
        t_breaker.join()

        if isinstance(res, str):
            return self.write({'error': True, 'data': res})

        self.write({'error': False, 'data': res})


url_patterns = [(r"/", MainHandler), ]


class MainApplication(tornado.web.Application):

    def __init__(self):
        logging.info("init MainApplication with settings: %s and %s" % (str(settings), url_patterns))
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    parse_command_line()
    if options.config:
        parse_config_file(options.config)
    app = MainApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
