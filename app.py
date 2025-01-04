from flask import Flask,render_template,request
import pickle
import numpy as np


popular_df=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Number of Ratings'].values),
                           ratings = list(popular_df['Average of Ratings'].values));


@app.route("/recommend")
def recommend_ui():
    return render_template('recommend.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Number of Ratings'].values),
                           ratings = list(popular_df['Average of Ratings'].values));


@app.route("/recommend_books",methods=["post"])
def recommend_books_ui():
    print("hii")
    user_input = request.form.get("user_input")
    print(user_input)
    index_of_book = np.where(pt.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index_of_book])),key=lambda x:x[1],reverse=True)[1:5]
    similar_books

    data = []
    for i in similar_books:
        item = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]         #getting the books that match 
        item.extend(list(temp.drop_duplicates("Book-Title")["Book-Title"]))
        item.extend(list(temp.drop_duplicates("Book-Title")["Book-Author"]))
        item.extend(list(temp.drop_duplicates("Book-Title")["Image-URL-M"]))

        data.append(item)

    return render_template("recommend.html",data=data)


if __name__ == "__main__":
    app.run(debug=True)