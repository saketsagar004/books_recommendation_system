from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open("popular_50.pkl","rb"))
pt = pickle.load(open("pt.pkl","rb"))
books = pickle.load(open("books.pkl","rb"))
books_50 = pickle.load(open("filter_rating_50.pkl","rb"))

similarity_scores = pickle.load(open("similarity_scores.pkl","rb"))

app = Flask(__name__,template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html",
                            book_name = list(popular_df["Book-Title"].values),
                           author=list(popular_df["Book-Author"].values),
                           image=list(popular_df["Image-URL-M"].values),
                           votes=list(popular_df["Num_rating"].values),
                           ratings=list(popular_df["avg_rating"].values)

                           )
@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html",
                           book_names = list(pt.index.values)
                           )

@app.route("/recommend_books",methods=["GET"])
def recommend():
    user_input = request.args.get("user_input")


    index = np.where(pt.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:10]
    data = []
    for book in similar_books:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[book[0]]]

        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(item)
    print(data)


    return render_template("recommend.html",data=data,
                            book_names=list(pt.index.values)
                           )

@app.route("/search",methods=["GET"])
def recommended():
    user_input = request.args.get("user_input")

    index = np.where(pt.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:10]
    data = []
    for book in similar_books:
        item = []
        temp_df = books[books["Book-Title"] == pt.index[book[0]]]

        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(item)
    print(data)

    return render_template("recommend.html",data=data,
                           book_names=list(pt.index.values)
                           )

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)