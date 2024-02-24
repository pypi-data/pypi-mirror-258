![Logi](https://raw.githubusercontent.com/mr-sami-x/sami_ai/main/logo.png)

# SAMI AI V0.6

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/release)
[![GitHub issues](https://img.shields.io/github/issues/mr-sami-x/sami_ai)](https://github.com/mr-sami-x/sami_ai/issues)
[![GitHub stars](https://img.shields.io/github/stars/mr-sami-x/sami_ai)](https://github.com/mr-sami-x/sami_ai/stargazers)

## Overview

sami_ai is an advanced artificial intelligence library designed to assist with the development of sophisticated and efficient software solutions.

## Features

- Powerful AI capabilities
- Fast and efficient algorithms
- Easy-to-use interface
- The reply settings feature has become available
## Installation

You can install sami-ai using pip:

```
pip install sami-ai==0.6
```

# Example:

## SAMI AI
```
from sami_ai import sami_ai


user_input = input("Enter Your Msg: ")
result = sami_ai(user_input)
print(result["response"])

```

## DEVILS GPT
```
from sami_ai import Devils_GPT


user_input = input("Enter Your Msg: ")
key = input("Enter Your key openai: ")
model = input("Enter Your model openai: ")
result = Devils_GPT(user_input,key,model)
print(result["response"])

```


## WORM GPT
```
from sami_ai import Worm_GPT


user_input = input("Enter Your Msg: ")
key = input("Enter Your key openai: ")
model = input("Enter Your model openai: ")
result = Worm_GPT(user_input,key,model)
print(result["response"])

```