# **HUD Project**

A **Heads-Up Display (HUD)** for vehicles that retrieves real-time data such as speed, RPM, throttle position, and coolant temperature via an OBD-II module and displays it on a graphical user interface.  

## Functionality

The HUD connects to a vehicle via an OBD-II adapter module and visualizes real-time data on a display. It uses the **Tkinter** library for the user interface and the **OBD-Python** library to fetch data from the car's OBD-II interface.  

### Key Features

*   **Speed**: Displays the current vehicle speed (km/h).
*   **RPM**: Shows the engine revolutions per minute.
*   **Throttle Position**: Visualizes the throttle position as a percentage.
*   **Coolant Temperature**: Displays engine temperature and changes the label's color based on temperature levels.

## Installation

### Prerequisites

*   Python 3.9 or newer
*   Installed Python libraries:
    *  [ `obd`](https://github.com/brendan-w/python-OBD)
    *   [`Pillow`](https://github.com/python-pillow/Pillow)
    *   [`tkinter`](https://docs.python.org/3/library/tkinter.html)

### Steps

1.  Clone this repository

1.  Install the dependencies:

```plain
pip install obd Pillow
```

1.  Ensure an OBD-II adapter is installed and connected to your vehicle. (Not necessary if you just want to view the UI)
2.  Run the program:

```plain
python HUD.py
```

###   
Additional Options

The HUD provides two optional startup parameters:

*   `--debug`: Enables frameborders around the frames to support placement of the UI elements.
*   `--bottom_orientation`: Aligns the UI at the bottom of the screen.

Example:

```plain
python HUD.py --debug --bottom_orientation
```

## Usage

1.  **OBD-II Connection**: Connect the OBD-II module to the vehicle and to your computer.
2.  **Start the Program**: Run the HUD script.
3.  **Display**: The vehicle data will appear on the screen. To close the HUD, press `ESC`.

_Sidenote: Since there is no easy way to mirror the screen with python I chose to use [OBS Studio](https://obsproject.com/de) to mirror the screen._  

## Code Structure

*   **`HUD.py`**: Main script managing the UI and OBD-II communication.
*   **`test_hud.py`**: Contains unit tests for the project.
*   **`assets`**: Includes images and other resources.

## Tests

The project includes unit tests implemented with **unittest**. To run the tests:

```plain
python -m unittest test_hud.py
```

The tests cover functions like data updates and temperature display.
