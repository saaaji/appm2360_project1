import matplotlib.pyplot as plt
import numpy as np

A0 = 750_000 # $750,000 initial value
r = 0.03 # 3% rate
n4 = 4 # 4 times annually
n12 = 12 # 12 times annually

# timelines
t1 = np.linspace(0, 30, 100)
t2 = np.linspace(25, 30, 20)

# interest functions
A4 = np.vectorize(lambda t: A0 * (1 + r/n4)**(n4 * t))
A12 = np.vectorize(lambda t: A0 * (1 + r/n12)**(n12 * t))
A_cont = lambda t: A0 * np.exp(r * t)

def plotter(ax, t):
  ax.plot(t, A4(t), label='compounding 4/yr.', linewidth=3, linestyle='-')
  ax.plot(t, A12(t), label='compounding 12/yr.', linewidth=2, linestyle='-')
  ax.plot(t, A_cont(t), label='compounding continuously', linewidth=1, linestyle='-')

  range_min = np.min(t)
  range_max = np.max(t)

  ax.set_xlabel('Time (years)')
  ax.set_ylabel('Loan Amount (millions $)')
  ax.set_title(f'Value of Loan vs. Time ({range_min}-{range_max} yrs.)')
  ax.legend()

def main():
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), layout='constrained')
  plotter(ax1, t1)
  plotter(ax2, t2)
  plt.show()

if __name__ == '__main__':
  main()