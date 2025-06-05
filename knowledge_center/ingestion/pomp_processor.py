#!/usr/bin/env python3
"""
The Pomp Letter Processor
Specialized processor for all Anthony Pompliano newsletters
"""

import imaplib
import sys
import asyncio
from datetime import datetime
import hashlib

# Add paths
sys.path.append('orion_core/knowledge')
sys.path.append('orion_core')

from knowledge_center_phase1 import KnowledgeCenter, KnowledgeDocument

# Email settings
EMAIL = 'abhartjes@icloud.com'
PASSWORD = 'qcqt-jrpp-bdhf-usto'
SERVER = 'imap.mail.me.com'
PORT = 993

class PompLetterProcessor:
    def __init__(self):
        self.knowledge_center = KnowledgeCenter()
    
    def connect_to_email(self):
        try:
            mail = imaplib.IMAP4_SSL(SERVER, PORT)
            mail.login(EMAIL, PASSWORD)
            return mail
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return None
    
    def process_pomp_letters(self, max_emails: int = 50):
        """Process The Pomp Letter emails from INBOX"""
        
        print(f"🚀 Processing The Pomp Letter emails (max: {max_emails})...")
        
        mail = self.connect_to_email()
        if not mail:
            return []
        
        try:
            # Select INBOX
            mail.select('"INBOX"')
            
            # Search specifically for Pomp Letter emails
            status, message_ids = mail.search(None, 'FROM "pomp@substack.com"')
            
            if status != 'OK' or not message_ids[0]:
                print("❌ No Pomp Letter emails found")
                return []
            
            found_ids = message_ids[0].split()
            print(f"📧 Found {len(found_ids)} Pomp Letter emails!")
            
            # Process recent emails (newest first)
            recent_ids = found_ids[-max_emails:] if len(found_ids) > max_emails else found_ids
            
            newsletters = []
            for i, msg_id in enumerate(reversed(recent_ids)):  # Newest first
                try:
                    print(f"📨 Processing {i+1}/{len(recent_ids)}")
                    
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
                            status2, body_data = mail.fetch(msg_id, '(BODY[1]<0.800>)')  # More content for Pomp
                            if status2 == 'OK' and body_data and body_data[0][1]:
                                body_preview = body_data[0][1].decode('utf-8', errors='ignore')
                                content = f"Preview: {body_preview[:600]}..."
                        except:
                            content = "Content preview not available"
                        
                        if subject and sender:
                            newsletters.append({
                                'subject': subject,
                                'sender': sender,
                                'date': date,
                                'content': content,
                                'message_id': message_id or f'pomp_{hash(subject + date)}'
                            })
                            print(f"✅ {subject[:50]}...")
                
                except Exception as e:
                    print(f"❌ Error processing email {i+1}: {e}")
                    continue
            
            mail.logout()
            return newsletters
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    async def add_pomp_letters_to_knowledge_center(self, newsletters):
        """Add Pomp Letters to Knowledge Center with special categorization"""
        
        print(f"\n📚 Adding {len(newsletters)} Pomp Letters to Knowledge Center...")
        
        added_count = 0
        for newsletter in newsletters:
            try:
                doc_id = f"pomp_{hashlib.md5(newsletter['message_id'].encode()).hexdigest()[:12]}"
                
                # High priority for all Pomp content
                priority = "high"
                
                # Determine specific category based on subject
                subject_lower = newsletter['subject'].lower()
                if any(word in subject_lower for word in ['bitcoin', 'btc', 'halving']):
                    category = "bitcoin_analysis"
                elif any(word in subject_lower for word in ['inflation', 'fed', 'economic']):
                    category = "economic_analysis" 
                elif any(word in subject_lower for word in ['crypto', 'blockchain']):
                    category = "crypto_analysis"
                else:
                    category = "investment_insights"
                
                content = f"""The Pomp Letter: {newsletter['subject']}
From: Anthony Pompliano via Substack
Date: {newsletter['date']}
Source: The Pomp Letter Newsletter

{newsletter['content']}

Newsletter URL: https://pomp.substack.com/
"""
                
                knowledge_doc = KnowledgeDocument(
                    id=doc_id,
                    title=f"Pomp: {newsletter['subject']}",
                    content=content,
                    source="pomp_letter",
                    category=category,
                    implementation_status="informational",
                    priority_level=priority,
                    timestamp=datetime.now(),
                    metadata={
                        'author': 'Anthony Pompliano',
                        'newsletter': 'The Pomp Letter',
                        'sender': newsletter['sender'],
                        'original_message_id': newsletter['message_id'],
                        'processing_date': datetime.now().isoformat(),
                        'source_type': 'newsletter'
                    }
                )
                
                success = await self.knowledge_center.vector_store.add_document(knowledge_doc)
                if success:
                    added_count += 1
                    print(f"✅ Added: {newsletter['subject'][:50]}...")
                else:
                    print(f"❌ Failed: {newsletter['subject'][:50]}...")
                    
            except Exception as e:
                print(f"❌ Error adding: {e}")
        
        print(f"\n🎉 Successfully added {added_count}/{len(newsletters)} Pomp Letters!")
        return added_count

async def main():
    processor = PompLetterProcessor()
    
    print("📰 THE POMP LETTER PROCESSOR")
    print("🎯 Processing Anthony Pompliano's investment newsletters...")
    
    # Process Pomp Letters
    newsletters = processor.process_pomp_letters(max_emails=30)  # Start with 30
    
    if newsletters:
        print(f"\n📊 Found {len(newsletters)} Pomp Letters:")
        
        # Group by category for display
        categories = {}
        for nl in newsletters:
            subject_lower = nl['subject'].lower()
            if 'bitcoin' in subject_lower or 'btc' in subject_lower:
                cat = 'Bitcoin Analysis'
            elif 'inflation' in subject_lower or 'fed' in subject_lower:
                cat = 'Economic Analysis'
            elif 'crypto' in subject_lower:
                cat = 'Crypto Analysis'
            else:
                cat = 'Investment Insights'
            
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(nl)
        
        for category, nls in categories.items():
            print(f"\n📈 {category} ({len(nls)} letters):")
            for nl in nls[:3]:  # Show first 3
                print(f"   • {nl['subject'][:60]}...")
        
        # Add to Knowledge Center
        added = await processor.add_pomp_letters_to_knowledge_center(newsletters)
        
        if added > 0:
            print(f"\n🔍 Search your Pomp Letter collection:")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'Pomp Bitcoin'")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'Pomp inflation'")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'Pomp investment'")
            print(f"python orion_core/knowledge/knowledge_center_phase1.py --search 'Anthony Pompliano'")
    else:
        print("💡 No Pomp Letters found to process")

if __name__ == "__main__":
    asyncio.run(main()) 