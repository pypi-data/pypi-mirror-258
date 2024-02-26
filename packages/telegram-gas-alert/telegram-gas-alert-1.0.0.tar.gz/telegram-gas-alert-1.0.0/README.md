# Telegram Gas Alert

This app is for making an alert if the gas on etherscan us under 20 gwei 


## How To Use this Repository in your local host
* To use the script you should clone this Repository
* Make sure you already have python 3 installed on your local host
* Create new telegram bot token and filled up this value below on the script
> TELEGRAM_BOT_TOKEN=`bot token from telegram`<br>
> TELEGRAM_CHAT_ID=`chat id from telegram`
* Create new api token on etherscan from your account and filled up this value below on the script
> ETHERSCAN_API_KEY=`api key from etherscan`
* Install python dependencies requirements to your local host
> pip install -r requirements.txt
* Execute this main python script 
> python3 package/main.py
