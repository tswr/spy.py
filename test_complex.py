import spy


spy.attach_to_builtins("complex")


def main():
    a = complex(1, 2)
    b = complex(3, 4)
    print(a + b)
    print(a * b)


if __name__ == "__main__":
    main()
