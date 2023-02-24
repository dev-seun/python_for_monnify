import json, base64, datetime, random, string
from requests import request
class InitializeMonnifySDKTransaction:
    """
        Author: Oladele seun
        Github: https://github.com/samwhitedove
        Linkedin: https://www.linkedin.com/in/archivas/
        Version: 0.0.1
        Date: 21:02:2023
        Descriptio: This module allow you to perform basic monnify actions, 
                    i didnt cover all their api but feel free to request for anyone you need :)

        Class to initialize connection to monnify server.. 
        
        While initializing this class you need to pass some default parameter which value can be uptained from monnify website after completing 
        your account registration.

        PARAMETER:TYPE ===== REQUIRED ===== DEFAULT ========================== TYPE =========== OPTIONS
        contractCode:str,    YES            NONE                               STRING           NONE
        currencyCode:str,    NO             NGN                                STRING           CHECK MONNIFY FOR YOUR COUNTRY CURRENCY CODE
        apiKey:str,          YES            NONE                               STRING           NONE
        secretKey:str,       YES            NONE                               STRING           NONE
        paymentMethods       NO            ["CARD","ACCOUNT_TRANSFER"]         LIST             ["CARD","ACCOUNT_TRANSFER","USSD","PHONE_NUMBER"]
    """
    
    def __init__(self, contractCode:str, apiKey:str, secretKey:str, currencyCode:str = "", paymentMethods:list = []) -> None:
        """Initializing thhe class fields"""
        self.__apiKey:str = apiKey
        self.__secretKey:str = secretKey
        self.__contractCode:str = contractCode
        self.__currencyCode:str = currencyCode
        self.__paymentMethods:str = paymentMethods
        self.__baseUrl:str = "https://sandbox.monnify.com"
        self.__token:str = ""
        self.__paymentMethods:str = ["CARD","ACCOUNT_TRANSFER"]
        self.__currencyCode:str = "NGN"
        self.__startRef:str = "MFY_PY"

    def __str__(self):
        value =  {
            "apiKey" : self.__apiKey,
            "secretKey" : self.__secretKey,
            "contractCode" : self.__contractCode,
            "currencyCode" : self.__currencyCode,
            "paymentMethods" : self.__paymentMethods,
            "baseUrl" : self.__baseUrl,
            "token" : self.__token,
            "paymentMethods" : self.__paymentMethods,
            "currencyCode" : self.__currencyCode,
            "startRef" : self.__startRef,
        }
        print(value)

    def __toBase64(self) -> str:
        """Convert the contract and the api key to a encoded base64 string"""
        _string =  f"{self.__apiKey}:{self.__secretKey}"
        _string_bytes = _string.encode("ascii")
        base64_bytes = base64.b64encode(_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def __getAccesstoken(self) -> dict:
        """Get access token to make request to other minnify api endpoint"""
        url = f"{self.__baseUrl}/api/v1/auth/login"
        encoded = self.__toBase64() #text=f"{self.__apiKey}:{self.__secretKey}"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded}'
        }
        resp = request('POST', url=url, headers=headers)
        data = json.loads(resp.text)
        if resp.status_code == 200:
            return {"accessToken": data['responseBody']['accessToken'], "message": data['responseMessage'], "statusCode": resp.status_code, 'responseCode': data['responseCode']}
        return {"message": "Invalid credential, Unable to get token", "statusCode": resp.status_code, 'responseCode': data['responseCode']}

    def __make_request(self, url:str, payload:dict={}, method:str="POST") -> dict:
        """ This is a general method for making http request to any monnify endpoint passing all the required oprtions and data"""
        accessToken = self.__getAccesstoken() # getting the access token before accessing other monnify payment endpoint
        if accessToken['statusCode'] == 200:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {accessToken["accessToken"]}'
            }

            resp = request(method, url=url, headers=headers, json=payload)
            data = json.loads(resp.text)
            if resp.status_code == 200:
                return {"data": data['responseBody'], "message": data['responseMessage'], "statusCode": resp.status_code, 'responseCode': data['responseCode'],}
            return {"message": data['responseMessage'], "statusCode": resp.status_code , 'responseCode': data['responseCode']}
        return {"message": accessToken['message'], "statusCode": accessToken['statusCode'], 'responseCode': accessToken['responseCode']}

    def __generate_receipt_id(self, start:str= "") -> str:
        """
            Generating a referrence code for every transaction made,
            the start parameter with be the STRING value that will be at the beginning of every transaction referrence code

            PARAMETER       REQUIRED        DEFAULT      TYPE 
            start           NO              MFY-PY       STRING
        """
        gen_ref_id:str =''.join(random.choices(string.ascii_lowercase, k=5))
        return f"{start if start != '' else self.__startRef}_{gen_ref_id.upper()}-{datetime.datetime.now().timestamp()}"

    def reserveBankName(self, customerName:str, customerEmail:str, customerBVN:str, preferredCodes:list=[]) -> dict:
        """
            This method allow you to reserve a dedicated account number for any of your app user e.g if you're running a wallet system.

            Its create a virtual account number that can be use to top up your user wallet a collection account number to transactons.

            These are the available banks for account number reservation.
              SN   NAME             CODE
              1  # Moniepoint       50515
              2  # Wema Bank        035
              3  # Sterling Bank    232
            
            if you did not specify any of the above bank code as a preferred or default bank.. monnify will virtually create account number on the 
            three bank per every request for account number.

            NOTE:: Customer Name will be use as the account name
            PARAMETERS          OPTIONAL ===== TYPE 
            accountName         NO             STRING
            customerEmail       NO             STRING
            bvn                 NO             STRING
            customerName        NO             STRING
            preferredBanks      YES            LIST
        """
        
        if isinstance(preferredCodes, list):
            url = f"{self.__baseUrl}/api/v2/bank-transfer/reserved-accounts"
            body = {
                "accountReference": self.__generate_receipt_id(start="ACC_REF"),
                "accountName": customerName,
                "currencyCode": self.__currencyCode,
                "contractCode":  self.__contractCode,
                "customerEmail": customerEmail,
                "bvn": customerBVN,
                "customerName": customerName,
                "getAllAvailableBanks": True if len(preferredCodes) == 0 else False
            }

            if len(preferredCodes) != 0:
                body.update({"preferredBanks": preferredCodes})

            resp = self.__make_request(url=url, payload=body)
            if resp['statusCode'] == 200:
                return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": resp['data'] }
            return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
        raise ValueError("preferredBanks must be a list of bank codes")

    def initializeTransaction(self, amount:str, customerName:str, paymentDescription:str, customerEmail:str, successUrl:str, refStart:str="") -> dict:
        """
            Method to initialize a single payment to monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
            amount                  YES            NONE         STRING
            customerName            YES            NONE         STRING
            customerEmail           YES            NONE         STRING
            paymentDescriptio       YES            NONE         STRING
            redirectUrl             YES            NONE         STRING
            refStart                NO             MFY_PY       STRING
        """

        url = f"{self.__baseUrl}/api/v1/merchant/transactions/init-transaction"
        body = {
            "amount": str(amount),
            "customerName": customerName,
            "customerEmail": customerEmail,#"stephen@ikhane.com",
            "paymentReference": self.__generate_receipt_id(start=refStart), # "123031klsadkad"
            "paymentDescription": paymentDescription, #"Trial transaction"
            "currencyCode": self.__currencyCode,
            "contractCode": self.__contractCode,
            "redirectUrl": successUrl, #"https://my-merchants-page.com/transaction/confirm"
            "paymentMethods": self.__paymentMethods,
        }

        resp = self.__make_request(url=url, payload=body)
        if resp['statusCode'] == 200:
            data = resp['data']
            return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
        return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
    
    def deleteReservedAccount(self, accountReference:str) -> dict:
        """
            Method to delete a reserved account on monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
            accountReference       YES            NONE         STRING

            The reference id is the account reference
            e.g ACC_REF_SIWSO-1677258463.370003
        """
        url = f"{self.__baseUrl}/api/v1/bank-transfer/reserved-accounts/reference/{accountReference}"

        resp = self.__make_request(url=url, method="DELETE")
        if resp['statusCode'] == 200:
            data = resp['data']
            return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
        return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
    
    def addReservedAccountToExistingCustomerReservedAccounts(self, preferredBanks:list, accountReference:str) -> dict:
        """
            Method to add a more account to an existing custormers reserved account on monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT ===== TYPE 
            accountReference       YES            NONE        LIST
            preferredBanks         YES            NONE        STRING

            The reference id is the account reference
            e.g ACC_REF_SIWSO-1677258463.370003

            e.g 
            a customer have a reserve account of sterlin bank and
            you want the customer to have another reserve account with wema bank etc.
        """
        if isinstance(preferredBanks, list):
            url = f"{self.__baseUrl}/api/v1/bank-transfer/reserved-accounts/add-linked-accounts/{accountReference}"
            body = {
                "getAllAvailableBanks": False,
                "preferredBanks": ["035"]
            }
            resp = self.__make_request(url=url, payload=body, method="PUT")
            if resp['statusCode'] == 200:
                data = resp['data']
                return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
            return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
        raise ValueError("preferred bank must be a list type")
    
    def updateCustomerReserveAccountBvn(self, bvn:str, accountReference:str) -> dict:
        """
            Method to update the bvn attached to a customer reserved account on monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
            accountReference       YES            NONE         STRING
            bvn                    YES            NONE         STRING

            The reference id is the account reference
            e.g ACC_REF_SIWSO-1677258463.370003

            a customer have a reserve account and you want to update the bvn attached
            to the customer reserve accounts.
        """
        url = f"{self.__baseUrl}/api/v1/bank-transfer/reserved-accounts/update-customer-bvn/{accountReference}"
        body = {
            "bvn": bvn
        }
        resp = self.__make_request(url=url, payload=body, method="PUT")
        if resp['statusCode'] == 200:
            data = resp['data']
            return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
        return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
    
    def getAllTransactionOnAReserveAccount(self, accountReference:str, page:str="0", size:str="10") -> dict:
        """
            Method to all transactions on a single reserved account on monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
            accountReference       YES            NONE         STRING
            page                   NO             0            STRING
            size                   NO             10           STRING

            The reference id is the account reference
            e.g ACC_REF_SIWSO-1677258463.370003
        """
        url = f"{self.__baseUrl}/api/v1/bank-transfer/reserved-accounts/transactions?accountReference={accountReference}&page={page}&size={size}"

        resp = self.__make_request(url=url, method="GET")
        if resp['statusCode'] == 200:
            data = resp['data']
            return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
        return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
    
    def getASingleCustomerAllReservedAccount(self, accountReference:str) -> dict:
        """
            Method to all transactions on a single reserved account on monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
            accountReference       YES            NONE         STRING

            To get the details of a customer's reservation with all account numbers reserved, 
            it will return all the details attached to that account Reference.
        """
        url = f"{self.__baseUrl}/api/v2/bank-transfer/reserved-accounts/{accountReference}"

        resp = self.__make_request(url=url, method="GET")
        if resp['statusCode'] == 200:
            data = resp['data']
            return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
        return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
    
    def validateTransactionStatus(self, transactionReference:str) -> dict:
        """
            Method to all transactions on a single reserved account on monnify server.. 
            
            PARAMETER:TYPE ========= REQUIRED ===== DEFAULT  ===== TYPE 
            transactionReference       YES            NONE         STRING

            This is use to verify a payment a payment status on the monnify server 
            e.g status for payment
            PAID, OVERPAID, PARTIALLY_PAID, PENDING, ABANDONED, CANCELLED, FAILED, REVERSED, EXPIRED
        """
        url = f"{self.__baseUrl}/api/v2/transactions/{transactionReference}"

        resp = self.__make_request(url=url, method="GET")
        if resp['statusCode'] == 200:
            data = resp['data']
            return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": data }
        return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}