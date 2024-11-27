from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import obd
import os
import argparse

class HUD:
    def __init__(self, root, testing = False):
        self.root = root
        #Gather information about the display
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        #close window on escape press
        self.root.bind('<Escape>', lambda e : root.destroy()) 
        self.base_folder = os.path.dirname(__file__) #Saving the path to this folder

        #Builds connection to the car
        self.connection = obd.OBD()
        
        #Setting up a parser to enable additional configurability
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true', help='Shows the frame borders to help with the placement of the UI elements')
        parser.add_argument('--bottom_orientation', action='store_true', help='Orients the UI at the bottom of the screen to support larger screens')
        self.args = parser.parse_args()

        #Setting up the variables
        self.speed = StringVar(value='0')
        self.throttlepercent = StringVar(value='0%')
        self.rpm = StringVar(value='0')
        self.temperature = StringVar(value='0°C')
        
        #Start the setup process of the window if not in testing mode
        if not testing:
            self.setup_window()

        #Configure a background style
        self.background_style = ttk.Style()
        self.background_style.configure('blackbg.TFrame', background='black')

        #begin the update loop if the car is connected
        if self.connection.is_connected():
            self.update_data()

    #Setting up the window that will contain the application
    def setup_window(self):
        self.root.title("Heads-up-display")
        self.root.attributes("-fullscreen", True)
        self.root.configure(background='black')

        #Starting the setup process for the frames contained in the window
        self.setup_frames()

        #Giving the frames their right weights so they conform to their given positions
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    #Setting up the frames that fill the window and putting them at their right positions
    def setup_frames(self):
        orientation = 'S' if self.args.bottom_orientation else 'NESW'

        self.mainframe = ttk.Frame(self.root, width=self.screen_width, height=self.screen_height, style='blackbg.TFrame')
        self.mainframe.grid(column=0, row=0, sticky=orientation)

        self.upperframe = ttk.Frame(self.mainframe, width=self.screen_width/2, height=self.screen_height/4, style='blackbg.TFrame')
        self.upperframe.grid(column=0, row=0, sticky='S')

        self.lowerframe = ttk.Frame(self.mainframe, width=self.screen_width/2, height=self.screen_height/4, style='blackbg.TFrame')
        self.lowerframe.grid(column=0, row=1, sticky='N')

        self.speedframe = ttk.Frame(self.upperframe, width=(self.screen_width/2)/3, height=self.screen_height/4, style='blackbg.TFrame')
        self.speedframe.grid(column=1, row=0)

        self.throttleframe = ttk.Frame(self.lowerframe, style='blackbg.TFrame')
        self.throttleframe.grid(column=1, row=0, padx=10)

        self.temperatureframe = ttk.Frame(self.lowerframe, style='blackbg.TFrame')
        self.temperatureframe.grid(column=2, row=0, padx=10)

        #Enables the frame borders if in debug mode
        if self.args.debug:
            self.enable_frame_borders()
        
        #Starts the setup process for the labels
        self.setup_labels()

    #Setting up all the labels that fill the frames and connecting them to their respective variables
    def setup_labels(self):
        self.speed_label = ttk.Label(self.speedframe, textvariable=self.speed, padding=5, foreground='white', background='black', font='Arial 80 bold', justify='right')
        self.speed_label.grid(column=0, row=0, columnspan=2, rowspan=2)
        self.unit_label = ttk.Label(self.speedframe, text='km/h', foreground='white', background='black', font='Arial 15 bold')
        self.unit_label.grid(column=2, row=1)

        self.throttlelabel = ttk.Label(self.throttleframe, textvariable=self.throttlepercent, foreground='white', background='black', font='Arial 30 bold')
        self.throttlelabel.grid(column=0, row=0)
        self.rpmlabel = ttk.Label(self.throttleframe, textvariable=self.rpm, foreground='white', background='black', font='Arial 30 bold')
        self.rpmlabel.grid(column=2, row=0)
        self.rpmunitlabel = ttk.Label(self.throttleframe, text='RPM', foreground='white', background='black', font='Arial 15 bold')
        self.rpmunitlabel.grid(column=3, row=0)

        self.throttleprogressbar = ttk.Progressbar(self.throttleframe, orient='horizontal', length=200, mode='determinate', maximum=100)
        self.throttleprogressbar.grid(column=1, row=0, padx=5)

        self.temperature_image = ImageTk.PhotoImage(Image.open(os.path.join(self.base_folder, 'assets/tempnorm.png')))
        self.temperature_label = ttk.Label(self.temperatureframe, image=self.temperature_image, background='black')
        self.temperature_label.grid(column=0, row=0)
        self.temperature_label = ttk.Label(self.temperatureframe, textvariable=self.temperature, foreground='white', background='black', font='Arial 30 bold')
        self.temperature_label.grid(column=1, row=0)

    #Enables the frame borders of each frame for debug purposes
    def enable_frame_borders(self):
        for frame in [self.mainframe, self.upperframe, self.lowerframe, self.speedframe, self.throttleframe, self.temperatureframe]:
            frame.configure(borderwidth=2, relief='groove')

    #This function safely queries for the given command, unpacks its returned value and returns this value
    def query_command(self, cmd):
        if cmd not in self.connection.supported_commands:
            print(f"Command {cmd} is not supported.")
            return "0"  # Default value if command is not supported
        try:
            queried_value = self.connection.query(cmd).value
            if queried_value is not None:
                return str(int(queried_value.magnitude)) if queried_value.magnitude is not None else '0'
        except Exception as e:
            print(f"Error querying {cmd}: {e}")
        return '0'  #Default value on failure
    
    #Function that queries all datapoints if called and keeps frame up to date
    def update_data(self):
        current_throttle = self.query_command(obd.commands.THROTTLE_POS)
        current_rpm = self.query_command(obd.commands.RPM)
        self.current_temperature = self.query_command(obd.commands.COOLANT_TEMP)

        self.speed.set(self.query_command(obd.commands.SPEED))
        self.throttlepercent.set(f'{current_throttle}%')
        self.rpm.set(current_rpm)
        self.throttleprogressbar['value'] = current_throttle
        self.temperature.set(f'{self.current_temperature}°C')

        #updating temperature label color
        self.update_temperature_color()

        #Adds update_data to the queue to be executed by the mainloop after 100ms if the car is still connected
        if self.connection.is_connected():
            self.root.after(100, self.update_data)
        else: self.root.destroy() #closes the HUD if the connection to the car has been lost
    
    #Function to update the temperature label's colour according to the engine temperature
    def update_temperature_color(self):
        match int(self.current_temperature):
            case num if num < 60:
                self.temperature_label.config(foreground='dodgerblue')
            case num if num > 120:
                self.temperature_label.config(foreground='red')
            case _:
                self.temperature_label.config(foreground='white')



if __name__ == "__main__":
    root = Tk()
    hud = HUD(root)
    root.mainloop()