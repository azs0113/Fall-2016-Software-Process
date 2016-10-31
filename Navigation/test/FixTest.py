'''
    Created on 10/12/16
    Modified on 10/30/16
    
    @author: Ankit Kumar Singh
    Test Cases for Fix component. These are part of CAO03 Assignment
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
        self.assertEqual(theFix.setSightingFile('file1.xml'),os.path.abspath('file1.xml'))

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
    def test200_970_RaiseExceptionFileNameInValid(self):
        xmlfile = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            xmlfile.setSightingFile("?#")              
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
        xmlfile.setSightingFile('text.xml')
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




#     Acceptance Test: 400
#        Analysis - setAriesFile
#            input:
#                ariesFile
#            output:
#                Returns a string whose value is the absolute
#                filepath of the file specified by the parameter.    
#            state change:
#                Writes the following entry to the log file:
#                The literal "Aries file:"    followed by
#                a tab (i.e., "\t")    followed by
#                the absolute filepath of the star file

#            Happy path
#                nominal case:  returns

#Happy path
    def test400_010_ShouldAcceptaTextFileAsParameter(self):
        fix = Fix.Fix()
        f = open('ariesFile.txt','a')
        ariesFile = fix.setAriesFile('ariesFile.txt')
        self.assertTrue(ariesFile==os.path.abspath('ariesFile.txt')) 
        f.close()
        
        
    def test400_020_ShouldWriteALiteral(self):
        fix = Fix.Fix()
        f = open('ariesFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        ariesFile = fix.setAriesFile('ariesFile.txt')
        self.assertNotEqual(lines[-1].find('Aries file:'),-1,'Wrong')
        f.close()
        log.close()
        
    def test400_030_ShouldWritesanAbsolutePath(self):
        fix = Fix.Fix()
        f = open('ariesFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        ariesFile = fix.setAriesFile('ariesFile.txt')
        self.assertNotEqual(lines[-1].find(os.path.abspath('ariesFile.txt')),-1,'Wrong')
        f.close()
        log.close()
        
    def test400_040_ShouldWritetheLiteralAndtheAbsolutePath(self):
        fix = Fix.Fix()
        f = open('ariesFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        ariesFile = fix.setAriesFile('ariesFile.txt')
        self.assertNotEqual(lines[-1].find('Aries file:\t'+os.path.abspath('ariesFile.txt')),-1,'Wrong')
        f.close()
        log.close()
        
    def test400_050_ShouldWriteTabSpaceBetweenLiteralAndtheAbsolutePath(self):
        fix = Fix.Fix()
        f = open('ariesFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        ariesFile = fix.setAriesFile('ariesFile.txt')
        self.assertEqual(lines[-1].find(os.path.abspath('ariesFile.txt'))-lines[-1].find('Aries file:'),12,'Wrong')
        f.close()
        log.close()    

    
    
 #Sad Path
 
 
 
    def test400_910_RaiseExceptionIfParameterIsEmpty(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setAriesFile('')


    def test400_920_RaiseExceptionIfParameterDoesNotHaveFileExtension(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            ariesFile = fix.setAriesFile('ariesFile')    


    def test400_930_RaiseExceptionIfParameterIsNotaValidFileName(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setAriesFile('#<56.txt')    


    def test400_940_RaiseExceptionIfFileNameIsOfInvalidSize(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setAriesFile('.txt')            



#     Acceptance Test: 500
#        Analysis - setStarFile
#            input:
#                starFile
#            output:
#                Returns a string whose value is the absolute
#                filepath of the file specified by the parameter.    
#            state change
#                Writes the following entry to the log file:
#                The literal "Star file:"    followed by
#                a tab (i.e., "\t")    followed by
#                the absolute filepath of the star file

#            Happy path
#                nominal case:  returns 


    def test500_010_ShouldAcceptfileAsParameterwithTxtExtension(self):
        fix = Fix.Fix()
        f = open('starFile.txt','a')
        starFile = fix.setStarFile('starFile.txt')
        self.assertTrue(starFile==os.path.abspath('starFile.txt')) 
        f.close()


    def test500_020_ShouldWriteALiteral(self):
        fix = Fix.Fix()
        f = open('starFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        fix.setStarFile('starFile.txt')
        self.assertGreater(lines[-1].find('Star file:'),-1,'Wrong')
        f.close()
        log.close()


    def test500_030_ShouldWritetheAbsolutePath(self):
        fix = Fix.Fix()
        f = open('starFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        starFile = fix.setStarFile('starFile.txt')
        self.assertNotEqual(lines[-1].find(os.path.abspath('starFile.txt')),-1,'Wrong')
        f.close()
        log.close()
        
    def test500_040_ShouldWriteTheLiteralAndtheAbsolutePath(self):
        fix = Fix.Fix()
        f = open('starFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        fix.setStarFile('starFile.txt')
        self.assertNotEqual(lines[-1].find('Star file:\t'+os.path.abspath('starFile.txt')),-1,'Wrong')
        f.close()
        log.close()
        
    def test500_050_ShouldWriteaTabSpaceBetweenLiteralAndtheAbsolutePath(self):
        fix = Fix.Fix()
        f = open('starFile.txt','a')
        log = open('log.txt','r')
        lines = log.readlines()
        fix.setStarFile('starFile.txt')
        self.assertEqual(lines[-1].find(os.path.abspath('starFile.txt'))-lines[-1].find('Star file:'),11,'Wrong')
        f.close()
        log.close()



#Sad Path                    
    def test500_910_RaiseExceptionIfParameterIsEmpty(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setStarFile('')
  

    def test500_920_RaiseExceptionIfParameterhasNoFileExtension(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setStarFile('ariesFile')
              
    def test500_930_RaiseExceptionIfParameterIsNotaValidFilename(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setStarFile('#?23.txt')
              
    def test500_940_RaiseExceptionIfSizeOfFileNameIsInvalid(self):
        fix = Fix.Fix()
        with self.assertRaises(ValueError):
            fix.setStarFile('.txt')

#Happy path for getSightingsFile



    def test600_010_ReturnstheCorrectValuewithValidInputFiles(self):
        fix = Fix.Fix()
        fix.starFile = 'stars.txt'
        fix.ariesFile = 'aries.txt'
        fix.getGeographicPosition('Sirius', '2017-04-17','09:30:30')
        
        
