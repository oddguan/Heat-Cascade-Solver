import numpy as np

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
            temperature_list: a reversely sorted list of temperature intervals.
        """
        for stream in self.stream_list:
            if stream.T_in_shifted not in self.temperature_list:
                self.temperature_list.append(stream.T_in_shifted)
            if stream.T_out_shifted not in self.temperature_list:
                self.temperature_list.append(stream.T_out_shifted)

        return sorted(self.temperature_list, reverse=True)

def formCpList(temperature_list, stream_list):
    """
    formulate a numpy array that stores the calculated Cp values corresponds to
    each temperature intervals.

    Args:
        temeperature_list: a list that stores the temperature intervals of the system.
        stream_list: a list that stores the Stream objects of the system.

    Return:
        Cp_list: a numpy array that stores Cp values in descending temperature order.
    """
    Cp_list = np.zeros(len(temperature_list)-1)
    for i in range(len(temperature_list)-1):
        for stream in stream_list:
            if stream.type == 'hot':
                if stream.T_in_shifted>=temperature_list[i] and \
                stream.T_out_shifted<=temperature_list[i+1]:
                    Cp_list[i]+=stream.Cp
            else:
                if stream.T_in_shifted<=temperature_list[i+1] and \
                stream.T_out_shifted>=temperature_list[i]:
                    Cp_list[i]-=stream.Cp

    return Cp_list

def calculateDeltaH(Cp_list, temperature_list):
    """
    A function that takes in a Cp list and a temperature list of a given system and calculate
    delta H values for the heating cascade.

    Args:
        Cp_list: A numpy array that stores the Cp for each temperature interval.
        temperature_list: A list that stores the temperature intervals of the system.

    Return:
        deltaH_list: A list that stores the enthalpy values for the heat cascade.
    """
    deltaH_list = list()
    for i in range(len(temperature_list)-1):
        delta_T = temperature_list[i] - temperature_list[i+1]
        deltaH_list.append(delta_T*Cp_list[i])

    return deltaH_list

def identifyPinch(deltaH_list):
    """
    A function that calculates and identifies where is the pinch of the system.

    Args:
        deltaH_list: a list that stores delta H values in order.

    Return:
        low: what is the lowest infeasible power reached during the cascade process.
    """
    _sum = 0
    low = 0
    index = 0
    for i in range(len(deltaH_list)):
        _sum += deltaH_list[i]
        if _sum<low:
            low = _sum
            index = i
    return (low, index)


def main():
    # Creating stream objects and system object
    one = Stream(60, 180, 3)
    two = Stream(180, 40, 2)
    three = Stream(30, 105, 2.6)
    four = Stream(150, 40, 4)
    streams = [one, two, three, four]
    for s in streams:
        s.shiftTemperature()
    sys = System(streams)

    # Main calculations
    temp_list = sys.formulateIntervals()
    print("Temperature intervals: " + str(temp_list))
    for i in range(len(temp_list)-1):
        delta_T = temp_list[i] - temp_list[i+1]

    Cp_list = formCpList(temp_list, streams)
    # print("Cp values: " + str(Cp_list))
    deltaH_list = calculateDeltaH(Cp_list, temp_list)
    print("Heat cascade values: " + str(deltaH_list))
    coldUtility = sum(deltaH_list)
    print("Heat dumps into the cold utility before adding pinch power: " + str(coldUtility) + "KW")
    low, index = identifyPinch(deltaH_list)
    print("The pinch occurs at interval #"+str(index+1)+", which is from ",\
    str(temp_list[index+1]) + "C to ",str(temp_list[index]) + "C")
    print("The pinch:", -low, "KW")
    print("Heat dumps after adding pinch power:", coldUtility-low, "KW")


if __name__ == '__main__':
    main()
