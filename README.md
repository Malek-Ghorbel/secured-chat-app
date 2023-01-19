# secured-chat-app
##  A chat application with end-to-end encryption 
This app was built in **python** using TKinter & based on Sockets and the encryption was made with the **RSA** protocol implemented by the [cryptography](https://cryptography.io/en/latest/) library
## the flow 
when you create a new client by signup or login it generates a public and private RSA keys when it connects to the server they exchange public keys
once it's connected the client can send 2 types of messages :
- to specific person : the client encrypts the message and the receiver with the server public key then the server decrypts it to extract the receiver and encrypt the rest with the receiver's public key and send it
- to everyone : the client encrypts the message with the server public key then the server decrypts it and broadcast it while encrypting it with each client public key before sending
#### before starting you need to run these commands to install necessary packages :
```
pip install --upgrade Pillow
pip install cryptography
```
#### to start you need to run the server first :
```
python server.py
```
#### then run signup.py to create some clients to communicate (or login.py if you have already an account) 
```
python signup.py
```
