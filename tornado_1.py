import tornado.ioloop
import tornado.web
import json
import tornado.web
import tornado.escape
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
import tornadoredis
import tornado.web
import tornado.gen


c = tornadoredis.Client()
c.connect()


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.engine
    @tornado.web.asynchronous
    def get(self):
    # async def get(self):
        # # try:
        #     http = AsyncHTTPClient()
        #     r = await http.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
        #     print(r.reason)
        #
        #     if r.reason == 'OK':
        #         print(r.body)
        #         date = json_decode(r.body)
        #         # print(date['bpi']['USD']['rate_float'])
        #         res = date['bpi']['USD']['rate_float']
        #         self.write("Bitcoin =  %s" % res)
        # # except:
        #     else:
        #         self.write("Try again")

        # try:
        print('tetst')
        http = AsyncHTTPClient()
        bit = yield tornado.gen.Task(c.get, "bit")
        print(bit)

        r = yield tornado.http.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")

        if r.reason == 'OK':
            print(r.body)
            date = json_decode(r.body)
            print(date['bpi']['USD']['rate_float'])
            res = date['bpi']['USD']['rate_float']
            # self.write("Bitcoin =  %s" % res)
            print(res)

            with c.pipeline() as pipe:
                pipe.set('foo', res, 12 * 60 * 60)
                yield tornado.gen.Task(pipe.execute)

        self.set_header('Content-Type', 'text/html')
        self.render("template.html", title="Simple demo", bit=bit)

        '''if r.reason == 'OK':
            print(r.body)
            date = json_decode(r.body)
            # print(date['bpi']['USD']['rate_float'])
            res = date['bpi']['USD']['rate_float']
            self.write("Bitcoin =  %s" % res)
            # except:
        else:
            self.write("Try again")'''


@tornado.gen.engine
async def create_test_data():
    c = tornadoredis.Client()
    r = await tornado.http.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")

    if r.reason == 'OK':
        print(r.body)
        date = json_decode(r.body)
        print(date['bpi']['USD']['rate_float'])
        res = date['bpi']['USD']['rate_float']
        # self.write("Bitcoin =  %s" % res)
        print(res)

        with c.pipeline() as pipe:
            pipe.set('foo', res, 12 * 60 * 60)
            await tornado.gen.Task(pipe.execute)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

application = tornado.web.Application([
    (r'/', MainHandler),
])

if __name__ == "__main__":
    # create_test_data()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print('Demo is runing at 0.0.0.0:8888\nQuit the demo with CONTROL-C')
    tornado.ioloop.IOLoop.instance().start()


    '''app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()'''
