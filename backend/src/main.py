from flask import Flask, render_template
import logging

app = Flask(__name__)
@app.route('/')

def index():
    return render_template('index.html')
    
def main():
    logging.info("Starting Python FLask")
    app.run(debug=True)

if __name__ == '__main__':
    main()