import numpy as np
import pandas as pd


class Berlekamp:

    def __init__(self, seed):
        self.seed = seed
        self.fx = np.zeros(len(self.seed))
        self.fx[0] = 1
        self.gx = np.zeros(len(self.seed))
        self.gx[0] = 1
        self.d = 0
        self.l = 0
        self.m = -1
        self.sn = 0
        self.tab = []

    def complete(self):
        for n in range(len(self.seed)):
            self.sn = int(self.seed[n])
            self.d = self.sn
            self.calcD(n)
            if self.d == 1:
                tx = np.copy(self.fx)
                self.calcFx(n)
                if 2 * self.l <= n:
                    self.l = n + 1 - self.l
                    self.m = n
                    self.gx = tx
            for i in range(len(self.fx)):
                self.fx[i] = self.fx[i] % 2
            self.tab.append(FormatBerlekamp(n, self.sn, self.d, self.l, np.copy(self.fx), self.m, np.copy(self.gx)))

    def calcFx(self, n):
        rx = np.zeros(len(self.fx))
        for i in range(len(self.gx)):
            if (i + n - self.m) < len(self.gx):
                rx[i + n - self.m] = self.gx[i]
        for i in range(len(self.fx)):
            self.fx[i] += rx[i]

    def calcD(self, n):
        for i in range(1, self.l + 1):
            self.d += self.fx[i] * int(self.seed[n - i])
        self.d = int(self.d % 2)

    def printFormat(self):
        t = []
        for i in self.tab:
            t.append([i.sn, i.d, i.l, self.printF(i.fx), i.m, self.printF(i.gx)])
        df = pd.DataFrame(t, [(i.n) for i in self.tab], ["sn", "d", "l", 'fx', "m", "gx"])
        print(df)

    def printF(self, fx):
        s = str(int(fx[0]))
        for i in range(1, len(fx)):
            if fx[i] != 0:
                s += " + x^{}".format(int(i))
        return s


class FormatBerlekamp:

    def __init__(self, n, sn, d, l, fx, m, gx):
        self.n = n
        self.sn = sn
        self.d = d
        self.l = l
        self.fx = fx
        self.m = m
        self.gx = gx

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(
            self.n, self.sn, self.d, self.l, self.fx, self.m, self.gx)
