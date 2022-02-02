import matplotlib.pyplot as plt


fig, ax = plt.subplots()


def plot(scores: list[int], mean_scores: list[int]):
    ax.clear()
    ax.plot(scores)
    ax.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.title("Training...")
    plt.xlabel("Number of games")
    plt.ylabel("Score")
    plt.plot()
    plt.pause(1)
