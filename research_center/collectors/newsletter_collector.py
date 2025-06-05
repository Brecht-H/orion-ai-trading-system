#!/usr/bin/env python3
"""
Working Newsletter Processor
Successfully processes AI newsletters and adds them to Knowledge Center
"""

import imaplib
import email
import sys
import os
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict
import hashlib

# Add paths
sys.path.append('orion_core/knowledge')
sys.path.append('orion_core')

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import Knowledge Center
from knowledge_center_phase1 import KnowledgeCenter, KnowledgeDocument

# Email settings
EMAIL = 'abhartjes@icloud.com'
PASSWORD = 'qcqt-jrpp-bdhf-usto'
SERVER = 'imap.mail.me.com'
PORT = 993

@dataclass
class NewsletterData:
    subject: str
    sender: str
    date: str
    content: str
    message_id: str

class WorkingNewsletterProcessor:
    def __init__(self):
        self.knowledge_center = KnowledgeCenter()
        self.logger = logging.getLogger(__name__)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def connect_to_email(self):
        """Connect to email server"""
        try:
            mail = imaplib.IMAP4_SSL(SERVER, PORT)
            mail.login(EMAIL, PASSWORD)
            return mail
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return None
    
    def extract_newsletter_content(self, email_message):
        """Extract readable content from email"""
        content = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
                elif content_type == "text/html" and not content:
                    try:
                        html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        # Basic HTML to text conversion
                        import re
                        text = re.sub('<[^<]+?>', '', html_content)
                        content += text
                    except:
                        pass
        else:
            try:
                content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                content = str(email_message.get_payload())
        
        return content.strip()
    
    def process_folder(self, folder_name: str, max_emails: int = 10):
        """Process newsletters from specified folder"""
        
        print(f"🔍 Processing folder: {folder_name}")
        
        mail = self.connect_to_email()
        if not mail:
            return []
        
        try:
            # Select folder
            status, count = mail.select(f'"{folder_name}"')
            if status != 'OK':
                print(f"❌ Could not select folder '{folder_name}'")
                return []
            
            print(f"📧 Folder has {count[0].decode()} messages")
            
            # Get recent messages
            status, message_ids = mail.search(None, 'ALL')
            if status != 'OK':
                print("❌ Search failed")
                return []
            
            message_ids = message_ids[0].split()
            recent_ids = message_ids[-max_emails:] if len(message_ids) > max_emails else message_ids
            
            newsletters = []
            
            for i, msg_id in enumerate(recent_ids):
                try:
                    print(f"📨 Processing {i+1}/{len(recent_ids)}: Message {msg_id.decode()}")
                    
                    # Get headers
                    status, header_data = mail.fetch(msg_id, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE MESSAGE-ID)])')
                    
                    if status == 'OK' and header_data and header_data[0][1]:
                        header_text = header_data[0][1].decode('utf-8', errors='ignore')
                        
                        # Parse headers
                        subject = ""
                        sender = ""
                        date = ""
                        message_id = ""
                        
                        for line in header_text.strip().split('\n'):
                            line = line.strip()
                            if line.startswith('SUBJECT:'):
                                subject = line[8:].strip()
                            elif line.startswith('FROM:'):
                                sender = line[5:].strip()
                            elif line.startswith('DATE:'):
                                date = line[5:].strip()
                            elif line.startswith('MESSAGE-ID:'):
                                message_id = line[11:].strip()
                        
                        # Get body preview
                        content = ""
                        try:
                            status2, body_data = mail.fetch(msg_id, '(BODY[1]<0.500>)')  # First 500 chars
                            if status2 == 'OK' and body_data and body_data[0][1]:
                                body_preview = body_data[0][1].decode('utf-8', errors='ignore')
                                content = f"Preview: {body_preview[:300]}..."
                        except:
                            content = "Content preview not available"
                        
                        if subject and sender:  # Only process if we have basic info
                            newsletter = NewsletterData(
                                subject=subject,
                                sender=sender,
                                date=date or str(datetime.now()),
                                content=content,
                                message_id=message_id or f'generated_{hash(subject + sender)}'
                            )
                            newsletters.append(newsletter)
                            print(f"✅ {subject[:50]}...")
                        else:
                            print(f"⚠️  Skipping - missing subject or sender")
                    
                except Exception as e:
                    print(f"❌ Error processing message {i+1}: {e}")
                    continue
            
            mail.logout()
            return newsletters
            
        except Exception as e:
            print(f"❌ Error: {e}")
            try:
                mail.logout()
            except:
                pass
            return []
    
    async def add_to_knowledge_center(self, newsletters: List[NewsletterData]):
        """Add newsletters to Knowledge Center"""
        
        print(f"\n📚 Adding {len(newsletters)} newsletters to Knowledge Center...")
        
        added_count = 0
        for newsletter in newsletters:
            try:
                # Create Knowledge Document
                doc_id = f"newsletter_{hashlib.md5(newsletter.message_id.encode()).hexdigest()[:12]}"
                
                # Determine priority based on content
                priority = "medium"
                if any(word in newsletter.subject.lower() for word in ['breakthrough', 'major', 'important', 'critical']):
                    priority = "high"
                if any(word in newsletter.content.lower() for word in ['crypto', 'bitcoin', 'trading', 'investment']):
                    priority = "high"
                
                content = f"""Newsletter: {newsletter.subject}
From: {newsletter.sender}
Date: {newsletter.date}
Source: AI Report Folder

{newsletter.content}
"""
                
                knowledge_doc = KnowledgeDocument(
                    id=doc_id,
                    title=newsletter.subject,
                    content=content,
                    source=f"email_ai_report",
                    category="newsletter",
                    implementation_status="informational",
                    priority_level=priority,
                    timestamp=datetime.now(),
                    metadata={
                        'sender': newsletter.sender,
                        'original_message_id': newsletter.message_id,
                        'processing_date': datetime.now().isoformat(),
                        'folder': 'AI report'
                    }
                )
                
                # Add to Knowledge Center
                success = await self.knowledge_center.vector_store.add_document(knowledge_doc)
                if success:
                    added_count += 1
                    print(f"✅ Added: {newsletter.subject[:50]}...")
                else:
                    print(f"❌ Failed to add: {newsletter.subject[:50]}...")
                    
            except Exception as e:
                print(f"❌ Error adding to KC: {e}")
        
        print(f"\n🎉 Successfully added {added_count}/{len(newsletters)} newsletters to Knowledge Center!")
        return added_count

async def main():
    """Main processing function"""
    
    processor = WorkingNewsletterProcessor()
    
    print("🚀 Starting COMPLETE Newsletter Processing...")
    
    # Process AI Report folder (already done, but check for new ones)
    print("📧 Processing AI report folder...")
    newsletters = processor.process_folder("AI report", max_emails=25)  # Check for any new ones
    
    if newsletters:
        print(f"📊 Found {len(newsletters)} newsletters in AI report")
        added = await processor.add_to_knowledge_center(newsletters)
        print(f"✅ Added {added} new AI Report newsletters")
    
    # Process Crypto folder
    print(f"\n📧 Processing Crypto folder...")
    crypto_newsletters = processor.process_folder("Crypto", max_emails=20)
    
    if crypto_newsletters:
        print(f"📊 Found {len(crypto_newsletters)} newsletters in Crypto folder:")
        for i, nl in enumerate(crypto_newsletters[:5], 1):  # Show first 5
            print(f"{i}. {nl.subject[:60]}...")
            print(f"   From: {nl.sender}")
        
        # Add these too
        crypto_added = await processor.add_to_knowledge_center(crypto_newsletters)
        print(f"🎉 Added {crypto_added} crypto newsletters!")
    else:
        print("⚠️  No crypto newsletters found or processed")
    
    # Try some other potential folders
    potential_folders = ["INBOX", "Newsletters", "Finance", "Trading"]
    
    for folder in potential_folders:
        try:
            print(f"\n📧 Trying folder '{folder}'...")
            test_newsletters = processor.process_folder(folder, max_emails=3)  # Just test with 3
            if test_newsletters:
                print(f"📊 Found {len(test_newsletters)} newsletters in {folder}:")
                for nl in test_newsletters:
                    print(f"   • {nl.subject[:50]}...")
                
                # Ask user if they want to process this folder fully
                print(f"💡 Found newsletters in '{folder}' - you can process this folder fully later")
        except Exception as e:
            print(f"⚠️  Folder '{folder}' not accessible: {e}")
    
    print(f"\n🎉 Newsletter processing complete!")
    print(f"\n🔍 Search your newsletters:")
    print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'crypto'")
    print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'trading'")
    print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'AI'")

if __name__ == "__main__":
    asyncio.run(main()) 