def respond(regex):

    def factory(func):
        func.response = True
        func.regex = regex
        return func

    return factory
