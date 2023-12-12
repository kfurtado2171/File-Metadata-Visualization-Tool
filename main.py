'''
Kyle Furtado
CIS 542
12/11/2023
File Metadata Visualization Tool
'''

''' ----- libraries ----- '''
# misc
import os                       # os access
import pwd                      # user account access
import csv                      # csv file manipulation
from datetime import datetime   # date manipulation

# gui
import tkinter as tk
from tkinter import filedialog, IntVar, Canvas, Frame, Scrollbar, ttk

# data manipulation
import pandas as pd
from collections import defaultdict, Counter

# data visualization
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import plotly.express as px


''' ----- file manipulation ----- '''
# combine .jpeg and .jpg
def combine_jpeg(file_extension):
    return '.jpeg' if file_extension.lower() == '.jpg' else file_extension.lower()


# make a list of metadata for each file in the directory
def get_metadata(directory):
    file_metadata = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_stat = os.stat(file_path)

            _, file_extension = os.path.splitext(file)
            file_extension = combine_jpeg(file_extension)

            metadata = {
                'Filename': file,
                'File Extension': file_extension,
                'Path': file_path,
                'Size (bytes)': file_stat.st_size,
                'Last Modified': file_stat.st_mtime,
                'Last Accessed': file_stat.st_atime,
                'Created': file_stat.st_ctime,
                'Owner': pwd.getpwuid(file_stat.st_uid).pw_name
            }

            file_metadata.append(metadata)

    return file_metadata


# create a csv of metadata
def create_csv(metadata, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = metadata[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in metadata:
            writer.writerow(data)


''' ----- visualization creation ----- '''
# display a table of the metadata
def metadata_table(metadata):
    table_window = tk.Toplevel()
    table_window.title('Metadata Table')

    tree = ttk.Treeview(table_window)
    tree["columns"] = list(metadata[0].keys())

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for item in metadata:
        values = [item[col] for col in tree["columns"]]
        tree.insert("", "end", values=values)

    tree.pack(expand=True, fill='both')


# display a bar chart of the file type distribution
def bar_chart(metadata, selected_file_types):
    file_types_count = defaultdict(int)

    for file in metadata:
        _, file_extension = os.path.splitext(file['Filename'])
        file_extension = combine_jpeg(file_extension)

        if not selected_file_types or file_extension in selected_file_types:
            file_types_count[file_extension] += 1

    sorted_file_types_count = dict(sorted(file_types_count.items(), key=lambda x: x[1], reverse=True))

    color_map = cm.tab20c

    plt.figure(num='Bar Chart - File Type Distribution', figsize=(1920 / 100, 1080 / 100), dpi=100)

    file_types = list(sorted_file_types_count.keys())
    counts = list(sorted_file_types_count.values())

    plt.bar(file_types, counts, color=[color_map(i) for i in range(len(sorted_file_types_count))], label=file_types)
    plt.xlabel('File Type')
    plt.ylabel('Count')
    plt.title('File Type Distribution')
    plt.legend()


# display a pie chart of the file type distribution
def pie_chart(metadata, selected_file_types):
    file_types_count = defaultdict(int)

    for file in metadata:
        _, file_extension = os.path.splitext(file['Filename'])
        file_extension = combine_jpeg(file_extension)

        if not selected_file_types or file_extension in selected_file_types:
            file_types_count[file_extension] += 1

    sorted_file_types_count = dict(sorted(file_types_count.items(), key=lambda x: x[1], reverse=True))

    color_map = cm.tab20c

    plt.figure(num='Pie Chart - File Type Distribution', figsize=(1920 / 100, 1080 / 100), dpi=100)

    file_types = list(sorted_file_types_count.keys())
    counts = list(sorted_file_types_count.values())

    plt.pie(counts, colors=[color_map(i) for i in range(len(sorted_file_types_count))], labels=file_types, autopct='')
    plt.title('File Type Distribution')
    plt.legend(title='File Types', loc='upper right', bbox_to_anchor=(1.1, 1))


# display a stacked area chart of the access time distribution by file type
def stacked_area_chart(metadata, selected_file_types):
    plt.figure(num='Stacked Area Chart - Access Time Distribution by File Type', figsize=(1920 / 100, 1080 / 100), dpi=100)

    file_types_count = defaultdict(int)
    access_times_by_type = defaultdict(list)

    for file in metadata:
        _, file_extension = os.path.splitext(file['Filename'])
        file_extension = combine_jpeg(file_extension)

        if not selected_file_types or file_extension in selected_file_types:
            file_types_count[file_extension] += 1
            access_times_by_type[file_extension].append(file['Last Accessed'])

    sorted_file_types_count = dict(sorted(file_types_count.items(), key=lambda x: x[1], reverse=True))

    color_map = cm.tab20c

    for i, (file_type, access_times) in enumerate(sorted_file_types_count.items()):
        access_dates = [datetime.fromtimestamp(timestamp).strftime('%Y-%m') for timestamp in
                        access_times_by_type[file_type]]
        plt.hist(access_dates, bins=20, alpha=0.7, label=file_type, stacked=True, color=color_map(i))

    plt.xlabel('Access Time (Year-Month)')
    plt.ylabel('Count')
    plt.title('Access Time Distribution by File Type')
    plt.legend()
    plt.xticks(rotation=45, ha='right')


# display a kde histogram of the file size distribution
def kde_histogram(metadata, selected_file_types):
    filtered_metadata = [file for file in metadata if
                         combine_jpeg(os.path.splitext(file['Filename'])[1]) in selected_file_types]

    file_sizes = [file['Size (bytes)'] for file in filtered_metadata]

    plt.figure(num='KDE Histogram - File Size Distribution', figsize=(1920 / 100, 1080 / 100), dpi=100)

    plt.hist(file_sizes, bins=20, density=True, color='skyblue', edgecolor='black', alpha=0.7)
    sns.kdeplot(file_sizes, color='red', linewidth=2)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Density')
    plt.title('File Size Distribution')


# display line chart of file creation and modification trends over time
def line_chart(metadata, selected_file_types):
    filtered_metadata = [file for file in metadata if
                         combine_jpeg(os.path.splitext(file['Filename'])[1]) in selected_file_types]

    creation_dates = [datetime.fromtimestamp(file['Created']).strftime('%Y-%m-%d') for file in filtered_metadata]
    modification_dates = [datetime.fromtimestamp(file['Last Modified']).strftime('%Y-%m-%d') for file in
                          filtered_metadata]

    creation_date_counts = Counter(creation_dates)
    modification_date_counts = Counter(modification_dates)

    sorted_creation_dates = sorted(creation_date_counts.keys())
    sorted_modification_dates = sorted(modification_date_counts.keys())

    data = {
        'Date': sorted_creation_dates + sorted_modification_dates,
        'Count': [creation_date_counts[date] for date in sorted_creation_dates] + [modification_date_counts[date] for
                                                                                   date in sorted_modification_dates],
        'Event': ['File Creation'] * len(sorted_creation_dates) + ['File Modification'] * len(
            sorted_modification_dates),
    }

    df = pd.DataFrame(data)

    fig = px.line(df, x='Date', y='Count', color='Event', markers=True,
                  title='Line Chart - File Creation and Modification Trends over Time')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(hovermode='x unified')

    fig.show()


# display a scatter plot of file size vs modification date colored by type
def scatter_plot_size_vs_modification(metadata, selected_file_types):
    filtered_metadata = [file for file in metadata if
                         combine_jpeg(os.path.splitext(file['Filename'])[1]) in selected_file_types]

    file_sizes = [file['Size (bytes)'] for file in filtered_metadata]
    modification_dates = [datetime.fromtimestamp(file['Last Modified']) for file in filtered_metadata]

    plotly_data = pd.DataFrame({'Filename': [file['Filename'] for file in filtered_metadata],
                                'Modification Date': modification_dates,
                                'Size': file_sizes,
                                'File Type': [combine_jpeg(os.path.splitext(file['Filename'])[1]) for file
                                              in filtered_metadata]})

    df = pd.DataFrame(plotly_data)

    fig = px.scatter(df, x='Modification Date', y='Size', color='File Type', hover_data=['Filename'])

    fig.update_layout(title='Scatterplot - File Sizes vs. Modification Dates',
                      xaxis_title='Modification Date',
                      yaxis_title='File Size (bytes)',
                      xaxis=dict(tickangle=45))

    fig.show()


# display a scatter plot of file size vs creation date colored by type
def scatter_plot_size_vs_created(metadata, selected_file_types):
    filtered_metadata = [file for file in metadata if
                         combine_jpeg(os.path.splitext(file['Filename'])[1]) in selected_file_types]

    created_times = [datetime.fromtimestamp(file['Created']) for file in filtered_metadata]
    file_sizes = [file['Size (bytes)'] for file in filtered_metadata]

    plotly_data = pd.DataFrame({'Filename': [file['Filename'] for file in filtered_metadata],
                                'Created': created_times,
                                'Size': file_sizes,
                                'File Type': [combine_jpeg(os.path.splitext(file['Filename'])[1]) for file
                                              in filtered_metadata]})

    fig = px.scatter(plotly_data, x='Created', y='Size', color='File Type', hover_data=['Filename'])

    fig.update_layout(title='Scatterplot - File Size vs. Time Created',
                      xaxis_title='Time Created',
                      yaxis_title='File Size (bytes)',
                      xaxis=dict(tickangle=45),
                      legend_title='File Type')

    fig.show()

# display a scatter plot of file last access date vs creation date colored by type
def scatter_plot_access_vs_created(metadata, selected_file_types):
    filtered_metadata = [file for file in metadata if
                         combine_jpeg(os.path.splitext(file['Filename'])[1]) in selected_file_types]

    created_times = [datetime.fromtimestamp(file['Created']) for file in filtered_metadata]
    last_accessed_times = [datetime.fromtimestamp(file['Last Accessed']) for file in filtered_metadata]
    file_types = [combine_jpeg(os.path.splitext(file['Filename'])[1]) for file in filtered_metadata]

    plotly_data = pd.DataFrame({'Filename': [file['Filename'] for file in filtered_metadata],
                                'Created': created_times,
                                'Last Accessed': last_accessed_times,
                                'File Type': file_types})

    fig = px.scatter(plotly_data, x='Created', y='Last Accessed', color='File Type', hover_data=['Filename'])

    fig.update_layout(title='Scatterplot - Time Last Accessed vs. Time Created',
                      xaxis_title='Time Created',
                      yaxis_title='Time Last Accessed',
                      xaxis=dict(tickangle=45),
                      legend_title='File Type')

    fig.show()


# initiate the creation and display of all visualizations
def generate_visualizations(metadata, selected_file_types):
    file_types_count = defaultdict(int)

    for file in metadata:
        _, file_extension = os.path.splitext(file['Filename'])
        file_extension = combine_jpeg(file_extension)
        file_types_count[file_extension] += 1

    metadata_table(metadata)
    bar_chart(metadata, selected_file_types)
    pie_chart(metadata, selected_file_types)
    stacked_area_chart(metadata, selected_file_types)
    kde_histogram(metadata, selected_file_types)
    line_chart(metadata, selected_file_types)
    scatter_plot_size_vs_modification(metadata, selected_file_types)
    scatter_plot_size_vs_created(metadata, selected_file_types)
    scatter_plot_access_vs_created(metadata, selected_file_types)

    plt.show()


''' ----- gui manipulation ----- '''
# gui configuration
def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

# main function to start tool
def main():
    root = tk.Tk()
    root.withdraw()

    directory = filedialog.askdirectory(title='Select a directory')

    if not directory:
        print('No directory selected. Exiting...')
        return

    metadata = get_metadata(directory)
    csv_filename = 'file_metadata.csv'

    create_csv(metadata, csv_filename)

    file_types = set(os.path.splitext(file['Filename'])[1].lower() for file in metadata)
    file_types.discard('')

    file_type_selection = tk.Toplevel(root)
    file_type_selection.title('File Type Selection')

    selected_file_types = set()

    # keep track of what file types are checked to visualize
    def update_selected_types():
        selected_file_types.clear()
        for file_type, var in file_type_vars.items():
            if var.get():
                selected_file_types.add(file_type)

    canvas = Canvas(file_type_selection, width=400, height=400)
    frame = Frame(canvas)
    scrollbar = Scrollbar(file_type_selection, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))

    file_type_vars = {file_type: IntVar(value=1) for file_type in file_types}

    for file_type, var in file_type_vars.items():
        chk = tk.Checkbutton(frame, text=file_type, variable=var, command=update_selected_types)
        chk.pack(anchor='w')

    update_selected_types()

    generate_button = tk.Button(file_type_selection, text='Generate Visualizations',
                                command=lambda: generate_visualizations(metadata, selected_file_types))
    generate_button.pack()

    file_type_selection.mainloop()


''' ----- tool initiation ----- '''
# main() function call to start the tool
main()
