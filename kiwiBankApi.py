import requests
import logging
from bs4 import BeautifulSoup

class KiwiBankApi(object):

    def __init__(self):
        self.session = requests.Session()
        self.logger = logging.getLogger()
        self.retRequest = None
        
        
    def login(self, login, password):   
        self.logger.info("Login attempt...")
        
        self.retRequest = self.session.get('https://www.ib.kiwibank.co.nz/login/')
        
        soup = BeautifulSoup(self.retRequest.content, 'html.parser')        
        self.logger.debug(soup.prettify())        
         
        data = [
          ('__LASTFOCUS', ''),
          ('__EVENTTARGET', 'ctl00$c$ProgressFinalSubmit$FinalStepButton'),
          ('__EVENTARGUMENT', ''),
          ('__VSTATE', 'nVJPT9swFF+cGEoHDdpGNIHUFqnagY2koGmj3FDFZRoc+LcLEpjYSb2mcbAfyzTxFThynNDO+0A772tsB+akTUvU7TIfnt/v/f29Z98bto2r61uvN7Y6nc23b2wH1Z+ekIhTAuyAXV4xBXuCMmQ4KLCps4hMLRFCWeDsCVf8ImI9iqxFjefJFQhfDJKIAcOmCALqVPKEGjK0tLIKeRmUY1RYl4zqQJ2lRMY8Dqm2OlbdJBHgyoehbbVuKunjFY8PSMiUx30Rn01S3JAHNOfUMDIywzYjVCmhx2P6OZwvw4WC4MxwzoJrNq11xD4DXn4vwiaPmyC0BCZjBs0LEvcz4hThjLnVkyzAKz2ARG17Xpqmbp+nPItyfeHGX7yGoaecK5rWyhzw3zY15j8Om7VHWlZpkpHb/pU61WfinCk7y0ubKzur0xt92J0+N3Hbh6jdbvmtY8XkvoBDBsfJrpRC7jGl9Bu2RrfqihikiOyQ4rUiaSdisitEn+dfkEtGp8KfvXxUo8OjVUN/Gq0F6F4fm2LvYSV4Rz6RQ1/yBP6v3A/3+7fG3dHHrzfn6+Hd6W3yZPP3q86v6+1+N9ohL37+AQ=='),
          ('__VIEWSTATE', ''),
          ('__EVENTVALIDATION', '/wEdAASvVXD1oYELeveMr0vHCmYPPwV9PorNx6c52mq8Z4/3YxLfEa1JDlqfj8bLh3VGcfhdY6yQmR47qzW9jZRay3GEDae84IwkKPW2UM9PlBZt3bQKLvc38FHQpRk5hdtJN0k='),
          ('ctl00$c$txtUserName', login),
          ('ctl00$c$txtPassword', password),
        ]
        
        self.retRequest = self.session.post('https://www.ib.kiwibank.co.nz/login/', data=data)
        
        soup = BeautifulSoup(self.retRequest.content, 'html.parser')
        self.logger.debug(soup.prettify()) 
        
            

    
    
    
    def resolveChallenge(self,questionsAnswers):  
        self.logger.info("Resolving challenge...")      
        
        soup = BeautifulSoup(self.retRequest.content, 'html.parser')
        question = soup.find(id="question").find_all('div')[1].string
        
        self.logger.info( 'Question is : ' + question)
        
        for k in questionsAnswers.keys():
            if(question == k):
                reponse = questionsAnswers[k]
                break

        
        answers = soup.find(id="answer").find_all('div')[1:]
        
        index = []
        
        challenge = ""
        i = 0
        for div in answers:
            if('required' in str(div)):
                index.append(i)
                challenge = challenge + "O"
            else:
                challenge = challenge + "X"
            i = i + 1
        
        letter1 = str(reponse[index[0]]) 
        letter2 = str(reponse[index[1]]) 
        
        self.logger.info('Challenge is : ' + challenge) 
        self.logger.info('Response : letter 1: ' + letter1 + ' letter 2: ' + letter2)


        vstate = soup.find(id="__VSTATE")['value']
        eventvalidation = soup.find(id="__EVENTVALIDATION")['value']
        
        
        data = [
          ('__EVENTTARGET', 'ctl00$c$ChallengeControl$SubmitAnswer$FinalStepButton'),
          ('__EVENTARGUMENT', ''),
          ('__VSTATE', vstate),
          ('__VIEWSTATE', ''),
          ('__EVENTVALIDATION', eventvalidation),
          ('letter1', letter1),
          ('letter2', letter2),
        ]
        
        self.retRequest = self.session.post('https://www.ib.kiwibank.co.nz/keepsafe/challenge/', data=data)
        
        
        
        soup = BeautifulSoup(self.retRequest.content, 'html.parser')            
        self.logger.debug(soup.prettify()) 
        
        
        
    def extractCSV(self,accountNum,dateFrom,dateTo):
        self.logger.info("Extracting CSV file...") 
        #Make a first get to the account to init html page
        self.retRequest = self.session.get('https://www.ib.kiwibank.co.nz/accounts/view/' + accountNum)
    
    
        soup = BeautifulSoup(self.retRequest.content, 'html.parser')
        self.logger.debug(soup.prettify()) 
    


        requestVerificationToken = soup.find(id="__RequestVerificationToken")['value']
        vstate = soup.find(id="__VSTATE")['value']
        eventvalidation = soup.find(id="__EVENTVALIDATION")['value']
    
        
        
        data = [
          ('__RequestVerificationToken', requestVerificationToken),
          ('__EVENTTARGET', 'ctl00$c$TransactionSearchControl$ActionButton'),
          ('__EVENTARGUMENT', ''),
          ('__LASTFOCUS', ''),
          ('__VSTATE', vstate),
          ('__VIEWSTATE', ''),
          ('__EVENTVALIDATION', eventvalidation),
          ('ctl00$c$TransactionSearchControl$AccountList', '/accounts/view/' + accountNum),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$initialDate$TextBox', dateFrom),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FromDateRegex_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FromDateTextBoxExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FromDateRegex_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$InitialDateNotFuture_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$InitialDateNotFutureTextBoxExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$InitialDateNotFuture_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FromHistoryLimit_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FromHistoryLimitExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FromHistoryLimit_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$finalDate$TextBox', dateTo),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$ToDateRegex_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FinalDateTextBoxExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$ToDateRegex_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$DateRangeValidity_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$DateRangeValidityExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$DateRangeValidity_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FutureDate_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FinalDateNotFutureExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$FutureDate_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$ToDateHistoryLimit_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$ToDateHistoryLimitExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DualDateSelector$ToDateHistoryLimit_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$AmountRange$TransactionAmountLowerBoundField', ''),
          ('ctl00$c$TransactionSearchControl$AmountRange$LowerBoundRegex_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$AmountRange$LowerBoundTextFieldExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$AmountRange$LowerBoundRegex_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$AmountRange$TransactionAmountUpperBoundField', ''),
          ('ctl00$c$TransactionSearchControl$AmountRange$UpperBoundRegex_Highlight_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$AmountRange$UpperBoundTextFieldExtender_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$AmountRange$UpperBoundRegex_ShowError_ClientState', 'VALID'),
          ('ctl00$c$TransactionSearchControl$DWGroup', 'DepositsAndWithdrawals'),
          ('ctl00$c$TransactionSearchControl$ExportFormats$List', 'CSV-Extended'),
          ('ctl00$c$AccountGoal$SaveGoalControl$Starting$AmountControl$TransferFundsAmountTextBox', '3540.53'),
          ('ctl00$c$AccountGoal$SaveGoalControl$Starting$AmountControl$AmountMandatoryValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$Starting$AmountControl$AmountFormatValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$Starting$AmountControl$AmountFormatValidator_ShowError_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$Starting$AmountControl$AmountValueValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$Starting$AmountControl$AmountValueValidator_ShowError_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$TargetBalance$AmountControl$TransferFundsAmountTextBox', '0.00'),
          ('ctl00$c$AccountGoal$SaveGoalControl$TargetBalance$AmountControl$AmountMandatoryValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$TargetBalance$AmountControl$AmountFormatValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$TargetBalance$AmountControl$AmountFormatValidator_ShowError_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$TargetBalance$AmountControl$AmountValueValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$TargetBalance$AmountControl$AmountValueValidator_ShowError_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$StartingAmountValidator_ErrorToggle_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$StartingAmountValidator_ErrorHighlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$GoalAmountValidator_ErrorToggle_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$GoalAmountValidator_ErrorHighLight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$AccountTitleTextField', ''),
          ('ctl00$c$AccountGoal$SaveGoalControl$customisedNameValidation_errorToggle_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$ToggleCssClassExtender1_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$SelectedDateControl$TextBox', ''),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$DateOverrideNull', ''),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$DateRequiredFieldValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$DateRangeValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$DateRangeValidator_ShowError_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$DateIsDateValidator_Highlight_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$DateControl$DateIsDateValidator_ShowError_ClientState', 'VALID'),
          ('ctl00$c$AccountGoal$SaveGoalControl$SelectedAccountGoalTypeField', 'Savings'),
        ]
        
        self.retRequest = self.session.post('https://www.ib.kiwibank.co.nz/accounts/view/' + accountNum, data=data)
    
        self.logger.debug('CSV file :\n\n' + str(self.retRequest.content) + '\n') 
        
        ret = self.retRequest.content.decode("utf-8")
        
        self.logger.debug("CSV file extracted : \n" + ret) 
        
        return( ret )
            
                
    
    
    
    
    
    
    def logout(self):            
        self.session.get('https://www.ib.kiwibank.co.nz/logout/')
