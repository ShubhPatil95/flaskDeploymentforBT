from flask import Flask, render_template, request
import os
import pickle
import logging.handlers
import logging

webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir,template_folder=template_dir)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                dict_req = dict(request.form)
                # response = form_response(dict_req)
                data = dict_req.values()
                data=list(data)
                data[-1]=[1 if data[-1]=="1" else 0][0]
                data = [list(map(float, data))]
                
                # response = predict(data)
                model_dir_path = "./regressor.pkl"
                model = pickle.load(open(model_dir_path,"rb"))
                scaler_x_path= "./Scaler_x.pkl"
                scaler_x=pickle.load(open(scaler_x_path,"rb"))
                data=scaler_x.transform(data)
                prediction = model.predict(data)
                scaler_y_path= "./Scaler_y.pkl"
                scaler_y=pickle.load(open(scaler_y_path,"rb"))
                prediction=scaler_y.inverse_transform(prediction)[0][0]
                
                return render_template("index.html", response=prediction)
        except Exception as e:
            print("e")
            error = {"error": e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)