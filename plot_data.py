import matplotlib.pyplot as plt
import pandas as pd
if __name__ == "__main__":
    fig, axes = plt.subplots()

    all_data = pd.read_csv("data/test4.csv", index_col=0)
    print(all_data)
    # Tracer S <-> temps.
    s_values = all_data.index.to_list()
    # print(all_data.columns)
    for k in all_data.columns:
        t_values = all_data[k]
        # print(k, t_values)
        axes.plot(s_values, t_values, label=f"k={k}")

    fig.legend()
    axes.set_xlabel("S")
    axes.set_ylabel("Temps d'exécution (s)")
    plt.show()
