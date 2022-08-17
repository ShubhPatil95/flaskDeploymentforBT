from flask import Flask, render_template, request
import os
import joblib


webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")


def predict(data):
    model_dir_path = "/home/shubham/Dhan_deploy/End_To_End_ML_Project/model.joblib"
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    return prediction

def form_response(dict_request):
    data = dict_request.values()
    data = [list(map(float, data))]
    response = predict(data)
    return response
    
app = Flask(__name__, static_folder=static_dir,template_folder=template_dir)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                dict_req = dict(request.form)
                response = form_response(dict_req)
                return render_template("index.html", response=response)
        except Exception as e:
            print("e")
            error = {"error": e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)