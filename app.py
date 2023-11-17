import os
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)


# Fetch the Firebase Admin SDK JSON from GitHub Secrets
firebase_admin_secret = os.getenv('FIREBASE_ADMIN_SDK_JSON')

# Initialize Firebase
cred = credentials.Certificate(firebase_admin_secret)

firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']

        if email:
            # Check if the email already exists in Firestore
            email_exists = False
            email_collection = db.collection('subscribers')
            docs = email_collection.stream()
            for doc in docs:
                if doc.to_dict().get('email') == email:
                    email_exists = True
                    break

            if not email_exists:
                # Save the email to Firestore
                email_data = {"email": email}
                email_collection.add(email_data)

                return redirect(url_for('success'))
            else:
                error_message = "You've already subscribed."
                return render_template('index.html', error_message=error_message)

        else:
            error_message = "Please provide a valid email address."
            return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=None)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
