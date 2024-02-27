# English to Azerbaijani(Arabic Script) Translator (Arabic Script)

This package provides an easy-to-use interface for translating text from English to Azerbaijani using Arabic script. Built with [PyTorch](https://pytorch.org/), it leverages advanced neural network models for accurate and fast translations.

## Features

- High-quality translation from English to Azerbaijani (Arabic Script).
- Simple and intuitive API.
- Lightweight and fast.

## Installation

Install the package using pip:

    pip install chevir-kartalol==0.1

Requirements
List your package requirements, but typically:

    Python >= 3.9
    Torch >= 2.0.0
    torchtext==0.6.0
    spacy

** 1- Note: You need to update spacy as follows:

    1- download tokenizer that we created for azb from the following link:
        - https://drive.google.com/file/d/1m6nQ13WIBW3pXGaLnLndd-6PYwExvUe8/view?usp=sharing
    
    2- move azb and lex_attrs.py folder into:
        - venv/lib/python3.10/site-packages/spacy/lang/

2- Note: if you have GPU make sure that you have done cuda setting correctly.


### To use the translator, follow these steps:

    from chevir_kartalol.evaluation import Dilmanc

    # Initialize the translator (make sure to adjust parameters as needed)
    translator = Dilmanc()

    # Translate text
    translated_text = translator.chevir("Your English text here")
    print(translated_text)



### License


This project is licensed under the Apache-2.0 License - see the LICENSE file for details.

### Support
For support and queries, raise an issue in the GitHub repository or contact the maintainers directly.