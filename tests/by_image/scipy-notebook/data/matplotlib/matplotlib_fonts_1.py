# Matplotlib: Test tex fonts
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["pgf.texsystem"] = "pdflatex"
matplotlib.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 18,
        "axes.labelsize": 20,
        "axes.titlesize": 24,
        "figure.titlesize": 28,
    }
)
matplotlib.rcParams["text.usetex"] = True

fig, ax = plt.subplots(1, 1)
x = [1, 2]
y = [1, 2]
ax.plot(x, y, label="a label")
ax.legend(fontsize=15)

file_path = "/tmp/test_fonts.png"
fig.savefig(file_path)
print(f"File {file_path} saved")
