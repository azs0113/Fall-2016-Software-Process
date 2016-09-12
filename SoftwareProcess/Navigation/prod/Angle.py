'''
    Created on 9/10/2016 
       
    Modified on 9/11/2016
    
    @author: Ankit Kumar Singh
    
    Angle is a class that represents an amount of rotation from a fixed point. When used for navigation, angles are expressed in degrees and minutes, where 1 degree= 60 minutes.
    This program contains methods:
    setDegrees(degrees): sets the value of the instance to a specified nuber of degrees
    
    setDegreesAndMinutes(angleString): sets the value of the instance based on a string that contains degrees and minutes
    
    add(angle): Adds the value of the parameterized value from the instance
    
    subtract(angle): Subtracts the value of the parameterized value from the current instance
    
    compare(angle): compares parameterized value to the current instance
    
    getString(): Returns a string value of the angle
    
    getDegrees(): Returns the angle as degrees(nd portions of degrees) 
       
'''

from operator import mod
class Angle():
    def __init__(self):
        # self.angle = ...       set to 0 degrees 0 minutes
        self.Angle = 0.0
        pass
    
    def setDegrees(self, degrees=0.0):
        try:
            if degrees > 0.0:
                self.Angle = mod(degrees, 360.0)
            elif degrees < 0.0 :
                self.Angle = 360.0 - abs(degrees) 
            else:
                self.Angle = degrees
            return self.Angle
        except:
            raise ValueError("Angle.setDegrees:  Parameter specification violated with non-numeric value ")        
        pass
    
    def setDegreesAndMinutes(self, angleString):
        try:
            x = angleString.split('d')
            degreePart = self.setDegrees(int(x[0]))
            minutesPart = float(x[1]) / 60.0
        
            self.Angle = degreePart + minutesPart 
         
            return round(self.Angle, 2)
        except:
            raise ValueError("Angle.setDegreesAndMinutes:  Parameter specification violated with illegal values")
        pass
    
    def add(self, angle):
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.add:  Invalid instance of angle is specified")
        else:
            self.Angle += angle.Angle
            return self.Angle
        pass
    
    def subtract(self, angle):
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.subtract:  Invalid instance of angle is specified")
        else:
            self.Angle -= angle.Angle
            return self.Angle
        pass
    
    def compare(self, angle):
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.compare:  Invalid instance of angle is specified")
        else:
            if self.Angle < angle.Angle:
                return -1
            elif self.Angle > angle.Angle:
                return +1
            else:
                return 0  
        pass
    
    def getString(self):
        
        str1 = str(int(self.Angle // 1))
        
        str2 = str(round(((self.Angle % 1) * 60.0), 2))
        
        return str1 + 'd' + str2
        pass
    
    def getDegrees(self):
        
        return round(self.Angle, 2)
        pass
