import numpy as np

def gj(a, b, x, n):
    l = len(a)
    y = x.copy()
    z = np.zeros(l)
    
    print("\niter | x | y | z")
    print("-" * 25)
    print(f"0 | {x[0]:.3f} | {x[1]:.3f} | {x[2]:.3f}")
    
    for k in range(n):
        for i in range(l):
            s = np.dot(a[i,:], y) - a[i,i] * y[i]
            z[i] = (b[i] - s) / a[i,i]
        
        z = np.round(z, 3)
        print(f"{k+1} | {z[0]:.3f} | {z[1]:.3f} | {z[2]:.3f}")
        
        if np.allclose(y, z, rtol=1e-6):
            return z
            
        y = z.copy()
    
    return z

n = int(input("enter iterations: "))
print("enter matrix:")
mat = []
for i in range(3):
    r = input()
    mat.append([float(x) for x in r.split()])

mat = np.array(mat)
a = mat[:, :3]
b = mat[:, 3]
x = np.zeros(3)

ans = gj(a, b, x, n)
print("\nans:", ans)