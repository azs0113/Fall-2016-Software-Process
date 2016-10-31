'''
    Created on 10/12/16
    Modified on 10/16/16
    
    @author: Ankit Kumar Singh
    Fix Component,  CAO02 Assignment
'''


from string import strip
import datetime
from time import strftime, gmtime
import sys
import math
from xml.dom.minidom import parse
import xml.dom.minidom
from math import sqrt
import Navigation.prod.Angle as Angle
from sqlite3 import collections
from cgi import logfile
class Fix():
    def __init__(self,logFile = 'log.txt'):
        try:
            if not(isinstance(logFile, basestring)):
                raise ValueError('Fix.Fix:  Parameter specification violated with non-numeric value')
            if logFile == '':
                raise ValueError('Fix.Fix:  Parameter specification violated with empty string')
            logfile= open(logFile, 'a')
            logfile.write("LOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime())+ ":\t")
            logfile.write('Start of log\n')
            logfile.close()
            self.sightingFile = None
            self.logFile = logFile
        except:
            raise ValueError('Fix.Fix:  The file cannot be created or appended')
        
    def setSightingFile(self, sightingFile= None):
        
        try:
            if not(isinstance(sightingFile, basestring)):
                raise ValueError('Fix.setSightingFile:  Parameter specification violated with non-numeric value')
            if sightingFile == '':
                raise ValueError('Fix.setSightingFile:  Parameter specification violated with empty string')
            if not sightingFile.endswith('.xml'):
                raise ValueError('Fix.setSightingFile:  Parameter specification violated with no file extension provided or incorrect extension provided')
            if sightingFile.startswith('.xml'):
                raise ValueError('Fix.setSightingFile:  Parameter specification violated with incorrect size of filename') 
            xmlfile = open(self.logFile,'a')
            xmlfile.flush()
            xmlfile.write('LOG:\t' + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()) + ':\tStart of sighting file '+ sightingFile+'\n')
            self.sightingFile = sightingFile
            xmlfile.close()
            
        except:
            raise ValueError('Fix.setSightingFile:  The file cannot be created or appended')
        return sightingFile
    
    
    def getSightings(self):
#         try:
            
            approximateLatitude = '0d0.0'
            approximateLongitude = '0d0.0'
            height = 0
            temperature = 72
            pressure = 1010
            horizon = "Natural"
            rFile= xml.dom.minidom.parse(self.sightingFile) 
            elements = rFile.documentElement
            sightings = elements.getElementsByTagName('sighting')
                
            for sight in sightings:
                if sight.getElementsByTagName("body"):
                    body = sight.getElementsByTagName("body")[0]
                    if (body.childNodes[0].data)==False:
                        raise ValueError("Fix.getSightings:  The xml file has no content in the body tag") 
                    body = body.childNodes[0].data
                else:
                    raise ValueError("Fix.getSightings:  The xml file has missing body tag") 
                if sight.getElementsByTagName("time"):
                    time = sight.getElementsByTagName("time")[0]
                    time = time.childNodes[0].data
                else:
                    raise ValueError("Fix.getSightings:  The xml file has missing time tag")    
                if sight.getElementsByTagName("date"):
                    date = sight.getElementsByTagName("date")[0]
                    date = date.childNodes[0].data
                else:
                    raise ValueError("Fix.getSightings:  The xml file has missing date tag") 
                if sight.getElementsByTagName("observation"):  
                    observation = sight.getElementsByTagName("observation")[0]
                    observation = observation.childNodes[0].data
                    x = observation.split('d')
                    degreePart = int(x[0])
                    minutesPart = float(x[1])
                    if degreePart<0:
                        raise ValueError("Fix.getSightings:  The degree part of the observation value specified in the xml file is less than 0") 
                    if degreePart>90:
                        raise ValueError("Fix.getSightings:  The degree part of the observation value specified in the xml file is more than 90") 
                    if 0.0 < minutesPart > 60.0:
                        raise ValueError("Fix.getSightings:  The minutes part of the observation value specified in the xml file is not ideal")
                    if degreePart ==0 and minutesPart<0.1:
                        raise ValueError("Fix.getSightings:  The minutes part of the observation value specified in the xml file is not ideal")                                        
                else:
                    raise ValueError("Fix.getSightings:  The xml file has missing observation tag")     
    
                height = sight.getElementsByTagName("height")[0]
                height = height.childNodes[0].data
                if float(height)< 0:
                    raise ValueError("Fix.getSightings:  The height value specified in the xml file cannot be less than zero")
                
                temperature = sight.getElementsByTagName("temperature")[0]
                temperature = temperature.childNodes[0].data
                if int(temperature) > 120:
                    raise ValueError("Fix.getSightings:  The temperature value specified in the xml file is not ideal")
                if int(temperature)< -20:
                    raise ValueError("Fix.getSightings:  The temperature value specified in the xml file is not ideal") 
                pressure = sight.getElementsByTagName("pressure")[0]
                pressure = pressure.childNodes[0].data
                if(int(pressure)> 1100 or int(pressure) < 100 ):
                    raise ValueError("Fix.getSightings:  The pressure value specified in the xml file is not ideal")
                    
                horizon = sight.getElementsByTagName("horizon")[0]
                horizon = horizon.childNodes[0].data
                if horizon not in ('Natural','Artificial'):
                    raise ValueError("Fix.getSightings:  The horizon value specified in the xml file is incorrect")
                 
                if (horizon =='Natural'):
                    dip = float((-0.97*math.sqrt(float(height)))/60.0)
                else:
                    dip = 0.0    
                celsiusTemp = ((int(temperature)) - 32) * 5.0/9.0
                anAngle = Angle.Angle()
                tempObservation = anAngle.setDegreesAndMinutes(observation)
                newAltitude = math.tan(tempObservation)  
                refraction = ((-0.00452* int(pressure))/(273+ celsiusTemp))/newAltitude
                adjustedAltitude = tempObservation + dip + refraction
                anAngle.setDegrees(adjustedAltitude)
                loggingFile = open('log.txt','a')
                loggingFile.flush()
                loggingFile.write('LOG:\t' + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()) + ":\t" + body + "\t" + date +"\t" + time +"\t"+ anAngle.getString()+ '\n' )     
            loggingFile.write('LOG:\t' + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()) + ':\tEnd of sighting file '+ self.sightingFile+'\n')        
            loggingFile.close()
            return (approximateLatitude,approximateLongitude)
        
#         except:
#             raise TypeError('Fix.getSightings:  The sighting file has not been setup')
    