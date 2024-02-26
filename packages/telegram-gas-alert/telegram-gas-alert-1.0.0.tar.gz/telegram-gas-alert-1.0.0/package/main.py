import requests
import time

TELEGRAM_BOT_TOKEN = "YourTelegramBotToken"  # Replace with your Telegram bot token
TELEGRAM_CHAT_ID = "YourChatID"  # Replace with your chat ID
ETHERSCAN_API_KEY = "YourEtherscanAPIKey"  # Replace with your Etherscan API key
ALERT_THRESHOLD = 20  # Gas price threshold in Gwei
RATE_LIMIT_DELAY = 2  # Delay in seconds to respect Etherscan API rate limit


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Telegram alert sent successfully.")
        else:
            print("Failed to send Telegram alert.")
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")


def get_gas_price():
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "1":
            fast_gas_price = int(data["result"]["FastGasPrice"])
            avg_gas_price = int(data["result"]["ProposeGasPrice"])
            low_gas_price = int(data["result"]["SafeGasPrice"])
            return fast_gas_price, avg_gas_price, low_gas_price
        else:
            print("Error: Unable to fetch gas prices.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    while True:
        gas_prices = get_gas_price()
        if gas_prices:
            fast_gas_price, _, _ = gas_prices
            if fast_gas_price < ALERT_THRESHOLD:
                message = f"⚠️ Alert: Gas price is below {ALERT_THRESHOLD} Gwei! Current fast gas price: {fast_gas_price} Gwei."
                send_telegram_message(message)
                print(message)
        time.sleep(RATE_LIMIT_DELAY)
