import numpy as np
s_values = np.array([2, 3, 4, 10])
zeta_approx = np.zeros_like(s_values, dtype=float)

for i, s in enumerate(s_values):
    zeta_approx[i] = np.sum(1 / np.power(np.arange(1, 1001), s))

print(f"Aproximaciones de zeta(s) para s = {s_values}: {zeta_approx}")