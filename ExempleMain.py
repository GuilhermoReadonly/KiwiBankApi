from kiwiBankApi import KiwiBankApi

import time
import logging



    

"""
The purpose of this main file is to show how to use the KiwiBankApi.
Of course all the logins, keepsafe and bank account informations here are fakes and need to be replaced by your own.
"""
if __name__ == '__main__':
    
    #login informations
    user = '1234567'
    password = 'MySuperPassword'
     
    #KeepSafe challenge informations
    questionsAnswers = {'The name of my first pet?':'pinette', 
                    'My mother\'s maiden name?':'duchesse d\'orléans',
                    'Another question?':'another response'
    }
     
    #CSV extract informations
    dateFrom = todayDate = '1/1/2017'
    dateTo = todayDate = str( time.strftime("%d/%m/%YYYY"))
    accountNum = '123456789ABCDEF123456789ABCDEF12'

    
    #Logging stuff
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(threadName)s %(levelname)s %(filename)s %(funcName)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
     
 
    kbApi = KiwiBankApi()
     
    kbApi.login(user, password)
    kbApi.resolveChallenge(questionsAnswers)
    csvTxt = kbApi.extractCSV(accountNum, dateFrom,dateTo)
    kbApi.logout()
    

    csvLines = csvTxt.split('\n')
    
    for line in csvLines:
        logger.info(line)
         
    
    
    logger.info('That\'s all folks !!!') 
    
 
    
