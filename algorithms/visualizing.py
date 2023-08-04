"""
    Utility file regarding all methods used for visualizing the final paths,
    clusters, and anything else of relevance to the Pool app.
"""


# ------ Environment Setup ------ #
import matplotlib.pyplot as plt             # visualizing path, clusters


# ------ Visualizing Results ------ #
"""
    Visualizes the path using a basic plotting approach. Order is set by the
    results of the algorithm.
"""
def visualize_path(ordered_coordinates: np.ndarray) -> None:
    # extract values
    x_values, y_values = zip(*ordered_coordinates)

    # plotting #
    # setup plot & points
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, marker="o", linestyle="-", color="b", markersize=8)

    # labels
    plt.text(
        x_values[0],
        y_values[0],
        "Start",
        ha="right",
        va="bottom",
        fontsize=12,
        weight="bold",
    )
    plt.text(
        x_values[-1],
        y_values[-1],
        "End",
        ha="left",
        va="top",
        fontsize=12,
        weight="bold",
    )
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.title("Path Visualization")
    plt.grid(True)

    # show plot & save
    plt.savefig("../datasets/path.png", dpi=100)
    plt.show()


"""
    Visualizes all the clusters created.
"""
def visualize_clusters(clusters: list) -> None:
    # setup #
    # constants
    num_clusters = len(clusters)

    # colors
    cmap = plt.cm.get_cmap("tab10")
    colors = [cmap(i) for i in np.linspace(0, 1, num_clusters)]

    # plotting #
    # put points
    plt.figure(figsize=(8, 6))
    for i, cluster in enumerate(clusters):
        x, y = zip(*cluster)
        plt.scatter(x, y, color=colors[i], label=f"Cluster {i+1}")

    # labeling
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Clusters Visualization")
    plt.legend()
    plt.grid(True)
    plt.savefig("../datasets/cluster.png")
    plt.show()


"""
    Visualizes the clusters and the paths generated.
"""
def visualize_whole(paths):
    # plotting #
    # setup figure
    plt.figure()
    
    # setup colors
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        
    # plot every point & path
    for idx, path in enumerate(paths):
        x = [point[0] for point in path]
        y = [point[1] for point in path]
        plt.plot(x, y, color=colors[idx % len(colors)], marker='o', label=f'Path {idx+1}')
    
    # labeling
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Visualizing Paths')
    plt.legend()
    plt.grid(True)
    plt.grid("../datasets/final_results.png")
    plt.show()

