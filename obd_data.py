import obd
import threading
import os
import numpy as np

class Data:
    def __init__(self):
        self.connection = None
        self.rpm = 0
        self.mph = 0
        self.gear = 0
        self.downshift = 0
        self.cel = False

    def connect(self):
        self.connection = obd.OBD("/dev/ttyUSB0",baudrate=38400, fast=True)

    def getRpm(self):
        return self.rpm

    def getMph(self):
        return self.mph

    def getGear(self):
        if self.gear > 0:
            return str(self.gear)
        if self.gear == 0:
            return "N"

    def getCel(self):
        return self.cel

    def data_in(self):
        while True:

            cmd = obd.commands.RPM
            r = self.connection.query(cmd)
            self.rpm = r.value.magnitude
            cmd = obd.commands.SPEED
            r = self.connection.query(cmd)
            self.mph = r.value.to('mph').magnitude
            self.calculate_gear()
            self.calculate_shiftpoint()
            self.cel_check()

    def calculate_gear(self):
        rpm = self.rpm
        r = 10.5
        speed = self.mph

        dict = {1: [3.77, 3.24],
                2: [2.09, 3.24],
                3: [1.47, 3.24],
                4: [1.09, 3.24],
                5: [1.10, 2.62],
                6: [0.91, 2.62]}

        newdict = {}
        if speed == 0:
            self.gear = 0

        else:
            for i in dict:
                newdict[i] = round((0.00595) * (rpm * r) / (dict[i][0] * dict[i][1]), 2)
                # if round(checkspeed) == round(speed):
                #     self.gear = i
                #
                # elif speed == 0:
                #     self.gear = 0


            for j in newdict:
                print(newdict[j])
                if speed > newdict[j]:
                    self.gear = j

    def getDownshift(self):
        return self.downshift

    def calculate_shiftpoint(self):
        gear = int(self.gear)
        dict = {1: [3.77, 3.24],
                2: [2.09, 3.24],
                3: [1.47, 3.24],
                4: [1.09, 3.24],
                5: [1.10, 2.62],
                6: [0.91, 2.62]}

        if gear-1>1:
            moneyshift = self.rpm * (dict[int(self.gear-1)][0] * dict[int(self.gear-1)][1])
            self.downshift = moneyshift

    def cel_check(self):
        cmd = obd.commands.STATUS
        r = self.connection.query(cmd)
        self.cel = r.value.MIL


    def main(self):

        x = threading.Thread(target=self.data_in)
        x.start()