import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from HUD import HUD
import obd

class TestHUD(unittest.TestCase):
    
    def setUp(self):
        #Setting up the HUD instance and mocking ther parser to not expect anything
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(debug=False, bottom_orientation=False)):
            self.root = Tk()
            self.hud = HUD(self.root, testing=True)
    
    @patch('obd.OBD')
    def test_query_command_supported(self, MockOBD):
        #Mocking the OBD connection and adding supported commands
        self.hud.connection = MockOBD()
        self.hud.connection.supported_commands = {obd.commands.SPEED}
        
        #simulate a positive outcome
        mock_response = MagicMock()
        mock_response.value.magnitude = 50  #Sets speed to 50 km/h
        self.hud.connection.query.return_value = mock_response
        
        result = self.hud.query_command(obd.commands.SPEED)
        self.assertEqual(result, '50')  #Expects 50 km/h as String
    
    @patch('obd.OBD')
    def test_query_command_unsupported(self, MockOBD):
        #Mocking the OBD connection and removing all supported commands
        self.hud.connection = MockOBD()
        self.hud.connection.supported_commands = set()
        result = self.hud.query_command(obd.commands.SPEED)
        self.assertEqual(result, '0')  #Expects return value '0' when a command is not supported

    @patch('obd.OBD')
    def test_query_command_exception(self, MockOBD):
        #Mocking the OBD connection, adding supported commands and introducing a connection error
        self.hud.connection = MockOBD()
        self.hud.connection.supported_commands = {obd.commands.SPEED}
        self.hud.connection.query.side_effect = Exception("Connection error")
        
        result = self.hud.query_command(obd.commands.SPEED)
        self.assertEqual(result, '0')  #Expects return value '0' when an exception occurs

    def test_update_temperature_color(self):
        #Mocking the temperature label
        self.hud.temperature_label = MagicMock()

        #Testing the 'low' temperature color of the label
        self.hud.current_temperature = '50'
        self.hud.update_temperature_color()
        self.hud.temperature_label.config.assert_called_with(foreground='dodgerblue')

        #Testing the 'normal' temperature color of the label
        self.hud.current_temperature = '90'
        self.hud.update_temperature_color()
        self.hud.temperature_label.config.assert_called_with(foreground='white')

        #Testing the 'hot' temperature color of the label
        self.hud.current_temperature = '130'
        self.hud.update_temperature_color()
        self.hud.temperature_label.config.assert_called_with(foreground='red')
    
    @patch('obd.OBD')
    def test_update_data(self, MockOBD):
        #Mocking the OBD connection, the throttle progressbar and the temperature label
        self.hud.connection = MockOBD
        self.hud.throttleprogressbar = MagicMock()
        self.hud.temperature_label = MagicMock()

        #Setting the return value of every query to 50
        with patch.object(self.hud, 'query_command', return_value = 50):
            self.hud.update_data()

            #Test if every value has been correctly updated
            self.assertEqual(self.hud.speed.get(), '50')
            self.assertEqual(self.hud.throttlepercent.get(), '50%')
            self.assertEqual(self.hud.rpm.get(), '50')
            self.assertEqual(self.hud.temperature.get(), '50°C')


if __name__ == '__main__':
    unittest.main()