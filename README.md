### MONNIFY PYTHON PACKAGE USER GUIDE
> Version 0.0.6

Before you can start integrating to Monnify, you will need to sign up on Monnify. https://app.monnify.com/create-account to sign up. After successful registration, login and for your credentials.

### CREDENTIAL NEEDED
``` 
1. API KEY
2. SECRET KEY
3. CONTRACT CODE
```
All this can be seen on the setting area when you login to you logged in.

### API ENDPOINT IN THE PACKAGE
```
1 .initializeTransaction
2. validateTransactionStatus
3. reserveBankName
4. deleteReservedAccount
5. addReservedAccount
6. updateCustomerReserveAccountBvn
7. getAllTransactionOnAReserveAccount
8. getASingleCustomerAllReservedAccount
```

### HOW TO USE THE PACKAGE

To use the PACKAGE, you have to use package installer (pip) by running: 
```
pip install py-monnify
```
After successfull installation, you can now use the package in your development environment by importing it in your project

### INITIALIZING PY_MODULE

While initializing this class you need to pass some parameter which value can be uptained from monnify website after completing your account registration.
Some of this parameters have a default value.
```
PARAMETER:TYPE ===== REQUIRED ===== DEFAULT ========================== TYPE =========== OPTIONS
contractCode         YES            NONE                               STRING           NONE
apiKey               YES            NONE                               STRING           NONE
secretKey            YES            NONE                               STRING           NONE
refStart             YES            PYMON_                             STRING           NONE
currencyCode         NO             NGN                                STRING           CHECK MONNIFY FOR YOUR COUNTRY CURRENCY CODE
paymentMethods       NO            ["CARD","ACCOUNT_TRANSFER"]         LIST             ["CARD","ACCOUNT_TRANSFER","USSD","PHONE_NUMBER"]
```

***USAGE***
```
from py_monnify import module as monnify

api_key = "MK_TEST_8UBXGKXXXXXXXX"
secret_key = "ENRC4FDYYYETKA53YPXBFXXXXXXXX"
contractCode = '29176XXXX'

init = monnify.InitializeMonnify(contractCode= contractCode, apiKey= api_key, secretKey= secret_key)
```

NOTE: dont forget to change credentials to live credentials, if you're TESTING with test account.
NOTE: refStart is a parameter that determine the text starting your transaction reference code for custimization you can change it to your preferred code, the default is PYMON_. 
NOTE: currencyCode is the supported monnify currency for every country. please check monnify website to find your country currency code
NOTE: paymentMethods are list of payment method monnify supports, please check monnify website to find out more.

### INITIALIZE A SINGLE TRANSACTION
Method to initialize a single payment to monnify server.
```
PARAMETER =========== REQUIRED ===== DEFAULT  ===== TYPE 
amount                  YES            NONE         STRING
customerName            YES            NONE         STRING
customerEmail           YES            NONE         STRING
paymentDescriptio       YES            NONE         STRING
redirectUrl             YES            NONE         STRING
refStart                NO             MFY_PY       STRING
```

***USAGE***
```
response = init.initializeTransaction(amount="100", customerName="John Doe", paymentDescription="Groceries", customerEmail="john@doe.com", redirectUrl="https://example.com/check-out")

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
{
  "requestSuccessful": true,
  "responseMessage": "success",
  "responseCode": "0",
  "responseBody": {
    "transactionReference": "MNFY|20190915200044|000090",
    "paymentReference": "1568577644707",
    "merchantName": "Test Limited",
    "apiKey": "MK_TEST_VR7J3UAACH",
    "enabledPaymentMethod": [
      "ACCOUNT_TRANSFER",
      "CARD"
    ],
    "checkoutUrl": "https://sandbox.sdk.monnify.com/checkout/MNFY|20190915200044|000090"
  }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

NOTE: The above required parameter are to be passed to the method.
NOTE: redirectUrl is the url where monnify will redirect your user after a successful or a failed transaction process. I will suggest you create a page withing your site or application that will take response payload from monnify after redirecting to your redirect page because while redirecting to this page monnify send a response payload.
NOTE: Always check verify transaction status using ***validateTransactionStatus*** method from monnify before given value to customers.

### VALIDATE TRANSACTION STATUS
Method to all transactions on a single reserved account on monnify server.. 
```
PARAMETER:TYPE ========= REQUIRED ===== DEFAULT  ===== TYPE 
transactionReference       YES            NONE         STRING
```
This is use to verify a payment a payment status on the monnify server 
e.g status for payment
PAID, OVERPAID, PARTIALLY_PAID, PENDING, ABANDONED, CANCELLED, FAILED, REVERSED, EXPIRED

***USAGE***
```
response = init.validateTransactionStatus(transactionReference="XXXXXXXXXXXXXXXXXXXXX")

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
visit for all response https://teamapt.atlassian.net/wiki/spaces/MON/pages/213909851/Get+Transaction+Status
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

### RESERVE BANK ACCOUNT

This method allow you to reserve a dedicated account number for any of your app user e.g if you're running a wallet system.

Its create a virtual account number that can be use to top up your user wallet, its a collection account number for transactons.

These are the available banks for account number reservation.
```
SN   NAME             CODE
1  # Moniepoint       50515
2  # Wema Bank        035
3  # Sterling Bank    232
```

if you did not specify any of the above bank code as a preferred or default bank.. monnify will virtually create account number on the 
three bank per every request for account number creation.
```
NOTE:: Customer Name will be use as the account name
PARAMETERS          REQUIRED       TYPE 
bvn                 YES             STRING
customerName        YES             STRING
customerEmail       YES             STRING
preferredBanks      NO              LIST
```

***USAGE***
```
response = init.reserveBankAccount(customerBVN="2234567XXXX", customerName="John Doe", customerEmail="john@doe.com")

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
{
    "requestSuccessful": true,
    "responseMessage": "success",
    "responseCode": "0",
    "responseBody": {
        "contractCode": "915483727511",
        "accountReference": "121614155748257",
        "accountName": "reservedAccountName",
        "currencyCode": "NGN",
        "customerEmail": "nnaemekapaschal@gmail.com",
        "customerName": "Pascool",
        "accounts": [
            {
                "bankCode": "035",
                "bankName": "bank 1",
                "accountNumber": "0000000033"
            },
            {
                "bankCode": "50515",
                "bankName": "Bank 2",
                "accountNumber": "8000021118"
            }
        ],
        "collectionChannel": "RESERVED_ACCOUNT",
        "reservationReference": "V5R4D9JKC9X9GNJR5QLR",
        "reservedAccountType": "GENERAL",
        "status": "ACTIVE",
        "createdOn": "2021-02-24 09:35:49.161",
        "incomeSplitConfig": [],
        "restrictPaymentSource": false
    }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

NOTE: customerName this parameter value will be use as the account name for the accounts that will be generated.
NOTE: preferredBanks is a optioinal parameter.. you can either pass a single bank code or pass all the list of bank code you want your user to have.

### DELETE A RESERVE ACCOUNT NUMBER

Method to delete a reserved account on monnify server.. 
```
PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
accountReference       YES            NONE         STRING
```

The reference id is the account reference
e.g ACC_REF_SIWSO-167725XXXX.37XXXX

***USAGE***
```
response = init.deleteReserveAccount(accountReference="ACC_REF_SIWSO-167725XXXX.37XXXX")

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
{
    "requestSuccessful": true,
    "responseMessage": "success",
    "responseCode": "0",
    "responseBody": {
        "contractCode": "797854529434",
        "accountReference": "reference12345#",
        "accountName": "Test Reserved Account",
        "currencyCode": "NGN",
        "customerEmail": "test@tester.com",
        "accountNumber": "9900725554",
        "bankName": "Providus Bank",
        "bankCode": "101",
        "reservationReference": "NRF72EMEBCGNN6WUKD35",
        "status": "ACTIVE",
        "createdOn": "2019-08-07 17:05:50.0"
    }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

### ADD A RESERVE ACCOUNT

Method to add a more account to an existing custormers reserved account on monnify server..
e.g 
a customer have a reserve account of sterlin bank and you want the customer to have another reserve account with wema bank etc. 
```
PARAMETER:TYPE ===== REQUIRED ===== DEFAULT ===== TYPE 
accountReference       YES            NONE        LIST
preferredBanksCodes    YES            NONE        STRING
```

The reference id is the account reference
e.g ACC_REF_SIWSO-167725XXXX.37XXXX

***USAGE***
```
response = init.addReservedAccount(accountReference="ACC_REF_SIWSO-167725XXXX.37XXXX", preferredBanksCodes=['XXX', 'XXX'])

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
 {
    "requestSuccessful": true,
    "responseMessage": "success",
    "responseCode": "0",
    "responseBody": {
        "contractCode": "915483727511",
        "accountReference": "121615386005862",
        "accountName": "reservedAccountName",
        "currencyCode": "NGN",
        "customerEmail": "nnaemekapaschal@gmail.com",
        "customerName": "Pascool",
        "accounts": [
            {
                "bankCode": "035",
                "bankName": "WEMA Bank",
                "accountNumber": "XXXX123456"
            },
            {
                "bankCode": "50515",
                "bankName": "Moniepoint",
                "accountNumber": "XXXX123456"
            },
            {
                "bankCode": "123",
                "bankName": "Bank 3",
                "accountNumber": "XXXX123456"
            }
        ],
        "collectionChannel": "RESERVED_ACCOUNT",
        "reservationReference": "8MHKXZS8GCEPVXB59ML6",
        "reservedAccountType": "GENERAL",
        "status": "ACTIVE",
        "createdOn": "2021-03-10 15:20:07.0",
        "restrictPaymentSource": false
    }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

### UPDATE RESERVE ACCOUNT ATTACHED BVN NUMBER

Method to update the bvn attached to a customer reserved account on monnify server.. 
```
PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
accountReference       YES            NONE         STRING
bvn                    YES            NONE         STRING
```

The reference id is the account reference
e.g ACC_REF_SIWSO-167725XXXX.37XXXX

***USAGE***
```
response = init.updateCustomerReserveAccountBvn(accountReference="ACC_REF_SIWSO-167725XXXX.37XXXX", bvn='1234567XXX')

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
{
    "requestSuccessful": true,
    "responseMessage": "success",
    "responseCode": "0",
    "responseBody": {
        "contractCode": "915483727511",
        "accountReference": "121612212051585",
        "currencyCode": "NGN",
        "customerEmail": "testuser@monnify.com",
        "customerName": "Pascool Oj",
        "accountNumber": "4290733572",
        "bankName": "Providus Bank",
        "bankCode": "101",
        "collectionChannel": "RESERVED_ACCOUNT",
        "reservationReference": "R8J4LCW3P82WN4X6LQCW",
        "reservedAccountType": "GENERAL",
        "status": "ACTIVE",
        "createdOn": "2021-02-01 21:40:55.0",
        "bvn": "21212121212",
        "restrictPaymentSource": false
    }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

### GET ALL TRANSACTION OF A RESERVED ACCOUNT
Method to all transactions on a single reserved account on monnify server.. 
```
PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
accountReference       YES            NONE         STRING
page                   NO             0            STRING
size                   NO             10           STRING
```

The reference id is the account reference
e.g ACC_REF_SIWSO-167725XXXX.37XXXX

***USAGE***
```
response = init.getAllTransactionOnAReserveAccount(accountReference="ACC_REF_SIWSO-167725XXXX.37XXXX", bvn='1234567XXX')

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
{
    "requestSuccessful": true,
    "responseMessage": "success",
    "responseCode": "0",
    "responseBody": {
        "content": [
            {
                "customerDTO": {
                    "email": "test@tester.com",
                    "name": "Test Reserved Account",
                    "merchantCode": "ALJKHDALASD"
                },
                "providerAmount": 0.21,
                "paymentMethod": "ACCOUNT_TRANSFER",
                "createdOn": "2019-07-24T14:12:27.000+0000",
                "amount": 100.00,
                "flagged": false,
                "providerCode": "98271",
                "fee": 0.79,
                "currencyCode": "NGN",
                "completedOn": "2019-07-24T14:12:28.000+0000",
                "paymentDescription": "Test Reserved Account",
                "paymentStatus": "PAID",
                "transactionReference": "MNFY|20190724141227|003374",
                "paymentReference": "MNFY|20190724141227|003374",
                "merchantCode": "ALJKHDALASD",
                "merchantName": "Test Limited"
                "payableAmount": 100.00,
                "amountPaid": 100.00,
                "completed": true
            },
            {
                "customerDTO": {
                    "email": "test@tester.com",
                    "name": "Test Reserved Account",
                    "merchantCode": "ALJKHDALASD"
                },
                "providerAmount": 0.11,
                "paymentMethod": "ACCOUNT_TRANSFER",
                "createdOn": "2019-07-24T11:14:45.000+0000",
                "amount": 50.00,
                "flagged": false,
                "providerCode": "98271",
                "fee": 0.79,
                "currencyCode": "NGN",
                "completedOn": "2019-07-24T11:14:45.000+0000",
                "paymentDescription": "Test Reserved Account",
                "paymentStatus": "PAID",
                "transactionReference": "MNFY|20190724111444|003259",
                "paymentReference": "MNFY|20190724111444|003259",
                "merchantCode": "ALJKHDALASD",
                "merchantName": "Test Limited",
                "settleInstantly": true,
                "payableAmount": 50.00,
                "amountPaid": 50.00,
                "completed": true
            }
        ],
        "pageable": {
            "sort": {
                "sorted": true,
                "unsorted": false,
                "empty": false
            },
            "pageSize": 10,
            "pageNumber": 0,
            "offset": 0,
            "unpaged": false,
            "paged": true
        },
        "totalElements": 2,
        "totalPages": 1,
        "last": true,
        "sort": {
            "sorted": true,
            "unsorted": false,
            "empty": false
        },
        "first": true,
        "numberOfElements": 2,
        "size": 10,
        "number": 0,
        "empty": false
    }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```

### GET A SINGLE USER ALL RESERVED ACCOUNT

Method to all transactions on a single reserved account on monnify server.. 
```          
PARAMETER:TYPE ===== REQUIRED ===== DEFAULT  ===== TYPE 
accountReference       YES            NONE         STRING
```
To get the details of a customer's reservation with all account numbers reserved, 
it will return all the details attached to that account Reference.

***USAGE***
```
response = init.getASingleCustomerAllReservedAccount(accountReference="ACC_REF_SIWSO-167725XXXX.37XXXX", bvn='1234567XXX')

do something with the response.
```

***SUCCESS RESPONSE EXAMPLE***
```
{
    "requestSuccessful": true,
    "responseMessage": "success",
    "responseCode": "0",
    "responseBody": {
        "contractCode": "915483727511",
        "accountReference": "1579703193286",
        "accountName": "TEAMAPT-TEAMAPT-res",
        "currencyCode": "NGN",
        "customerEmail": "nnaemekapaschal@gmail.com",
        "customerName": "Monnify dev",
        "accounts": [
            {
                "bankCode": "232",
                "bankName": "bank 1",
                "accountNumber": "0000000033"
            },
            {
                "bankCode": "111",
                "bankName": "Bank 2",
                "accountNumber": "8000021118"
            }
        ],
        "collectionChannel": "RESERVED_ACCOUNT",
        "reservationReference": "KS4CSY7Y9BULTV2BLP8F",
        "reservedAccountType": "GENERAL",
        "status": "ACTIVE",
        "createdOn": "2020-01-22 14:26:34.0",
        "contract": {
            "name": "Default Contract 2",
            "code": "915483727511",
            "description": null
        },
        "transactionCount": 0,
        "bvn": "56787654577",
        "restrictPaymentSource": false
    }
}
```
***ERROR RESPONSE EXAMPLE***
```
{
    'statusCode': XXX, 
    'message': response message, 
    'responseCode': 'XX'
}
```