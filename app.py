from flask import Flask,render_template,request
import comments
import views
import likes
import dislikes
app = Flask(__name__)
@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/submit',methods = ['POST','GET'])
def process(): 
    datas = request.form.get('url') 
    # process the data using Python code
    view = views.get_input(datas)
    like = likes.get_input(datas)
    dislike = dislikes.get_input(datas)
    result,polarity = comments.get_input(datas) 
    return render_template('output.html',like = like,view = view,polarity = polarity,dislikes=dislike,result = result)

if __name__ == '__main__':
    app.run(debug=True)