# Nfc door lock

TODO 
- How to distinguish android from tag

# TOTP example

```
otpauth://TYPE/LABEL?PARAMETERS

type = hotp | totp

label = acoountname | issuer ( ":" | "%3A") * "%20" accountname

pareameter =
    issuer
    secret - Base32 (no padding)

```


# Android key process

```plantuml

@startuml

hnote across: If sense android

Reader -> Android: SELECT AID 
Android -> Reader: 9000
...
Reader -> Android: READ PASS Bad Issuer
Android -> Reader: 6A 83 Not found
...
Reader -> Android: READ PASS Good Issuer
Android -> Reader: LA ACCOUNT LP PASSWORD 90 00

hnote across: If sense tag



@enduml

```