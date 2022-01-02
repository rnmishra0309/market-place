from com import app

if __name__=="__main__":
    HOST = '127.0.0.1'
    PORT = '8080'
    app.run(HOST, PORT, debug=True)