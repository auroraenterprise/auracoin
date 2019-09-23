# Auracoin Node API
Every Auracoin node has an API built-in to allow for the network of nodes to
communicate. This API is used by wallets, applications and other nodes so that
the Auracoin network works like clockwork!

API commands are written after the IP address, so for example if you wanted to
execute the `/getBlockHeight` command on an Auracoin miner instance connected at
`127.0.0.1`, you would use:

```
http://127.0.0.1/getBlockHeight
```

This would give you a return message similar to the following:

```
Status/ok/10000
```

Arguments are written as URI argument queries, so for example if you wanted to
execute the `/getBlockchain` command with the parameters `cutoff` as `2` and
`address` as `B4Dfxfp8Ye` on an Auracoin miner instance connected at
`127.0.0.1`, you would use:

```
http://127.0.0.1/getBlockchain?cutoff=2&address=B4Dfxfp8Ye
```

This would give you a return message similar to the following:

```json
{"blocks": [{"data": [{"body": {"certificate": "000000000012ce3d4f9c137d337d5c07972ac99caa3ecc08aff96d876d702d9e31ae8a37e27dd9498591bd3d9ce62f71cc7164c6f51059395c89c8703a7fb9826348b0ee1eB4Dfxfp8Ye1000000009222528413476485610", "receiver": "B4Dfxfp8Ye", "amount": 100000000, "signature": "d0089ccb3962ad0cc99232a6df43ab75b25866d98a4c9ddb8487ea36b359fb6e505945fd10893af398d07260b48aa7dddde1c5c0942a0c76cade00b699d080e6", "senderPublicKey": "12ce3d4f9c137d337d5c07972ac99caa3ecc08aff96d876d702d9e31ae8a37e27dd9498591bd3d9ce62f71cc7164c6f51059395c89c8703a7fb9826348b0ee1e", "sender": "0000000000", "nonce": 9222528413476485610}, "type": "transaction"}], "hash": "000006d4749aea3940e6b0ad5e7d99c9f82e30c8d90669eb98aad1e99c5e9893", "timestamp": 1569167560.858298, "difficulty": 0.25, "previousHash": "0000025195a1c0f530bf65b88a2ff4f7b836744dce25693972379a4e2a8b9c0a", "nonce": 512559}, {"data": [{"body": {"certificate": "000000000012ce3d4f9c137d337d5c07972ac99caa3ecc08aff96d876d702d9e31ae8a37e27dd9498591bd3d9ce62f71cc7164c6f51059395c89c8703a7fb9826348b0ee1eB4Dfxfp8Ye10000000017965350742336070646", "receiver": "B4Dfxfp8Ye", "amount": 100000000, "signature": "a39492e5a208133aa6f2053098957e0da37c206d0b0ae6ef66c129383d5961d3a47aeedeb37e34251658232038e73f2bce6927d039672929ef1175b409466953", "senderPublicKey": "12ce3d4f9c137d337d5c07972ac99caa3ecc08aff96d876d702d9e31ae8a37e27dd9498591bd3d9ce62f71cc7164c6f51059395c89c8703a7fb9826348b0ee1e", "sender": "0000000000", "nonce": 17965350742336070646}, "type": "transaction"}], "hash": "00000889279687fb27b5aca60252989bef0a42921f1a94db41fd92032310165f", "timestamp": 1569167573.588723, "difficulty": 0.25, "previousHash": "000006d4749aea3940e6b0ad5e7d99c9f82e30c8d90669eb98aad1e99c5e9893", "nonce": 334410}], "difficulty": 0.25, "verifiedAmounts": {"B4Dfxfp8Ye": 69800000000}}
```

## Commands
| Command                            | Parameters                                                                                                                                       | Description                                                                                                                                                                                         |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                                |                                                                                                                                                  | Get the general information about the miner, such as the version number and the reward address.                                                                                                     |
| `/getBlockchain`                   | `cutoff`: number (optional), `address`: address (optional)                                                                                       | Get the current blockchain and associated data, including the balances of addresses. This blockchain does not include not yet verified blocks.                                                      |
| `/getBlockHeight`                  |                                                                                                                                                  | Get the current block height.                                                                                                                                                                       |
| `/handleData`                      | `data`: string                                                                                                                                   | Store specified data on the blockchain as type `data`.                                                                                                                                              |
| `/handleTransaction`               | `sender`: address, `senderPublicKey`: string, `receiver`: address, `amount`: number, `certificate`: string, `signature`: string, `nonce`: number | Store transaction on the blockchain as type `transaction`. Transaction must be valid or otherwise it would be rejected.                                                                             |
| `/getAddressPublicKey`             | `address`: address                                                                                                                               | Get the public key of an address.                                                                                                                                                                   |
| `/getAddressBalance`               | `address`: address                                                                                                                               | Get the current balance of an address, including added or removed amounts that are not yet verified. To get verified amounts, use  `/getBlockchain`.                                                |
| `/handleRegistration`              |                                                                                                                                                  | Create a new address and get the registration details. This only works reliably for one miner, so it is reccommended for you to generate a keypair and then use `/handleRegistrationFromPublicKey`. |
| `/handleRegistrationFromPublicKey` | `publicKey`: string                                                                                                                              | Create a new address from an existing public key and get the registration details.                                                                                                                  |