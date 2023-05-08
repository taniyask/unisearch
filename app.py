import os
from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import recommendation_svd



data = pd.read_csv("univ.csv")
classified = pd.read_csv("classified.csv")

app = Flask(__name__)



#with open('scaler.pkl', 'wb') as f:
   #pickle.dump(scaler, f)

#with open('svd.pkl', 'wb') as f:
    #pickle.dump(svd, f)
    
    
@app.route('/')
def home():
   return render_template('Home.html')

@app.route('/profile_eval')
def profile_eval():
    return render_template('Profile_Eval.html')

@app.route('/university_eval', methods =["GET","POST"])
def university_eval():
    if request.method == "POST":


        gre_verbal = request.form.get("verbal")
        gre_quant = request.form.get("quant")
        ielts_score = request.form.get("ielts")
        undergrad_gpa = request.form.get("gpa")


        if int(gre_verbal) >= 155 and int(gre_quant) >= 155 and float(ielts_score) >= 7.5 and float(undergrad_gpa) > 9:
            results = recommendation_svd.model(gre_verbal, gre_quant, ielts_score, undergrad_gpa)
            return render_template("Reco_page.html", result = results)
    return render_template("Profile_Eval.html")




@app.route('/university', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        uni = request.form.get("university")
        univ_name = data[data["UNI_NAME"]==uni]["UNI_NAME"]
        rank = data[data["UNI_NAME"]==uni]["QS_Ranking"]
        link = data[data["UNI_NAME"]==uni]["Link"]
        loc = data[data["UNI_NAME"]==uni]["Location"]
        overall_ranking = data[data["UNI_NAME"]==uni]["Overall_Ranking"]
        img = os.path.join("static/img", str(int(rank.values[0]))+".png")
        positive_review = classified[classified["UNI_NAME"]==uni][classified["Sentiment"]=="Positive"][classified['Type']=='Comment']
        negative_review = classified[classified["UNI_NAME"]==uni][classified["Sentiment"]=="Negative"][classified['Type']=='Comment']
        neutral_review = classified[classified["UNI_NAME"]==uni][classified["Sentiment"]=="Neutral"][classified['Type']=='Comment']
        # print(positive_review.values[2])
        result = [int(rank.values[0]), str(link.values[0]), str(loc.values[0]),  str(univ_name.values[0]), img, positive_review.values, int(len(positive_review)), negative_review.values ,int(len(negative_review)), neutral_review.values, int(len(neutral_review)), int(overall_ranking.values[0])]
        # print(result)
        return render_template("College_deets.html", result = result)
    return render_template("College_deets.html")

@app.route('/university/<uni_name>', methods =["GET", "POST"])
def gfg1(uni_name):
    # create the page for the university given by name uniname
    uni = uni_name
    univ_name = data[data["UNI_NAME"]==uni]["UNI_NAME"]
    rank = data[data["UNI_NAME"]==uni]["QS_Ranking"]
    link = data[data["UNI_NAME"]==uni]["Link"]
    loc = data[data["UNI_NAME"]==uni]["Location"]
    overall_ranking = data[data["UNI_NAME"]==uni]["Overall_Ranking"]
    img = os.path.join("/static/img", str(int(rank.values[0]))+".png")
    positive_review = classified[classified["UNI_NAME"]==uni][classified["Sentiment"]=="Positive"][classified['Type']=='Comment']
    negative_review = classified[classified["UNI_NAME"]==uni][classified["Sentiment"]=="Negative"][classified['Type']=='Comment']
    neutral_review = classified[classified["UNI_NAME"]==uni][classified["Sentiment"]=="Neutral"][classified['Type']=='Comment']

    result = [int(rank.values[0]), str(link.values[0]), str(loc.values[0]),  str(univ_name.values[0]), img, positive_review.values, int(len(positive_review)), negative_review.values ,int(len(negative_review)), neutral_review.values, int(len(neutral_review)), int(overall_ranking.values[0])]

    return render_template("College_deets.html", result = result)
    
if __name__ == '__main__':
    from os import path, walk
    app.secret_key = "super secret key"
    extra_dirs = ['.',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0', extra_files=extra_files)
    # app.config[‘TEMPLATES_AUTO_RELOAD’] = True
    # app.config[‘SEND_FILE_MAX_AGE_DEFAULT’] = 0
    # app.run(debug=True)