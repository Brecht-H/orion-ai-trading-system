#!/usr/bin/env python3
"""
Smart Mailbox Newsletter Processor
Replicates the AI & Crypto Newsletters Smart Mailbox search via IMAP
"""

import imaplib
import email
import sys
import os
import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict
import hashlib

# Add paths
sys.path.append('orion_core/knowledge')
sys.path.append('orion_core')

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

class SmartMailboxProcessor:
    def __init__(self):
        self.knowledge_center = KnowledgeCenter()
        self.logger = logging.getLogger(__name__)
        
        # Newsletter sources from Smart Mailbox criteria
        self.newsletter_sources = [
            "pomp letter", "substack", "alexander klopping", "reflexivityresearch",
            "coingecko", "blockchain", "feedspot", "bankless", "bitcoin magazine",
            "blockware", "bybit", "swissborg", "crypto.com", "marcel oost",
            "bitrue", "techdev", "fintech", "binance", "metaversal",
            "lenny's", "connecting"
        ]
        
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
    
    def search_newsletters_in_folder(self, mail, folder_name: str, max_emails: int = 50):
        """Search for newsletters in specific folder using Smart Mailbox criteria"""
        
        try:
            # Select folder
            status, count = mail.select(f'"{folder_name}"')
            if status != 'OK':
                return []
            
            print(f"📧 Searching in '{folder_name}' ({count[0].decode()} messages)")
            
            newsletters = []
            
            # Search for emails from each newsletter source
            for source in self.newsletter_sources:
                try:
                    # Search for emails containing the source in FROM or TO fields
                    search_criteria = f'(OR FROM "{source}" TO "{source}")'
                    status, message_ids = mail.search(None, search_criteria)
                    
                    if status == 'OK' and message_ids[0]:
                        found_ids = message_ids[0].split()
                        print(f"🔍 Found {len(found_ids)} emails for '{source}'")
                        
                        # Process found emails (limit to avoid overwhelming)
                        for msg_id in found_ids[-5:]:  # Take last 5 per source
                            try:
                                newsletter = self.process_single_email(mail, msg_id)
                                if newsletter:
                                    newsletters.append(newsletter)
                                    if len(newsletters) >= max_emails:
                                        break
                            except Exception as e:
                                continue
                        
                        if len(newsletters) >= max_emails:
                            break
                            
                except Exception as e:
                    continue
            
            return newsletters
            
        except Exception as e:
            print(f"❌ Error searching folder '{folder_name}': {e}")
            return []
    
    def process_single_email(self, mail, msg_id):
        """Process a single email message"""
        try:
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
                    status2, body_data = mail.fetch(msg_id, '(BODY[1]<0.500>)')
                    if status2 == 'OK' and body_data and body_data[0][1]:
                        body_preview = body_data[0][1].decode('utf-8', errors='ignore')
                        content = f"Preview: {body_preview[:400]}..."
                except:
                    content = "Content preview not available"
                
                if subject and sender:
                    return NewsletterData(
                        subject=subject,
                        sender=sender,
                        date=date or str(datetime.now()),
                        content=content,
                        message_id=message_id or f'generated_{hash(subject + sender)}'
                    )
        
        except Exception as e:
            pass
        
        return None
    
    def process_smart_mailbox_newsletters(self, max_emails: int = 30):
        """Process newsletters matching Smart Mailbox criteria"""
        
        print("🚀 Starting Smart Mailbox Newsletter Processing...")
        print(f"🔍 Searching for: {', '.join(self.newsletter_sources[:10])}... and more")
        
        mail = self.connect_to_email()
        if not mail:
            return []
        
        all_newsletters = []
        
        # Search in multiple folders
        folders_to_search = ["INBOX", "AI report", "Crypto"]
        
        try:
            for folder in folders_to_search:
                print(f"\n📂 Searching folder: {folder}")
                newsletters = self.search_newsletters_in_folder(mail, folder, max_emails // len(folders_to_search))
                all_newsletters.extend(newsletters)
                
                if len(all_newsletters) >= max_emails:
                    break
            
            mail.logout()
            
            # Remove duplicates based on message ID
            unique_newsletters = {}
            for nl in all_newsletters:
                if nl.message_id not in unique_newsletters:
                    unique_newsletters[nl.message_id] = nl
            
            return list(unique_newsletters.values())
            
        except Exception as e:
            print(f"❌ Error: {e}")
            try:
                mail.logout()
            except:
                pass
            return []
    
    async def add_to_knowledge_center(self, newsletters: List[NewsletterData]):
        """Add newsletters to Knowledge Center"""
        
        print(f"\n📚 Adding {len(newsletters)} Smart Mailbox newsletters to Knowledge Center...")
        
        added_count = 0
        for newsletter in newsletters:
            try:
                # Create Knowledge Document
                doc_id = f"smartbox_{hashlib.md5(newsletter.message_id.encode()).hexdigest()[:12]}"
                
                # Determine priority based on source
                priority = "medium"
                sender_lower = newsletter.sender.lower()
                if any(source in sender_lower for source in ['pomp', 'bankless', 'coingecko', 'binance']):
                    priority = "high"
                
                content = f"""Newsletter: {newsletter.subject}
From: {newsletter.sender}
Date: {newsletter.date}
Source: Smart Mailbox (AI & Crypto Newsletters)

{newsletter.content}
"""
                
                knowledge_doc = KnowledgeDocument(
                    id=doc_id,
                    title=newsletter.subject,
                    content=content,
                    source=f"smart_mailbox_crypto",
                    category="newsletter",
                    implementation_status="informational",
                    priority_level=priority,
                    timestamp=datetime.now(),
                    metadata={
                        'sender': newsletter.sender,
                        'original_message_id': newsletter.message_id,
                        'processing_date': datetime.now().isoformat(),
                        'source_type': 'smart_mailbox'
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
        
        print(f"\n🎉 Successfully added {added_count}/{len(newsletters)} Smart Mailbox newsletters!")
        return added_count

async def main():
    """Main processing function"""
    
    processor = SmartMailboxProcessor()
    
    print("🎯 Processing Smart Mailbox: AI & Crypto Newsletters")
    print("📧 This will search across folders for specific newsletter sources...")
    
    # Process Smart Mailbox criteria
    newsletters = processor.process_smart_mailbox_newsletters(max_emails=25)
    
    if newsletters:
        print(f"\n📊 Found {len(newsletters)} newsletters matching Smart Mailbox criteria:")
        
        # Group by source for display
        by_source = {}
        for nl in newsletters:
            source = nl.sender.split('<')[0].strip() if '<' in nl.sender else nl.sender
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(nl)
        
        for source, nls in by_source.items():
            print(f"\n📰 {source} ({len(nls)} newsletters):")
            for nl in nls[:3]:  # Show first 3 per source
                print(f"   • {nl.subject[:60]}...")
        
        # Add to Knowledge Center
        added = await processor.add_to_knowledge_center(newsletters)
        
        if added > 0:
            print(f"\n🔍 Search your Smart Mailbox newsletters:")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'Pomp'")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'Bankless'")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'CoinGecko'")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'crypto newsletter'")
    else:
        print("\n💡 No Smart Mailbox newsletters found")

if __name__ == "__main__":
    asyncio.run(main()) 