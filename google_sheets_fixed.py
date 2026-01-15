"""
Google Sheets Handler with Quota Management
"""

import gspread
from google.oauth2.service_account import Credentials
import time
import json
from datetime import datetime
from typing import List, Dict
from config.settings import SERVICE_ACCOUNT_FILE, GOOGLE_SHEETS_ID

class GoogleSheetsFixed:
    """Google Sheets with proper quota handling"""
    
    def __init__(self):
        self.sheets_id = GOOGLE_SHEETS_ID
        self.client = self._authenticate()
        self.batch_size = 30  # Upload 30 items at a time
        self.delay_between_batches = 10  # 10 seconds delay
    
    def _authenticate(self):
        """Authenticate with Google Sheets"""
        try:
            scope = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, 
                scopes=scope
            )
            client = gspread.authorize(creds)
            print("✅ Google Sheets authenticated")
            return client
        except Exception as e:
            print(f"❌ Google Sheets auth failed: {str(e)}")
            return None
    
    def create_or_clear_sheet(self, sheet_name):
        """Create or clear existing sheet"""
        try:
            spreadsheet = self.client.open_by_key(self.sheets_id)
            
            try:
                # Try to get existing worksheet
                worksheet = spreadsheet.worksheet(sheet_name)
                # Clear existing data but keep header
                worksheet.clear()
                print(f"📄 Cleared existing sheet: {sheet_name}")
                return worksheet
            except gspread.exceptions.WorksheetNotFound:
                # Create new worksheet
                worksheet = spreadsheet.add_worksheet(
                    title=sheet_name,
                    rows=1000,
                    cols=20
                )
                print(f"📄 Created new sheet: {sheet_name}")
                return worksheet
                
        except Exception as e:
            print(f"❌ Error with sheet {sheet_name}: {str(e)}")
            return None
    
    def upload_data_smart(self, data: List[Dict], sheet_name: str, max_items: int = 30):
        """
        Upload data with quota management
        Uploads exactly max_items with smart batching
        """
        if not self.client:
            print("❌ Google Sheets client not available")
            return False
        
        if not data:
            print(f"⚠️  No data for {sheet_name}")
            return False
        
        # Limit to max_items
        if len(data) > max_items:
            data = data[:max_items]
            print(f"📊 Limiting {sheet_name} to {max_items} items")
        
        try:
            worksheet = self.create_or_clear_sheet(sheet_name)
            if not worksheet:
                return False
            
            # Prepare headers from first item
            headers = list(data[0].keys())
            
            # Upload headers
            worksheet.append_row(headers)
            print(f"📝 Uploaded headers for {sheet_name}")
            time.sleep(2)  # Small delay after headers
            
            # Upload data in smart batches
            total_items = len(data)
            uploaded = 0
            
            # Calculate batch sizes (smaller batches to avoid quota)
            if total_items <= 15:
                batches = [data]  # One batch if small
            elif total_items <= 30:
                # Two batches of ~15 items
                mid = total_items // 2
                batches = [data[:mid], data[mid:]]
            else:
                # Multiple batches of ~10 items
                batch_size = 10
                batches = [data[i:i + batch_size] for i in range(0, total_items, batch_size)]
            
            print(f"📦 Uploading {total_items} items in {len(batches)} batches...")
            
            for i, batch in enumerate(batches, 1):
                try:
                    print(f"   Batch {i}/{len(batches)}: {len(batch)} items...")
                    
                    # Upload batch
                    for item in batch:
                        row = [str(item.get(h, "")) for h in headers]
                        worksheet.append_row(row)
                        uploaded += 1
                    
                    # Progress update
                    print(f"   ✅ Uploaded: {uploaded}/{total_items}")
                    
                    # Delay between batches (except last batch)
                    if i < len(batches):
                        print(f"   ⏳ Waiting {self.delay_between_batches} seconds...")
                        time.sleep(self.delay_between_batches)
                        
                except Exception as batch_error:
                    print(f"   ⚠️  Batch {i} error: {str(batch_error)}")
                    print(f"   ⏳ Waiting 30 seconds before retry...")
                    time.sleep(30)
                    
                    try:
                        # Retry the batch
                        print(f"   🔄 Retrying batch {i}...")
                        for item in batch:
                            row = [str(item.get(h, "")) for h in headers]
                            worksheet.append_row(row)
                            uploaded += 1
                        print(f"   ✅ Batch {i} retry successful")
                    except:
                        print(f"   ❌ Batch {i} failed after retry")
                        continue
            
            print(f"🎉 Successfully uploaded {uploaded} items to {sheet_name}")
            return True
            
        except Exception as e:
            print(f"❌ Critical error uploading {sheet_name}: {str(e)}")
            # Save locally as backup
            self._save_local_backup(data, sheet_name)
            return False
    
    def _save_local_backup(self, data: List[Dict], sheet_name: str):
        """Save data locally as backup"""
        try:
            backup_dir = "sheets_backup"
            import os
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{backup_dir}/{sheet_name}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"📁 Local backup saved: {filename}")
            
        except Exception as e:
            print(f"⚠️  Could not save local backup: {str(e)}")
    
    def upload_all_data(self, all_data: Dict[str, List[Dict]], items_per_sheet: int = 30):
        """
        Upload all platform data
        
        Args:
            all_data: Dictionary with platform names as keys
            items_per_sheet: Number of items to upload per sheet
        """
        if not self.client:
            print("❌ Google Sheets not available")
            return False
        
        print(f"\n📤 Uploading to Google Sheets (max {items_per_sheet} items per sheet)...")
        
        results = {}
        platform_order = ['google_news', 'youtube', 'reddit']  # Fixed order
        
        for platform in platform_order:
            if platform in all_data:
                data = all_data[platform]
                print(f"\n{'='*40}")
                print(f"📊 {platform.upper()} DATA")
                print(f"{'='*40}")
                
                if data:
                    print(f"📁 Found {len(data)} items")
                    success = self.upload_data_smart(data, platform, items_per_sheet)
                    results[platform] = success
                    
                    # Longer delay between platforms
                    if platform != platform_order[-1]:
                        print(f"\n⏳ Waiting 20 seconds before next platform...")
                        time.sleep(20)
                else:
                    print(f"⚠️  No data for {platform}")
                    results[platform] = False
            else:
                print(f"⚠️  Platform {platform} not in data")
        
        # Summary
        print(f"\n{'='*40}")
        print("📋 UPLOAD SUMMARY")
        print(f"{'='*40}")
        
        success_count = sum(1 for result in results.values() if result)
        
        for platform, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{platform}: {status}")
        
        if success_count == len(results):
            print(f"\n🎉 All {len(results)} platforms uploaded successfully!")
        else:
            print(f"\n⚠️  {success_count}/{len(results)} platforms uploaded")
        
        return success_count > 0