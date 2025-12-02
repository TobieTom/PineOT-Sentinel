import asyncio
import websockets
import json
import requests
from colorama import Fore, Style, init

# Initialize colors
init(autoreset=True)

# FIXED: Changed from 'async def' to 'def' so it works with to_thread
def check_socials(uri):
    """
    Fetches the metadata JSON from the IPFS URI to find social links.
    """
    try:
        # We use a reliable IPFS gateway to read the data fast
        response = requests.get(uri, timeout=2)
        if response.status_code == 200:
            data = response.json()
            # Check if Telegram exists in the metadata
            telegram = data.get("telegram", None)
            website = data.get("website", None)
            twitter = data.get("twitter", None)
            return telegram, website, twitter
    except:
        return None, None, None
    return None, None, None

async def subscribe_new_tokens():
    uri = "wss://pumpportal.fun/api/data"
    
    print(f"{Fore.CYAN}[*] Sniper v2.1 Loaded. Filtering for Telegram links...{Style.RESET_ALL}")
    
    async with websockets.connect(uri) as websocket:
        payload = { "method": "subscribeNewToken" }
        await websocket.send(json.dumps(payload))
        
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                if 'mint' in data:
                    token_uri = data.get('uri')
                    
                    # 1. IMMEDIATE FILTER: If no metadata URI, skip.
                    if not token_uri:
                        continue

                    # 2. DEEP SCAN: Fetch the socials in a separate thread to keep the stream fast
                    telegram, website, twitter = await asyncio.to_thread(check_socials, token_uri)

                    # 3. QUALIFICATION: Only print if Telegram exists
                    if telegram:
                        print(f"{Fore.GREEN}[+] QUALIFIED LEAD FOUND{Style.RESET_ALL}")
                        print(f"Coin: {data.get('name')} ({data.get('symbol')})")
                        print(f"Telegram: {Fore.BLUE}{telegram}{Style.RESET_ALL}")
                        print(f"Pump Link: https://pump.fun/{data.get('mint')}")
                        
                        # Bonus: Alert if they lack a website (Upsell opportunity)
                        if not website:
                            print(f"{Fore.YELLOW}(!) OPPORTUNITY: No Website Detected (Pitch the Web-Sprint){Style.RESET_ALL}")
                        
                        print("-" * 50)
                    else:
                        # Print a small dot to show the script is scanning
                        print(f"{Fore.RED}.{Style.RESET_ALL}", end="", flush=True)

            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    try:
        # Check if requests is installed, just in case
        import requests
        asyncio.run(subscribe_new_tokens())
    except ImportError:
        print("Error: You need to install 'requests'. Run: pip install requests")
    except KeyboardInterrupt:
        print("\nStopping Sniper...")