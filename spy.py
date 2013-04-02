def attach_to_callable(f):
    print("==> Spying on {}".format(f.__name__))

    def g(*args, **kwargs):
        print("--> {} : args={!r}, kwargs={!r}".format(f.__name__,
                                                       args, kwargs))
        return f(*args, **kwargs)

    return g


def attach_to_object_init(f):
    print("==> Spying on {}, setting up a dummy".format(f.__name__))

    def g(*args, **kwargs):
        print("--> {} [muted] : args={!r}, kwargs={!r}".format(f.__name__,
                                                               args, kwargs))

    return g


def attach_to_object_new(f):
    s = "==> Spying on {}, setting up with the argument cutter"
    print(s.format(f.__name__))

    def g(*args, **kwargs):
        print("--> {} : args={!r}, kwargs={!r}".format(f.__name__,
                                                       args, kwargs))
        return f(args[0])

    return g


def attach_to_class(*targets):
    cls = None
    if len(targets) == 1 and type(targets[0]) is type:
        cls = targets[0]
        targets = []

    def real_attach_to_class(cls):
        if targets:
            attrs = targets
            ignore = []
        else:
            attrs = dir(cls)
            ignore = ["__class__", "__repr__"]
        for attr_name in attrs:
            if attr_name in ignore:
                continue
            attr = getattr(cls, attr_name)
            if callable(attr):
                setattr(cls, "__orig_" + attr_name, attr)
                if attr is object.__init__:
                    print("!!> Skipping {}".format(attr))
                    setattr(cls, attr_name, attach_to_object_init(attr))
                elif attr is object.__new__:
                    print("!!> Skipping {}".format(attr))
                    setattr(cls, attr_name, attach_to_object_new(attr))
                else:
                    setattr(cls, attr_name, attach_to_callable(attr))
        print("==> Attached to {}".format(cls))
        return cls

    if cls:
        return real_attach_to_class(cls)
    return real_attach_to_class


def subclass(cls):
    return type(cls.__name__, (cls,), {})


def attach_to_builtins(*targets):
    for t in targets if targets else __builtins__.keys():
        if type(__builtins__[t]) is type:
            try:
                __builtins__[t] = attach_to_class(subclass(__builtins__[t]))
            except:
                print("!!> Failed to attach to {}".format(t))
