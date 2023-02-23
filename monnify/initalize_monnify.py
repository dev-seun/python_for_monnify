import json, base64, datetime, random, string
from requests import request


class InitializeMonnifySDKTransaction:
    """
        Author: Oladele seun
        Github: https://github.com/samwhitedove
        Linkedin: https://www.linkedin.com/in/archivas/
        Version: 0.0.1
        Date: 21:02:2023

        Class to initialize connection to monnify server.. 
        
        While initializing this class you need to pass some default parameter which value can be uptained from monnify website after completing 
        your account registration.

        PARAMETER:TYPE ===== REQUIRED ===== DEFAULT ============================================== OPTIONS
        contractCode:str,    YES            NONE                                                   NONE
        currencyCode:str,    NO             NGN                                                    CHECK MONNIFY FOR YOUR COUNTRY CURRENCY CODE
        apiKey:str,          YES            NONE                                                   NONE
        secretKey:str,       YES            NONE                                                   NONE
        paymentMethods       NO            ["CARD","ACCOUNT_TRANSFER"]                             ["CARD","ACCOUNT_TRANSFER","USSD","PHONE_NUMBER"]
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

            PARAMETER       REQUIRED        DEFAULT
            start           NO              MFY-PY
        """
        gen_ref_id:str =''.join(random.choices(string.ascii_lowercase, k=5))
        return f"{start if start != '' else self.__startRef}_{gen_ref_id.upper()}-{datetime.datetime.now().timestamp()}"

    def initializeTransaction(self, amount:str, customerName:str, paymentDescription:str, customerEmail:str, successUrl:str, refStart:str="") -> dict:
        """
            Method to initialize a single payment to monnify server.. 
            
            PARAMETER:TYPE ===== REQUIRED ===== DEFAULT 
            amount:str              YES            NONE 
            customerName:str        YES            NONE 
            customerEmail:str       YES            NONE 
            paymentDescription:str  YES            NONE 
            redirectUrl             YES            NONE 
            refStart                NO             MFY_PY 
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
            PARAMETERS          OPTIONAL
            accountName         NO              
            customerEmail       NO
            bvn                 NO
            customerName        NO
            preferredBanks      YES
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

            print(body)
            resp = self.__make_request(url=url, payload=body)
            if resp['statusCode'] == 200:
                return {  "statusCode": resp['statusCode'],  'responseCode': resp['responseCode'], "data": resp['data'] }
            return {"statusCode": resp['statusCode'], "message": resp['message'], 'responseCode': resp['responseCode']}
        raise ValueError("preferredBanks must be a list of bank codes")
    
    def validatePayment(self, refID:str) -> dict:
        url = f"{self.__baseUrl}/api/v2/transactions/{refID}"
        resp = self.__make_request(url=url, method="GET")
        if resp['statusCode'] == 200:
            return {"statusCode": resp['statusCode'], "data": resp['message']}
        return {"statusCode": resp['statusCode'], "data": resp['message']}







# { 
#                     "transactionReference": data['transactionReference'],
#                     "paymentReference": data['paymentReference'],
#                     "merchantName": data['merchantName'],
#                     "enabledPaymentMethod": data['enabledPaymentMethod'],
#                     "checkoutUrl": data['checkoutUrl'],
#                 },