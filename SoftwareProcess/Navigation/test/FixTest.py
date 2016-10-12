import unittest
import Navigation.prod.Fix as Fix

class FixTest(unittest.TestCase):
    
    def setUp(self):
        self.Classname = "Fix."
    
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
#                nominal case for input string logFile with string length .GE.1 :  Fix("logFile") invalidated
#                
#            Sad path
#                missing param: Fix() 
#                empty String param: Fix("")   
#                non-string param: Fix(1)   
#                
#                                  
#    Acceptance Test: 200
#        Analysis - setSightingFile
#            inputs
#                string of the form "f.xml" where f is the file name and .xml is the extension
#            outputs
#                return True, if the file f.xml is new,
#                return False , if file specified as input already exists

#            state change
#                Writes the following entry to a new log file: "Start of sighting file f.xml"
#
#            Happy path
#                nominal case for input: Input file name with string length of filename .GE.1 and with extension .xml: setSightingFile("f.xml")  
#                
#            Sad path
#                missing param: setSightingFile()
#                empty String param: setSightingFile("")
#                non-string param: setSightingFile(1)
#                incorrect size of filename string or no file name specified: setSightingFile(".xml")
#                missing filename extension in param: setSightingFile("f")
#                incorrect filename extension param: setSightingFile("f.xyz")
#                
#                
#    Acceptance Test: 300
#        Analysis - getSightings
#            inputs
#                none
#            outputs
#                return True, if the file f.xml is new,
#                return False , if file specified as input already exists
#
#            state change
#                Writes the following entry to a new log file: "Start of sighting file f.xml"
#
#            Happy path
#                nominal case for input: Input file name with string length of filename .GE.1 and with extension .xml: setSightingFile("f.xml")  
#                
#            Sad path
#                missing param: setSightingFile()
#                empty String param: setSightingFile("")
#                non-string param: setSightingFile(1)
#                incorrect size of filename string or no file name specified: setSightingFile(".xml")
#                missing filename extension in param: setSightingFile("f")
#                incorrect filename extension param: setSightingFile("f.xyz")
#                
#                
#
#                                  
#                                
#                
#
#