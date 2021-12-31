import numpy as np


class par:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0
        self.vx = 0
        self.vy = 0
        self.pbest = 9999999

    def p_update(self, x, y, i):
        self.pbest = i
        self.px = x
        self.py = y


def pso(no_par, terrain, iterations, wt=0.2, pc=0.5, gc=2):
    particle = []
    rows = len(terrain)
    cols = len(terrain[0])
    globalbest = 9999999
    globaldim = [0, 0]
    for i in range(no_par):
        a = par()
        a.x = np.random.randint(0, cols)
        a.y = np.random.randint(0, rows)
        a.vx = np.random.randint(0, int(rows / 2))
        a.vy = np.random.randint(0, int(cols / 2))
        particle.append(a)
        # print("Initial position of particle",str(i),"is",str([a.x,a.y]),"& velocity is",str([a.vx,a.vy]))

    for j in range(iterations):
        co = []
        # print("In iteration",str(j))
        for k in range(len(particle)):
            i = particle[k]
            co.append([i.y, i.x])
            fit_val = terrain[i.y][i.x]
            if fit_val < i.pbest:
                i.p_update(i.x, i.y, fit_val)
            if i.pbest < globalbest:
                globalbest = i.pbest
                globaldim[0] = i.x
                globaldim[1] = i.y
                # print("Global best so far :",tuple(globaldim))
            # print("Co-ordinates of particle",str(k),"are:",str([i.x,i.y]),"& velocity is",str([i.vx,i.vy]))
            i.vx = int(wt * np.random.rand() * i.vx + pc * np.random.rand() * (i.px - i.x) + gc * np.random.rand() * (
                        globaldim[0] - i.x))
            i.vy = int(wt * np.random.rand() * i.vy + pc * np.random.rand() * (i.py - i.y) + gc * np.random.rand() * (
                        globaldim[1] - i.y))
            # print("w * Vx + pc * (Px-Vx) + gc * (Gx-Vx) = ",str(i.vx))
            # print("w * Vy + pc * (Py-Vy) + gc * (Gy-Vy) = ",str(i.vy))
            i.x = i.x + i.vx
            if i.x < 0:
                i.x = 0
            elif i.x >= cols:
                i.x = cols - 1
            # print("X Co-ordinate of particle",k,"X(n) = X(n-1) + Vx =",i.x)
            i.y = i.y + i.vy
            if i.y < 0:
                i.y = 0
            elif i.y >= rows:
                i.y = rows - 1
            # print("Y Co-ordinate of particle",k,"Y(n) = Y(n-1) + Vy =",i.y)

        # Printing
        for k in range(rows):
            for l in range(cols):
                if [k, l] in co:
                    print("*", end='')
                else:
                    print(" ", end='')
            print()
        print("###############################")
    return tuple(globaldim), globalbest


while True:
    print("Let's assume that we have the data of the surface of a mountain range as follows")
    print("Using PSO algorithm lets find the area with lowest surface level")
    terrain = np.random.randint(1, 9999998, (500, 90))
    print(terrain)
    no_par = int(input("Enter the no of particles : "))
    iterations = int(input("Enter the no of iterations : "))
    dim, best = pso(no_par, terrain, iterations)

    print("The global best is at", dim, "i.e", best, " the min is ", np.min(terrain))
