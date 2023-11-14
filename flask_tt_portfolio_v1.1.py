from flask import Flask,render_template,redirect,url_for,request
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
@app.route("/test2",  methods = ["POST", "GET"])
def try_calc():
    if request.method == "POST":
        take_home_pay = float(request.form["take_home"])
        savings_rate = float(request.form["savings_rate"])
        with open("form_post_data.txt","w",encoding='utf-8') as f1:
            f1.write(str(take_home_pay) + "|" + str(savings_rate))
        savings_actual = savings_calc()
        with open("form_post_data_processed.txt","w",encoding='utf-8') as f2:
            f2.write(str(savings_actual))
        return redirect(url_for("processed",th = savings_actual))
    else:
        return render_template("form_data.html")
@app.route("/test2_result")
def processed():
    with open("form_post_data_processed.txt", "r", encoding='utf-8') as f2:
        content_processed = f2.readlines()
    return render_template("test2_result.html",th=content_processed[0])

def savings_calc():
    data = []
    with open("form_post_data.txt","r", encoding='utf-8') as f:
        d = f.readlines()
        for line1 in d:
            data.append(line1.split("|"))
    return (float(data[0][0])*float(data[0][1]))/100

if __name__ == "__main__":
    content = []
    with open("portfolio_val_test.txt","r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        content.append(line.rstrip())
    content_length = len(content)
    app.run(debug=True)
    savings_calc()