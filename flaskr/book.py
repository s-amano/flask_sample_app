"""
書籍一覧の取得・新規追加・編集・削除を行う
"""

from flaskr import app, db
from flaskr.models import Book, User

from datetime import datetime
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required


bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/')
@login_required
def index_book():
    """書籍の一覧を取得する"""


    # 書籍データを取得
    user_id = session.get('user_id')

    books = Book.query.filter(Book.user_id == user_id).all()

    # 書籍一覧画面へ遷移
    return render_template('book/index_book.html',
                           books=books,
                           title='ログイン',
                           year=datetime.now().year)


@bp.route('/create_book', methods=('GET', 'POST'))
@login_required
def create_book():
    """
    GET ：書籍登録画面に遷移
    POST：書籍登録処理を実施
    """
    if request.method == 'GET':
        # 書籍登録画面に遷移
        return render_template('book/create_book.html',
                               title='書籍の追加',
                               year=datetime.now().year)


    # 書籍登録処理
    if request.method == 'POST':

        # ユーザーIDを取得
        user_id = session.get('user_id')

        # 登録フォームから送られてきた値を取得
        title = request.form['title']



        # エラーチェック
        error_message = None

        if not title:
            error_message = '書籍タイトルの入力は必須です'

        if error_message is not None:
            # エラーがあれば、それを画面に表示させる
            flash(error_message, category='alert alert-danger')
            return redirect(url_for('book.create_book'))

        # エラーがなければテーブルに登録する
        if error_message is None:
            book = Book(title=request.form['title'],
                        author=request.form['author'],
                        publisher=request.form['publisher'],
                        user_id=user_id)
            db.session.add(book)
            db.session.commit()

            # 書籍一覧画面へ遷移
            flash('書籍が追加されました', category='alert alert-info')
            return redirect(url_for('book.index_book'))


@bp.route('/<int:book_id>/update_book', methods=('GET', 'POST'))
@login_required
def update_book(book_id):
    """
    GET ：書籍更新画面に遷移
    POST：書籍更新処理を実施
    """

    # 書籍データの取得と存在チェック
    book = get_book_and_check(book_id)

    if request.method == 'GET':
        # 書籍更新画面に遷移
        return render_template('book/update_book.html',
                               book=book,
                               title='書籍の編集',
                               year=datetime.now().year)

    # 書籍編集処理
    if request.method == 'POST':

        # 登録フォームから送られてきた値を取得
        title = request.form['title']




        # エラーチェック
        error_message = None

        if not title:
            error_message = '書籍タイトルの入力は必須です'

        if error_message is not None:
            # エラーがあれば、それを画面に表示させる
            flash(error_message, category='alert alert-danger')
            return redirect(url_for('book.update_book', book_id=book_id))


        # エラーがなければテーブルに登録する
        if error_message is None:
            book.title=request.form['title']
            book.author=request.form['author']
            book.publisher=request.form['publisher']

            db.session.commit()

            # 書籍一覧画面へ遷移
            flash('書籍が編集されました', category='alert alert-info')
            return redirect(url_for('book.index_book'))




@bp.route('/<int:book_id>/delete_book', methods=('GET', 'POST'))
@login_required
def delete_book(book_id):
    """
    GET ：書籍削除確認画面に遷移
    POST：書籍削除処理を実施
    """
    # 書籍データの取得と存在チェック
    book = get_book_and_check(book_id)

    if request.method == 'GET':
        # 書籍削除確認画面に遷移
        return render_template('book/delete_book.html',
                               book=book,
                               title='書籍の削除',
                               year=datetime.now().year)

    # 書籍の削除処理
    if request.method == 'POST':

        db.session.delete(book)
        db.session.commit()

        # 書籍一覧画面へ遷移
        flash('書籍が削除されました', category='alert alert-info')
        return redirect(url_for('book.index_book'))


def get_book_and_check(book_id):
    """書籍の取得と存在チェックのための関数"""

    book = Book.query.filter(Book.id == book_id).first()


    if book is None:
        abort(404, 'There is no such book!!')

    return book