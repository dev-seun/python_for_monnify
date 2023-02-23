
from initalize_monnify import InitializeMonnifySDKTransaction

initializeSDK = InitializeMonnifySDKTransaction(contractCode="2465911000", apiKey="MK_TEST_FA1LZQ0KRW", secretKey="BY8RLEDX3EEUG1GJEDBHKKR5JGYAL3YF")
# initializeSDK.__str__()
# test = initializeSDK.initializeTransaction(amount= "100", customerName=f'Alade AK', paymentDescription="Wallet Services", customerEmail="email@email.com", successUrl="")
test = initializeSDK.reserveBankName(customerName="AYom", customerEmail="email@email.com", customerBVN="12236726473", preferredCodes="['232']")
print(test)