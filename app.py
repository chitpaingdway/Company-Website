import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- NEW FUNCTION: Sends the professional reply to the CLIENT ---
def send_reply_to_client(user_data):
    sender_email = "chit.paingdway@gmail.com"
    sender_password = "uygdjuldmiwdfhbh" 
    client_email = user_data['email']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Thank you for contacting Necmergens"
    msg['From'] = f"Necmergens Corporate <{sender_email}>"
    msg['To'] = client_email

    # The template for the client (includes logo and signature)
    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #334155; line-height: 1.6;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background-color: #0f172a; padding: 25px; text-align: center;">
                <img src="https://www.necmergens.com/static/logo.png" alt="Necmergens" style="max-height: 50px;">
            </div>
            <div style="padding: 40px; background: white;">
                <h2 style="color: #059669; margin-top: 0;">Hello {user_data['name']},</h2>
                <p>Thank you for reaching out to <strong>Necmergens Corporate Services</strong>.</p>
                <p>We have received your inquiry regarding <b>{user_data['service']}</b>. One of our expert advisors will review your requirements and get back to you within 24 hours.</p>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #059669;">
                    <p style="margin: 0; font-weight: bold; color: #0f172a;">Best Regards,</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #059669; font-weight: 800;">Necmergens Team</p>
                    <p style="margin: 5px 0; font-size: 13px; color: #64748b;">
                        XL Tower Room 502, Marasi Drive, Business Bay<br>
                        Dubai, United Arab Emirates
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 14px;">
                        <strong>Phone:</strong> +971 52 355 7541<br>
                        <strong>Email:</strong> contact@necmergens.com
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, client_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Reply Error: {e}")
        return False

# --- YOUR EXISTING ADMIN FUNCTION ---
def send_email_to_admin(user_data):
    sender_email = "chit.paingdway@gmail.com"
    sender_password = "uygdjuldmiwdfhbh"
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
                <p><strong>Name:</strong> {user_data['name']}</p>
                <p><strong>Email:</strong> {user_data['email']}</p>
                <p><strong>Phone:</strong> {user_data['phone']}</p>
                <p><strong>Service:</strong> {user_data['service']}</p>
                <p><strong>Message:</strong> {user_data['description']}</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-started', methods=['POST'])
def get_started():
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'service': request.form.get('service'),
        'description': request.form.get('description')
    }
    
    # 1. Notify you (Admin)
    admin_success = send_email_to_admin(data)
    
    # 2. Reply to the Client (Auto-reply)
    if admin_success:
        send_reply_to_client(data) 
        return jsonify({"status": "success", "message": "Enquiry sent successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send"}), 500

if __name__ == '__main__':
    app.run(debug=True)
