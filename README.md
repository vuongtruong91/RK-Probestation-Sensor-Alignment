# RK-Probestation-Sensor-Alignment
This repository contains two python scripts that both analyzes 2S, PSS, and PSP sensors.
To run the code, the script requires one argument, in the format of example.txt. The script will run with the following commands;
<python alignment.py example.txt>
The difference in the python scripts is calibrated_alignment.py takes into account of the RK probestation missing approximately 100 microns going from one edge of the sensor to the next.
The script requires the .txt to be in the same working directory as the script itself.
