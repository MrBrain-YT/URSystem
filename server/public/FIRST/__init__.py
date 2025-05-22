from utils.public_loader.loader import loader
app = loader.app

@app.route("/mymodule")
def my_module():
    # home site
    return """<h1>Hello user!</h1>"""

def return_app():
    return app