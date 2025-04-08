"""
********************************************************************************
 _  _  _ ___ _     _ 
| \|_)/ \ _/| \  ||_|
|_/| \\_//__|_/\_|| |
                                                          
--------------------------------------------------------------------------------
File:         csv_import_sharper.py
Author:       drozdja
Created:      2025-04-08
Description:  This script imports points from csv file (x - 1st column, y - 2nd
                column, without headers) to Salome sharper, and creates a closed
                curve from those points.
              
Usage:        Change the csv_path so it points to the right file. In Salome 
                Sharper press Ctrl+T, and open this script.
Dependencies: [salome sharper 9.14, csv]
Revision History:
    - 2025-04-08: Initial creation.
********************************************************************************
"""

import salome.shaper.model as model
import csv

model.begin()
partSet = model.moduleDocument()
Part = model.addPart(partSet)
Part_doc = Part.document()

# Create a new sketch on the XOY plane
sketch = model.addSketch(Part_doc, model.defaultPlane("XOY"))
sketch.setName("Airfoil_Sketch")

# Define CSV file path (update wtith your file location)
csv_path = "path/to/file/Naca0015_150_clean.csv"

# Read points from CSV (assumes two columns: X and Y)
points = []
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            x, y = float(row[0]), float(row[1])
            points.append((x, y))
        except ValueError:
            print("Skipping invalid row:", row)

# Ensure the curve is closed: add the first point at the end if needed
if points[0] != points[-1]:
    points.append(points[0])

# Create line segments by directly providing coordinates
lines = []
for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]
    line = sketch.addLine(x1, y1, x2, y2)
    lines.append(line)

model.do()

# Create selections from each line using its feature name
selections = [model.selection("EDGE", line.feature().name()) for line in lines]

# Combine the selected lines into a single wire (closed polyline)
wire = model.addWire(Part_doc, selections, True)
wire.setName("Airfoil_Wire")
model.do()

# Create a selection for the wire.
# Use the wire feature's name (e.g. "Airfoil_Wire") and wrap it in a list.
wire_sel = model.selection("WIRE", wire.feature().name())

# Now apply a translation to the wire by passing a list of selections.
translated_wire = model.addTranslation(Part_doc, [wire_sel], 10, 0, 0)
translated_wire.setName("Translated_Airfoil_Wire")
model.do()

model.end()

