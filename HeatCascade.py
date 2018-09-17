class Stream():
    """
    A class that represents a single stream in a given system.

    Args:
        T_in: The temperature when the stream enters the system (in degree Celsius).
        T_out: The temeprature when the steam exits the system (in degree Celsius).
        Cp: The heat capacity flowrate of the stream (in kW/K).
        T_min: The pinch of the system (default=10 degree Celsius.)
    """

    def __init__(self, T_in, T_out, Cp, T_min=10):
        self.T_in = T_in
        self.T_out = T_out
        self.Cp = Cp
        self.T_min = T_min

        # Identify which type of stream it is
        if T_in > T_out:
            self.type = 'hot'
        else:
            self.type = 'cold'

    def shiftTemperature(self):
        """
        shift the temperature based on which type of stream it is.
        """
        if self.type == 'hot':
            self.T_in_shifted = self.T_in - self.T_min/2
            self.T_out_shifted = self.T_out - self.T_min/2
        else:
            self.T_in_shifted = self.T_in + self.T_min/2
            self.T_out_shifted = self.T_out + self.T_min/2
    

class System():
    """
    A class that represents the whole heat cascade system.

    Args:
        stream_list: A list of streams that consist the system.
    """

    def __init__(self, stream_list):
        self.stream_list = stream_list
        self.temperature_list = list()

    def formulateIntervals(self):
        """
        Formulate the intervals by using the shifted temperatures of all streams.

        Return:
<<<<<<< HEAD
            temperature_list: a reversely sorted list of temperature intervals.
=======
            temperature_list: a sorted list of temperature intervals
>>>>>>> 4ac8a9b16f143dbf5cc2bdb47055a5c9aa34c42f
        """
        for stream in self.stream_list:
            if stream.T_in_shifted not in self.temperature_list:
                self.temperature_list.append(stream.T_in_shifted)
            if stream.T_out_shifted not in self.temperature_list:
                self.temperature_list.append(stream.T_out_shifted) 
        
<<<<<<< HEAD
        return sorted(self.temperature_list, reverse=True)
=======
        return sorted(self.temperature_list)
>>>>>>> 4ac8a9b16f143dbf5cc2bdb47055a5c9aa34c42f

def main():
    one = Stream(20, 135, 2)
    two = Stream(170, 60, 3)
    three = Stream(80, 140, 4)
    four = Stream(150, 30, 1.5)
    streams = [one, two, three, four]
    for s in streams:
        s.shiftTemperature()
    sys = System(streams)
    print(sys.formulateIntervals())

if __name__ == '__main__':
    main()
