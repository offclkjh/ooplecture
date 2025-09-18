class A:
    def hello(self):
        print("Hello from A")


class B(A):
    def hello(self):
        print("Hello from B")
        super().hello()


class C(A):
    def hello(self):
        print("Hello from C")
        super().hello()


class D(B, C):
    def hello(self):
        print("Hello from D")
        super().hello()


class E(C):
    pass

class F(B, E):
    pass

print(F.mro())


class D2(C, B):
    pass


class X(D, D2):
    pass