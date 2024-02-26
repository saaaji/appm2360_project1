from typing import Callable
import sys, getopt, textwrap
import matplotlib.pyplot as plt
import numpy as np

A0 = 750_000 # $750,000 initial value
r = 0.05 # 5% rate
p1 = 4000 # $4000 monthly payment
p2 = 4500 # $4500 monthly payment

h1 = 0.5
h2 = 0.01

# section 1
dAdt_sec1 = lambda t, A: r * A - 12 * p1
analytic_A = lambda t: ((A0 * r - 12 * p1) * np.exp(r * t) + 12 * p1) / r

# section 2
r_ARM = lambda t: 0.03 if t <= 5 else 0.03 + 0.015 * np.sqrt(t-5)
dAdt_sec2_1 = lambda t, A: r_ARM(t) * A - 12 * p1
dAdt_sec2_2 = lambda t, A: r_ARM(t) * A - 12 * p2

def eulers_method(f: Callable[[float], float], h: float, A0: float, t0: float):
  # A_(n+1) = A_n + h * f(t_n, A_n)
  t = np.array([t0])
  A = np.array([A0])

  while A[-1] > 0:
    t_prev = t[-1]
    A_prev = A[-1]

    t_next = t_prev + h
    A_next = A_prev + h * f(t_prev, A_prev)

    t = np.append(t, [t_next])
    A = np.append(A, [A_next])
  
  return (t, A)

def plotter_sec1(ax, h):
  (t, numerical_A) = eulers_method(f=dAdt_sec1, h=h, A0=A0, t0=0)

  range_min = int(np.ceil(np.min(t)))
  range_max = int(np.ceil(np.max(t)))
  cont_t = np.linspace(range_min, range_max, 100)

  ax.plot(t, numerical_A, label='numerical solution', linestyle='-')
  ax.plot(cont_t, analytic_A(cont_t), label='analytic solution', linestyle='--')

  ax.set_xlabel('Time (years)')
  ax.set_ylabel('Loan Amount ($)')
  ax.set_title(textwrap.fill(f'Value of Loan vs. Time, h={h}', 25))
  ax.annotate(
    f'Paid at t={t[-1]:.2f} yrs.', 
    xy=(t[-1], numerical_A[-1]), 
    xytext=(t[-1] - 13, numerical_A[-1]))
  ax.legend()

def plotter_sec2(ax):
  (t1, numerical_A1) = eulers_method(f=dAdt_sec2_1, h=h2, A0=A0, t0=0)
  (t2, numerical_A2) = eulers_method(f=dAdt_sec2_2, h=h2, A0=A0, t0=0)

  ax.plot(t1, numerical_A1, label=f'numerical solution, p=${p1}', color='red', linestyle='-')
  ax.plot(t2, numerical_A2, label=f'numerical solution, p=${p2}', color='blue', linestyle='--')
  
  ax.set_xlabel('Time (years)')
  ax.set_ylabel('Loan Amount ($)')
  ax.set_title(textwrap.fill(f'Value of ARM Loan vs. Time, h={h2}', 25))
  
  tf1 = t1[-1]
  tf2 = t2[-1]
  paid1 = (tf1 * 12 * p1) - A0 
  paid2 = (tf2 * 12 * p2) - A0

  ax.annotate(
    f'Paid at t={t1[-1]:.2f} yrs.\nTotal interest paid: ~${paid1:.0f}', 
    xy=(t1[-1], numerical_A1[-1]), 
    xytext=(t1[-1] - 11, numerical_A1[-1]),
    bbox=dict(boxstyle='round,pad=0.3', fc='pink', ec='red', lw=1))

  ax.annotate(
    f'Paid at t={t2[-1]:.2f} yrs.\nTotal interest paid: ~${paid2:.0f}', 
    xy=(t2[-1], numerical_A1[-1]), 
    xytext=(t2[-1] - 11, numerical_A2[-1]),
    bbox=dict(boxstyle='round,pad=0.3', fc='lightblue', ec='blue', lw=1))

  print(f'A1: {numerical_A1[-1]}, A2: {numerical_A2[-1]}')
  ax.legend()

def main():
  try:
    opts, _ = getopt.getopt(sys.argv[1:], 's:')
  except getopt.GetoptError as err:
    print(err)
    sys.exit(1)

  for (o, a) in opts:
    if o == '-s' and a == '1':
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), layout='constrained')
      plotter_sec1(ax1, h1)
      plotter_sec1(ax2, h2)
      plt.show()
    elif o == '-s' and a == '2':
      fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
      plotter_sec2(ax)
      plt.show()

  if len(opts) == 0:
    print('no section specified')

if __name__ == '__main__':
  main()