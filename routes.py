routes = list()
routes.append(("GET", "/", "Demo.Demo.welcome"))
routes.append(("get", "/test/(.*)", "Demo.Demo.test"))
