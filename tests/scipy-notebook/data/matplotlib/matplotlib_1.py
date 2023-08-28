# Matplotlib: Create a simple plot example.
# Refs: https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html

# Optional test with [Matplotlib Jupyter Integration](https://github.com/matplotlib/ipympl)
# %matplotlib widget
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(
    xlabel="time (s)",
    ylabel="voltage (mV)",
    title="About as simple as it gets, folks",
)
ax.grid()

# Note that the test can be run headless by checking if an image is produced
file_path = "/tmp/test.png"
fig.savefig(file_path)
print(f"File {file_path} saved")
