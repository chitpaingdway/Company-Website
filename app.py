import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart # အသစ်ထည့်ထားသည်
from flask import Flask, render_template, request

app = Flask(__name__)

def send_email_to_admin(user_data):
    sender_email = "chit.paingdway@gmail.com"
    sender_password = "uygdjuldmiwdfhbh" # App Password ကို ဒီမှာပြန်ထည့်ပါ
    receiver_email = "chit.dwe@burnsys.io"

    # Create Message Container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🚀 New Inquiry: {user_data['company']}"
    msg['From'] = f"Necmergens Web <{sender_email}>"
    msg['To'] = receiver_email

    # Professional HTML Template
    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="background-color: #059669; padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px; letter-spacing: 2px;">NECMERGENS</h1>
                <p style="color: #d1fae5; margin: 5px 0 0 0;">New Business Inquiry Received</p>
            </div>
            
            <div style="padding: 30px; color: #334155;">
                <h2 style="color: #064e3b; font-size: 18px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;">Client Details</h2>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                    <tr>
                        <td style="padding: 10px 0; color: #64748b; width: 35%;">Full Name:</td>
                        <td style="padding: 10px 0; font-weight: bold;">{user_data['name']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #64748b;">Company:</td>
                        <td style="padding: 10px 0; font-weight: bold;">{user_data['company']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #64748b;">Email Address:</td>
                        <td style="padding: 10px 0; font-weight: bold;"><a href="mailto:{user_data['email']}" style="color: #2563eb; text-decoration: none;">{user_data['email']}</a></td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #64748b;">Phone Number:</td>
                        <td style="padding: 10px 0; font-weight: bold;">{user_data['phone']}</td>
                    </tr>
                </table>

                <h2 style="color: #064e3b; font-size: 18px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; margin-top: 30px;">Inquiry Description</h2>
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; margin-top: 15px; font-style: italic; line-height: 1.6; color: #475569;">
                    "{user_data['description']}"
                </div>

                <div style="margin-top: 30px; text-align: center;">
                    <a href="tel:{user_data['phone']}" style="background-color: #059669; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">Call Client Now</a>
                </div>
            </div>

            <div style="background-color: #f1f5f9; padding: 20px; text-align: center; color: #94a3b8; font-size: 12px;">
                This inquiry was sent from the contact form on necmergens.com<br>
                © 2026 Necmergens Business Setup Services.
            </div>
        </div>
    </body>
    </html>
    """

    # Attach HTML content
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

# ... ကျန်တဲ့ @app.route logic တွေက အရင်အတိုင်းပဲ ထားပါ ...

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-started', methods=['POST'])
def get_started():
    data = {
        'name': request.form.get('name'),
        'company': request.form.get('company'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'description': request.form.get('description')
    }
    success = send_email_to_admin(data)
    if success:
        return "<h1>Success!</h1><p>Your professional request has been sent.</p><a href='/'>Go Back</a>"
    else:
        return "<h1>Error!</h1>"

if __name__ == '__main__':
    app.run(debug=True)