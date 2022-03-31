from flask import Flask , jsonify , request 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Setting Configuration
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post_database.db'

db = SQLAlchemy(app)
marsh = Marshmallow(app)

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

# Post Model Schema for API
class PostSchema(marsh.Schema):
    class Meta :
        fields = ['id' , 'post', 'description']
 

@app.route('/', methods=['GET' , 'POST'])
def PostAPI():
    if request.method == 'GET' :
        post = Post.query.all()
        if not post :
            return jsonify({"Not Found" : "No such data exist"})    
        post_schema = PostSchema(many=True)
        result = post_schema.dump(post)
        return jsonify(result)

    if request.method == 'POST' :
        print("POST : ",request.json['post'])
        post = request.json['post']
        description = request.json['description']
        postdb = Post(post=post,description=description)
        db.session.add(postdb)
        db.session.commit()
        return jsonify({"Success":"Data save succesfully in db."})
    
@app.route('/<int:id>',methods=['GET' , 'DELETE', 'PUT'])
def PostDetailAPI(id):
    if request.method == 'GET' :
        post = Post.query.get(id)
        if not post :
            return jsonify({"Not Found" : "No such data exist"})
        schema = PostSchema()
        data = schema.dump(post)
        return schema.jsonify(data)
    if request.method == 'DELETE' :
        post = Post.query.get(id)
        if not post :
            return jsonify({"Not Found" : "No such data exist"})
        db.session.delete(post)
        db.session.commit()
        return jsonify({'result' : 'user deleted successfully.'})

    if request.method == 'PUT' :
        post = Post.query.get(id)
        if not post :
            return jsonify({"Not Found" : "No such data exist"})
        post.post = request.json['post']
        post.description = request.json['description']
        db.session.commit()
        return jsonify({'result' : 'user updated successfully.'})
        


# if __name__ == "__main__":
#     app.run(debug=True)