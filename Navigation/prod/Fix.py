'''
    Created on 10/12/16
    Last Modified on 12/2/16
    
    @author: Ankit Kumar Singh
    Fix Component,  CAO03 Assignment
'''

from genericpath import isfile
import datetime
import time
import xml.etree.ElementTree as ET
import math
from operator import itemgetter
import os
from __builtin__ import str
from _ast import Str

class Fix():
    def __init__(self, logFile = 'log.txt'):
        self.logFile = logFile
        self.sightingFile = None
        self.ariesFile = None
        self.starFile = None
        self.sightingError = 0
        self.sighting_tuples = []
        if not isinstance(logFile, str):
            raise ValueError('Fix.__init__:  "logFile" is a string')
        if (len(logFile) < 1):
            raise ValueError('Fix.__init__:  "logFile" should have a length .GE. 1')
        if not isfile(logFile):
            try:
                log = open(logFile, 'w')
            except:
                raise ValueError('Fix.__init__:  "logFile" can not be created')            
        else:
            try:
                log = open(logFile, 'a')    
            except:
                raise ValueError('Fix.__init__:  "logFile" can not be opened for appending')
        logEntry = self.message("Log file:\t" + os.path.abspath(self.logFile))
        try:
            log.write(logEntry)
        except:
            raise ValueError('Fix.__init__:  "logFile" can not be appended')
        log.close()
    
    def message(self, message):
        start = "LOG:\t"
        date = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        timezone = "-06:00\t"
        result = start + date + timezone + message + "\n"
        return result

    def setSightingFile(self, sightingFile = None):
        if sightingFile == None:
            raise ValueError('Fix.setSightingFile:  "sightingFile" can not be empty')
        if not isinstance(sightingFile, str):
            raise ValueError('Fix.setSightingFile:  the file name violates the parameter specification')
        try:
            extend = sightingFile.split(".", 1)[1]
            if not extend == "xml":
                raise ValueError('Fix.setSightingFile:  the file name violates the parameter specification')
        except:
            raise ValueError('Fix.setSightingFile:  the file name violates the parameter specification')
        if len(sightingFile) < 5:
            raise ValueError('Fix.setSightingFile:  the file name violates the parameter specification')
        try:
            sighting = open(sightingFile, 'r')
        except:
            raise ValueError('Fix.setSightingFile:  the file can not be opened')
        logEntry = self.message("Sighting file:\t" + os.path.abspath(sightingFile))
        try:
            log = open(self.logFile, 'a+') 
        except:
            raise ValueError('Fix.setSightingFile:  "logFile" can not be opened for appending')
        try:
            log.write(logEntry)
        except:
            raise ValueError('Fix.setSightingFile:  "logFile" can not be appended')     
        log.close()    
        sighting.close()        
        self.sightingFile = sightingFile
        
        return os.path.abspath(sightingFile)

    def setAriesFile(self, ariesFile = None):
        if ariesFile == None:
            raise ValueError('Fix.setAriesFile:  "AriesFile" can not be empty')
        if not isinstance(ariesFile, str):
            raise ValueError('Fix.setAriesFile:  the file name violates the parameter specification')
        try:
            extend = ariesFile.split(".", 1)[1]
            if not extend == "txt":
                raise ValueError('Fix.setAriesFile:  the file name violates the parameter specification')
        except:
            raise ValueError('Fix.setAriesFile:  the file name violates the parameter specification')
        if len(ariesFile) < 5:
            raise ValueError('Fix.setAriesFile:  the file name violates the parameter specification')
        try:
            aries = open(ariesFile, 'r')
        except:
            raise ValueError('Fix.setAriesFile:  the file can not be opened')
        logEntry = self.message("Aries file:\t" + os.path.abspath(ariesFile))
        try:
            log = open(self.logFile, 'a+') 
        except:
            raise ValueError('Fix.setAriesFile:  "logFile" can not be opened for appending')
        try:
            log.write(logEntry)
        except:
            raise ValueError('Fix.setAriesFile:  "logFile" can not be appended')     
        log.close()    
        aries.close()        
        self.ariesFile = ariesFile
        return os.path.abspath(ariesFile)
    
    def setStarFile(self, starFile = None):
        if starFile == None:
            raise ValueError('Fix.setStarFile:  "StarFile" can not be empty')
        if not isinstance(starFile, str):
            raise ValueError('Fix.setStarFile:  the file name violates the parameter specification')
        try:
            extend = starFile.split(".", 1)[1]
            if not extend == "txt":
                raise ValueError('Fix.setStarFile:  the file name violates the parameter specification')
        except:
            raise ValueError('Fix.setStarFile:  the file name violates the parameter specification')
        if len(starFile) < 5:
            raise ValueError('Fix.setStarFile:  the file name violates the parameter specification')
        try:
            star = open(starFile, 'r')
        except:
            raise ValueError('Fix.setStarFile:  the file can not be opened')
        logEntry = self.message("Star file:\t" + os.path.abspath(starFile))
        try:
            log = open(self.logFile, 'a+') 
        except:
            raise ValueError('Fix.setStarFile:  "logFile" can not be opened for appending')
        try:
            log.write(logEntry)
        except:
            raise ValueError('Fix.setStarFile:  "logFile" can not be appended')     
        log.close()    
        star.close()        
        self.starFile = starFile
        return os.path.abspath(starFile)

    def getSightings(self, assumedLatitude="0d0.0", assumedLongitude="0d0.0"):
        if self.sightingFile == None:
            raise ValueError('Fix.getSightings:  "SightingFile" should not be empty')
        if self.ariesFile == None:
            raise ValueError('Fix.getSightings:  "AriesFile" should not be empty')
        if self.starFile == None:
            raise ValueError('Fix.getSightings:  "StarFile" should not be empty')
        if not isinstance(assumedLatitude, str) or not isinstance(assumedLongitude, str):
            raise ValueError('Fix.getSightings:  parameters violate the specification')
        hemisphere = ""
        assumed_latitude = 0.0
        assumed_longitude = 0.0
        if assumedLatitude[0] == "N" or assumedLatitude[0] == "S":
            hemisphere = assumedLatitude[0]
            latitude_degree = assumedLatitude[1:]
            try:
                xdy = latitude_degree.split("d", 1)
                assumedLatitude_degree = int (xdy[0])
                if assumedLatitude_degree < 0 or assumedLatitude_degree >= 90:
                    raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
                assumedLatitude_minute = float (xdy[1])
                if assumedLatitude_minute < 0 or assumedLatitude_minute >= 60:
                    raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
                if assumedLatitude_degree == 0 and assumedLatitude_minute == 0:
                    raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
                d_index = xdy[1].find(".")
                if not d_index == len(xdy[1]) - 2:
                    raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
            except:
                raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
            assumed_latitude = assumedLatitude_degree + assumedLatitude_minute / 60.0
            if hemisphere == "S":
                assumed_latitude = 0 - assumed_latitude
        else:
            if not assumedLatitude == "0d0.0":
                raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
        try:
            xdy = assumedLongitude.split("d", 1)
            assumedLongitude_degree = int (xdy[0])
            if assumedLongitude_degree < 0 or assumedLongitude_degree >= 360:
                raise ValueError('Fix.getSightings:  assumedLatitude violate the specification')
            assumedLongitude_minute = float (xdy[1])
            if assumedLongitude_minute < 0 or assumedLongitude_minute >= 60:
                raise ValueError('Fix.getSightings:  assumedLongitude violate the specification')
            d_index = xdy[1].find(".")
            if not d_index == len(xdy[1]) - 2:
                raise ValueError('Fix.getSightings:  assumedLongitude violate the specification')
        except:
            raise ValueError('Fix.getSightings:  assumedLongitude violate the specification')
        assumed_longitude = assumedLongitude_degree + assumedLongitude_minute / 60.0
        approximateLatitude = 0.0
        approximateLongitude = 0.0
        try:
            log = open(self.logFile, 'a+') 
        except:
            raise ValueError('Fix.getSightings:  "logFile" can not be opened for appending')
        sighting_tuples = []
        tree = ET.parse(self.sightingFile)
        root = tree.getroot()
        if root.tag == "fix":
            for child in tree.findall("sighting"):
                #body content
                bodyTag = child.find("body")
                if bodyTag == None:
                    self.sightingError = self.sightingError + 1
                    continue
                else:
                    body = bodyTag.text
                    if body == None:
                        self.sightingError = self.sightingError + 1
                        continue
                #date content
                dateTag = child.find("date")   
                if dateTag == None:
                    self.sightingError = self.sightingError + 1
                    continue
                else:
                    date = dateTag.text
                    try:
                        time.strptime(date, "%Y-%m-%d")  
                    except:  
                        self.sightingError = self.sightingError + 1
                        continue 
                dateInAriesStar = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%y")
                #time content
                timeTag = child.find("time")
                if timeTag == None:
                    self.sightingError = self.sightingError + 1
                    continue
                else:
                    timee = timeTag.text
                    try:
                        time.strptime(timee, "%H:%M:%S")
                    except:
                        self.sightingError = self.sightingError + 1
                        continue
                shi, fen, miao = timee.split(":")
                shi = int (shi)
                fen = int (fen)
                miao = int (miao)
                #observation content   
                observationTag = child.find("observation")   
                if observationTag == None:
                    self.sightingError = self.sightingError + 1
                    continue
                else:
                    observation = observationTag.text
                    if observation.find("d") == -1:
                        self.sightingError = self.sightingError + 1
                        continue
                    xdy = observation.split("d")
                    if len(xdy) != 2:
                        self.sightingError = self.sightingError + 1
                        continue
                    else:
                        try:
                            xdy[0] = int (xdy[0])
                        except:
                            self.sightingError = self.sightingError + 1
                            continue
                        if xdy[0] < 0:
                            self.sightingError = self.sightingError + 1
                            continue
                        if xdy[0] >= 90:
                            self.sightingError = self.sightingError + 1
                            continue
                        try:
                            xdy[1] = float (xdy[1])
                        except:
                            self.sightingError = self.sightingError + 1
                            continue
                        if xdy[1] < 0.0:
                            self.sightingError = self.sightingError + 1
                            continue
                        if xdy[1] >= 60.0:
                            self.sightingError = self.sightingError + 1
                            continue
                        if xdy[1] * 10 % 1 != 0:
                            self.sightingError = self.sightingError + 1
                            continue
                        if xdy[0] == 0 and xdy[1] < 0.1:
                            self.sightingError = self.sightingError + 1
                            continue
                        observationAltitude = xdy[0] + xdy[1] / 60.0
                heightTag = child.find("height")
                if heightTag == None:
                    height = 0
                else:
                    height = heightTag.text
                    if height == "":
                        height = 0
                    try:
                        height = float (height)
                    except:
                        self.sightingError = self.sightingError + 1
                        continue
                    if height < 0:
                        self.sightingError = self.sightingError + 1
                        continue
                temperatureTag = child.find("temperature")
                if temperatureTag == None:
                    temperature = 72
                else:
                    temperature = temperatureTag.text
                    if temperature == "":
                        temperature = 72
                    try:
                        temperature = int (temperature)
                    except:
                        self.sightingError = self.sightingError + 1
                        continue
                    if temperature < -20:
                        self.sightingError = self.sightingError + 1
                        continue
                    if temperature > 120:
                        self.sightingError = self.sightingError + 1
                        continue
                pressureTag = child.find("pressure")
                if pressureTag == None:
                    pressure = 1010
                else:
                    pressure = pressureTag.text
                    if pressure == "":
                        pressure = 1010
                    try:
                        pressure = int (pressure)
                    except:
                        self.sightingError = self.sightingError + 1
                        continue
                    if pressure < 100:
                        self.sightingError = self.sightingError + 1
                        continue
                    if pressure > 1100:
                        self.sightingError = self.sightingError + 1
                        continue
                horizonTag = child.find("horizon")
                if horizonTag == None:
                    horizon = "natural"
                else:
                    horizon = horizonTag.text
                    if horizon == "":
                        horizon = "natural"
                    horizon = horizon.lower()
                    if horizon != "artificial" and horizon != "natural":
                        self.sightingError = self.sightingError + 1
                        continue                   
                if horizon == "natural":
                    dip = (-0.97 * math.sqrt(height)) / 60
                else:
                    dip = 0
                Ctemperature = (temperature - 32) / 1.8   
                refraction = (-0.00452 * pressure) / (273 + Ctemperature) / math.tan(observationAltitude * math.pi / 180.0)
                adjustedAltitude = observationAltitude + dip + refraction
                degree = int (adjustedAltitude)
                minute = round((adjustedAltitude - degree) * 60, 1)
                altitude = str (degree) + "d" + str (minute)
                SHA_latitude = self.searchStar(self.starFile, body, dateInAriesStar)
                if SHA_latitude == []:
                    self.sightingError = self.sightingError + 1
                    continue
                else:
                    SHA_star = SHA_latitude[0]
                    self.latitude = SHA_latitude[1].strip()                                    
                SHA_star = self.setDegreesAndMinutesInFix(SHA_star)
                if SHA_star == []:
                    self.sightingError = self.sightingError + 1
                    continue
                if SHA_star[0] < 0 or SHA_star[0] >= 360:
                    self.sightingError = self.sightingError + 1
                    continue
                SHA_Star = SHA_star[0] + SHA_star[1] / 60
                self.latitude = self.setDegreesAndMinutesInFix(self.latitude)
                if self.latitude == []:
                    self.sightingError = self.sightingError + 1
                    continue
                if self.latitude[0] <= -90 or self.latitude[0] >= 90:
                    self.sightingError = self.sightingError + 1
                    continue
                latitude = str (self.latitude[0]) + "d" + str (self.latitude[1])
                if self.latitude[0] < 0 :
                    geographic_latitude = self.latitude[0] - self.latitude[1] / 60.0
                else:
                    geographic_latitude = self.latitude[0] + self.latitude[1] / 60.0
                GHA = self.searchAriesFile(self.ariesFile, dateInAriesStar, shi)
                if not len(GHA) == 2:
                    self.sightingError = self.sightingError + 1
                    continue
                try:
                    GHA_Aries1 = GHA[0].split("\t")[-1].strip()
                    GHA_Aries2 = GHA[1].split("\t")[-1].strip()
                except:
                    self.sightingError = self.sightingError + 1
                    continue
                try:
                    GHA_Hour2 = GHA[1].split("\t")[1]
                    GHA_Date2 = GHA[1].split("\t")[0]
                except:
                    self.sightingError = self.sightingError + 1
                    continue
                try:
                    GHA_date2 = datetime.datetime.strptime(GHA_Date2, "%m/%d/%y")
                    GHA_hour2 = int (GHA_Hour2)
                    if GHA_hour2 < 0 or GHA_hour2 > 23:
                        self.sightingError = self.sightingError + 1
                        continue
                except:
                    self.sightingError = self.sightingError + 1
                    continue
                AriesDay = datetime.datetime.strptime(dateInAriesStar, "%m/%d/%y")
                oneday = datetime.timedelta(days = 1)
                nextday = (AriesDay + oneday).strftime("%m/%d/%y")
                if shi != 23 and GHA_Date2 != dateInAriesStar and GHA_Hour2 != str(shi + 1):
                    self.sightingError = self.sightingError + 1
                    continue
                if shi == 23 and GHA_Date2 != nextday and GHA_Hour2 != "0":
                    self.sightingError = self.sightingError + 1
                    continue
                try:
                    GHA_Aries1_degree, GHA_Aries1_minute = self.setDegreesAndMinutesInFix(GHA_Aries1)
                    GHA_Aries2_degree, GHA_Aries2_minute = self.setDegreesAndMinutesInFix(GHA_Aries2)
                except:
                    self.sightingError = self.sightingError + 1
                    continue
                if GHA_Aries1_degree < 0 or GHA_Aries1_degree >= 360 or GHA_Aries2_degree < 0 or GHA_Aries2_degree >= 360:
                    self.sightingError = self.sightingError + 1
                    continue
                GHA_Aries1 = GHA_Aries1_degree + GHA_Aries1_minute / 60
                GHA_Aries2 = GHA_Aries2_degree + GHA_Aries2_minute / 60
                s = fen * 60 + miao
                GHA_Aries = GHA_Aries1 + abs(GHA_Aries2 - GHA_Aries1) * (s / 3600.0)
                #geographic position longitude
                self.longitude = (GHA_Aries + SHA_Star) % 360                 
                longitude_degree = int (self.longitude) 
                longitude_minute = round((self.longitude - longitude_degree) * 60, 1)
                longitude = str (longitude_degree) + "d" + str (longitude_minute)
                self.longitude = longitude_degree + longitude_minute / 60.0               
                LHA = (self.longitude + assumed_longitude) % 360
                sinlat1 = math.sin(geographic_latitude*math.pi/180)
                sinlat2 = math.sin(assumed_latitude*math.pi/180)
                sinlat = sinlat1 * sinlat2
                coslat1 = math.cos(geographic_latitude*math.pi/180)
                coslat2 = math.cos(assumed_latitude*math.pi/180)
                cosLHA = math.cos(LHA*math.pi/180)
                coslat = coslat1 * coslat2 * cosLHA
                intermediate_distance = sinlat + coslat
                corrected_altitude = math.asin(intermediate_distance) * 180 / math.pi
                distance_adjustment = int(round((corrected_altitude - adjustedAltitude) * 60))
                
                azimuth_numerator = math.sin(geographic_latitude*math.pi/180) - math.sin(assumed_latitude*math.pi/180)*intermediate_distance
                azimuth_denominator = math.cos(assumed_latitude*math.pi/180)*math.cos(corrected_altitude*math.pi/180)
                intermediate_azimuth = azimuth_numerator / azimuth_denominator
                azimuth_adjustment = math.acos(intermediate_azimuth) * 180 / math.pi                
                azimuth_adjustment_degree = int (azimuth_adjustment)
                azimuth_adjustment_minute = round((azimuth_adjustment - azimuth_adjustment_degree) * 60, 1)
                azimuth_adjustment_string = str (azimuth_adjustment_degree) + "d" + str (azimuth_adjustment_minute)
                approximateLatitude = approximateLatitude + distance_adjustment * math.cos(azimuth_adjustment*math.pi/180)
                approximateLongitude = approximateLongitude + distance_adjustment * math.sin(azimuth_adjustment*math.pi/180)
                sighting = (body, date, timee, altitude, latitude, longitude, assumedLatitude, assumedLongitude, azimuth_adjustment_string, distance_adjustment)
                sighting_tuples.append(sighting)
            sighting_tuples = sorted(sighting_tuples, key = itemgetter(1, 2, 0))
            self.sighting_tuples = sighting_tuples
            for ss in sighting_tuples:
                message = self.readtuple(ss)
                logEntry = self.message(message)
                try:
                    log.write(logEntry)
                except:
                    raise ValueError('Fix.getSightings:  "logFile" can not be appended')                               
        SightingErrorEntry = self.message("Sighting errors:\t" + str(self.sightingError))
        approximateLatitude = approximateLatitude / 60 + assumed_latitude
        approximateLatitude_degree = int (approximateLatitude)
        if approximateLatitude_degree < 0:
            hemisphere = "S"
        approximateLatitude_minute = abs(round((approximateLatitude - approximateLatitude_degree) * 60, 1))
        approximateLatitude_degree = abs(approximateLatitude_degree)
        approximate_latitude = hemisphere + str(approximateLatitude_degree) + "d" + str(approximateLatitude_minute)
        approximateLongitude = approximateLongitude / 60 + assumed_longitude
        approximateLongitude_degree = int (approximateLongitude)
        approximateLongitude_minute = round((approximateLongitude - approximateLongitude_degree) * 60, 1)
        approximate_longitude = str(approximateLongitude_degree) + "d" + str(approximateLongitude_minute)
        ApproximateEntry = self.message("Approximate latitude:\t" + approximate_latitude + "\t" + "Approximate longitude:\t" + approximate_longitude)
        try:
            log.write(SightingErrorEntry)
            log.write(ApproximateEntry)
        except:
            raise ValueError('Fix.getSightings:  "logFile" can not be appended')
        log.close()
        return (approximate_latitude,approximate_longitude)
    
    def setDegreesAndMinutesInFix(self, string):
        if string == None:
            return []
        if string.find("d") == -1:
            return []
        wdz = string.split("d")
        if len(wdz) != 2:
            return []
        else:
            try:
                wdz[0] = int (wdz[0])
            except:
                return []
            try:
                wdz[1] = float (wdz[1])
            except:
                return []
            if wdz[1] < 0.0:
                return []
            if wdz[1] >= 60.0:
                return []
            if wdz[1] * 10 % 1 != 0:
                return []
        return [wdz[0], wdz[1]]
        
    def searchStar(self, starFile, body, date):
        star = open(starFile)
        lines = []
        for line in star.readlines():
            item = line.split("\t")
            if item[0] == body and item[1] <= date:
                lines.append(line)
        star.close()
        if not lines == []:
            lines = sorted(lines, key = itemgetter(1))
            SHA_star = lines[-1].split("\t")[-2]
            latitude = lines[-1].split("\t")[-1]
            return [SHA_star, latitude]
        else:
            return[]      
                  
    def searchAriesFile(self, ariesFile, date, hour):
        aries = open(ariesFile)
        ariesFile = sorted(aries, key = itemgetter(0, 1))
        GHA = []
        id = -1
        for index, line in enumerate(ariesFile):
            item = line.split("\t")
            if item[0] == date and int (item[1]) == hour:
                GHA.append(line)
                id = index
        aries.close()
        if not len(GHA) == 1:
            return []
        try:
            GHA_Aries2 = ariesFile[id + 1]
        except:
            return[]
        return [GHA[0], GHA_Aries2]
    
    def readtuple(self, tuples):
        message = ""
        for item in tuples:
            message = message + str(item) + "\t"
        return message.rstrip()  