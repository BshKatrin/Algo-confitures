import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":
    fig, axes = plt.subplots(nrows=3, ncols=1)

    for d in range(2, 5):
        all_data = pd.read_csv(f"data/backtrack_s10000_k6_d{d}.csv", index_col=0)
        s = all_data.index.to_list()
        for k in sorted(all_data.columns):
            k_data = all_data[k]

            # Outliers
            roll = k_data.rolling(window=10, center=True, closed="left", min_periods=1)
            mean, std = roll.mean(), roll.std()

            all_data["rolling_mean"] = mean
            all_data["rolling_std"] = std
            threshold = 1.0
            outliers = np.abs(k_data - all_data["rolling_mean"]) > threshold * all_data['rolling_std']

            # Remplacer outliers avec la valeur moyenne
            # all_data.loc[outliers, k] = all_data["rolling_mean"][outliers]
            # axes[d-2].plot(s, all_data[k], label=f"k={k}")

            # OU supprimer outliers
            # data_cleaned = k_data[~outliers].copy()
            # axes[d-2].plot(data_cleaned.index.to_list(), data_cleaned, label=f"k={k}")
            axes[d-2].plot(k_data.index.to_list(), k_data, label=f"k={k}")

            axes[d-2].set_xlabel("S")
            axes[d-2].set_ylabel("Temps CPU (sec)")

            axes[d-2].text(0.05, 0.90, s=f"d={d}", horizontalalignment='center',
                           verticalalignment='center', transform=axes[d-2].transAxes)

    h, _ = axes[0].get_legend_handles_labels()  # eviter repetitions dans legend
    fig.legend(handles=h)
    fig.suptitle("Algorithme II. Backtrack")
    plt.subplots_adjust(left=0.087, bottom=0.11, right=0.9, top=0.93, wspace=0.2, hspace=0.33)
    plt.show()
