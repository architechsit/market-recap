# market-recap
Market Recap Script for pulling futures and previous day closings on major indices using Yahoo Finance data

## Create a dedicated folder
### Open Terminal and run:

mkdir ~/market-recap

cd ~/market-recap

## Create a virtual environment

python3 -m venv venv

## Activate the virtual environment

source venv/bin/activate

## Install the required packages

pip install yfinance tabulate colorama

## Download the market_recap.py script and run. 

python market_recap.py
