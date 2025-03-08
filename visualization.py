import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.widgets import Button, RadioButtons
from maze_solver import create_maze, bfs, a_star, dfs

class MazeVisualizer:
    def __init__(self):
        self.dim = 9  # Default maze size
        self.start = None
        self.end = None
        self.path = []
        self.execution_times = {}
        self.selected_button = None
        self.path_lines = []  # Store the drawn path lines
        self.execution_texts = []  # Store execution time text objects
        self.create_size_selection_gui()

    def create_size_selection_gui(self):
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set_title("Select Maze Size")
        ax.axis("off")
        radio_ax = plt.axes([0.3, 0.4, 0.4, 0.3])
        self.radio = RadioButtons(radio_ax, ('9x9', '16x16', '21x21'))
        submit_ax = plt.axes([0.35, 0.1, 0.3, 0.2])
        submit_button = Button(submit_ax, 'Generate')
        submit_button.on_clicked(self.set_maze_size)
        plt.show()

    def set_maze_size(self, event):
        selected = self.radio.value_selected
        self.dim = int(selected.split('x')[0])
        plt.close()
        self.generate_maze()

    def generate_maze(self):
        self.maze = create_maze(self.dim)
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.imshow(self.maze, cmap=plt.cm.binary, interpolation='nearest')
        self.create_buttons()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.execution_times.clear()
        self.path_lines = []
        self.execution_texts = []
        plt.show()

    def create_buttons(self):
        ax_bfs = plt.axes([0.55, 0.02, 0.1, 0.05])
        ax_astar = plt.axes([0.67, 0.02, 0.1, 0.05])
        ax_dfs = plt.axes([0.79, 0.02, 0.1, 0.05])
        ax_fastest = plt.axes([0.91, 0.02, 0.1, 0.05])
        ax_clear = plt.axes([0.43, 0.02, 0.1, 0.05])

        self.btn_bfs = Button(ax_bfs, 'BFS')
        self.btn_astar = Button(ax_astar, 'A*')
        self.btn_dfs = Button(ax_dfs, 'DFS')
        self.btn_fastest = Button(ax_fastest, 'Fastest')
        self.btn_clear = Button(ax_clear, 'Clear Path')

        self.btn_bfs.on_clicked(lambda event: self.run_algorithm('BFS', bfs, self.btn_bfs))
        self.btn_astar.on_clicked(lambda event: self.run_algorithm('A*', a_star, self.btn_astar))
        self.btn_dfs.on_clicked(lambda event: self.run_algorithm('DFS', dfs, self.btn_dfs))
        self.btn_fastest.on_clicked(self.run_fastest)
        self.btn_clear.on_clicked(self.clear_path)

    def highlight_button(self, button):
        if self.selected_button:
            self.selected_button.ax.set_facecolor('lightgray')
        button.ax.set_facecolor('yellow')
        self.selected_button = button
        plt.draw()

    def on_click(self, event):
        if event.inaxes:
            x, y = int(event.ydata), int(event.xdata)
            if self.maze[x, y] == 1:
                return  # Prevent selecting walls
            if self.start is None:
                self.start = (x, y)
                self.ax.plot(y, x, marker='o', color='green', markersize=10)
            elif self.end is None:
                self.end = (x, y)
                self.ax.plot(y, x, marker='o', color='blue', markersize=10)
            self.fig.canvas.draw()

    def run_algorithm(self, algorithm, func, button):
        if self.start and self.end:
            self.highlight_button(button)
            path, exec_time = func(self.maze, self.start, self.end)
            if path:
                self.execution_times[algorithm] = exec_time
                self.display_execution_time()
                self.draw_path(path)

    def run_fastest(self, event):
        if self.start and self.end:
            times = {}
            for algo, func in [('BFS', bfs), ('A*', a_star), ('DFS', dfs)]:
                path, exec_time = func(self.maze, self.start, self.end)
                if path:
                    times[algo] = (path, exec_time)
            if times:
                fastest_algo = min(times, key=lambda k: times[k][1])
                self.execution_times[fastest_algo] = times[fastest_algo][1]
                self.display_execution_time()
                self.draw_path(times[fastest_algo][0])

    def display_execution_time(self):
        for text in self.execution_texts:
            text.remove()
        self.execution_texts.clear()
        y_pos = 2
        for algo, time_taken in sorted(self.execution_times.items()):
            text = self.ax.text(self.maze.shape[1] + 1, y_pos, f"{algo}: {time_taken:.4f} sec", fontsize=10, color='black')
            self.execution_texts.append(text)
            y_pos += 2
        self.fig.canvas.draw()

    def draw_path(self, path):
        for (x, y) in path:
            line, = self.ax.plot(y, x, marker='o', color='red', markersize=5)
            self.path_lines.append(line)
            self.fig.canvas.draw()
            time.sleep(0.05)

    def clear_path(self, event):
        for line in self.path_lines:
            line.remove()
        self.path_lines = []
        for text in self.execution_texts:
            text.remove()
        self.execution_texts = []
        self.fig.canvas.draw()

if __name__ == "__main__":
    MazeVisualizer()
