'''
    Author: Zach Lewis

    Description: 
      Initial Simplified for use by Crime Stats Process
      Reading Gmail for Crime Data Emails using a custom label
      Simple Parsing for Crime Stats.

    Date: 12/22/2019 
    Version:  Beta 0.25
'''

from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
# import dateutil.parser as parser
import csv
from time import strftime, gmtime
import sys

types = [ "Arson", "Assault", "Burglary", "Disturbing the Peace", "Drugs / Alcohol Violations", "DUI", "Fraud", "Homicide", "Motor Vehicle Theft", "Robbery", "Sex Crimes", "Theft / Larceny", "Vandalism", "Vehicle Break-In / Theft", "Weapons"]

def ReadEmailDetails(service, user_id, msg_id):

  temp_dict = { }

  try:

      message = service.users().messages().get(userId=user_id, id=msg_id,format='raw' ).execute() # fetch the message using API
      msg_str = str(base64.urlsafe_b64decode(message['raw'].encode('ASCII')))
      
      waitForNext = False;
      
      crimeline = "";
      
      linepre = msg_str.replace('\\n', '\n').replace('\\r','');
      i = 0;
      for linestr in linepre.splitlines():
       
       if ( linestr in types or waitForNext):
         
         i = i + 1;
         if ( i > 5 ):
           waitForNext = False;
           crimeline = crimeline + "\"" + linestr + "\""
           print(crimeline);
           
           crimeline = ""
           i = 0;
         else:
           waitForNext = True;
           if ( i == 5  ):
              street = linestr.split();
              
             # print( street[ len(street) - 2 ] );
              crimeline = crimeline + "\"" + linestr + "\"," + "\"" + street[len(street) - 2] + "\","
           elif(i == 6) :
              street = linestr.split();
              crimeline = crimeline + "\"" + linestr + "\"," + "\"" + street[0] + "\","
           else:
              crimeline = crimeline + "\"" + linestr + "\","

  except Exception as e:
      print(e)
      temp_dict = None
      pass

  finally:
      return temp_dict
  

def ListMessagesWithLabels(service, user_id, label_ids=[]):
  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=['Label_984599473385438091'],
                                               maxResults=15500).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])
    
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']

      #NOTE: Label (Label_984599473385438091) is my crime data label in Gmail.

      response = service.users().messages().list(userId=user_id,
                                                 labelIds=['Label_984599473385438091'],
                                                 pageToken=page_token,
                                                 maxResults=15500).execute()

      messages.extend(response['messages'])
      
      sys.stdout.flush()
      sys.exit(1);
      quit(1);
    return messages

  except errors.HttpError as error:
    print('An error occurred: %s' % error)


if __name__ == "__main__":

  # Print Header:
  print("CrimeType,Blank,CrimeDetails,DateId,Street,StreetName,DateTime");

  SCOPES = 'https://www.googleapis.com/auth/gmail.modify' 
  store = file.Storage('storage.json')
  creds = store.get()

  if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
      creds = tools.run_flow(flow, store)

  GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

  user_id =  'me'
  
  email_list = ListMessagesWithLabels(GMAIL, user_id, [])

  final_list = [ ]

  sys.stdout.flush()
  rows = 0
  
  for email in email_list:
        msg_id = email['id'] 
    
        email_dict = ReadEmailDetails(GMAIL,user_id,msg_id)
       
        if email_dict is not None:
          rows += 1
  quit();
  sys.stdout.flush()

