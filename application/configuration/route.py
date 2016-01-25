route = list()
route.append(("GET", "/", "Demo.Demo.welcome"))
route.append(("get", "/hello/(.*)", "Demo.Demo.hello"))
