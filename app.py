import json
import uuid
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db_string = 'postgresql://postgres:example@localhost:5432/tree'
db = SQLAlchemy()
app = Flask(__name__)
engine = create_engine(db_string)

app.config["SQLALCHEMY_DATABASE_URI"] = db_string
db.init_app(app)


class Tree(db.Model):
    __tablename__ = 'tree'
    user_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    tree = db.Column(db.String)
    modified = db.Column(db.String, nullable=True)

    def __init__(self, user_id, tree, modified):
        self.user_id = user_id
        self.tree = tree
        self.modified = modified


# Add these lines to create the tables
with app.app_context():
    db.drop_all() # todo delete this line in production
    db.create_all()


def tree_as_json(tree):
    return {
        "user_id": tree.user_id,
        "tree": tree.tree,
        "modified": tree.modified
    }


@app.route('/tree', methods=['POST'])
def post_tree():
    print("POST TREE")
    data = request.get_json()
    data_tree = {
        'user_id': data['userId'],
        'lastModified': data['modified'],
        'tree': data['tree'],
    }
    # check if tree for user already exists
    tree = Tree.query.filter_by(user_id=data_tree['user_id']).first()
    if tree is None:
        # tree does not exist, create new db tree
        print(f"Tree for user {data_tree['user_id']} does not exist")
        tree = Tree(data_tree['user_id'], data_tree['tree'], data_tree['lastModified'])
        db.session.add(tree)
        db.session.commit()
        return tree_as_json(tree).get("tree"), 201
    else:
        print(f"Tree for user {data_tree['user_id']} exists")
        print(f"DB last modified: {tree.modified}\n Request last modified: {data_tree['lastModified']}")
        # pretty print tree
        if int(tree.modified) < data_tree['lastModified']:
            # tree in db is older, update db tree
            print(f"tree in db is older, update db tree")
            tree.tree = data_tree['tree']
            tree.modified = data_tree['lastModified']
            db.session.add(tree)
            db.session.commit()
            return tree_as_json(tree).get("tree"), 200
        else:
            print(f"tree in db is newer/same, return db tree")
            # tree in db is newer/same, return db tree
            return tree_as_json(tree).get("tree"), 200


@app.route('/tree/<userId>', methods=['GET'])
def handle_get(userId):
    print(userId)
    tree = Tree.query.filter_by(user_id=userId).first()
    if tree is None:
        # create initial tree
        first_date = datetime(1970, 1, 1)
        time_since = datetime.now() - first_date
        seconds = int(time_since.total_seconds())
        initial_tree = {
          "modified": seconds,
          "root": {
            "uuid": str(uuid.uuid4()),
            "name": "Root",
            "description": "This is the root node",
            "completed": None,
            "dueDate": None,
            "priority": 1,
            "children": []
          }
        }
        print(initial_tree.get("modified"))
        print(type(initial_tree.get("modified")))
        # add tree to db
        tree = Tree(userId, json.dumps(initial_tree), str(initial_tree.get("modified")))
        db.session.add(tree)
        db.session.commit()
        return tree_as_json(tree).get("tree"), 201
    else:
        return tree_as_json(tree).get("tree"), 200


if __name__ == '__main__':
    app.run(debug=True)


