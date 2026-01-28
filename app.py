import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def send_email_to_admin(user_data):
    # Email configuration
    sender_email = "chit.paingdway@gmail.com"
    sender_password = "uygdjuldmiwdfhbh"  # Gmail App Password
    receiver_email = "chit.dwe@burnsys.io"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🚀 New Inquiry from {user_data['name']} - {user_data['service']}"
    msg['From'] = f"Necmergens Website <{sender_email}>"
    msg['To'] = receiver_email

    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6; padding: 40px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="background-color: #059669; padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px;">NECMERGENS</h1>
                <p style="color: #d1fae5;">New Business Inquiry Received</p>
            </div>
            <div style="padding: 30px; color: #334155;">
                <h2 style="color: #064e3b; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;">Details</h2>
                <p><strong>Name:</strong> {user_data['name']}</p>
                <p><strong>Email:</strong> {user_data['email']}</p>
                <p><strong>Phone:</strong> {user_data['phone']}</p>
                <p><strong>Service:</strong> {user_data['service']}</p>
                <h2 style="color: #064e3b; margin-top: 20px;">Message</h2>
                <div style="background: #f8fafc; padding: 15px; border-radius: 10px; font-style: italic;">
                    "{user_data['description']}"
                </div>
            </div>
            <div style="background: #f1f5f9; padding: 15px; text-align: center; font-size: 12px; color: #64748b;">
                Sent from Necmergens Automated System
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-started', methods=['POST'])
def get_started():
    # Capture all fields from the form
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'service': request.form.get('service'),
        'description': request.form.get('description')
    }
    
    # Send email
    success = send_email_to_admin(data)
    
    if success:
        return jsonify({"status": "success", "message": "Email sent"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send email"}), 500

if __name__ == '__main__':
    app.run(debug=True)
