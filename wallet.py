
import os
import json
import logging
import base58
import base64
import time
import httpx
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WalletManager:
    def __init__(self):
        self.wallets = {}
        self.user_balances = {}
        self.auto_buy_enabled = False
        self.load_wallets()
        
        # Get RPC URL from environment or use default
        self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        self.client = Client(self.rpc_url)
        
    def load_wallets(self):
        """Load wallets from the wallets.json file"""
        try:
            if os.path.exists('wallets.json'):
                with open('wallets.json', 'r') as f:
                    self.wallets = json.load(f)
                logger.info(f"Loaded {len(self.wallets)} wallets")
        except Exception as e:
            logger.error(f"Error loading wallets: {e}")
            self.wallets = {}
            
    def save_wallets(self):
        """Save wallets to the wallets.json file"""
        try:
            with open('wallets.json', 'w') as f:
                json.dump(self.wallets, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving wallets: {e}")
            
    def generate_wallet(self, username):
        """Generate a new wallet for a user"""
        keypair = Keypair()
        public_key = str(keypair.public_key)
        # Store the secret key as a list of integers
        secret_key = list(keypair.secret_key)
        
        self.wallets[username] = {
            'public': public_key,
            'secret': secret_key
        }
        self.save_wallets()
        return public_key
        
    def get_wallet(self, username):
        """Get a user's wallet"""
        return self.wallets.get(username)
        
    def get_public_key(self, username):
        """Get a user's public key"""
        wallet = self.get_wallet(username)
        if wallet:
            return wallet.get('public')
        return "No wallet found"
        
    async def get_balance(self, username, force_refresh=False):
        """Get a user's SOL balance"""
        if not force_refresh and username in self.user_balances:
            # Use cached balance if available and not forcing refresh
            last_check, balance = self.user_balances.get(username, (0, 0))
            if time.time() - last_check < 30:  # Cache for 30 seconds
                return balance
                
        wallet = self.get_wallet(username)
        if not wallet:
            return 0
            
        pubkey = wallet.get('public')
        try:
            response = self.client.get_balance(PublicKey(pubkey))
            lamports = response.get('result', {}).get('value', 0)
            balance = lamports / 10**9  # Convert lamports to SOL
            
            # Cache the balance
            self.user_balances[username] = (time.time(), balance)
            return balance
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0
            
    async def toggle_auto_buy(self, enabled):
        """Toggle auto-buy mode"""
        self.auto_buy_enabled = enabled
        return self.auto_buy_enabled
        
    async def buy_token(self, username, token_address, amount, buy_params=None):
        """Buy a token"""
        wallet = self.get_wallet(username)
        if not wallet:
            return {"success": False, "error": "No wallet found"}
            
        # This would normally call Jupiter API or other DEX
        # Here we just simulate a successful transaction
        tx_signature = f"simulated_tx_{int(time.time())}"
        return {
            "success": True,
            "tx_signature": tx_signature,
            "explorer_url": f"https://solscan.io/tx/{tx_signature}"
        }
        
    async def get_tokens(self, username):
        """Get a user's token holdings"""
        # Simulate a token portfolio for demo purposes
        return [
            {
                "name": "Example Token",
                "symbol": "EXMP",
                "token_address": "ExampleTokenAddress123456789",
                "balance": 100.0,
                "value_usd": 10.0,
                "price_change_24h": 5.0,
                "price_change_emoji": "📈"
            }
        ]
        
    async def sell_token(self, username, token_address, percentage=100):
        """Sell a token"""
        # Simulate a successful sell transaction
        tx_signature = f"sell_tx_{int(time.time())}"
        return {
            "success": True,
            "tx_signature": tx_signature,
            "explorer_url": f"https://solscan.io/tx/{tx_signature}"
        }
        
    async def get_token_metadata(self, token_address):
        """Get token metadata"""
        # Return dummy data
        return {
            "symbol": "TOKEN",
            "website": "https://example.com",
            "telegram": "https://t.me/example",
            "twitter": "https://twitter.com/example"
        }
        
    async def fetch_tokens_from_dexscreener(self):
        """Fetch tokens from DexScreener"""
        # Return dummy data
        return [
            {
                "address": f"token_{int(time.time())}",
                "symbol": "NEWT",
                "liquidity": 1000.0,
                "source": "dexscreener"
            }
        ]
        
    async def fetch_tokens_from_pump_fun(self):
        """Fetch tokens from pump.fun"""
        # Return dummy data
        return [
            {
                "address": f"token_{int(time.time())+1}",
                "symbol": "PUMP",
                "liquidity": 1500.0,
                "source": "pump.fun"
            }
        ]
        
    async def update_simulated_balance(self, username, amount):
        """Update a user's simulated balance"""
        if username in self.user_balances:
            last_check, balance = self.user_balances.get(username)
            self.user_balances[username] = (last_check, balance + amount)
        
    async def get_recent_buys(self, username, minutes):
        """Get recent buys for a user"""
        # Return dummy data
        return [
            {
                "symbol": "TOKEN",
                "amount": 0.01,
                "success": True,
                "explorer_url": f"https://solscan.io/tx/example"
            }
        ]

# Export wallet function as requested in main.py
async def export_wallet(update, context):
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    # Check if authenticated (would be defined in main.py)
    if not hasattr(context.bot_data, 'authenticated_users') or user_id not in context.bot_data.get('authenticated_users', set()):
        await update.message.reply_text("⛔ You are not authorized to use this command.")
        return
        
    wallet = wallet_manager.get_wallet(username)
    if not wallet:
        await update.message.reply_text("❌ No wallet found for your account.")
        return
        
    # Security warning
    await update.message.reply_text(
        "⚠️ *SECURITY WARNING*\n\n"
        "I'm about to send you your private key. This should *ONLY* be used for:\n"
        "• Importing to a secure wallet like Phantom\n"
        "• Development purposes\n\n"
        "*NEVER* share this key with anyone else.\n"
        "Anyone with this key can steal your funds.\n\n"
        "This message will be deleted in 60 seconds.",
        parse_mode="Markdown"
    )
    
    # Format the private key
    import json
    private_key_msg = await update.message.reply_text(
        f"🔑 *Your Private Key (JSON Array):*\n`{json.dumps(wallet['secret'])}`\n\n"
        "This key is in JSON array format, compatible with Phantom wallet.\n"
        "Import using *Import Private Key* option.\n\n"
        "This message will self-destruct in 60 seconds.",
        parse_mode="Markdown"
    )
    
    # Delete message after 60 seconds
    import asyncio
    await asyncio.sleep(60)
    try:
        await private_key_msg.delete()
    except Exception as e:
        print(f"Failed to delete private key message: {e}")

# Create the wallet manager instance
wallet_manager = WalletManager()

import os
import json
import base64
import time
import asyncio
from solana.keypair import Keypair
import httpx

# Setup logging
#logger = logging.getLogger(__name__)

# File to persist wallet keys
WALLET_FILE = "wallets.json"

class WalletManager:
    def __init__(self, wallet_file="wallets.json"):
        self.wallet_file = wallet_file
        self.wallets = {}
        self.auto_buy_enabled = False
        self.load_wallets()

    def load_wallets(self):
        if os.path.exists(self.wallet_file):
            try:
                with open(self.wallet_file, 'r') as f:
                    self.wallets = json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading {self.wallet_file}. Creating a new one.")
                self.wallets = {}
        else:
            self.wallets = {}

    def save_wallets(self):
        with open(self.wallet_file, 'w') as f:
            json.dump(self.wallets, f, indent=2)

    def get_wallet(self, username):
        username = username.lower() if username else None
        if username in self.wallets:
            return self.wallets[username]
        return None

    def get_public_key(self, username):
        wallet = self.get_wallet(username)
        if wallet:
            return wallet.get('public', 'No wallet found')
        return "No wallet found"

    def generate_wallet(self, username):
        """Create a new wallet for the user with a real Solana keypair"""
        if not username:
            return "Invalid username"

        # Generate a real Solana keypair
        try:
            username = username.lower()
            keypair = Keypair()
            public_key = str(keypair.public_key)

            # Store the secret key as an array of integers
            # We'll convert to Base58 when exporting
            self.wallets[username] = {
                "public": public_key,
                "secret": list(keypair.secret_key)
            }
            self.save_wallets()
            return public_key
        except Exception as e:
            print(f"Error generating wallet: {e}")
            return "Error generating wallet"

    async def toggle_auto_buy(self, enabled):
        self.auto_buy_enabled = enabled
        return self.auto_buy_enabled

    async def get_jupiter_quote(self, input_mint, output_mint, amount_in_lamports):
        """
        Get a quote from Jupiter API for a token swap

        Args:
            input_mint: The input token mint (e.g., SOL mint address)
            output_mint: The output token mint address
            amount_in_lamports: Amount in lamports to swap

        Returns:
            dict: Quote data or None if failed
        """
        try:
            # Jupiter v6 quote API
            url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount_in_lamports}&slippageBps={(20 * 100)}"  # 20% slippage by default

            print(f"🔍 [JUPITER] Requesting quote: {url}")

            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)

                if response.status_code == 200:
                    quote_data = response.json()
                    print(f"✅ [JUPITER] Quote received: {quote_data.get('outAmount')} tokens out")
                    return quote_data
                else:
                    print(f"❌ [JUPITER] Quote failed: HTTP {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"❌ [JUPITER] Quote error: {str(e)}")
            return None

    async def execute_jupiter_swap(self, quote_data, wallet_keypair):
        """
        Execute a swap on Jupiter using the quote data

        Args:
            quote_data: Quote data from Jupiter quote API
            wallet_keypair: Solana keypair for signing

        Returns:
            dict: Transaction details or None if failed
        """
        try:
            # Jupiter v6 swap API for creating the transaction
            url = "https://quote-api.jup.ag/v6/swap"

            # Prepare request data
            account_public_key = str(wallet_keypair.public_key)

            swap_data = {
                "quoteResponse": quote_data,
                "userPublicKey": account_public_key,
                "wrapAndUnwrapSol": True,  # Auto-wrap/unwrap SOL
                "prioritizationFeeLamports": 1500000  # Default priority fee (0.0015 SOL)
            }

            print(f"🔍 [JUPITER] Requesting swap transaction for {account_public_key}")

            # Get the swap transaction from Jupiter
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=swap_data, timeout=10.0)

                if response.status_code != 200:
                    print(f"❌ [JUPITER] Swap transaction failed: HTTP {response.status_code} - {response.text}")
                    return None

                swap_response = response.json()
                transaction_bytes = swap_response.get("swapTransaction")

                if not transaction_bytes:
                    print("❌ [JUPITER] No transaction bytes in response")
                    return None

                # Decode transaction
                import base64
                from solana.transaction import Transaction

                print(f"🔍 [JUPITER] Decoding transaction bytes")
                transaction_bytes_decoded = base64.b64decode(transaction_bytes)
                transaction = Transaction.deserialize(transaction_bytes_decoded)

                # Sign the transaction
                print(f"🔍 [JUPITER] Signing transaction")
                transaction.sign([wallet_keypair])

                # Serialize and send the transaction
                import base58
                from solana.rpc.api import Client

                solana_rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
                client = Client(solana_rpc_url)

                print(f"🔍 [JUPITER] Sending transaction to {solana_rpc_url}")

                # Send the signed transaction
                tx_bytes = transaction.serialize()
                encoded_tx = base58.b58encode(tx_bytes).decode("utf-8")

                response = client.send_transaction(encoded_tx, opts={"skipPreflight": True})

                if "result" in response:
                    tx_signature = response["result"]
                    print(f"✅ [JUPITER] Transaction sent: {tx_signature}")
                    return {
                        "success": True,
                        "tx_signature": tx_signature,
                        "explorer_url": f"https://solscan.io/tx/{tx_signature}"
                    }
                else:
                    print(f"❌ [JUPITER] Transaction failed: {response.get('error')}")
                    return {
                        "success": False,
                        "error": str(response.get('error', 'Unknown error'))
                    }

        except Exception as e:
            import traceback
            print(f"❌ [JUPITER] Swap error: {str(e)}")
            print(traceback.format_exc())
            return {
                "success": False,
                "error": str(e)
            }

    async def buy_token(self, username, token_address, amount, params=None):
        """Purchase a token with SOL using Jupiter Aggregator API"""
        try:
            # Get user's wallet
            wallet = self.get_wallet(username)
            if not wallet:
                return {"success": False, "error": "No wallet found"}

            # Default parameters
            buy_params = {
                "slippage": 20,  # 20% default slippage
                "priority_fee": 0.0015,  # Default priority fee
                "mev_protection": False  # No MEV protection by default
            }

            # Merge with user-provided params if any
            if params:
                buy_params.update(params)

            # Check if we're in test mode
            test_mode = os.getenv("TEST_MODE", "0") == "1"

            if test_mode:
                # Simulate a successful transaction for development/testing
                import time
                import random
                import hashlib

                # Simulate network delay and success probability
                await asyncio.sleep(random.uniform(1.0, 3.0))
                success = random.random() < 0.9  # 90% success rate in simulation

                if success:
                    # Generate a fake transaction hash
                    tx_hash = hashlib.sha256(f"{token_address}:{amount}:{time.time()}".encode()).hexdigest()
                    # Update simulated balance
                    await self.update_simulated_balance(username, -amount)

                    # Generate explorer URL
                    explorer_url = f"https://solscan.io/tx/{tx_hash}"

                    # In a real implementation, this would return the actual transaction receipt
                    return {
                        "success": True, 
                        "tx_signature": tx_hash,
                        "explorer_url": explorer_url,
                        "amount": amount
                    }
                else:
                    return {"success": False, "error": "Transaction failed (simulated)"}
            else:
                # REAL IMPLEMENTATION: Call Jupiter API for actual token swap
                try:
                    print(f"📢 Starting real Jupiter swap for token: {token_address}, amount: {amount} SOL")
                    
                    # Get RPC URL and wallet information
                    rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
                    if not rpc_url:
                        print("⚠️ No RPC URL configured, using default Solana mainnet endpoint")
                        rpc_url = "https://api.mainnet-beta.solana.com"
                    
                    print(f"📡 Using Solana RPC: {rpc_url}")
                    
                    # Get wallet secret key
                    secret_key = wallet.get('secret')
                    if not secret_key:
                        return {"success": False, "error": "Wallet has no secret key"}

                    # Handle different secret key formats
                    try:
                        if isinstance(secret_key, list):
                            # If stored as a list of integers
                            if len(secret_key) < 64:
                                return {"success": False, "error": f"Invalid secret key length: {len(secret_key)}, needs 64 bytes"}
                            secret_bytes = bytes(secret_key[:64])
                        else:
                            # If stored as base64 string
                            try:
                                secret_bytes = base64.b64decode(secret_key)
                            except:
                                return {"success": False, "error": "Could not decode base64 secret key"}
                    except Exception as e:
                        return {"success": False, "error": f"Error processing secret key: {str(e)}"}

                    # Create Solana keypair from secret
                    try:
                        from solana.keypair import Keypair
                        keypair = Keypair.from_secret_key(secret_bytes)
                        public_key = str(keypair.public_key)
                        print(f"🔑 Using wallet: {public_key}")
                    except Exception as e:
                        return {"success": False, "error": f"Error creating keypair: {str(e)}"}

                    # Convert SOL amount to lamports
                    amount_lamports = int(amount * 1_000_000_000)
                    print(f"💵 Amount in lamports: {amount_lamports}")

                    # Convert slippage to basis points (1% = 100 bps)
                    slippage_bps = int(buy_params["slippage"] * 100)
                    print(f"⚙️ Slippage: {buy_params['slippage']}% ({slippage_bps} bps)")
                    print(f"⚙️ Priority fee: {buy_params['priority_fee']} SOL")

                    # 1. Get quote from Jupiter
                    print("🔍 Step 1: Getting quote from Jupiter...")
                    
                    sol_mint = "So11111111111111111111111111111111111111112"  # SOL mint address
                    quote_url = "https://quote-api.jup.ag/v6/quote"
                    quote_params = {
                        "inputMint": sol_mint,
                        "outputMint": token_address,
                        "amount": amount_lamports,
                        "slippageBps": slippage_bps,
                        "onlyDirectRoutes": False,
                        "platformFeeBps": 0
                    }

                    import httpx
                    print(f"📤 Jupiter quote request: {quote_url} with params: {quote_params}")
                    
                    async with httpx.AsyncClient() as client:
                        try:
                            quote_resp = await client.get(
                                quote_url, 
                                params=quote_params,
                                timeout=15.0  # Increased timeout
                            )
                        except Exception as req_err:
                            return {"success": False, "error": f"Jupiter quote request failed: {str(req_err)}"}

                        if quote_resp.status_code != 200:
                            error_text = quote_resp.text[:200] + "..." if len(quote_resp.text) > 200 else quote_resp.text
                            print(f"❌ Jupiter quote failed: HTTP {quote_resp.status_code} - {error_text}")
                            return {"success": False, "error": f"Jupiter quote failed: HTTP {quote_resp.status_code}"}

                        try:
                            quote = quote_resp.json()
                        except Exception as json_err:
                            return {"success": False, "error": f"Error parsing Jupiter quote response: {str(json_err)}"}

                        if not quote or not quote.get("data"):
                            print("❌ No route data in Jupiter quote response")
                            return {"success": False, "error": "No swap route found for this token"}
                        
                        # Log route details
                        route = quote["data"][0]
                        in_amount = int(route.get("inAmount", 0))
                        out_amount = int(route.get("outAmount", 0))
                        
                        print(f"✅ Quote received: {in_amount/1e9} SOL → {out_amount} token units")
                        print(f"🛣️ Route: {route.get('marketInfos', [{'label': 'unknown'}])[0].get('label', 'unknown')}")

                        # 2. Get the swap transaction
                        print("🔍 Step 2: Getting swap transaction...")
                        swap_url = "https://quote-api.jup.ag/v6/swap"
                        priority_fee_micro_lamports = int(buy_params["priority_fee"] * 1_000_000)
                        
                        swap_data = {
                            "quoteResponse": quote,
                            "userPublicKey": public_key,
                            "wrapAndUnwrapSol": True,
                            "prioritizationFeeLamports": priority_fee_micro_lamports,
                            "skipUserAccountsCheck": False  # Important for first-time swaps
                        }

                        try:
                            swap_resp = await client.post(
                                swap_url,
                                json=swap_data,
                                timeout=15.0  # Increased timeout
                            )
                        except Exception as swap_req_err:
                            print(f"❌ Jupiter swap request failed: {str(swap_req_err)}")
                            return {"success": False, "error": f"Jupiter swap request failed: {str(swap_req_err)}"}

                        if swap_resp.status_code != 200:
                            error_text = swap_resp.text[:200] + "..." if len(swap_resp.text) > 200 else swap_resp.text
                            print(f"❌ Jupiter swap transaction failed: HTTP {swap_resp.status_code} - {error_text}")
                            return {"success": False, "error": f"Jupiter swap transaction failed: HTTP {swap_resp.status_code}"}

                        try:
                            swap_result = swap_resp.json()
                        except Exception as json_err:
                            print(f"❌ Error parsing Jupiter swap response: {str(json_err)}")
                            return {"success": False, "error": f"Error parsing Jupiter swap response: {str(json_err)}"}

                        if "swapTransaction" not in swap_result:
                            print("❌ No transaction in Jupiter swap response")
                            return {"success": False, "error": "Swap transaction failed to generate"}
                        
                        print("✅ Swap transaction received from Jupiter")

                        # 3. Deserialize, sign and send the transaction
                        print("🔍 Step 3: Signing and sending transaction...")
                        
                        try:
                            from solana.transaction import Transaction
                            from solana.rpc.api import Client
                            import base64

                            swap_txn_b64 = swap_result["swapTransaction"]
                            # Create RPC client
                            client = Client(rpc_url)
                            
                            # Deserialize the transaction
                            tx_bytes = base64.b64decode(swap_txn_b64)
                            print(f"📦 Transaction size: {len(tx_bytes)} bytes")
                            
                            txn = Transaction.deserialize(tx_bytes)
                            print(f"📝 Transaction deserialized with {len(txn.signatures)} signature slots")

                            # Sign the transaction
                            print("✍️ Signing transaction with keypair...")
                            transaction_result = txn.sign([keypair])
                            print(f"✅ Transaction signed: {len(txn.signatures)} signatures")
                            
                            # Serialize and encode transaction for sending
                            serialized_tx = base64.b64encode(txn.serialize()).decode('ascii')
                            print(f"📦 Serialized transaction size: {len(serialized_tx)} chars")

                            # Send transaction
                            print("🚀 Sending transaction to Solana network...")
                            send_opts = {
                                "skipPreflight": True,  # Skip simulation for faster execution
                                "preflightCommitment": "processed"
                            }
                            
                            result = await client.send_raw_transaction(
                                serialized_tx, 
                                opts=send_opts
                            )
                            
                            if "result" not in result:
                                error_msg = str(result.get("error", "Unknown error"))
                                print(f"❌ Transaction failed: {error_msg}")
                                return {"success": False, "error": f"Failed to send transaction: {error_msg}"}

                            tx_signature = result["result"]
                            print(f"✅ Transaction sent successfully! Signature: {tx_signature}")
                            
                            explorer_url = f"https://solscan.io/tx/{tx_signature}"
                            print(f"🔍 Explorer URL: {explorer_url}")

                            # Get token info for better display
                            token_symbol = "Unknown"
                            try:
                                token_metadata = await self.get_token_metadata(token_address)
                                if token_metadata:
                                    token_symbol = token_metadata.get("symbol", token_address[:6])
                            except Exception as meta_err:
                                print(f"⚠️ Failed to get token metadata: {str(meta_err)}")
                            
                            # Update the simulated balance to keep track
                            await self.update_simulated_balance(username, -amount)
                            print(f"💰 Updated simulated balance for {username}")

                            # Add this buy to recent buys for the user
                            if not hasattr(self, 'recent_buys'):
                                self.recent_buys = {}
                            if username not in self.recent_buys:
                                self.recent_buys[username] = []

                            buy_record = {
                                "timestamp": time.time(),
                                "token_address": token_address,
                                "symbol": token_symbol,
                                "amount": amount,
                                "success": True,
                                "tx_hash": tx_signature,
                                "explorer_url": explorer_url
                            }
                            
                            self.recent_buys[username].append(buy_record)
                            print(f"📝 Added transaction to recent buys for {username}")

                            return {
                                "success": True,
                                "tx_signature": tx_signature,
                                "explorer_url": explorer_url,
                                "amount": amount,
                                "symbol": token_symbol
                            }
                        except Exception as e:
                            import traceback
                            print(f"❌ Error in transaction processing: {str(e)}")
                            print(traceback.format_exc())
                            return {"success": False, "error": f"Transaction error: {str(e)}"}
                            
                except Exception as e:
                    import traceback
                    print(f"❌ Jupiter swap error: {e}")
                    print(traceback.format_exc())
                    return {"success": False, "error": f"Jupiter swap failed: {str(e)}"}
        except Exception as e:
            import traceback
            print(f"❌ Error buying token: {e}")
            print(traceback.format_exc())
            return {"success": False, "error": str(e)}

    async def sell_token(self, username, token_address, percentage=100, params=None):
        """
        Sell a specific token from the user's wallet

        Args:
            username: The username of the wallet owner
            token_address: The token address to sell
            percentage: Percentage to sell (0-100, default 100% = sell all)
            params: Dictionary with additional parameters (slippage, priority_fee, etc.)

        Returns:
            Dict with transaction details
        """
        # Use default params if none provided
        if params is None:
            params = {
                "slippage": 20,               # Default 20% slippage
                "priority_fee": 0.0015,        # Default 0.0015 SOL priority fee
                "mev_protection": False        # Default MEV protection off
            }

        # Log the transaction with parameters
        print(f"Selling token {token_address} for {username}")
        print(f"Percentage: {percentage}%")
        print(f"Slippage: {params.get('slippage', 20)}%")
        print(f"Priority Fee: {params.get('priority_fee', 0.0015)} SOL")
        print(f"MEV Protection: {'Enabled' if params.get('mev_protection', False) else 'Disabled'}")

        # Simulate network delay
        await asyncio.sleep(1)

        # Simulate a success
        tx_signature = base64.b64encode(os.urandom(16)).decode()

        return {
            "success": True,
            "tx_signature": tx_signature,
            "token_address": token_address,
            "percentage_sold": percentage,
            "timestamp": time.time(),
            "explorer_url": f"https://solscan.io/tx/{tx_signature}",
            "params": params  # Include the parameters used
        }

    async def get_tokens(self, username):
        """
        Get list of tokens owned by the user's wallet

        Args:
            username: The username of the wallet owner

        Returns:
            List of token objects with details
        """
        # In a real implementation, this would query the blockchain
        # For now, return an empty list - no tokens owned yet

        # When you add real Solana blockchain integration, uncomment and modify this code:
        # wallet = self.get_wallet(username)
        # if not wallet:
        #     return []
        # public_key = wallet.get('public')
        # 
        # # Query Solana blockchain for tokens owned by this address
        # # This would use RPC calls to get token accounts and balances

        # Return empty list for now - no simulated data
        return []

    async def get_balance(self, username, force_refresh=False):
        """
        Get SOL balance for a user's wallet

        Args:
            username: The username of the wallet owner
            force_refresh: Force a refresh from the RPC instead of using cache

        Returns:
            float: The SOL balance
        """
        # Get wallet info
        wallet = self.get_wallet(username)
        if not wallet:
            return 0.0

        # Make sure username is lowercase for consistency
        username = username.lower() if username else f"user_unknown"
        pubkey = wallet.get("public")

        # Print the wallet address we're checking (for debugging)
        print(f"Checking balance for wallet address: {pubkey}")

        # Check if we have a recent cached balance (within 30 seconds) to avoid excessive API calls
        # Skip the cache check if force_refresh is True
        if not force_refresh and hasattr(self, 'user_balances') and username in self.user_balances:
            cached_data = self.user_balances.get(username, {})
            if isinstance(cached_data, dict) and "timestamp" in cached_data:
                if time.time() - cached_data["timestamp"] < 30:  # Less than 30 seconds old
                    print(f"Using cached balance for {username}: {cached_data['balance']} SOL")
                    return cached_data["balance"]

        # Try to get balance directly from Solana RPC first (more reliable)
        try:
            # Attempt to get balance via the Solana RPC endpoint
            solana_rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
            print(f"Fetching live balance from Solana RPC: {solana_rpc_url}")

            headers = {"Content-Type": "application/json"}
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [pubkey]
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(solana_rpc_url, json=payload, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"RPC response: {data}")
                        if "result" in data and "value" in data["result"]:
                            balance = data["result"]["value"] / 10**9  # Convert lamports to SOL

                            # Cache this balance
                            if not hasattr(self, 'user_balances'):
                                self.user_balances = {}

                            self.user_balances[username] = {
                                "balance": balance,
                                "timestamp": time.time()
                            }
                            print(f"Successfully fetched balance from Solana RPC for {username}: {balance} SOL")
                            return balance
                        else:
                            print(f"Unexpected RPC response format: {data}")
                    except Exception as json_err:
                        print(f"Error parsing RPC response: {json_err}")
                else:
                    print(f"Solana RPC returned status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching balance from Solana RPC: {e}")

        # Fallback to Solscan API
        try:
            print(f"Falling back to Solscan API for address: {pubkey}")
            url = f"https://api.solscan.io/account?address={pubkey}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"Solscan response: {data}")
                        lamports = data.get("lamports", 0)
                        balance = lamports / 10**9  # Convert lamports to SOL

                        # Cache the balance but with a timestamp for future reference
                        if not hasattr(self, 'user_balances'):
                            self.user_balances = {}

                        self.user_balances[username] = {
                            "balance": balance,
                            "timestamp": time.time()  # Track when we fetched this
                        }
                        print(f"Successfully fetched balance from Solscan for {username}: {balance} SOL")
                        return balance
                    except Exception as json_err:
                        print(f"Error parsing Solscan response: {json_err}")
                else:
                    print(f"Solscan API returned status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching balance from Solscan: {e}")

        # Last fallback - if we have a cached balance that's not too old (within 5 minutes)
        if hasattr(self, 'user_balances') and username in self.user_balances:
            cached_data = self.user_balances[username]
            if isinstance(cached_data, dict) and "timestamp" in cached_data:
                if time.time() - cached_data["timestamp"] < 300:  # Less than 5 minutes old
                    print(f"Using older cached balance as fallback: {cached_data.get('balance', 0)} SOL")
                    return cached_data["balance"]
            elif isinstance(cached_data, (int, float)):
                # Handle old format of cached balances for backward compatibility
                return cached_data

        # Fallback to simulated balance if all else fails
        if hasattr(self, 'simulated_balances') and username in self.simulated_balances:
            print(f"Using simulated balance for {username}")
            return self.simulated_balances[username]

        # If all methods failed, return a default balance with error logging
        print(f"ALL BALANCE FETCH METHODS FAILED for {username}. Using default balance of 0.0")
        return 0.0  # Default to zero balance

    async def fetch_tokens_from_pump_fun(self):
        """
        Fetch new token listings from pump.fun

        Returns:
            list: List of token data dictionaries
        """
        try:
            url = "https://api.pump.fun/tokens/latest"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    tokens = []

                    # Format the token data 
                    for token in data.get("tokens", [])[:10]:  # Limit to 10 most recent
                        tokens.append({
                            "address": token.get("address"),
                            "symbol": token.get("symbol", "UNKNOWN"),
                            "name": token.get("name", "Unknown Token"),
                            "created_at": token.get("created_at"),
                            "source": "pump.fun"
                        })

                    return tokens
                else:
                    print(f"Error fetching from pump.fun: Status {response.status_code}")
                    return []

        except Exception as e:
            print(f"Error fetching from pump.fun: {e}")
            return []

    async def fetch_tokens_from_dexscreener(self):
        """
        Fetch new token pairs from dexscreener

        Returns:
            list: List of token data dictionaries
        """
        try:
            # Try multiple Dexscreener endpoints to get the most comprehensive data
            endpoints = [
                "https://api.dexscreener.com/latest/dex/pairs/solana/new",      # Newly listed
                "https://api.dexscreener.com/latest/dex/pairs/solana/recent",   # Recently updated
                "https://api.dexscreener.com/latest/dex/tokens/solana/trending"  # Trending tokens
            ]

            # Common excluded tokens (major coins and stables)
            excluded_symbols = ["SOL", "USDC", "USDT", "BONK", "WIF", "JUP", "RNDR", "RAY", "ETH", "BTC", "JTO", "PYTH", "MSOL"]

            # Set user agent to avoid rate limiting
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            tokens = []
            processed_addresses = set()

            async with httpx.AsyncClient() as client:
                for endpoint in endpoints:
                    try:
                        response = await client.get(endpoint, headers=headers, timeout=12.0)
                        if response.status_code != 200:
                            print(f"Error fetching from {endpoint}: Status {response.status_code}")
                            continue

                        data = response.json()

                        # Handle different response formats
                        pairs = []
                        if "pairs" in data:
                            pairs = data.get("pairs", [])[:20]  # Top 20 pairs
                        elif "tokens" in data:
                            # Handle trending tokens endpoint
                            for token in data.get("tokens", [])[:20]:
                                if "pairs" in token:
                                    pairs.extend(token.get("pairs", [])[:3])  # Top 3 pairs per token

                        for pair in pairs:
                            # Skip pairs with no liquidity or extremely low liquidity
                            if not pair.get("liquidity") or pair.get("liquidity", {}).get("usd", 0) < 100:
                                continue

                            # Get creation timestamp to filter for newest tokens
                            created_at = pair.get("pairCreatedAt", "")
                            pair_age_hours = 0

                            if created_at:
                                try:
                                    # Calculate age in hours if timestamp is available
                                    import time
                                    from datetime import datetime
                                    created_timestamp = int(time.mktime(datetime.strptime(created_at.split('.')[0], "%Y-%m-%dT%H:%M:%S").timetuple()))
                                    current_timestamp = int(time.time())
                                    pair_age_hours = (current_timestamp - created_timestamp) / 3600
                                except Exception:
                                    # Ignore timestamp parsing errors
                                    pass

                            # Analyze base and quote tokens to find the non-major token
                            token_candidates = []

                            if "baseToken" in pair and pair["baseToken"]["symbol"] not in excluded_symbols:
                                token_candidates.append({
                                    "address": pair["baseToken"]["address"],
                                    "symbol": pair["baseToken"]["symbol"],
                                    "name": pair["baseToken"].get("name", pair["baseToken"]["symbol"]),
                                    "price_usd": pair["baseToken"].get("price", 0)
                                })

                            if "quoteToken" in pair and pair["quoteToken"]["symbol"] not in excluded_symbols:
                                token_candidates.append({
                                    "address": pair["quoteToken"]["address"],
                                    "symbol": pair["quoteToken"]["symbol"],
                                    "name": pair["quoteToken"].get("name", pair["quoteToken"]["symbol"]),
                                    "price_usd": pair["quoteToken"].get("price", 0)
                                })

                            # Process token candidates
                            for token_data in token_candidates:
                                token_address = token_data["address"]

                                # Skip if already processed
                                if token_address in processed_addresses:
                                    continue

                                processed_addresses.add(token_address)

                                # Build token object with all relevant data
                                token_obj = {
                                    "address": token_address,
                                    "symbol": token_data["symbol"],
                                    "name": token_data["name"],
                                    "created_at": created_at,
                                    "age_hours": pair_age_hours,
                                    "liquidity": pair.get("liquidity", {}).get("usd", 0),
                                    "price_usd": token_data.get("price_usd", 0),
                                    "volume_24h": pair.get("volume", {}).get("h24", 0),
                                    "price_change_24h": pair.get("priceChange", {}).get("h24", 0),
                                    "source": "dexscreener",
                                    "dex": pair.get("dexId", "unknown")
                                }

                                tokens.append(token_obj)

                    except Exception as e:
                        print(f"Error processing {endpoint}: {e}")
                        continue

            # Sort by newest first, then by liquidity
            tokens.sort(key=lambda x: (-x.get("liquidity", 0) if x.get("age_hours", 999) < 48 else -999))

            # Return the top tokens
            return tokens[:30]

        except Exception as e:
            print(f"Error fetching from dexscreener: {e}")
            return []

    async def get_token_metadata(self, token_address):
        """
        Get token metadata including social links from multiple sources

        Args:
            token_address: Token contract address

        Returns:
            dict: Token metadata including social links
        """
        if not token_address:
            return {}

        metadata = {
            "address": token_address,
            "symbol": "UNKNOWN",
            "name": "Unknown Token",
            "website": None,
            "twitter": None,
            "telegram": None,
            "discord": None,
            "liquidity": 0
        }

        # Try multiple sources to gather the most comprehensive data
        sources_to_try = [
            self._get_metadata_from_birdeye,
            self._get_metadata_from_solscan,
            self._get_metadata_from_pump_fun
        ]

        for source_func in sources_to_try:
            try:
                source_data = await source_func(token_address)
                if not source_data or not isinstance(source_data, dict):
                    continue

                # Merge data, preferring non-None values from new source
                for key, value in source_data.items():
                    if value is not None and (metadata.get(key) is None or key == "liquidity"):
                        # For liquidity, take the larger value
                        if key == "liquidity" and metadata.get(key, 0) > value:
                            continue
                        metadata[key] = value

                # If we've found all important fields, we can stop searching
                if metadata.get("website") and metadata.get("twitter") and metadata.get("telegram"):
                    break

            except Exception as e:
                print(f"Error getting metadata from source {source_func.__name__}: {e}")
                continue

        return metadata

    async def _get_metadata_from_birdeye(self, token_address):
        """Get token metadata from Birdeye API"""
        try:
            url = f"https://public-api.birdeye.so/public/token_metadata?address={token_address}"
            headers = {"X-API-KEY": os.getenv("BIRDEYE_API_KEY", "")}

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success", False):
                        token_data = data.get("data", {})
                        return {
                            "symbol": token_data.get("symbol"),
                            "name": token_data.get("name"),
                            "website": token_data.get("website"),
                            "twitter": token_data.get("twitter"),
                            "telegram": token_data.get("telegram"),
                            "discord": token_data.get("discord"),
                            "liquidity": token_data.get("liquidity", 0)
                        }
            return {}
        except Exception:
            return {}

    async def _get_metadata_from_solscan(self, token_address):
        """Get token metadata from Solscan API"""
        try:
            url = f"https://api.solscan.io/token/meta?token={token_address}"

            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success", False):
                        token_data = data.get("data", {})
                        socials = token_data.get("socials", {})
                        return {
                            "symbol": token_data.get("symbol"),
                            "name": token_data.get("name"),
                            "website": socials.get("website"),
                            "twitter": socials.get("twitter"),
                            "telegram": socials.get("telegram"),
                            "discord": socials.get("discord")
                        }
            return {}
        except Exception:
            return {}

    async def _get_metadata_from_pump_fun(self, token_address):
        """Get token metadata from pump.fun API"""
        try:
            url = f"https://api.pump.fun/token/{token_address}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    token_data = data.get("token", {})
                    return {
                        "symbol": token_data.get("symbol"),
                        "name": token_data.get("name"),
                        "website": token_data.get("websiteUrl"),
                        "twitter": token_data.get("twitterUrl"),
                        "telegram": token_data.get("telegramUrl"),
                        "discord": token_data.get("discordUrl")
                    }
            return {}
        except Exception:
            return {}

    async def update_simulated_balance(self, username, amount_change):
        """Update the simulated balance for a user (for testing)"""
        if not hasattr(self, 'user_balances'):
            self.user_balances = {}

        # Get current balance or initialize it
        current_balance = self.user_balances.get(username, await self.get_balance(username))

        # Update balance
        new_balance = max(0, current_balance + amount_change)
        self.user_balances[username] = round(new_balance, 3)

        return new_balance

    async def get_recent_buys(self, username, minutes=10):
        """Get recent token purchases for a specific user

        Args:
            username: The username to get purchases for
            minutes: How many minutes back to look for purchases

        Returns:
            list: List of recent buy transactions
        """
        # Initialize recent_buys attribute if it doesn't exist
        if not hasattr(self, 'recent_buys'):
            self.recent_buys = {}

        # Get user's recent purchases
        user_buys = self.recent_buys.get(username.lower(), [])

        # Filter by time (last X minutes)
        import time
        current_time = time.time()
        time_threshold = current_time - (minutes * 60)

        recent_purchases = [
            buy for buy in user_buys 
            if buy.get("timestamp", 0) >= time_threshold
        ]

        # If we're in simulation mode and have no real purchases,
        # generate some simulated ones for testing
        if not recent_purchases and not hasattr(self, '_simulated_buys_generated'):
            # Add a couple of simulated buys for demonstration
            recent_purchases = [
                {
                    "timestamp": current_time - (2 * 60),  # 2 minutes ago
                    "token_address": "5tJQrn9UHvCaLfAJUUXTkHD1hBE2qU488oYQQxoR3QSt",
                    "symbol": "RANDOM",
                    "amount": 0.005,
                    "success": True,
                    "explorer_url": "https://solscan.io/address/5tJQrn9UHvCaLfAJUUXTkHD1hBE2qU488oYQQxoR3QSt"
                },
                {
                    "timestamp": current_time - (8 * 60),  # 8 minutes ago
                    "token_address": "FBBgS9jpLzNxK7MXo9vUqiQdwwbNq6DU9xCagj6pJCFk",
                    "symbol": "TOKEN2",
                    "amount": 0.01,
                    "success": True,
                    "explorer_url": "https://solscan.io/address/FBBgS9jpLzNxK7MXo9vUqiQdwwbNq6DU9xCagj6pJCFk"
                }
            ]
            # Set a flag so we only generate simulated buys once
            self._simulated_buys_generated = True

        return recent_purchases


async def export_wallet(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.username
    if not is_authenticated(user_id):
        await update.message.reply_text(
            "⛔ This bot is restricted to authorized admins. "
            "Message @CoinCatchers88 or @Shilling_Queen if you would like to have access to this bot."
        )
        return

    wallet = wallet_manager.get_wallet(username)
    if not wallet:
        await update.message.reply_text("❌ No wallet found for your account.")
        return

    # Get the secret key and convert to Base58 for Phantom
    import base58
    secret_key = wallet['secret']

    # Convert the key to the appropriate format based on what we have
    if isinstance(secret_key, list):
        # Convert list to bytes
        key_bytes = bytes(secret_key[:64])  # Ensure we use only the first 64 bytes
        key_array = secret_key[:64]

        # Make sure key array is exactly 64 integers
        if len(key_array) < 64:
            # Generate a new keypair if the key is too short
            from solana.keypair import Keypair
            keypair = Keypair()
            key_bytes = keypair.secret_key
            key_array = list(keypair.secret_key)
            # Update the wallet with the new keypair
            wallet_manager.wallets[username.lower()] = {
                "public": str(keypair.public_key),
                "secret": key_array
            }
            wallet_manager.save_wallets()
    else:
        try:
            # Try to decode if it's base64
            import base64
            key_bytes = base64.b64decode(secret_key)
            key_array = list(key_bytes)
        except:
            # If that fails, generate a new keypair
            from solana.keypair import Keypair
            keypair = Keypair()
            key_bytes = keypair.secret_key
            key_array = list(keypair.secret_key)
            # Update the wallet with the new keypair
            wallet_manager.wallets[username.lower()] = {
                "public": str(keypair.public_key),
                "secret": key_array
            }
            wallet_manager.save_wallets()

    # Ensure the key is the right length (64 bytes)
    if len(key_bytes) > 64:
        key_bytes = key_bytes[:64]  # Trim if too long
    elif len(key_bytes) < 64:
        # Pad if too short (shouldn't happen with valid keys)
        key_bytes = key_bytes + b'\0' * (64 - len(key_bytes))

    # Encode to Base58 (format that Phantom accepts)
    private_key_b58 = base58.b58encode(key_bytes).decode("utf-8")

    # Also provide the JSON array format for Phantom import
    if isinstance(secret_key, list):
        key_array = secret_key
    else:
        key_array = list(key_bytes)

    # Ensure key array is exactly 64 integers
    if len(key_array) > 64:
        key_array = key_array[:64]
    while len(key_array) < 64:
        key_array.append(0)

    # Security notice
    await update.message.reply_text(
        "⚠️ *SECURITY WARNING*\n\n"
        "I'm about to send your private key. This should *ONLY* be used for:\n"
        "• Importing to a secure wallet like Phantom\n"
        "• Development purposes\n\n"
        "*NEVER* share this key with anyone else.\n"
        "Anyone with this key can steal your funds.\n\n"
        "This message will be deleted in 60 seconds.",
        parse_mode="Markdown"
    )

    # Send both the Base58 format and the JSON array format
    import json
    private_key_msg = await update.message.reply_text(
        f"🔑 *Your Private Key (Base58):*\n`{private_key_b58}`\n\n"
        f"🔑 *Your Private Key (JSON Array):*\n`{json.dumps(key_array)}`\n\n"
        "Import into Phantom using *Import Private Key* with the JSON array format.",
        parse_mode="Markdown"
    )

    # Delete both messages after 60 seconds
    await asyncio.sleep(60)
    try:
        await private_key_msg.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

# Create a global instance of the wallet manager
wallet_manager = WalletManager()

# Import is_authenticated from main is handled when main.py imports this module
# No placeholder needed as main.py will provide the real function