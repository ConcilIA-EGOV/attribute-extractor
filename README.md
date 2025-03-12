# Attribute Extractor API Caller



## Overview

The repository aims to run a series of prompts on OpenAI models to extract information from legal judgments in the Portuguese language.

## Installation

To install dependencies run the following:

``
pip install -r requirements.txt
``

Put the OpenAI API token in the `.env` file in the root folder:


``
OPENAI_API_KEY=00000000000
``

## Usage

To run the diferents funcionalities of project, run:

``
make
``
It will show all the diferent running option

## Data


### Sentences

The raw `txt` files should be placed in this directory `data/sentencas`

### Prompts

The prompts files should be placed in this directory `data/prompts`

### Resultados

The outputs generated for each prompt will be automatically saved here.

### api.py

API calls to the OpenAI API

### file_operations.py

Overview of the I/O operations on files provided by `file_operations.py`.

## Acknowledgments

Give credit to individuals or projects that inspired or contributed to your project.

## Source Code

