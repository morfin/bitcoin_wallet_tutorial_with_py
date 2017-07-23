# Step by Step Bitcoin Wallet Tutorial

Are you a developer trying to figure out how a bitcoin "wallet" is actually generated without getting into all the ins and outs? This guide might help you. 

The guide is based on this excellent webpage:
http://www.mobilefish.com/services/cryptocurrency/cryptocurrency.html
So most of the comments where extrated from that page.

The procedural code demo will introduce you to all the concepts involved in the creation of a bitcoin wallet. If you follow the code step by step in main.py and utils.py, some of your basic questions regarding Private Keys, Public Keys, WIF's, uncompressed/compressed WIF's, etc. will be answered by looking at an actual implemenation.

This guide will assume that you know the basics of the following topics:
* base-2 (binary)
* base-10 (decimal)
* base-16 (hexadecimal)
* base-64
* Asymmetric cryptography A.K.A Public Key Cryptography
* Hashing

In order to follow along, you'll need Python 2.7 and some crypto/bitcoin libraries:

```sh
$ pip install hashlib
$ pip install pybitcointools 
$ pip install pybitcoin
```
Once those libraries are installed, you can just simply run the main.py:
```sh
$ python main.py
```
Disclaimer:
----
The provided code is only intended to show you the basics of a bitcoin wallet creation. Use the code at your own risk.

License
----

MIT
