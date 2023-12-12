# File-Metadata-Visualization-Tool

Kyle Furtado

University of Massachusetts Dartmouth - CIS 542 Project (Fall 2023) 

12/11/2023

## Goal
The primary goal of this project is to develop a tool that generates visual representations of metadata extracted from files in a selected directory. These visualizations will allow users to analyze a directory’s overall content at a quick glance. For instance, the organization of the directory will be exhibited, making it easier to search for files of interest. From a digital forensics perspective, this tool will provide insight on files and provide preliminary aid in evidence analysis, timeline reconstruction, identifying patterns/trends, and determining points of interest. It is important to note that this tool is not intended to single-handedly solve digital forensics investigations, but is rather meant to be the first step in looking at the overall structure and behavior of the files in a directory under analysis.

## Scope
This tool exists as a simple graphical user interface (GUI) that allows a user to select a directory from their device’s native file explorer, filter what file types to visualize, and then click to produce a variety of general data analysis visualizations. This tool does not look to implement any Artificial Intelligence or Machine Learning predictions on the directory. Thus, any anomaly, pattern, and correlation detections will have to be done manually by the user themselves.



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
