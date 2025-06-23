# ECC with Precomputation: A Python Implementation

This repository contains a Python implementation of the cryptographic method described in the paper: **"Security Measures for Ensuring Confidentiality of Information Using Encryption by Elliptic Curve with Precomputation"** by Fatimah Dawoud Mousay, Souad I. Mugassabi, and Asma Ail Budalal.

Our project successfully replicates the paper's novel technique for enhancing the security of Elliptic Curve Cryptography (ECC) and serves as a practical demonstration of its concepts.

## The Cryptographic Method

The core of this project is the implementation of a specific Elliptic Curve Cryptography (ECC) scheme based on the ElGamal protocol. The paper's primary contribution is an added layer of security through obfuscation.

### How it Works

In standard ECC, the curve parameters (`a`, `b`, and `p`) are often public. An attacker, therefore, knows the exact mathematical field they are operating in. This paper proposes a method to hide the true curve.

1. **Public Fractional Curve:** Instead of announcing the real, integer-based curve `y² = x³ + Ax + B`, the user (Bob) announces a "fractional" version:
    $$y^2 \equiv x^3 + (a/n)x + (b/m) \pmod{p}$$

2. **Secret Transformation:** The transformation from the public "fractional" curve to the real, hidden curve relies on a secret integer `l`, which is the least common multiple (`lcm`) of the denominators `n` and `m`.

3. **Coordinate Obfuscation:** All public points (like the generator `P` and the public key `kP`) are also converted from the real curve's coordinate system to the obfuscated fractional coordinate system before being announced.

An attacker, who does not know the secret value `l`, cannot easily reverse this transformation to find the true curve where the cryptographic operations are actually being performed. This adds a significant layer of security.

## Our Implementation

We implemented this scheme in Python using an Object-Oriented approach for clarity, robustness, and reusability. The project is split into two main files.

### `clases.py` - The Cryptographic Engine

This file contains the core logic inside a `Curve` class. It handles all the underlying mathematics of the elliptic curve operations.

#### Precomputation in the Constructor

The `__init__` method takes the public fractional parameters and immediately performs the precomputation to derive the real, internal curve coefficients `A` and `B`.

```python
class Curve:
    def __init__ (self, p, aNum, aDen, bNum, bDen):
        self.p = p
        self.l = math.lcm(aDen, bDen)

        # A = (a/n)*l^4 = a * inv(n) * l^4 mod p
        self.A = (aNum * pow(aDen, -1, self.p) * pow(self.l, 4, self.p)) % self.p
        # B = (b/m)*l^6 = b * inv(m) * l^6 mod p
        self.B = (bNum * pow(bDen, -1, self.p) * pow(self.l, 6, self.p)) % self.p
```

#### Point Addition

The `point_add` method is the fundamental building block of ECC. It implements the geometric "chord-and-tangent" rules for adding two points.

```python
def point_add(self, P, Q):
    # ... code to handle points at infinity ...

    # Case for point doubling (P == Q)
    if P == Q:
        m = (3 * pow(x1, 2) + self.A) * \
            pow(2 * y1, -1, self.p) % self.p
    # Case for point addition (P != Q)
    else:
        m = (y2 - y1) * \
            pow(x2 - x1, -1, self.p) % self.p

    x3 = (pow(m, 2) - x1 - x2) % self.p
    y3 = (m * (x1 - x3) - y1) % self.p

    return (x3, y3)
```

#### Scalar Multiplication

The `scalar_mult` function computes `kP` using the efficient **double-and-add algorithm**. This is critical for performance and is used for both key generation and the creation of the shared secret.

```python
def scalar_mult(self, k, P):
    result = None
    addend = P

    while k:
        if (k & 1): # If k is odd
            result = self.point_add(addend, result)
        
        # Double the point
        addend = self.point_add(addend, addend)
        
        k >>= 1 # Halve k
    
    return result
```

### `main.py` - The Simulation

This script serves as a driver to simulate the entire cryptographic process described in the paper, using the exact values from their example:

1. It initializes the `Curve` object.
2. It simulates Bob generating his private and public keys.
3. It simulates Alice using Bob's public information to encrypt a message.
4. It simulates Bob using his private key to successfully decrypt the message.

## How to Run

The script is written in standard Python 3 and has no external dependencies.

To run the simulation, simply execute the `main.py` file from your terminal:

```bash
python main.py
```

## Example Output

Running the script produces the following output, demonstrating the full, successful cryptographic exchange:

```
Bob announces:
E(7/3, 2/5), p=178987, P=(116485/15^2, 32401/15^3), kP=(65007/15^2, 117978/15^3)
E: y^2=x^3+7/3x+2/5 mod 178987

Alice precomputes:
x=X/15^2, y=Y/15^3
From ecuation E:
(Y/15^3)^2=(X/15^2)^3+(X/15^2)(7/3)+(2/5) mod 178987
=>
Y^2=X^3=118125X+81575 mod 178987

Alice set the message M: (47542, 46746)

Alice encrypts and sends:
  C1 = (67495, 154491)
  C2 = (32123, 89875)

Bob decrypts the message:
  M = (47542, 46746)
```

As shown, the original message `M` set by Alice is perfectly recovered by Bob after the decryption process, proving that our implementation of the paper's method is correct and functional.
