import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
fig.set_tight_layout(True)

# Query the figure's on-screen size and DPI. Note that when saving the figure to
# a file, we need to provide a DPI for that separately.
print('fig size: {0} DPI, size in inches {1}'.format(
    fig.get_dpi(), fig.get_size_inches()))

var_t="Freq"
var_x="Time"
var_y="xx"
source="scope"

min_y=min(merge_df[(var_y+"_"+source)].min(),0)
max_y=merge_df[(var_y+"_"+source)].max()
ax.set_ylim(min_y,max_y)

# Plot a scatter that persists (isn't redrawn) and the initial line.
var_t_vals = merge_df[var_t].unique()
var_t_val=var_t_vals[0]
var_x_vals =merge_df.loc[merge_df[var_t]==var_t_val,var_x]

var_y_vals = merge_df.loc[merge_df[var_t]==var_t_val,(var_y+"_"+source)]
#ax.scatter(x, x + np.random.normal(0, 3.0, len(x)))
line, = ax.plot(var_x_vals, var_y_vals, color=colour_models(var_y), linewidth=2)


def update(i):
    var_t_val=var_t_vals[i]
    label = str(var_t_val)
#    print(label)
    # Update the line and the axes (with a new xlabel). Return a tuple of
    # "artists" that have to be redrawn for this frame.
    
    var_x_vals = merge_df.loc[merge_df[var_t]==var_t_val,var_x]
    
    var_y_vals = merge_df.loc[merge_df[var_t]==var_t_val,(var_y+"_"+source)]
    line.set_xdata(var_x_vals)
    line.set_ydata(var_y_vals)
    ax.set_xlabel(label)
    return line, ax

if __name__ == '__main__':
    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 200ms between frames.
    anim = FuncAnimation(fig, update, frames=np.arange(0, len(var_t_vals)), interval=20)
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('line.gif', dpi=80, writer='imagemagick')
    else:
        # plt.show() will just loop the animation forever.
        plt.show()