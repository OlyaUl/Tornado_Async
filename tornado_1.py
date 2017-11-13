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
    async def get(self):
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
        http = AsyncHTTPClient()
        foo = await tornado.gen.Task(c.get, "foo")
        print(foo)
        self.set_header('Content-Type', 'text/html')
        self.render("template.html", title="Simple demo", foo=foo)

        '''if r.reason == 'OK':
            print(r.body)
            date = json_decode(r.body)
            # print(date['bpi']['USD']['rate_float'])
            res = date['bpi']['USD']['rate_float']
            self.write("Bitcoin =  %s" % res)
            # except:
        else:
            self.write("Try again")'''


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
