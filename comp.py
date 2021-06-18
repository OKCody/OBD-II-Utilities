import pandas
import matplotlib.pyplot as mpl
from PIL import Image

# Paths to CSV data files
data_1 = '20210616/log_before_MAP.csv'
data_2 = '20210616/log_after_MAP.csv'

# Path to generated plot image
# Extension determines image type
plot_name = 'img/BEFORE_AFTER_INTAKE_PRESSURE.png'

# Define which parameters to plot.
# These should exactly match select headers in the data files
# If 'y_axis_alt' is unused set it equal to False
x_axis = 'RPM (revolutions_per_minute)' # often 'TIME (UTC)'
y_axis_1 = 'INTAKE_PRESSURE (kilopascal)'
y_axis_2 = 'INTAKE_PRESSURE (kilopascal)'
y_axis_alt = 'INTAKE_TEMP (degC)'

# Define color of plot lines and axis labels
y_axis_1_color = 'blue'
y_axis_2_color = 'red'

# Read each CSV data file into its own Pandas dataframe
data_1_df = pandas.read_csv(data_1)
data_2_df = pandas.read_csv(data_2)

# X-axis should typically be sorted whether it is time or otherwise
data_1_df = data_1_df.sort_values(x_axis)
data_2_df = data_2_df.sort_values(x_axis)

# Convert timestamp column to datetime datatype
data_1_df['TIME (UTC)'] = pandas.to_datetime(data_1_df['TIME (UTC)'])
data_2_df['TIME (UTC)'] = pandas.to_datetime(data_2_df['TIME (UTC)'])

# Make plot with aspect ratio of a standard sheet of paper
fig = mpl.figure(figsize=[11,8.5], dpi=100)

# Make first of two plots (top)
ax1 = mpl.subplot(211)
ax1.set_xlabel(x_axis)
ax1.set_ylabel(y_axis_1, color=y_axis_1_color)
ax1.plot(data_1_df[x_axis], data_1_df[y_axis_1], color=y_axis_1_color)
ax1.tick_params(axis='y', labelcolor=y_axis_1_color)
ax1.set_ylim(0,50)

# Add a second y-axis (right) if 'y_axis_alt' is defined
if y_axis_alt:
    ax2 = ax1.twinx()
    ax2.set_ylabel(y_axis_alt, color='black')
    ax2.plot(data_1_df[x_axis], data_1_df[y_axis_alt], color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.set_ylim(0,60)

# Make second of two plots (bottom)
ax1 = mpl.subplot(212)
ax1.set_xlabel(x_axis)
ax1.set_ylabel(y_axis_2, color=y_axis_2_color)
ax1.plot(data_2_df[x_axis], data_2_df[y_axis_2], color=y_axis_2_color)
ax1.tick_params(axis='y', labelcolor=y_axis_2_color)
ax1.set_ylim(0,50)

# Add a second y-axis (right) if 'y_axis_alt' is defined
if y_axis_alt:
    ax2 = ax1.twinx()
    ax2.set_ylabel(y_axis_alt, color='black')
    ax2.plot(data_2_df[x_axis], data_2_df[y_axis_alt], color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.set_ylim(0,60)

# Save plot using provided extension as filetype
mpl.savefig(plot_name)

# Dsiplay plot using system default viewer.
# mpl requires QT. Avoiding installing QT . . .
img = Image.open(plot_name)
img.show()
