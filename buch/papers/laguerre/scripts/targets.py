import numpy as np
import scipy.special

import gamma_approx as ga


def find_best_loc(N=200, a=1.375, b=0.5, ns=None):
    if ns is None:
        ns = np.arange(2, 13)
    bests = []
    step = 1 / (N - 1)
    x = np.linspace(step, 1 - step, N + 1)
    gamma = scipy.special.gamma(x)
    for n in ns:
        zeros, weights = np.polynomial.laguerre.laggauss(n)
        est = np.ceil(b + a * n)
        targets = np.arange(max(est - 2, 0), est + 3)
        rel_error = []
        for target in targets:
            gamma_lag = ga.eval_laguerre_gamma(x, target=target, x=zeros, w=weights, func="shifted")
            rel_error.append(np.abs(ga.calc_rel_error(gamma, gamma_lag)))
        rel_error = np.stack(rel_error, -1)
        best = np.argmin(rel_error, -1) + targets[0]
        bests.append(best)
    return np.stack(bests, 0)


if __name__ == "__main__":
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    mpl.rcParams.update(
        {
            "mathtext.fontset": "stix",
            "font.family": "serif",
            "font.serif": "TeX Gyre Termes",
        }
    )
    
    N = 200
    ns = np.arange(1, 13)
    
    bests = find_best_loc(N, ns=ns)

    fig, ax = plt.subplots(num=1, clear=True, constrained_layout=True, figsize=(3.5, 2.1))
    v = ax.imshow(bests, cmap=ga.cmap, aspect="auto", interpolation="nearest")
    plt.colorbar(v, ax=ax, label=r"$m^*$")
    ticks = np.arange(0, N + 1, N // 5)
    ax.set_xlim(0, 1)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{v:.2f}" for v in ticks / N])
    ax.set_xticks(np.arange(0, N + 1, N // 20), minor=True)
    ax.set_yticks(np.arange(len(ns)))
    ax.set_yticklabels(ns)
    ax.set_xlabel(r"$z$")
    ax.set_ylabel(r"$n$")
    # fig.savefig(f"{ga.img_path}/targets.pgf")
    fig.savefig(f"{ga.img_path}/targets.pdf")
