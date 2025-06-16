from dataclasses import dataclass

# Clase que representa un struct para enviar E(a/n, b/m)
@dataclass
class MyStruct:
    A: int
    B: int

class Alice:
    def __init__(self, curve, p, P, Q):
