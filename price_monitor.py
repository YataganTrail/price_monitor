import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime
import json

def check_prices():
    # Email configuration - using environment variables for security
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')
    
    # Load items to monitor from JSON file
    with open('items_to_monitor.json', 'r') as f:
        items = json.load(f)
    
    print(f"Monitoring {len(items)} items for price drops")
    
    for item in items:
        name = item['name']
        url = item['url']
        css_selector = item['css_selector']
        target_price = item['target_price']
        
        print(f"\nChecking price for: {name}")
        print(f"URL: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            price_element = soup.select_one(css_selector)
            
            if price_element:
                price_text = price_element.text.strip()
                # Extract digits and decimal point
                price_digits = ''.join(c for c in price_text if c.isdigit() or c == '.')
                
                if price_digits:
                    current_price = float(price_digits)
                    print(f"Current price: ${current_price}")
                    
                    if current_price <= target_price:
                        print(f"Price drop detected! (${current_price} <= ${target_price})")
                        
                        # Send email notification
                        subject = f"Price Drop Alert: {name}"
                        body = f"Price drop detected!\n\nItem: {name}\nCurrent price: ${current_price}\nTarget price: ${target_price}\nURL: {url}\n\nChecked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        
                        msg = MIMEText(body)
                        msg['Subject'] = subject
                        msg['From'] = sender_email
                        msg['To'] = sender_email  # Sending to yourself
                        
                        with smtplib.SMTP(smtp_server, smtp_port) as server:
                            server.starttls()
                            server.login(sender_email, password)
                            server.send_message(msg)
                        
                        print("Alert email sent successfully!")
                        
                    else:
                        print(f"Current price (${current_price}) is still above target (${target_price})")
                else:
                    print("Could not extract price from text:", price_text)
            else:
                print(f"Price element not found with selector: {css_selector}")
                
        except Exception as e:
            print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    check_prices()
