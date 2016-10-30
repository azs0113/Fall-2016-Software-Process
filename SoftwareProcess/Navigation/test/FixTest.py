'''
    Created on 10/12/16
    Modified on 10/16/16
    
    @author: Ankit Kumar Singh
    Test Cases for Fix component. These are part of CAO02 Assignment
'''
import unittest
import datetime
import os as os
import Navigation.prod.Fix as Fix

class FixTest(unittest.TestCase):
    
    def setUp(self):
        self.className = "Fix."
    
    def tearDown(self):
        pass
    
#    Acceptance Test: 100
#        Analysis - Constructor
#            inputs
#                logFile
#            outputs
#                instance of Fix
#            state change
#                Writes the following entry to a new log file: "Start of log"
#
#            Happy path
#                nominal case for input string with string length .GE.1 :  Fix("logFile")
#                                      This creates a new file logFile.txt with contents "LOG:    date and time:    Start of log"

#                missing param, creating a log file "log.txt": Fix()
#                                        This creates a new file log.txt with contents "LOG:    date and time:    Start of log"
#            Sad path
#                empty String param: Fix('')  
#                non-string param: Fix(1)  
#                invalid characters: Fix($<)
#Happy path

    def test100_010_ShouldCreateNewFilelogMissingParameter(self):
        #testing = 'log.txt'
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
#         expected = 'Start of log\n'#'LOG:\t'+datetime.datetime.now().isoformat()+':\tStart of log\n'
#         result = open(testing).read() #data[len(data)-1] 
#         self.assertEquals(result,expected)
#         os.remove('log.txt')

       
    def test100_020_ShouldCreateNewFilelogUsingParameter(self):
        #Fix.Fix('logFile.txt')
        self.assertIsInstance(Fix.Fix('logFile.txt'), Fix.Fix)        
#         expected = 'Start of log\n'
#         result = open('logFile.txt').read()
#         self.assertEquals(result,expected)
#         os.remove('logFile.txt')
            
#Sad path
    def test100_910_ShouldRaiseExceptionForEmptyString(self):
        with self.assertRaises(ValueError):
            Fix.Fix('')
            
    def test100_920_ShouldRaiseExceptionForNonStringParam(self):
        with self.assertRaises(ValueError):
            Fix.Fix(5)

    def test100_910_ShouldRaiseExceptionForInvalidFileNameCharacters(self):
        with self.assertRaises(ValueError):
            Fix.Fix('<$%')            
                                 
#    Acceptance Test: 200
#        Analysis - setSightingFile
#            inputs
#                string of the form "f.xml" where f is the file name and .xml is the extension
#            outputs
#                A string having the values passed as the "sightingFile"
#
#            state change
#                Writes the following entry to a new log file: "Start of sighting file f.xml"
#
#            Happy path
#                nominal case for input: Input file name with string length of filename .GE.1 and with extension .xml: setSightingFile("f.xml")  
#                
#            Sad path
#                missing param: setSightingFile()
#                empty String param: setSightingFile('')
#                non-string param: setSightingFile(1)
#                incorrect size of filename string or no file name specified: setSightingFile(".xml")
#                missing filename extension in param: setSightingFile("f")
#                incorrect filename extension param: setSightingFile("f.xyz")
#

#Happy path

    def test200_010_ShouldInputFile(self):
        theFix = Fix.Fix()
        self.assertEqual(theFix.setSightingFile('file1.xml'),'file1.xml')

#Sad path

    def test200_910_RaiseExceptionforMissingParameter(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError):
            xmlfile.setSightingFile()

    def test200_920_RaiseExceptionforEmptyStringParameter(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError):
            xmlfile.setSightingFile('')
            
    def test200_930_RaiseExceptionforNonStringParameter(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError):
            xmlfile.setSightingFile(5)
            
    def test200_940_RaiseExceptionforFileExtensionMissing(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError):
            xmlfile.setSightingFile('f')
            
    def test200_950_RaiseExceptionforIncorrectFileExtension(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError):
            xmlfile.setSightingFile('f.abc')
            
    def test200_960_RaiseExceptionforIncorrectFileNameLength(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError):
            xmlfile.setSightingFile('.xml')
                                                                                                 
#     
#                 
#                                  
#    Acceptance Test: 300
#        Analysis - getSightings
#            inputs
#                 none
#            outputs
#                  (approximateLatitude,approximateLongitude) maybe both are 0d0.0 
#                 
#            state change
#                  navigational calculations are written to log file 
#
#            Happy path
#                nominal case: getSightings() returns LOG: <current Date and time> <sighting name> <sighting date and time> <adjusted altitude>  
#                
#            Sad path 
#                no sightingFile has been set
#                 fix tag missing in the sightingFile
#                 sighting tag missing in the sightingFile
#                 body tag missing in the sightingFile
#                 date tag is missing  in the sightingFile
#                 time tag is missing in the sightingFile
#                 observation tag is missing in the sightingFile
#                 body tag contains invalid input: no values specified
#                                                  non-string value
#                                                  empty string
#                 date tag contains invalid input: no value specified
#                                                  date in wrong format/ non-date value specified                
#                 time tag contains invalid input: no value specified
#                                                  time in wrong format/ non-time value specified                                          
#                 observation tag contain value of the form xdy.y: x is not .GE.0 and .LT.90
#                                                                  y.y is not .GE.0.0 and .LT.60.0
#                                                                  x is 0 and y.y is .LT.0.1
#                                 does not contain any value 
#                                 does not contain value of the form xdy.y                        
#                 height tag contains data that is non-numeric 
#                                          that is .LT.0
#                temperature tag contains data that is non-integer
#                                                that is .LT.-20 or .GT. 120
#                 pressure tag contains data that is non-numeric
#                                            that is .LT.100 or .GT.1100               
#                horizon tag contains: empty- string
#                                       string which is not "artificial" or "natural"
    def test300_010_ShouldReturnApproxLatitudeAndLongitude(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile('f1.xml')
        self.assertEqual(xmlfile.getSightings(),('0d0.0','0d0.0'))


    def test300_020_SholdReturnLogwithSameDate(self):
        xmlfile = Fix.Fix("sortedsamedatelog.txt")
        xmlfile.setSightingFile("sameDate.xml")
        self.assertEqual(xmlfile.getSightings(),('0d0.0','0d0.0'))
        
    def test300_030_Sortsamedateandtime(self):
        xmlfile = Fix.Fix("sortedsamedateandtimelog.txt")
        xmlfile.setSightingFile("sameDateAndTime.xml")
        self.assertEqual(xmlfile.getSightings(),('0d0.0','0d0.0'))

        
        
#Sad path        
    def test300_920_ShouldRaiseExceptionForBodyMissing(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("bodyMissing.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()
            
    def test300_930_ShouldRaiseExceptionForDateMissing(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("dateMissing.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()
            
            
    def test300_940_ShouldRaiseExceptionForTimeMissing(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("timeMissing.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()
            
            
    def test300_950_ShouldRaiseExceptionForObservationMissing(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("observationMissing.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()


    def test300_960_ShouldRaiseExceptionForIncorrectHorizonValue(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("incorrectHorizonValue.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()  

    def test300_970_ShouldRaiseExceptionforLowerPressureValue(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("pressureLowerLimit.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()        
            
    def test300_980_shouldRaiseExceptionforUpperPressureValue(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("pressureUpperLimitExceeded.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()   

    def test300_990_ShouldRaiseExceptionforUpperTemperature(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("tempAboveLimit.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings() 
            
    def test300_991_ShouldRaiseExceptionforLowerTemperature(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("tempBelowLimit.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()    
                        
    def test300_992_ShouldRaiseExceptionforHeightBelowIdeal(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("heightBelowIdeal.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings() 
                 
    def test300_993_ShouldRaiseExceptionforHighDegrees(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("obsDegGreater90.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()        


    def test300_994_ShouldRaiseExceptionforLowDegrees(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("obsDegLessThan0.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()   
            

    def test300_995_ShouldRaiseExceptionforLowMinutes(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("obsMinLessThan0.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()    
            
    def test300_996_ShouldRaiseExceptionforHighMinutes(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("obsMinGreater60.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()      

    def test300_997_ShouldRaiseExceptionObsTooLow(self):
        xmlfile = Fix.Fix()
        xmlfile.setSightingFile("obsAltitudeLess.xml")
        with self.assertRaises(ValueError):
            xmlfile.getSightings()                            


#     def test300_960_ShouldRaiseExceptionForSightingMissing(self):
#         xmlfile = Fix.Fix()
#         xmlfile.setSightingFile("sightingMissing.xml")
#         with self.assertRaises(ValueError):
#             xmlfile.getSightings()            
#                                                                              