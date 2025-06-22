import clases as ecc

aNum, aDen, bNum, bDen = 7, 3, 2, 5
p = 178987
l = 15
P = (116485, 32401)
curve = ecc.Curve(p, aNum, aDen, bNum, bDen)
n = ecc.Curve.order(curve, P)
M = (47542, 46746) 

# Check that P, M are on the curve
assert curve.is_on_curve(P)
assert curve.is_on_curve(M)

# Creation of entities
alice = ecc.Entity()
bob = ecc.Entity()

# Generation of Bob's key pair
bob.priv_key, bob.pub_key = ecc.key_gen(curve, P, n)

print("Bob announces:")
print(f"E({aNum}/{aDen}, {bNum}/{bDen}), p={p}, P=({P[0]}/{l}^2, {P[1]}/{l}^3), kP=({bob.pub_key[0]}/{l}^2, {bob.pub_key[1]}/{l}^3)")
print(f"E: y^2=x^3+{aNum}/{aDen}x+{bNum}/{bDen} mod {p}")

# Precomputationn prepared by alice
print("\n\nAlice precomputes:")
print(f"x=X/{l}^2, y=Y/{l}^3")
print("From ecuation E:")
print(f"(Y/{l}^3)^2=(X/{l}^2)^3+(X/{l}^2)({aNum}/{aDen})+({bNum}/{bDen}) mod {p}")
print("=>")
print(f"Y^2=X^3={curve.A}X+{curve.B} mod {p}")

# Alice encrypts the message M
print(f"\n\nAlice set the message M: {M}")
C = ecc.encrypt(curve, P, bob.pub_key, M, n)
print("\nAlice encrypts and sends:")
print("  C1 =", C[0])
print("  C2  =", C[1])

# Bob decrypts the message
print("\n\nBob decrypts the message:")
M_decrypted = ecc.decrypt(curve, P, n, bob.priv_key, C)
print("  M =", M_decrypted)
