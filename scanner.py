
import logging
import requests
from config import REQUIRE_TELEGRAM, REQUIRE_WEBSITE, REQUIRE_TWITTER, REQUIRE_CLEAN_BUBBLE_MAP, MIN_HOLDERS, MAX_SINGLE_HOLDER_PERCENT

logger = logging.getLogger(__name__)

class TokenScanner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Token scanner initialized")
    
    async def scan_contract(self, contract_address):
        """
        Scan a Solana contract address and analyze it based on configured filters
        """
        self.logger.info(f"Scanning contract: {contract_address}")
        
        # Placeholder for real implementation
        results = {
            "contract_address": contract_address,
            "name": "Sample Token",
            "symbol": "SMPL",
            "total_holders": 250,
            "has_telegram": True,
            "has_website": True,
            "has_twitter": True,
            "largest_holder_percentage": 8.5,
            "bubble_map_clean": True,
            "passes_filters": True
        }
        
        # Apply filters
        result_summary = self._apply_filters(results)
        return result_summary
    
    def _apply_filters(self, token_data):
        """Apply configured filters to token data"""
        passes_all = True
        reasons = []
        
        # Check for social media presence
        if REQUIRE_TELEGRAM and not token_data.get("has_telegram"):
            passes_all = False
            reasons.append("No Telegram group/channel")
            
        if REQUIRE_WEBSITE and not token_data.get("has_website"):
            passes_all = False
            reasons.append("No website")
            
        if REQUIRE_TWITTER and not token_data.get("has_twitter"):
            passes_all = False
            reasons.append("No Twitter/X account")
        
        # Check holders distribution
        if token_data.get("total_holders", 0) < MIN_HOLDERS:
            passes_all = False
            reasons.append(f"Too few holders ({token_data.get('total_holders', 0)} < {MIN_HOLDERS})")
            
        if token_data.get("largest_holder_percentage", 100) > MAX_SINGLE_HOLDER_PERCENT:
            passes_all = False
            reasons.append(f"Whale dominated ({token_data.get('largest_holder_percentage')}% > {MAX_SINGLE_HOLDER_PERCENT}%)")
            
        if REQUIRE_CLEAN_BUBBLE_MAP and not token_data.get("bubble_map_clean"):
            passes_all = False
            reasons.append("Suspicious bubble map")
        
        # Create summary
        summary = {
            "contract_address": token_data.get("contract_address"),
            "name": token_data.get("name"),
            "symbol": token_data.get("symbol"),
            "passes_all_filters": passes_all,
            "fail_reasons": reasons if not passes_all else [],
            "raw_data": token_data
        }
        
        return summary
    
    async def format_scan_results(self, results):
        """Format scan results for Telegram display"""
        if not results:
            return "❌ Error scanning contract"
            
        status = "✅ PASSED" if results["passes_all_filters"] else "❌ FAILED"
        
        message = f"*Scan Results for {results['name']} ({results['symbol']})*\n\n"
        message += f"*Status*: {status}\n"
        message += f"*Contract*: `{results['contract_address']}`\n\n"
        
        if not results["passes_all_filters"]:
            message += "*Failed Checks:*\n"
            for reason in results["fail_reasons"]:
                message += f"• {reason}\n"
        else:
            message += "✅ Passed all quality checks!\n"
            
        # Add more token details
        raw = results["raw_data"]
        message += f"\n*Token Details:*\n"
        message += f"• Holders: {raw.get('total_holders')}\n"
        message += f"• Largest Holder: {raw.get('largest_holder_percentage')}%\n"
        message += f"• Social: "
        message += "✅ " if raw.get("has_telegram") else "❌ "
        message += "TG | "
        message += "✅ " if raw.get("has_website") else "❌ "
        message += "Web | "
        message += "✅ " if raw.get("has_twitter") else "❌ "
        message += "Twitter\n"
        
        return message
