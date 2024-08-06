import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

import matplotlib
matplotlib.use('Agg')

def plot_gantt_chart(tasks, assignments):
    # Convert dates to datetime objects
    for i in range(len(tasks)):
        tasks[i] = list(tasks[i])
        tasks[i][3] = datetime.strptime(tasks[i][3], '%Y-%m-%d')
        tasks[i][4] = datetime.strptime(tasks[i][4], '%Y-%m-%d')

    # Create a figure and a subplot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Add bars for each task
    for task in tasks:
        task_id, task_name, task_position, start_date, end_date, task_predecessors = task
        duration = (end_date - start_date).days
        ax.barh(task_name, duration, left=start_date, color='skyblue')
        ax.text(start_date + (end_date - start_date) / 2, task_name, assignments[task_name], va='center', ha='center', color='black')

    # Format the x-axis to show dates
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Set labels and title
    plt.xlabel('Date')
    plt.ylabel('Task')
    plt.title('Project Schedule Gantt Chart')

    # Return the figure instead of showing it
    plt.grid(True)
    return fig
