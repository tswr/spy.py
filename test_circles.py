import spy
spy.attach_to_builtins("property")

import circle1
import circle2


def test(cls):
    print(">>> Testing {}".format(cls))
    c = cls(1, 2, 3)
    str(c)
    c.r
    c.r = 4
    c.area()
    c + c


def main():
    test(spy.attach_to_class(circle1.Circle))
    test(spy.attach_to_class(circle2.Circle))


if __name__ == "__main__":
    main()
