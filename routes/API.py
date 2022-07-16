from email.policy import default
from flask import Blueprint, jsonify, request
import sys
sys.path.append("../")
from database import Engine, create_session, Article

router = Blueprint("API", __name__, url_prefix="/api")

class ArticlePostValueError(Exception):
    pass

class ArticleNotFoundError(Exception):
    pass

@router.route("/post", methods=["POST"])
def post():
    try:
        title = request.form.get("title", None, type=str)
        body = request.form.get("body", None, type=str)

        if (title is None) or (body is None) or (title == "") or (body == ""):
            raise ArticlePostValueError("タイトルと本文を入力してください")
        
        session = create_session()
        article = Article(
            title=title,
            body=body
        )
        session.add(article)
        session.commit()

        return jsonify({
            "result": True
        })
    except ArticlePostValueError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 400
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500

@router.route("/articles")
def get_articles():
    try:
        session = create_session()
        articles = session.query(Article).all()
        return jsonify([article.to_dict() for article in articles])
    except:
        return jsonify([]), 500

@router.route("/article/<int:_id>")
def get_article(_id):
    try:
        session = create_session()
        article = session.query(Article).filter(Article.id == _id).first()
        if article is None:
            raise ArticleNotFoundError("記事が存在しません")
        return jsonify({
            "result": True,
            "article": article.to_dict()
        })
    except ArticleNotFoundError as e:
        print(ArticleNotFoundError)
        return jsonify({
            "result": False,
            "message": "記事が存在しません"
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500

@router.route("/update", methods=["POST"])
def update():
    try:
        title = request.form.get("title", None, type=str)
        body = request.form.get("body", None, type=str)
        _id = request.form.get("id", None, type=int)

        if _id is None:
            raise ArticlePostValueError("idを入力してください")

        if (title is None) and (body is None) or (title == "") and (body == ""):
            raise ArticlePostValueError("タイトルと本文を入力してください")
        
        session = create_session()
        article = session.query(Article).filter(Article.id == _id).first()
        if article is None:
            raise ArticleNotFoundError("記事が見つかりません")
        
        if title:
            article.title = title
        if body:
            article.body = body
        session.commit()

        return jsonify({
            "result": True
        })
    except ArticlePostValueError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 400
    except ArticleNotFoundError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500

@router.route("/delete", methods=["DELETE"])
def delete():
    try:
        session = create_session()
        _id = request.form.get("id", None, type=int)

        if _id is None:
            raise ArticlePostValueError("IDを入力してください")

        article = session.query(Article).filter(Article.id == _id).first()
        if article is None:
            raise ArticleNotFoundError("記事が見つかりません")
        
        session.delete(article)
        session.commit()

        return jsonify({
            "result": True
        })

    except ArticlePostValueError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 400
    except ArticleNotFoundError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500

