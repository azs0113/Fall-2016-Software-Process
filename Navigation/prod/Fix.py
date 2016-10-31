'''
    Created on 10/12/16
    Modified on 10/30/16
    
    @author: Ankit Kumar Singh
    Fix Component,  CAO03 Assignment
'''


from string import strip
from xml.dom import minidom as dom
import datetime
from time import strftime, gmtime
import sys
import math
import os
from xml.dom.minidom import parse
import xml.dom.minidom
from math import sqrt, tan, pi
import Navigation.prod.Angle as Angle
from sqlite3 import collections
from operator import itemgetter
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
            logfile.write('Log File:\t' + os.path.abspath(logFile))
            logfile.close()
            self.sightingFile = None
            self.logFile = logFile
            self.ariesFile = None
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
            xmlfile.write('\nLOG:\t' + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
            xmlfile.write(' Sighting file:\t'+os.path.abspath(sightingFile))
            self.sightingFile = sightingFile
            xmlfile.close()
            
        except:
            raise ValueError('Fix.setSightingFile:  The file cannot be created or appended')
        return os.path.abspath(sightingFile)
    
    
    def setAriesFile(self,ariesFile):
        try:
            if not(ariesFile.find('.txt')>0):
                raise ValueError('Fix.setAriesFile:  Aries File should be a text file with .txt format')
            temp = open(ariesFile,'r')
            f = open(self.logFile,'a')
            f.flush()
            f.write("\nLOG: " + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
            f.write(' Aries file:\t'+os.path.abspath(ariesFile))
            f.close()
            temp.close()
            self.ariesFile = ariesFile
            return os.path.abspath(ariesFile)
          
        except:
            raise ValueError('Fix.setAriesFile:  File Exception Error in setting aries file')    
    
    
    def setStarFile(self,starFile):
        try:
            if not(starFile.find('.txt')>0):
                raise ValueError('Fix.setStarFile: Aries File should be a text file with .txt format')
            temp = open(starFile,'r')
            f = open(self.logFile,'a')
            f.flush()
            f.write("\nLOG: " + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
            f.write(' Star file:\t'+os.path.abspath(starFile))
            f.close()
            temp.close()
            self.StarFile = starFile
            return os.path.abspath(starFile)
        except:
            raise ValueError('Fix.setStarFile: File Exception Error in setting aries file')
       
    
    def getSightings(self):
        
        try:
            errors = 0
            if(self.starFile == None) or (self.ariesFile==None) or (self.sightingFile == None):
                errors += 1
            angle = Angle.Angle()
            approximateLatitude = '0'
            approximateLongitude = '0'
            f = open(self.logFile,'a')
            xmlFile = dom.parse(self.sightingFile)
            sightings = xmlFile.getElementsByTagName('sighting')
            tuples = []
              
            for sighting in sightings:
                
                height = 0
                temperature = 72
                pressure = 1010
                horizon = 'Natural'
                
                if not(sighting.getElementsByTagName('body').count>0):
                    raise ValueError('Fix.getSightings: No body found')
                else:
                    name = sighting.getElementsByTagName('body')[0].childNodes[0].nodeValue
                    
                if not(sighting.getElementsByTagName('date').count>0):
                    raise ValueError('Fix.getSightings: No date found')
                else:
                    date = sighting.getElementsByTagName('date')[0].childNodes[0].nodeValue
                    
                if not(sighting.getElementsByTagName('time').count>0):
                    raise ValueError('Fix.getSightings: No body found')
                else:
                    time = sighting.getElementsByTagName('time')[0].childNodes[0].nodeValue
                    
                if not(sighting.getElementsByTagName('observation').count>0):
                    raise ValueError('Fix.getSightings: No body found')
                else:
                    observation = sighting.getElementsByTagName('observation')[0].childNodes[0].nodeValue    
                observedAltitude = angle.setDegreesAndMinutes(observation)
                
                height = sighting.getElementsByTagName('height')[0].childNodes[0].nodeValue
                if not(float(height)>=0.0):
                    raise ValueError('Fix.getSightings: Height should be greater than 0') 
                
                temperature = sighting.getElementsByTagName('temperature')[0].childNodes[0].nodeValue
                if not(int(temperature)>=(-20) and int(temperature)<=120):
                    raise ValueError('Fix.getSighting: temperature should be in the range -20 to 120')
                 
                pressure = sighting.getElementsByTagName('pressure')[0].childNodes[0].nodeValue
                f.write(str(int(pressure)+500))
                if not(int(pressure)>=100 and int(pressure)<=1100):
                    raise ValueError('Fix.getSightings: Pressure should be in the range 100-1100')
                
                horizon = sighting.getElementsByTagName('horizon')[0].childNodes[0].nodeValue                
                if(horizon == 'Natural'):
                    dip = float((-0.97 * sqrt(float(height)))/60.0)
                elif(horizon == 'Artificial'):
                    dip = 0.0
                else:
                    raise ValueError('Fix.getSightings: Incorrect horizon Value')
                
                refraction = (-0.00452*int(pressure))/(273+self.Celsius(int(temperature))) / tan(observedAltitude * pi/180) 
                adjustedAltitude = round(observedAltitude + dip + refraction, 3) 
                angle.angle = adjustedAltitude
                sightingSingle = [name,date, time, angle.getString()]
                tuples.append(sightingSingle)
                
            tuples = sorted(tuples, key=itemgetter(1,2,3))
            for eachSighting in tuples:
                (geoLatitude,geoLongitude) = self.getGeographicPosition(str(eachSighting[0]),str(eachSighting[1]),str(eachSighting[2]))
                f.write("\nLOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
                f.write(":\t"+ eachSighting[0] + ":\t" + eachSighting[1] + "\t" + eachSighting[2] + "\t" + eachSighting[3]+"\t"+ str(geoLatitude.getString()) + "\t"+str(geoLongitude.getString()))
            f.write("\nLOG:\t" + strftime("%Y-%m-%d %H:%M:%S-06:00",gmtime()))
            f.write(':\nEnd of sighting file '+self.sightingFile)
            f.close()
        except:
                raise ValueError('Fix.getSightings: Raised Value Error')
        return (approximateLatitude,approximateLongitude)
    
    def getGeographicPosition(self, body=None, observationDate = None, observationTime = None):
        
        if(observationTime == None):
            raise ValueError('Fix.getGeographicPosition: hour missing')
        if(body==None):
            raise ValueError('Fix.getGeographicPosition: body missing')
        if(observationDate==None):
            raise ValueError('File.getPositions: date missing')
        
        f1 = open('starFile.txt','a') 
        starFile = self.starFile
        ariesFile = self.ariesFile
        tempArr = str(observationTime).split(':')
        observationHour = int(tempArr[0])
        s = (int(tempArr[1])*60) +int(tempArr[2])
        geographicPositionLatitude = Angle.Angle()
        geographicPositionLongitude = Angle.Angle()
        ghaAries1 = ''
        ghaAries2 = ''
        tempArray = observationDate.split('-')
        previousStarObservation = None
        shaStar = None
        observationYear = int(tempArray[0])%2000
        observationMonth = int(tempArray[1])
        observationDay = int(tempArray[2])
        f1 = open('starFile.txt','a') #test
        f = open(starFile,'r')
        starObservations = f.readlines()
            
        for Observation in starObservations:
            temp = Observation.split('\t')
                
            bodyInStarFile = temp[0]
                
            if(body==bodyInStarFile):
                    
                date = temp[1].split('/')
                    
                    
                    
                    #f1.write("\n"+date)
                if(observationYear <= int(date[2]) and observationMonth <= int(date[0]) and observationDay <= int(date[1]) ):
                        
                    previousStarObservation = temp
                        
                        
            
        geographicPositionLatitude.setDegreesAndMinutes(previousStarObservation[3])
            
        shaStar = previousStarObservation[2]
        shaStarAngle = Angle.Angle()
        shaStarAngle.setDegreesAndMinutes(shaStar)
            
            
        f2 = open(ariesFile,'r')
        ariesObservations = f2.readlines()    
        for Observation in ariesObservations:
            temp = Observation.split('\t')
            tempDate = str(observationMonth).zfill(2)+'/'+str(observationDay).zfill(2)+'/'+str(observationYear)
            if(tempDate == temp[0]):
                if(observationHour==23):
                    if(int(temp[1])==0):
                        ghaAries2 = temp[2]
                        f1.write("\n gha2:"+ghaAries2)        
                if( observationHour == int(temp[1])):
                    ghaAries1 = temp[2]
                    f1.write("\n gha1:"+ghaAries1)
                if(observationHour + 1 == int(temp[1])):
                    ghaAries2 = temp[2]
                    f1.write("\n gha2:"+ghaAries2)
            
            
        ghaAriesAngle1 = Angle.Angle()
        f1.write('\n gha:'+str(ghaAries1))
        ghaAriesAngle1.setDegreesAndMinutes(ghaAries1)
        temp1 = float(ghaAriesAngle1.angle)
        ghaAriesAngle2 = Angle.Angle()
        ghaAriesAngle2.setDegreesAndMinutes(ghaAries2)
        temp2 = float(ghaAriesAngle2.angle)
        ghaAriesAngle = Angle.Angle()
            
            #ghaAriesAngle.angle = ghaAriesAngle2.subtract(ghaAriesAngle1)
        tempAngle = abs(temp2-temp1)
        tempAngle = float(tempAngle)*s/3600 
        ghaAriesAngle.setDegrees(tempAngle) 
        ghaAriesAngle.add(ghaAriesAngle1)
              
        geographicPositionLongitude.setDegrees(round(float(ghaAriesAngle.add(shaStarAngle)) % 360,1))                    
        return (geographicPositionLatitude,geographicPositionLongitude)     