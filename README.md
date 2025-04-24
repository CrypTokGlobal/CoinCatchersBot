
# 🪙 CoinCatchersBot – Private Telegram Sniper Bot for Solana

## 🚀 Project Goal
CoinCatchersBot is a private admin-only Telegram bot built for Solana token sniping. It scans newly launched Solana contract addresses and filters them based on social media presence and wallet holder distribution (a.k.a. "bubble map") to reduce risk and automatically execute buys.

## 🔐 Key Features
- ✅ Auto-snipes Solana tokens passing custom filter checks
- 🔐 Admin-only Telegram command interface
- 🧠 Filters for verified socials: Telegram, Website, X/Twitter
- 🌀 Detects clean bubble map (not whale-dominated)
- 🧪 Manual contract scanning: `/scan [contract_address]`
- 🛠️ Admin dashboard (future): add/remove/pause admins
- 📈 Logging of all buys and scans
- 🔁 Full bot control: `/autobuy_on`, `/autobuy_off`, `/status`

## 🛠 Stack
- **Language:** Python 3
- **Telegram Interface:** `python-telegram-bot`
- **Solana Integration:** `solana-py`, `requests`, `base58`, `asyncio`
- **Hosting:** Replit (always-on, serverless)
- **Security:** Hardcoded or config-based admin whitelist

## 🧩 Planned Features
- UI dashboard for admin control
- Telegram notifications on buys
- Graph analysis for bubble maps
- Phantom or CLI wallet integration

## 🔒 Access
Only approved Telegram usernames can interact with the bot. Currently only @shilling_queen has access.
# CoinCatchersBot - Solana Token Sniper

A Telegram bot for automatically finding and purchasing new Solana tokens based on configurable criteria.

## Features

- 🔍 **Multi-Source Scanning**: Monitors new token launches from Birdeye, DexScreener, and Pump.fun
- 🔄 **Auto-Buy**: Automatically purchases tokens that meet your filter criteria
- 🛡️ **Quality Filters**: Filter tokens by required website, Telegram, Twitter presence
- 💰 **Wallet Management**: Built-in Solana wallet generation and management
- 🔑 **Export & Import**: Export keys for use in Phantom wallet
- ⚙️ **Advanced Settings**: Customize slippage, MEV protection, priority fees, and more

## Setup

1. Create a Telegram bot using BotFather and get your bot token
2. Configure the following environment variables in Replit Secrets:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `SOLANA_RPC_URL`: Solana RPC endpoint
   - `BIRDEYE_API_KEY`: API key for Birdeye (optional)
   
3. Run the bot with: `python main.py`
4. Admin users are configured in `config.py` or `chat_ids.json`

## Commands

Use `/help` in the bot to see all available commands.

## Deployment

This bot is designed to run continuously. Use Replit's "Always On" feature to keep it running.

## Security

- Never share your private keys or wallet secret
- Be cautious with the amount of SOL you add to your bot wallet
- Only add admins you trust to the configuration

## Disclaimer

Trading cryptocurrencies involves risk. This bot is provided for educational purposes only.
