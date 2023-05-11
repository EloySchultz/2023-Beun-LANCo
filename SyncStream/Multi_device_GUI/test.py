import animations_new  # import c_animations
import inspect


# python2

def read_animations():
    a = inspect.getmembers(animations_new.c_animations(), predicate=inspect.ismethod)
    animations = []
    blacklist = ["__init__", "cycle"]
    for b in a:
        if not (b[0] in blacklist):
            animations.append(b[0])
    return animations

