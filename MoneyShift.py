class Gear:
    coefficient = None
    def __init__(self,number):
        self.number = number
        self.next = None
        self.previous = None
    def __repr__(self):
        return self.number

    def calc_coefficient(self,rpm,speed):
        self.coefficient = float(rpm) / speed

    def get_rpm(self,speed):
        return speed * self.coefficient

    # def get_gear(self,mph,rpm):

class GearSet:
    def __init__(self,gears=None,initgears=None):
        self.head = None
        if gears is not None:
            gear = Gear(number=gears.pop(0))
            gear.previous = None
            self.head = gear
            for elem in gears:
                gear.next = Gear(number=elem)
                gear.next.previous = gear
                gear = gear.next
        if initgears is not None:
            gear = initgears.pop(0)
            gear.previous = None
            self.head = gear
            for elem in initgears:
                elem.previous = gear
                gear.next = elem
                gear = gear.next
    def __repr__(self):
        gear = self.head
        gears = []
        while gear is not None:
            gears.append(gear.number)
            gear = gear.next
        gears.append("None")
        return " -> ".join(str(v) for v in gears)
    def __iter__(self):
        gear = self.head
        while gear is not None:
            yield gear
            gear = gear.next

class MoneyShift:
    gearset = None

    def __init__(self,numGears=0,cfs=None):
        if cfs is not None:
            tempgears = []
            for number,coeff in enumerate(cfs,start=1):
                gear = Gear(number)
                gear.coefficient = coeff
                tempgears.append(gear)
            self.gearset = GearSet(initgears=tempgears)
            self.calibrate()
        else:
            gearnums = []
            for i in range(int(numGears)):
                gearnums.append(i+1)
            self.gearset = GearSet(gearnums)
            self.calibrate()

    def calibrate(self):
        for gear in self.gearset:
            if gear.coefficient is None:
                print(f'Calibrating Gear {gear.number}')
                #fetch current rpm, temp use console in
                print("Current RPM:")
                rpm = float(input())
                #fetch current speed
                print("Current Speed:")
                speed = float(input())
                gear.calc_coefficient(rpm=rpm,speed=speed)
                print(f'Calibrated Gear {gear.number} coefficient to be {gear.coefficient}')
                #print("Calibrated Gear " + gear.number + " coefficient to be " + gear.coefficient)
            else:
                print(f'Gear {gear.number} coefficient is set to {gear.coefficient}')
                #print("Gear " + gear.number + " coefficient is set to " + gear.coefficient)

    def give_local_shiftpoints(self, obd_info):
        #fetch speed
        print("Current Speed:")
        speed = obd_info.getMph()
        #fetch gear
        print("Current Gear:")
        currentgear = obd_info.getGear()
        for gear in self.gearset:
            if gear.number == currentgear:
                print(f'Current Gear: {str(gear.number)}, Prev Gear: {str(gear.previous.number)}, 'f'Next Gear: {str(gear.next.number)}')
                upshift = gear.next.get_rpm(speed)
                downshift = gear.previous.get_rpm(speed=speed)
                print(f'Shift to Gear {gear.next.number} at {upshift} RPM')
                print(f'Shift to Gear {gear.previous.number} at {downshift} RPM')

    def give_all_shiftpoints(self):
        #fetch speed
        print("Current Speed:")
        speed = float(input())
        for gear in self.gearset:
            print(f'Shift to Gear {gear.number} at {gear.get_rpm(speed)} RPM')
    def give_all_shiftpoints_range(self,minrpm,maxrpm):
        #fetch speed
        print("Current Speed:")
        speed = float(input())
        for gear in self.gearset:
            shiftpoint = gear.get_rpm(speed)
            if shiftpoint > minrpm and shiftpoint < maxrpm:
                print(f'Shift to Gear {gear.number} at {shiftpoint} RPM')
            else:
                print(f'Gear {gear.number} inaccessible at this speed')

# Known Ratios (perhaps from saved configurations)

print("Testing Constructor With Known Gear Coefficients")
print("")
ms = MoneyShift(cfs=[3.77,2.09,1.32,.98,.98,.81])
print(ms.gearset)

ms.give_local_shiftpoints()
ms.give_all_shiftpoints()
ms.give_all_shiftpoints_range(500,7500)

#print("")
#print("")

# Establish ratios via calibration

#print("Testing Constructor + Calibration Given Number of Gears")
#print("")
#ms2 = MoneyShift(6)
#ms2.give_local_shiftpoints()
#ms2.give_all_shiftpoints()
#ms2.give_all_shiftpoints_range(500,7500)
