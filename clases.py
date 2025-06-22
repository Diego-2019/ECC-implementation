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
        
        x1, y1 = P
        x2, y2 = Q

        # Case when P + (-P) = 0 where Q = -P 
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        
        # Addition when P = Q (point doubling)
        if P == Q:
            m = (3 * pow(x1, 2) + self.A) * pow(2 * y1, -1, p) % p
        # Addition when P != Q (point addition)
        else:
            m = (y2 - y1) * pow(x2 - x1, -1, p) % p

        x3 = (pow(m, 2) - x1 - x2) % p
        y3 = (m * (x1 - x3) - y1) % p

        return (x3, y3)
    
    def scalar_mult(self, k: int, P: Point) -> Point:
        result: Point = None
        addend: Point = P

        while k:
            # if number k is odd the addition is between different points
            if (k & 1): # k % 2 == 1
                result = self.point_add(addend, result)
            addend = self.point_add(addend, addend)
            k >>= 1 # Integer division k // 2
        
        return result
    
    # Order of a point
    def order(self, G: Point) -> int:
        Q = G
        n = 1
        while Q is not None:
            Q = self.point_add(Q, G)
            n += 1
        
        return n
    
    # Precomputation
    def to_fractional(self, P: Point) -> Point:
        if P is None:
            return None
        x, y = P
        X = (x * pow(self.l, 2, p)) % p
        Y = (y * pow(self.l, 3, p)) % p
        return (X, Y)

    def from_fractional(self, P: Point) -> Point:
        if P is None:
            return None
        X, Y = P
        linv = pow(self.l, -1, p)
        x = (X * pow(linv, 2, p)) % p
        y = (Y * pow(linv, 3, p)) % p
        return (x, y)

# Class for Alice and Bob
class Entity:
    def __init__(self):
        self.priv_key = None
        self.pub_key = None    


# Bob's key pair generation 
def key_gen(curve: Curve, P: Point, n: int) -> Tuple[int, Point]:
    # Private key
    k = random.randint(1, n - 1)
    # Public key
    kP = curve.scalar_mult(k, P)
    return k, kP

# Alice encrypt
def encrypt(curve: Curve, P: Point, kP: Point, M: Point, n: int) -> Tuple[Point, Point]:
    # Private key
    r = random.randint(1, n - 1)
    # Public key (C1 = rP)
    C1 = curve.scalar_mult(r, P)
    # Shared secret (S = krP = rkP)
    S = curve.scalar_mult(r, kP)
    # C2 = M + krP = M + S
    C2 = curve.point_add(M, S)
    
    # We convert both points to their fractional form before transmitting them
    return curve.to_fractional(C1), curve.to_fractional(C2)

# Bob decrypt
def decrypt(curve: Curve, P: Point, n: int, d: int, C: Tuple[Point, Point]) -> Point:
    # Unpack C
    C1, C2 = C

    # We reverse the fraction to return to the real curve
    C1 = curve.from_fractional(C1)
    C2 = curve.from_fractional(C2)

    # Shared secret (S = dC1 = d(rP) = r(dP))
    S = curve.scalar_mult(d, C1)
    # Additive inverse of S
    S_neg = curve.negate(S)
    # M = C2 - dC1 = M + S - S
    M = curve.point_add(C2, S_neg)

    return M







# ?Seccion para probar los metodos
aNum, aDen, bNum, bDen = 7, 3, 2, 5
p = 178987
l = 15
P = (116485, 32401)
C = Curve(p, aNum, aDen, bNum, bDen)

# print((bNum * pow(bDen, -1, p)) * pow(l, 6, p) % p)
# print(C.is_on_curve(P))
# print(C.negate(P))
# print(C.point_add((5,2), (2,7)))
# print(C.order(P))
# assert C.is_on_curve(P)