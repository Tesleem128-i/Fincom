from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

@app.route('/send-mail', methods=['GET', 'POST'])
def send_mail():
    if request.method == 'POST':
        msg = Message("Test Email", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=["recipient@example.com"])
        msg.body = "Hello, this is a test email!"
        mail.send(msg)
        return "Email Sent Successfully!"

    return render_template("send_mail.html")

if __name__ == '__main__':
    app.run(debug=True)
