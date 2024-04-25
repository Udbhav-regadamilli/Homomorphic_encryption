from flask import Flask, render_template, request, session
from homomorphic import generate_key, concatenate_strings
import time
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'Udbhav@958'
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the filesystem
app.config['SESSION_FILE_DIR'] = './Session'

Session(app)

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/index3.html')
def homePage():
    return render_template('index3.html')

@app.route('/index1.html')
def about():
    return render_template('index1.html')

@app.route('/page3.html')
def encryption():
    print(session['e_time'])
    return render_template('page3.html', messages=session['e_time'])

@app.route('/key.html', methods=['POST', 'GET'])
def key():
    print(request.method)
    if request.method == 'POST':
        start = time.time()
        n, e, d = generate_key()
        end = time.time()
        
        session['e'] = e
        session['d'] = d
        session['n'] = n
        session['key_time'] = end - start

        message = [e, d, end - start]
        return render_template('key.html', messages=message)
    else:
        if 'e' in session.keys():
            e = session['e']
            d = session['d']
            key_time = session['key_time']

            message = [e, d, key_time]
            return render_template('key.html', messages=message)
        return render_template('key.html')

@app.route('/form1.html', methods=['POST', 'GET'])
def rsa():
    if request.method == 'POST':
        e = session['e']
        d = session['d']
        n = session['n']

        encryption = 0
        decryption = 0
        result_str = ""

        fileName = request.form.get('fileUpload')

        if not fileName:
            msg1 = request.form.get('input1')
            affineEncryption, result_str, encryption, decryption, encrypted_text = concatenate_strings(msg1, n, e, d, encryption, decryption)
        else:
            count = 0

            with open(fileName, 'r') as file:
                for line in file:
                    count += 1
                    affineEncryption, concatenated_str, encryption, decryption, encrypted_text = concatenate_strings(line, n, e, d, encryption, decryption)
                    result_str += concatenated_str
                    print(f"line {count}: done")

        session['e_mul'] = encrypted_text
        session['d_mul'] = result_str
                    
        session['e_time'] = encryption
        session['d_time'] = decryption
        
        session['affineEncryption'] = affineEncryption

        print("Encryption: ", encryption)
        print("Decryption: ", decryption)
        return render_template('homomorphic.html', e_messages=encrypted_text, d_messages=result_str)
    else:
        return render_template('form1.html')

@app.route('/homomorphic.html')
def homomorphic():
    encrypted_text = session['e_mul']
    return render_template('homomorphic.html', e_messages=encrypted_text)

@app.route('/result.html')
def result():
    message = session['d_time']
    return render_template('result.html', message=message)

@app.route('/affineEncryption')
def affineEncryption():
    return render_template('affineEnc.html', message=session['affineEncryption'])

@app.route('/affineDecryption')
def affineDecryption():
    result_str = session['d_mul']
    return render_template('affineDecryption.html', message=result_str)

if __name__ == '__main__':
    app.run(debug=True)
