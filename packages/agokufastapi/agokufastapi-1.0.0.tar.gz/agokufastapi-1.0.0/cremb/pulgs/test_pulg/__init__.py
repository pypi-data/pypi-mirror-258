from agoku.pulg import IBasePlugin


class HealthCheckPluginClient(IBasePlugin):
    pass

    def on_startup(self, app):
        pass
        print(self.name, "on_startup")

    def on_shutdown(self, app):
        pass
        print("大爷的on_shutdown")

    def on_request_start(self, request):
        pass
        print("插件里面介绍", request)

    def on_request_finished(self, request,response):
        pass
        print("插件里面介绍on_request_finished", request,response.body)
