# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# from queue import Queue

# # Open the maze image and make it grayscale
# im = Image.open(r"C:\Users\User\Desktop\MazeWalker\MazeWalker\maze_photo.JPG").convert('L')
# w, h = im.size

# # Ensure all black pixels are 0 and all white pixels are 1
# binary = im.point(lambda p: p > 128 and 1 or 0)  # black (0) for walls, white (1) for paths

# # Resize to half its height and width for better visibility
# binary = binary.resize((w // 2, h // 2), Image.NEAREST)
# w, h = binary.size

# # Convert to Numpy array (maze structure)
# nim = np.array(binary)

# # Variables to hold the start and goal points
# start_point = None
# end_point = None

# # Define the BFS algorithm to find the path
# def bfs(maze, start, end):
#     directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#     visited = np.zeros_like(maze, dtype=bool)
#     visited[start] = True
#     queue = Queue()
#     queue.put((start, []))

#     while not queue.empty():
#         (node, path) = queue.get()
#         for dx, dy in directions:
#             next_node = (node[0] + dx, node[1] + dy)
#             if next_node == end:
#                 return path + [next_node]
#             if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
#                 maze[next_node] == 1 and not visited[next_node]):  # 1 represents path
#                 visited[next_node] = True
#                 queue.put((next_node, path + [next_node]))

#     return None

# # Event handling for capturing start and end points
# def on_click(event):
#     global start_point, end_point

#     if event.inaxes:
#         # Map the figure click position to the binary matrix coordinates
#         x, y = int(event.ydata), int(event.xdata)

#         # Ensure the click is within the valid area of the maze
#         if 0 <= x < nim.shape[0] and 0 <= y < nim.shape[1]:
#             # Check if the clicked point corresponds to a white (path) area in the binary matrix (i.e., value 1)
#             if nim[x, y] == 1:  # 1 represents a white space (path)
#                 if start_point is None:
#                     start_point = (x, y)
#                     print(f"Start Point: {start_point}")
#                     plt.plot(y, x, marker='o', color='green', markersize=10)
#                     plt.text(y + 0.3, x - 0.3, 'Start', color='green', fontsize=12)
#                 elif end_point is None:
#                     end_point = (x, y)
#                     print(f"End Point: {end_point}")
#                     plt.plot(y, x, marker='o', color='blue', markersize=10)
#                     plt.text(y + 0.3, x - 0.3, 'End', color='blue', fontsize=12)
#                 plt.draw()

# # Draw the maze and allow the user to select start and end points by clicking
# def draw_maze():
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.imshow(nim, cmap='gray', interpolation='nearest')  # Keep the original maze color scheme
#     fig.canvas.mpl_connect('button_press_event', on_click)
#     plt.show()

# # Function to visualize the path step by step
# def show_path_stepwise(maze, path):
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.imshow(maze, cmap='gray', interpolation='nearest')  # Keep the original maze color scheme

#     # Plot the start and end points
#     plt.plot(start_point[1], start_point[0], marker='o', color='green', markersize=10)
#     plt.text(start_point[1] + 0.3, start_point[0] - 0.3, 'Start', color='green', fontsize=12)
#     plt.plot(end_point[1], end_point[0], marker='o', color='blue', markersize=10)
#     plt.text(end_point[1] + 0.3, end_point[0] - 0.3, 'End', color='blue', fontsize=12)

#     # Plot the path step by step
#     for (x, y) in path:
#         ax.plot(y, x, marker='o', color='red', markersize=5)
#         plt.draw()
#         plt.pause(0.1)  # Add a short pause to see the path step by step

#     plt.show()

# # Main function
# if __name__ == "__main__":
#     print("Please select a maze image...")

#     # Draw the maze and allow the user to select start and end points by clicking
#     draw_maze()

#     # Wait until both start and end points are selected
#     while start_point is None or end_point is None:
#         plt.pause(0.1)

#     print(f"Start Point: {start_point}, End Point: {end_point}")

#     # Pathfinding (BFS)
#     path = bfs(nim, start_point, end_point)

#     # Show path step by step
#     if path:
#         print(f"Path: {path}")
#         show_path_stepwise(nim, path)  # Show the path step by step
#     else:
#         print("No path found.")


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
from tkinter import Tk, filedialog

# Function to open the file dialog and select an image
def upload_image():
    # Hide the tkinter root window
    root = Tk()
    root.withdraw()  # Don't need the root window
    file_path = filedialog.askopenfilename(
        title="Select a Maze Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    return file_path

# Function to process the uploaded image
def process_image(file_path):
    # Open the maze image and make it grayscale
    im = Image.open(file_path).convert('L')
    w, h = im.size

    # Ensure all black pixels are 0 and all white pixels are 1
    binary = im.point(lambda p: p > 128 and 1 or 0)  # black (0) for walls, white (1) for paths

    # Resize to half its height and width for better visibility
    binary = binary.resize((w // 2, h // 2), Image.NEAREST)
    w, h = binary.size

    # Convert to Numpy array (maze structure)
    nim = np.array(binary)
    
    return nim

# Variables to hold the start and goal points
start_point = None
end_point = None

# Define the BFS algorithm to find the path
def bfs(maze, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))

    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0] + dx, node[1] + dy)
            if next_node == end:
                return path + [next_node]
            if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
                maze[next_node] == 1 and not visited[next_node]):  # 1 represents path
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))

    return None

# Event handling for capturing start and end points
def on_click(event):
    global start_point, end_point

    if event.inaxes:
        # Map the figure click position to the binary matrix coordinates
        x, y = int(event.ydata), int(event.xdata)

        # Ensure the click is within the valid area of the maze
        if 0 <= x < nim.shape[0] and 0 <= y < nim.shape[1]:
            # Check if the clicked point corresponds to a white (path) area in the binary matrix (i.e., value 1)
            if nim[x, y] == 1:  # 1 represents a white space (path)
                if start_point is None:
                    start_point = (x, y)
                    print(f"Start Point: {start_point}")
                    plt.plot(y, x, marker='o', color='green', markersize=5)
                    plt.text(y + 0.3, x - 0.3, 'Start', color='green', fontsize=8)
                elif end_point is None:
                    end_point = (x, y)
                    print(f"End Point: {end_point}")
                    plt.plot(y, x, marker='o', color='blue', markersize=5)
                    plt.text(y + 0.3, x - 0.3, 'End', color='blue', fontsize=8)
                plt.draw()

# Draw the maze and allow the user to select start and end points by clicking
def draw_maze():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(nim, cmap='gray', interpolation='nearest')  # Keep the original maze color scheme
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

# Function to visualize the path step by step
def show_path_stepwise(maze, path):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(maze, cmap='gray', interpolation='nearest')  # Keep the original maze color scheme

    # Plot the start and end points
    plt.plot(start_point[1], start_point[0], marker='o', color='green', markersize=5)
    plt.text(start_point[1] + 0.3, start_point[0] - 0.3, 'Start', color='green', fontsize=8)
    plt.plot(end_point[1], end_point[0], marker='o', color='blue', markersize=5)
    plt.text(end_point[1] + 0.3, end_point[0] - 0.3, 'End', color='blue', fontsize=8)

    # Plot the path step by step
    for (x, y) in path:
        ax.plot(y, x, marker='o', color='red', markersize=4)
        plt.draw()
        plt.pause(0.06)  # Add a short pause to see the path step by step

    plt.show()

# Main function
if __name__ == "__main__":
    print("Please select a maze image...")

    # Open file dialog to upload maze image
    file_path = upload_image()

    # Process the uploaded image
    nim = process_image(file_path)

    # Draw the maze and allow the user to select start and end points by clicking
    draw_maze()

    # Wait until both start and end points are selected
    while start_point is None or end_point is None:
        plt.pause(0.1)

    print(f"Start Point: {start_point}, End Point: {end_point}")

    # Pathfinding (BFS)
    path = bfs(nim, start_point, end_point)

    # Show path step by step
    if path:
        print(f"Path: {path}")
        show_path_stepwise(nim, path)  # Show the path step by step
    else:
        print("No path found.")
