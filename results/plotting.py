import matplotlib.pyplot as plt
import numpy as np

def plot_multi_sentiment(data):
    data = np.array(data)
    x = np.arange(data.shape[1])

    for i in range(data.shape[0]):
        plt.plot(x, data[i], label=f'Juror {i+1}')

    plt.xlabel("Round")
    plt.ylabel("Sentiment (Normalized)")
    plt.title("Judge Sentiment Over Time")
    plt.legend()
    plt.show()