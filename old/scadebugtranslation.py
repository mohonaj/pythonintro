import sys
import os

argZero = sys.argv[0]
numArgs = len(sys.argv)
if ( numArgs > 2 ):
     scaPropertiesFile = sys.argv[1]
     srcDir = sys.argv[2]

     f=open(scaPropertiesFile, "r")
     if f.mode == 'r':
      if ( not os.path.exists("scaDebugTranslation_logfiles")):
           os.system("mkdir scaDebugTranslation_logfiles") 
      allLines =f.readlines()
      for currentLine in allLines:
        property=currentLine.split("=")
        if ( property[0] == "com.fortify.sca.DefaultFileTypes"):
         print(property[1])
         filetypes=property[1].split(",")
         for fileType in filetypes:
           fileTypeStr = str(fileType).rstrip('\n')
           if ( not os.path.exists("files_" + fileTypeStr) ):
             os.system("mkdir files_" + fileTypeStr) 
           cmd = '/usr/bin/find ' + srcDir + ' -name "*.' + fileTypeStr + '" -exec /bin/cp {} files_'+ fileTypeStr + ' \;'
           print(cmd)
           rt = os.system(cmd)
           cmd = "sourceanalyzer -b debug_" + fileTypeStr + " -verbose -logfile scaDebugTranslation_logfiles/debug_" + fileTypeStr + ".log -debug files_" + fileTypeStr
           rt = os.system(cmd)
           cmd = "sourceanalyzer -b debug_" + fileTypeStr + " -show-build-warnings >>" + "scaDebugTranslation_logfiles/" + fileTypeStr + "_BuildWarnings.log "
           rt = os.system(cmd)
else:
  print("usage: " + argZero + " <SCA Properties File Path> <Source Dir>")
      
