import argparse
import requests
import time
import os
import sys


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Telegram alert sent successfully.")
        else:
            print("Failed to send Telegram alert.")
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")


def get_env_value(key):
    value = os.environ.get(key, None)
    if not value:
        print(f"ERROR: environment {key} is needed")
        sys.exit(1)
    return value


def get_gas_price(api_key):
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api_key}"
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
    parser = argparse.ArgumentParser(description="Gas price alerting script")
    parser.add_argument("--telegram_bot_token", type=str, help="Telegram bot token")
    parser.add_argument("--telegram_chat_id", type=str, help="Telegram chat ID")
    parser.add_argument("--etherscan_api_key", type=str, help="Etherscan API key")
    parser.add_argument(
        "--alert_threshold", type=int, default=20, help="Gas price threshold in Gwei"
    )
    parser.add_argument(
        "--rate_limit_delay",
        type=int,
        default=10,
        help="Delay in seconds to respect Etherscan API rate limit",
    )

    args = parser.parse_args()

    # Check if any required argument is missing, if so, use environment variables
    if not all(vars(args).values()):
        args.telegram_bot_token = args.telegram_bot_token or get_env_value(
            "TELEGRAM_BOT_TOKEN"
        )
        args.telegram_chat_id = args.telegram_chat_id or get_env_value(
            "TELEGRAM_CHAT_ID"
        )
        args.etherscan_api_key = args.etherscan_api_key or get_env_value(
            "ETHERSCAN_API_KEY"
        )
    # Infinite loop to continuously fetch gas prices
    while True:
        gas_prices = get_gas_price(args.etherscan_api_key)
        if gas_prices:
            fast_gas_price, _, _ = gas_prices
            if fast_gas_price < args.alert_threshold:
                message = f"⚠️ Alert: Gas price is below {args.alert_threshold} Gwei! Current fast gas price: {fast_gas_price} Gwei."
                send_telegram_message(
                    args.telegram_bot_token, args.telegram_chat_id, message
                )
                print(message)
        time.sleep(args.rate_limit_delay)
