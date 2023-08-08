from flask import request, render_template, redirect, flash
from flask.views import MethodView
from src.db import mysql

class IndexController(MethodView):
    def get(self):
        with mysql.cursor() as cur:
            cur.execute("SELECT * FROM tbb_products")
            data = cur.fetchall()
            cur.execute("SELECT * FROM tbb_categories")
            categories = cur.fetchall()
            print(data)
            return render_template('public/index.html', data=data, categories=categories)
    
    def post(self):
        code = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        category = request.form['category']
        
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO tbb_products VALUES(%s, %s, %s, %s, %s)", (code, name, stock, value, category))
                cur.connection.commit()
                flash('El producto ha sido agregado correctamente', 'success')
            except:
                flash('Un error ha ocurrido', "error")
            return redirect('/')

class DeleteProductController(MethodView):
    def post(self, code):
        with mysql.cursor() as cur:
            try:
                cur.execute("DELETE FROM tbb_products WHERE code = %s", (code, ))
                cur.connection.commit()
                flash("El producto se ha borrado correctamente", "success")
            except:
                flash("Ha ocurrido un error mientras intentabamos borrar el producto", "error")
            return redirect('/')

class UpdateProductController(MethodView):
    def get(self, code):
        with mysql.cursor() as cur:
            cur.execute("SELECT * FROM tbb_products WHERE code = %s", (code, ))
            product = cur.fetchone()
            return render_template('public/update.html', product=product)
    
    def post(self, code):
        productCode = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        
        with mysql.cursor() as cur:
            try:
                cur.execute("UPDATE tbb_products SET code = %s, name = %s, stock = %s, value = %s WHERE code = %s", (productCode, name, stock, value, code))
                cur.connection.commit()
                flash("El producto se ha actualizado", "success")
            except:
                flash("Un error ha ocurrido al actualizar el producto", "error")
            return redirect('/')

class CreateCategoriesController(MethodView):
    def get(self):
        return render_template("public/categories.html")
    
    def post(self):
        id = request.form['id']
        name = request.form['name']
        description = request.form['description']
        
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO tbb_categories VALUES(%s, %s, %s)", (id, name, description))
                cur.connection.commit()
                flash("La categoría se ha creado", "success")
            except:
                flash("Un error ha ocurrido", "error")
            return redirect('/')