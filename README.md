# secured-chat-app
##  A chat application with end-to-end encryption 
This app was built in **python** and the encryption was made with the **RSA** protocol implemented by the [cryptography](https://cryptography.io/en/latest/) library: the server and the clients each have a pair of keys: public one for encryption which is available and private one for decryption which is personal
###### before starting you need to run these commands to install necessary packages :
```
pip install --upgrade Pillow
pip install cryptography
```
###### to start you need to run the server first :
```
python server.py
```
###### then run signup.py to create some clients to communicate (or login.py if you have already an account) 
```
python signup.py
```
