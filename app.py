import os
import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = []

# Desativar quando o projeto for finalizado
os.environ['FLASK_DEBUG'] = 'True'

# Configurando o modo de depuração com base na variável de ambiente
app.debug = os.environ.get('FLASK_DEBUG') == 'True'

@app.route('/')
def home():
    return render_template('index.html', glossario=glossario)

# Rotas para tarefas
@app.route('/tarefas.html')
def listar_tarefas():
    return render_template('tarefas.html', tarefas=tarefas)

@app.route('/tarefas/adicionar', methods=['GET', 'POST'])
def adicionar_tarefa():
    if request.method == 'POST':
        tarefa = request.form['tarefa']
        tarefas.append(tarefa)
        return redirect(url_for('listar_tarefas'))
    return render_template('adicionar_tarefa.html')

@app.route('/tarefas/alterar/<tarefa>', methods=['GET', 'POST',])
def alterar_tarefa(tarefa):
    if request.method == 'POST':
        nova_tarefa = request.form['nova_tarefa']
        index = tarefas.index(tarefa)
        tarefas[index] = nova_tarefa
        return redirect(url_for('listar_tarefas'))
    return render_template('alterar_tarefa.html', tarefa=tarefa)

@app.route('/tarefas/deletar/<tarefa>')
def deletar_tarefa(tarefa):
    tarefas.remove(tarefa)
    return redirect(url_for('listar_tarefas'))

    #o glossário
@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open(
            'bd_glossario.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)
            
    return render_template('glossario.html',glossario=glossario_de_termos)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open(
            'bd_glossario.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)