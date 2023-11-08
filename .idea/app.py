from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://jocean:1234@cluster0.an6epdw.mongodb.net/")
db = client["veiculos_db"]
veiculos = db["veiculos"]

@app.route('/')
def listar_veiculos():
    veiculos_list = veiculos.find()
    return render_template('listar_veiculos.html', veiculos=veiculos_list)

@app.route('/inserir', methods=['GET', 'POST'])
def inserir_veiculo():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        categoria = request.form['categoria']
        preco = request.form['preco']
        tipo = request.form['tipo']

        if ano:
            ano = int(ano)

        veiculo = {
            'marca': marca,
            'modelo': modelo,
            'ano': ano,
            'categoria': categoria,
            'preco': preco,
            'tipo': tipo
        }
        veiculos.insert_one(veiculo)

        return redirect('/')
    return render_template('cadastrar_veiculo.html')

@app.route('/editar/<string:veiculo_id>', methods=['GET', 'POST'])
def editar_veiculo(veiculo_id):
    veiculo = veiculos.find_one({'_id': ObjectId(veiculo_id)})

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        categoria = request.form['categoria']
        preco = request.form['preco']
        tipo = request.form['tipo']

        if ano:
            ano = int(ano)


        veiculos.update_one({'_id': ObjectId(veiculo_id)}, {'$set': {
            'marca': marca,
            'modelo': modelo,
            'ano': ano,
            'categoria': categoria,
            'preco': preco,
            'tipo': tipo
        }})

        return redirect('/')
    return render_template('editar_veiculo.html', veiculo=veiculo)

@app.route('/excluir/<string:veiculo_id>')
def excluir_veiculo(veiculo_id):
    veiculos.delete_one({'_id': ObjectId(veiculo_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
