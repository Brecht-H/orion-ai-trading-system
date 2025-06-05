"""
📧 Email Checker Module for AI & Crypto Newsletters
Automated email processing and newsletter detection system
"""

import imaplib
import email
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import sqlite3

class EmailChecker:
    """
    Advanced email checker for AI and Crypto newsletters
    Integrates with AC Mailbox configuration from .env
    """
    
    def __init__(self):
        self.setup_logging()
        self.load_email_config()
        self.setup_database()
        
    def setup_logging(self):
        """Configure logging for email operations"""
        log_dir = Path("logs/knowledge_center")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "newsletter_email.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_email_config(self):
        """Load email configuration from environment variables"""
        self.email = os.getenv('AC_EMAIL', 'abhartjes@icloud.com')
        self.password = os.getenv('AC_PASSWORD', 'qcqt-jrpp-bdhf-usto')
        self.imap_server = os.getenv('AC_IMAP_SERVER', 'imap.mail.me.com')
        self.imap_port = int(os.getenv('AC_IMAP_PORT', '993'))
        
        self.logger.info(f"Email config loaded for: {self.email}")
        
    def setup_database(self):
        """Setup newsletter tracking database"""
        db_path = Path("databases/sqlite_dbs/newsletter_tracking.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(str(db_path))
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                subject TEXT NOT NULL,
                received_date TIMESTAMP NOT NULL,
                content_preview TEXT,
                category TEXT,
                processed BOOLEAN DEFAULT FALSE,
                relevance_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
    def connect_to_email(self) -> Optional[imaplib.IMAP4_SSL]:
        """Establish secure connection to email server"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email, self.password)
            self.logger.info("Successfully connected to email server")
            return mail
        except Exception as e:
            self.logger.error(f"Failed to connect to email: {e}")
            return None
            
    def identify_newsletters(self, mail: imaplib.IMAP4_SSL, days_back: int = 7) -> List[Dict[str, Any]]:
        """Identify newsletters from the last N days"""
        newsletters = []
        
        # Newsletter keywords for filtering
        newsletter_keywords = [
            'newsletter', 'crypto', 'bitcoin', 'ethereum', 'defi', 'nft',
            'blockchain', 'ai', 'artificial intelligence', 'machine learning',
            'trading', 'market', 'analysis', 'trend', 'signal'
        ]
        
        try:
            mail.select('INBOX')
            
            # Search for emails from the last N days
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            _, message_ids = mail.search(None, f'(SINCE {since_date})')
            
            for msg_id in message_ids[0].split():
                try:
                    _, msg_data = mail.fetch(msg_id, '(RFC822)')
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    sender = email_message['From']
                    subject = email_message['Subject'] or ''
                    date = email_message['Date']
                    
                    # Check if this looks like a newsletter
                    content_preview = self.extract_content_preview(email_message)
                    
                    if self.is_newsletter(sender, subject, content_preview, newsletter_keywords):
                        newsletter_data = {
                            'sender': sender,
                            'subject': subject,
                            'date': date,
                            'content_preview': content_preview[:500],  # First 500 chars
                            'category': self.categorize_newsletter(subject, content_preview),
                            'relevance_score': self.calculate_relevance_score(subject, content_preview, newsletter_keywords)
                        }
                        newsletters.append(newsletter_data)
                        
                except Exception as e:
                    self.logger.warning(f"Error processing email {msg_id}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error searching emails: {e}")
            
        self.logger.info(f"Found {len(newsletters)} newsletters")
        return newsletters
        
    def extract_content_preview(self, email_message) -> str:
        """Extract readable content preview from email"""
        content = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            
        return content.strip()
        
    def is_newsletter(self, sender: str, subject: str, content: str, keywords: List[str]) -> bool:
        """Determine if an email is likely a newsletter"""
        # Check sender patterns
        newsletter_senders = [
            'newsletter', 'noreply', 'news', 'updates', 'crypto', 'ai',
            'coindesk', 'cointelegraph', 'decrypt', 'blockworks'
        ]
        
        sender_lower = sender.lower()
        subject_lower = subject.lower()
        content_lower = content.lower()
        
        # Check for newsletter sender patterns
        sender_match = any(pattern in sender_lower for pattern in newsletter_senders)
        
        # Check for newsletter keywords in subject/content
        keyword_match = any(keyword.lower() in subject_lower or keyword.lower() in content_lower 
                           for keyword in keywords)
        
        # Check for unsubscribe links (common in newsletters)
        unsubscribe_match = 'unsubscribe' in content_lower
        
        return sender_match or (keyword_match and unsubscribe_match)
        
    def categorize_newsletter(self, subject: str, content: str) -> str:
        """Categorize newsletter by topic"""
        subject_lower = subject.lower()
        content_lower = content.lower()
        
        if any(word in subject_lower or word in content_lower 
               for word in ['bitcoin', 'ethereum', 'crypto', 'defi', 'nft', 'blockchain']):
            return 'CRYPTO'
        elif any(word in subject_lower or word in content_lower 
                 for word in ['ai', 'artificial intelligence', 'machine learning', 'llm']):
            return 'AI'
        elif any(word in subject_lower or word in content_lower 
                 for word in ['trading', 'market', 'analysis', 'signal']):
            return 'TRADING'
        else:
            return 'GENERAL'
            
    def calculate_relevance_score(self, subject: str, content: str, keywords: List[str]) -> float:
        """Calculate relevance score based on keyword density"""
        text = (subject + " " + content).lower()
        
        keyword_count = sum(1 for keyword in keywords if keyword.lower() in text)
        max_possible = len(keywords)
        
        return (keyword_count / max_possible) if max_possible > 0 else 0.0
        
    def save_newsletters(self, newsletters: List[Dict[str, Any]]) -> int:
        """Save newsletters to database"""
        saved_count = 0
        
        for newsletter in newsletters:
            try:
                # Check if already exists
                cursor = self.conn.execute(
                    "SELECT id FROM newsletter_emails WHERE sender = ? AND subject = ? AND received_date = ?",
                    (newsletter['sender'], newsletter['subject'], newsletter['date'])
                )
                
                if not cursor.fetchone():
                    self.conn.execute('''
                        INSERT INTO newsletter_emails 
                        (sender, subject, received_date, content_preview, category, relevance_score)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        newsletter['sender'],
                        newsletter['subject'], 
                        newsletter['date'],
                        newsletter['content_preview'],
                        newsletter['category'],
                        newsletter['relevance_score']
                    ))
                    saved_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error saving newsletter: {e}")
                
        self.conn.commit()
        self.logger.info(f"Saved {saved_count} new newsletters")
        return saved_count
        
    def check_for_new_newsletters(self, days_back: int = 1) -> Dict[str, Any]:
        """Main method to check for new newsletters"""
        self.logger.info(f"Checking for newsletters from last {days_back} days")
        
        mail = self.connect_to_email()
        if not mail:
            return {'success': False, 'error': 'Failed to connect to email'}
            
        try:
            newsletters = self.identify_newsletters(mail, days_back)
            saved_count = self.save_newsletters(newsletters)
            
            mail.logout()
            
            return {
                'success': True,
                'newsletters_found': len(newsletters),
                'newsletters_saved': saved_count,
                'categories': self.get_category_summary()
            }
            
        except Exception as e:
            self.logger.error(f"Error in newsletter check: {e}")
            return {'success': False, 'error': str(e)}
            
    def get_category_summary(self) -> Dict[str, int]:
        """Get summary of newsletters by category"""
        cursor = self.conn.execute('''
            SELECT category, COUNT(*) as count 
            FROM newsletter_emails 
            WHERE processed = FALSE 
            GROUP BY category
        ''')
        
        return dict(cursor.fetchall())
        
    def get_unprocessed_newsletters(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get unprocessed newsletters for analysis"""
        cursor = self.conn.execute('''
            SELECT id, sender, subject, content_preview, category, relevance_score, received_date
            FROM newsletter_emails 
            WHERE processed = FALSE 
            ORDER BY relevance_score DESC, received_date DESC
            LIMIT ?
        ''', (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    def mark_as_processed(self, newsletter_ids: List[int]):
        """Mark newsletters as processed"""
        placeholders = ','.join('?' * len(newsletter_ids))
        self.conn.execute(f'''
            UPDATE newsletter_emails 
            SET processed = TRUE 
            WHERE id IN ({placeholders})
        ''', newsletter_ids)
        self.conn.commit()

# Example usage and testing
if __name__ == "__main__":
    checker = EmailChecker()
    result = checker.check_for_new_newsletters(days_back=7)
    print(f"Newsletter check result: {result}")
    
    unprocessed = checker.get_unprocessed_newsletters()
    print(f"Found {len(unprocessed)} unprocessed newsletters")
    for newsletter in unprocessed[:3]:  # Show first 3
        print(f"- {newsletter['category']}: {newsletter['subject'][:50]}...") 