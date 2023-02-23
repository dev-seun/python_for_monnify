# from django.shortcuts import render
# from rest_framework.views import APIView
# from .initialize_sdk import InitializeMonnifySDKTransaction
# from  backend import data_model_import  as dt_model
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from pay_bill_user import  validator
# # Create your views here.



# initializeSDK = InitializeMonnifySDKTransaction(contractCode="2465911000", apiKey="MK_TEST_FA1LZQ0KRW", secretKey="BY8RLEDX3EEUG1GJEDBHKKR5JGYAL3YF")
# initialize.__str__
# class InitializePayment(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         @validator.decode_token(request)
#         def base_function(user:dt_model.user_model):
#             test = initializeSDK.initializeTransaction(amount=request.data['amount'] , customerName=f'{user.first_name} {user.last_name}', paymentDescription=f"{user.first_name} {user.last_name}, wallet top up for VTUHQ Services", customerEmail=user.email)
#             if test['statusCode'] == 200:
#                 data = {
#                     'requestSuccessful': test['data']['requestSuccessful'],
#                     'responseMessage': test['data']['responseMessage'],
#                     'paymentReference': test['data']['responseBody']['paymentReference'],
#                     'checkoutUrl': test['data']['responseBody']['checkoutUrl']
#                 }
#                 return Response(data={"message": "successful", 'data':data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
#             return Response(data={'message': "Initialization not successful", "data":test, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#         return base_function

# class GetAllReservedBank(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         @validator.decode_token(request)
#         def base_function(user:dt_model.user_model):
#             hasAccount = dt_model.bank_request_record_model.objects.filter(username=user.pk).exists()
#             if hasAccount:
#                 return Response(data={'message': "You have already request for a reserved bank account", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)   
            
#             test = initializeSDK.reserveBankName(customerBVN=request.data['bvn'], customerEmail=user.email, customerName=f'{user.first_name} {user.last_name}')
#             if test['statusCode'] == 200:
#                 bankNames:list = []; accountNumbers:list = []; accountName:list = []
#                 for i in test['data']['responseBody']['accounts']:
#                     bankNames.append(i['bankName'])
#                     accountNumbers.append(i['accountNumber'])
#                     accountName.append(i['accountName'])

#                 user.bank_info.account_name = ",".join(bankNames)
#                 user.bank_info.account_number = ",".join(accountNumbers)
#                 user.bank_info.bank_account_name = ",".join(accountName)
#                 user.bank_info.bvn = request.data['bvn']
#                 user.bank_info.save()
#                 dt_model.bank_request_record_model.objects.create(
#                     username = user,
#                     accountReference = test['data']['responseBody']['accountReference'],
#                     accountName = accountName,
#                     currencyCode = test['data']['responseBody']['currencyCode'],
#                     customerEmail = user.email,
#                     accountNames = accountName,
#                     accountNumbers = accountNumbers,
#                     bankName = bankNames,
#                     customerName = test['data']['responseBody']['customerName'],
#                     collectionChannel = test['data']['responseBody']['collectionChannel'],
#                     reservationReference = test['data']['responseBody']['reservationReference'],
#                     reservedAccountType = test['data']['responseBody']['reservedAccountType'],
#                     status = True if test['data']['requestSuccessful'] == "true" else False,
#                     createdOn =  test['data']['responseBody']['createdOn'],
#                     bvn = request.data['bvn'],
#                     restrictPaymentSource = True if test['data']['responseBody']['restrictPaymentSource'] == "true" else False,
#                 )
#                 resp = {
#                     "status": test['data']['responseBody']['status'],
#                     "currencyCode": test['data']['responseBody']['currencyCode'],
#                     "customerName": test['data']['responseBody']['customerName'],
#                     "accounts": test['data']['responseBody']['accounts'],
#                     "reservedAccountType": test['data']['responseBody']['reservedAccountType'],
#                     "reservationReference": test['data']['responseBody']['reservationReference'],
#                     "accountReference": test['data']['responseBody']['accountReference'],
#                     "restrictPaymentSource": test['data']['responseBody']['restrictPaymentSource'],
#                     "createdOn": test['data']['responseBody']['createdOn'],
#                 }
#                 return Response(data={"message": "successful generate banks", 'data': resp, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
#             return Response(data={'message': "generating banks not successful", "data":test, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#         return base_function

# class ValidatePayment(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         @validator.decode_token(request)
#         def base_function(user:dt_model.user_model):
#             test = initializeSDK.validatePayment(refID= request.data['ref'])
#             if test['statusCode'] == 200:
#                 data= {
#                     "requestSuccessful": test['data']['requestSuccessful'],
#                     "responseMessage": test['data']['responseMessage'],
#                     "amountPaid": test['data']['responseBody']['amountPaid'],
#                     "paymentStatus": test['data']['responseBody']['paymentStatus'],
#                     "paymentMethod": test['data']['responseBody']['paymentMethod'],
#                     "email": test['data']['responseBody']['customer']['email'],
#                     "name": test['data']['responseBody']['customer']['name'],
#                 }
#                 return Response(data={"message": "successful", 'data':data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
#             return Response(data={'message': "Payment not successful, Try again", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#         return base_function


# #         {
# #     "message": "successful",
# #     "data": {
# #         "statusCode": 200,
# #         "data": {
# #             "requestSuccessful": true,
# #             "responseMessage": "success",
# #             "responseCode": "0",
# #             "responseBody": {
# #                 "transactionReference": "MNFY|33|20230219120630|000034",
# #                 "paymentReference": "VTUHG_DBKPP-1676804789.686509",
# #                 "amountPaid": "0.00",
# #                 "totalPayable": "0.00",
# #                 "settlementAmount": null,
# #                 "paidOn": "19/02/2023 12:40:42 PM",
# #                 "paymentStatus": "EXPIRED",
# #                 "paymentDescription": "Wallet TopUp",
# #                 "currency": "NGN",
# #                 "paymentMethod": "ACCOUNT_TRANSFER",
# #                 "product": {
# #                     "type": "WEB_SDK",
# #                     "reference": "VTUHG_DBKPP-1676804789.686509"
# #                 },
# #                 "cardDetails": null,
# #                 "accountDetails": null,
# #                 "accountPayments": [],
# #                 "customer": {
# #                     "email": "smart123@gmail.com",
# #                     "name": "Seun Samuel"
# #                 },
# #                 "metaData": {}
# #             }
# #         }
# #     },
# #     "status": 200
# # }



# #     "message": "successful fetch banks",
# #     "data": {
# #         "statusCode": 200,
# #         "data": {
# #             "requestSuccessful": true,
# #             "responseMessage": "success",
# #             "responseCode": "0",
# #             "responseBody": {
# #                 "contractCode": "2465911000",
# #                 "accountReference": "ACREF_ITKAD-1676743598.799265",
# #                 "accountName": "Seu",
# #                 "currencyCode": "NGN",
# #                 "customerEmail": "smart123@gmail.com",
# #                 "customerName": "Seun Samuel",
# #                 "accounts": [
# #                     {
# #                         "bankCode": "035",
# #                         "bankName": "Wema bank",
# #                         "accountNumber": "5000462145",
# #                         "accountName": "Seu"
# #                     },
# #                     {
# #                         "bankCode": "232",
# #                         "bankName": "Sterling bank",
# #                         "accountNumber": "6001356570",
# #                         "accountName": "Seu"
# #                     }
# #                 ],
# #                 "collectionChannel": "RESERVED_ACCOUNT",
# #                 "reservationReference": "S675N6A2WXRSJ7QAUS1V",
# #                 "reservedAccountType": "GENERAL",
# #                 "status": "ACTIVE",
# #                 "createdOn": "2023-02-18 19:06:43.839",
# #                 "incomeSplitConfig": [],
# #                 "bvn": "21212121212",
# #                 "restrictPaymentSource": false
# #             }
# #         }
# #     },
# #     "status": 200
# # }