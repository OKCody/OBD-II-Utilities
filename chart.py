import pandas
import matplotlib.pyplot as mpl
from PIL import Image

# Path to data file
data_file = '20210616/log_after_MAP.csv'

# Path to generated plot
plot_name = 'INTAKE_PRESSURE_v_RPM.png'

x_axis = 'TIME (UTC)'
y_axis = 'RPM (revolutions_per_minute)'
y_axis_alt = 'INTAKE_PRESSURE (kilopascal)'

# Read data file into a Pandas dataframe
df = pandas.read_csv(data_file)

# Convert timestamp column to datetime datatype
df['TIME (UTC)'] = pandas.to_datetime(df['TIME (UTC)'])

# Make plot with aspect ratio of a standard sheet of paper
fig, ax1 = mpl.subplots(figsize=[11,8.5], dpi=100)

# Plot parameter using left vertical axis as scale
color = 'red'
ax1.set_xlabel(x_axis)
ax1.set_ylabel(y_axis, color=color)
ax1.plot(df[x_axis], df[y_axis], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Create second vertical axis on right-hand side of figure, x-axis is shared
ax2 = ax1.twinx()

# Plot parameter using left vertical axis as scale
color = 'blue'
ax2.set_ylabel(y_axis_alt, color=color)
ax2.plot(df[x_axis], df[y_axis_alt], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Save plot using provided extension as filetype
mpl.savefig(plot_name)

# Dsiplay plot using system default viewer.
# mpl requires QT. Avoiding installing QT . . .
img = Image.open(plot_name)
img.show()
