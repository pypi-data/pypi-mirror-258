class Infix(object):
    def __init__(self, function):
        self.function = function

    def __rmod__(self, other):
        return Infix(lambda x: self.function(other, x))

    def __mod__(self, other):
        return self.function(other)


like = Infix(lambda x, y: x.like(y))
ilike = Infix(lambda x, y: x.ilike(y))
isin = Infix(lambda x, y: x.isin(y))
notin = Infix(lambda x, y: x.notin(y))
is_ = Infix(lambda x, y: x.isnull() if y is None else x == y)
isnt = Infix(lambda x, y: x.notnull() if y is None else x != y)
