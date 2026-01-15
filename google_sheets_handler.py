"""
Store collected data in Google Sheets - WITH QUOTA HANDLING
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict
import time
from config.settings import SERVICE_ACCOUNT_FILE, GOOGLE_SHEETS_ID

class GoogleSheetsHandler:
    """Handle Google Sheets operations with quota management"""
    
    def __init__(self):
        self.sheets_id = GOOGLE_SHEETS_ID
        self.client = self._authenticate()
        self.quota_delay = 60  # Wait 60 seconds if quota exceeded
    
    def _authenticate(self):
        """Authenticate with Google Sheets"""
        try:
            if not SERVICE_ACCOUNT_FILE or SERVICE_ACCOUNT_FILE == "credentials/service-account.json":
                print("⚠️  No Google Sheets credentials file specified")
                print("   Using local storage only")
                return None
                
            scope = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, 
                scopes=scope
            )
            client = gspread.authorize(creds)
            print("✅ Authenticated with Google Sheets")
            return client
        except Exception as e:
            print(f"⚠️  Google Sheets authentication failed: {str(e)}")
            print("   Using local storage only")
            return None
    
    def store_data(self, data: List[Dict], sheet_name: str, max_retries: int = 3):
        """
        Store data in Google Sheets with quota handling
        
        Args:
            data: List of dictionaries with data
            sheet_name: Name of the sheet/tab
            max_retries: Maximum retry attempts
        """
        if not self.client:
            print(f"   Saving locally instead of Google Sheets")
            self._save_locally(data, sheet_name)
            return False
        
        for attempt in range(max_retries):
            try:
                # Open spreadsheet
                spreadsheet = self.client.open_by_key(self.sheets_id)
                
                # Create or open sheet
                try:
                    worksheet = spreadsheet.worksheet(sheet_name)
                except:
                    worksheet = spreadsheet.add_worksheet(
                        title=sheet_name, 
                        rows=1000, 
                        cols=20
                    )
                
                # Prepare headers and data
                if data:
                    # Get headers from first item
                    headers = list(data[0].keys())
                    
                    # Clear existing data and write headers
                    worksheet.clear()
                    
                    # Write in batches to avoid quota issues
                    batch_size = 50
                    
                    # Write headers
                    worksheet.append_row(headers)
                    
                    # Write data in batches
                    for i in range(0, len(data), batch_size):
                        batch = data[i:i + batch_size]
                        for item in batch:
                            row = [str(item.get(h, "")) for h in headers]
                            worksheet.append_row(row)
                        
                        # Small delay between batches
                        if i + batch_size < len(data):
                            time.sleep(1)
                    
                    print(f"✅ Stored {len(data)} items in '{sheet_name}' sheet")
                    return True
                
            except Exception as e:
                error_msg = str(e)
                if "quota" in error_msg.lower() or "429" in error_msg:
                    print(f"⚠️  Quota exceeded (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        print(f"   Waiting {self.quota_delay} seconds before retry...")
                        time.sleep(self.quota_delay)
                    else:
                        print("   Max retries reached. Saving locally instead.")
                        self._save_locally(data, sheet_name)
                        return False
                else:
                    print(f"❌ Error storing data: {error_msg}")
                    self._save_locally(data, sheet_name)
                    return False
        
        return False
    
    def _save_locally(self, data: List[Dict], sheet_name: str):
        """Save data locally as backup"""
        import json
        import os
        
        # Create backup directory
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = f"{backup_dir}/{sheet_name}_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"   📁 Data saved locally: {filename}")
    
    def read_data(self, sheet_name: str) -> List[Dict]:
        """Read data from Google Sheets or local backup"""
        if not self.client:
            return self._read_locally(sheet_name)
        
        try:
            spreadsheet = self.client.open_by_key(self.sheets_id)
            worksheet = spreadsheet.worksheet(sheet_name)
            
            # Get all values
            data = worksheet.get_all_records()
            print(f"📖 Read {len(data)} items from '{sheet_name}'")
            return data
            
        except Exception as e:
            print(f"⚠️  Error reading from Google Sheets: {str(e)}")
            print("   Trying local backup...")
            return self._read_locally(sheet_name)
    
    def _read_locally(self, sheet_name: str) -> List[Dict]:
        """Read data from local backup"""
        import json
        import os
        
        # Try to find latest backup
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            return []
        
        # Find files for this sheet
        import glob
        pattern = f"{backup_dir}/{sheet_name}_*.json"
        files = glob.glob(pattern)
        
        if not files:
            return []
        
        # Get latest file
        latest_file = max(files, key=os.path.getctime)
        
        with open(latest_file, "r") as f:
            data = json.load(f)
        
        print(f"📖 Read {len(data)} items from local backup: {latest_file}")
        return data