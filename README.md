# File-Metadata-Visualization-Tool

Kyle Furtado

University of Massachusetts Dartmouth - CIS 542 Project

12/11/2023

## Getting Started
1) Clone this repository onto your local machine.
2) Install Python 3 if it is not already (I used Python 3.10).
3) Install the libraries imported at the top of main.py if they are not already ("pip install ..." or "pip3 install ...").

## Working with the Tool
1) Run main.py (from an IDE or terminal).
2) Your native file explorer will open. Select the directory you want to visualize. Click the "Choose" button.
3) A "File Type Selection" window will open. Check which file types present in the directory you want to visualize. Click the "Generate Visualizations" button.
4) A table of all the metadata used and the following visualizations will appear:
- Bar Chart - File Type Distribution
- Pie Chart - File Type Distribution
- Stacked Area Chart - Access Time Distribution by File Type
- KDE Histogram - File Size Distribution
- Line Chart - File Creation and Modification Trends over Time
- Scatterplot - File Sizes vs. Modification Dates (Colored by Type)
- Scatterplot - File Size vs. Time Created (Colored by Type)
- Scatterplot - Time Last Accessed vs. Time Created (Colored by Type)
5) Go back to Step 3 and repeat the process generating different sets of visualizations from the "File Type Selection" window.
6) Terminate the tool when finished.
