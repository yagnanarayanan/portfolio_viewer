from flask import Flask,render_template,redirect,url_for
app =  Flask(__name__)
@app.route("/")
def home():
    return redirect(url_for("homepage"))
@app.route("/about")
def about_page():
    return render_template("about.html")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html", content = content[content_length - 9 :content_length])
@app.route("/history")
def history():
    return render_template("history.html", content=content)
@app.route("/test")
def testing():
    return render_template("testing.html", content = content[content_length - 9 :content_length])
if __name__ == "__main__":
    content = []
    with open("portfolio_val_test.txt","r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        content.append(line.rstrip())
    content_length = len(content)
    app.run(debug=True)