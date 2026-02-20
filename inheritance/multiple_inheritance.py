# 1
class CanFly:
    def fly(self):
        return "I can fly"

class CanSwim:
    def swim(self):
        return "I can swim"

class Duck(CanFly, CanSwim):
    pass

d = Duck()
print(d.fly())
print(d.swim())

# 2
class A:
    def hello(self):
        return "Hello from A"

class B:
    def hello(self):
        return "Hello from B"

class C(A, B):
    pass

print(C().hello())        # uses A first
print(C.__mro__)          # show order

# 3
class Base:
    def __init__(self):
        self.steps = ["Base"]

class Left(Base):
    def __init__(self):
        super().__init__()
        self.steps.append("Left")

class Right(Base):
    def __init__(self):
        super().__init__()
        self.steps.append("Right")

class Both(Left, Right):
    def __init__(self):
        super().__init__()
        self.steps.append("Both")

b = Both()
print(b.steps)            # order depends on MRO
print(Both.__mro__)

# 4
class TimestampMixin:
    def stamp(self):
        return "2026-02-21"

class Note(TimestampMixin):
    def __init__(self, text):
        self.text = text

n = Note("Buy milk")
print(n.text, n.stamp())