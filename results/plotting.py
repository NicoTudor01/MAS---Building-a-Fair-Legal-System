import matplotlib.pyplot as plt
import numpy as np

def plot_multi_sentiment(data):
    data = np.array(data).T 

    x = np.arange(data.shape[1]) 

    for i in range(data.shape[0]):
        plt.plot(x, data[i], marker='o', label=f'Juror {i+1}')

    plt.xlabel("Round")
    plt.ylabel("Sentiment (Normalized)")
    plt.title("Juror Sentiment Over Time")

    plt.xticks(
        ticks=x,
        labels=[f"Round {i+1}" for i in x]
    )

    plt.legend()
    plt.show()

def plot_bar_single(data):
    data = np.array(data)

    first_round = data[0]

    x = np.arange(len(first_round))

    plt.bar(x, first_round)

    plt.xlabel("Juror")
    plt.ylabel("Sentiment (Normalized)")
    plt.title("Juror Sentiment (Single Run)")

    plt.xticks(
        ticks=x,
        labels=[f"Juror {i+1}" for i in x]
    )

    plt.show()