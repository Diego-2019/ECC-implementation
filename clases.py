from __future__ import annotations
import math
import random
from typing import Optional, Tuple

# Can take the value of a int tuple (x, y) or None for the point at infinity
Point = Optional[Tuple[int, int]] 

class Curve:
    def __init__ (
            self, 
            p: int, 
            aNum: int, # Numerator of A
            aDen: int, # Denominator of A
            bNum: int, # Numerator of B
            bDen: int, # Denominator of B
            ) -> None:
        
        if p <= 3:
            raise ValueError("p must be a prime grater than 3")
        
        # self.p = p
        self.l = math.lcm(aDen, bDen)

        # A = (a / n) * l^4 = a * inverse mod n * l^4
        self.A = aNum * pow(aDen, -1, p) * pow(self.l, 4, p) % p
        # B = (b / m) * l^6 = b * inverse mod m * l^6
        self.B = bNum * pow(bDen, -1, p) * pow(self.l, 6, p) % p

    # Method to check if a point is on the curve
    def is_on_curve(self, P: Point) -> bool:
        # When P = None represents the point at infinity which belongs to the curve
        if P is None:
            return True
        
        x, y = P

        return (pow(y, 2) - pow(x, 3) - self.A * x - self.B) % p == 0
    
    # Additive inverse method of P
    def negate(self, P: Point) -> Point:
        if P is None:
            return None
        
        x, y = P

        return (x, -y % p)
    
    # Point addition method
    def point_add(self, P: Point, Q: Point) -> Point:
        # Cases where P or Q is None (Point at infinity)
        if P is None:
            return Q
        if Q is None:
            return P
        p=11
        x1, y1 = P
        x2, y2 = Q

        # Case when P + (-P) = 0 where Q = -P 
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        
        # Addition when P = Q
        if P == Q:
            m = (3 * pow(x1, 2) + self.A) * pow(2 * y1, -1, p) % p
        else:
            m = (y2 - y1) * pow(x2 - x1, -1, p) % p

        x3 = (pow(m, 2) - x1 - x2) % p
        y3 = (m * (x1 - x3) - y1) % p

        return (x3, y3)
    
    def escalar_mult(self, k: int, P: Point) -> Point:
        result: Point = None
        addend: Point = P

        while k:
            # if number k is odd the addition is between different points
            if (k & 1): # k % 2 == 1
                result = self.point_add(addend, result)
            addend = self.point_add(addend, addend)
            k >>= 1 # Integer division k // 2
        
        return result
    
    # Precomputation
    def to_fractional(self, P: Point) -> Point:
        if P is None:
            return None
        x, y = P
        X = (x * pow(self.l, 2, self.p)) % self.p
        Y = (y * pow(self.l, 3, self.p)) % self.p
        return (X, Y)

    def from_fractional(self, P: Point) -> Point:
        if P is None:
            return None
        X, Y = P
        linv = pow(self.l, -1, self.p)
        x = (X * pow(linv, 2, self.p)) % self.p
        y = (Y * pow(linv, 3, self.p)) % self.p
        return (x, y)


# Bob's key pair generation 
def key_gen(curve: Curve, P: Point):
    pass

# Alice encrypt
def encrypt(curve: Curve, bobP: Point, bobQ: Point, M: Point):
    pass

# Bob decrypt
# def decrypt(curve: Curve, AliceQ: Point, C: Point)







# ?Seccion para probar los metodos
aNum, aDen, bNum, bDen = 7, 3, 2, 5
p = 178987
l = 15
P = (116485, 32401)
C = Curve(p, aNum, aDen, bNum, bDen)

# print((bNum * pow(bDen, -1, p)) * pow(l, 6, p) % p)
# print(C.is_on_curve(P))
# print(C.negate(P))
print(C.point_add((5,2), (2,7)))