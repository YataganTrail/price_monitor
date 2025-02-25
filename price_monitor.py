import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime

def check_price():
    # Configuration
    url = "https://www.countryroad.co.nz/regular-fit-australian-good-earth-cotton-oxford-shirt-60297833-100"
    css_selector = "#__next > div.relative.z-0.flex.h-full.min-h-screen.flex-col > div.relative.flex.grow.flex-col > main > div.relative > div.py-ds-s.flex.flex-col.justify-between.md\:flex-row.items-start.pt-0 > div.md\:pl-ds-m.px-ds-s.float-right.my-2.w-full.md\:pr-3.lg\:w-\[30rem\].md\:top-18.relative.md\:sticky.md\:mr-9 > div.flex.flex-col.justify-between > div:nth-child(1) > section > div > div.price_break > div > span > span.value"
    target_price = 300.0
    
    # Email configuration - using environment variables for security
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')
    
    print(f"Checking price for: {url}")
    
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
                    subject = "Price Drop Alert!"
                    body = f"Price drop detected!\n\nItem: Country Road Oxford Shirt\nCurrent price: ${current_price}\nTarget price: ${target_price}\nURL: {url}\n\nChecked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    
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
        print(f"Error: {e}")

if __name__ == "__main__":
    check_price()
