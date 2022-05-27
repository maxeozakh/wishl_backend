# upload

- get JSON from client
- generate key for encrypt content
- encrypt 🤪
- upload encrypted JSON and generate uid at server
- use jwk to convert binary key -> base64
- return uid + base64_key = URL

# download

- sent request with uid and key from client
- 