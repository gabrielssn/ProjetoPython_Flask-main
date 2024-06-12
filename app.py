import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente para modo de desenvolvimento debug
os.environ['FLASK_DEBUG'] = 'True'
app.debug = os.environ.get('FLASK_DEBUG') == 'True'

# Arquivo CSV das disciplinas
DISCIPLINAS_CSV = 'bd_disciplinas.csv'
# Arquivo CSV dos eventos
EVENTOS_CSV = 'bd_eventos.csv'

@app.route('/')
def pagina_home():
    return render_template('index.html')

@app.route('/sobre')
def pagina_sobre():
    return render_template('sobre.html')

@app.route('/disciplinas')
def disciplinas():
    disciplinas_lista = []
    with open(DISCIPLINAS_CSV, newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            disciplinas_lista.append(l)
    return render_template('disciplinas.html', glossario=disciplinas_lista)

@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')

@app.route('/criar_termo', methods=['POST'])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']
    carga_horaria = request.form['cargaHoraria']
    with open(DISCIPLINAS_CSV, 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao, carga_horaria])
    return redirect(url_for('disciplinas'))

@app.route('/editar_eventoo/<int:evento_id>', methods=['GET', 'POST'])
def editar_eventoo(evento_id):
    if request.method == 'POST':
        nova_data = request.form['data']
        nova_descricao = request.form['descricao']
        novo_tipo = request.form['tipo']
        with open(EVENTOS_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            linhas = list(reader)
        # Atualizar o evento com base no ID
        if 0 <= evento_id < len(linhas):
            linhas[evento_id] = [nova_data, nova_descricao, novo_tipo]
        # Salvar as alterações de volta no arquivo
        with open(EVENTOS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(linhas)
        return redirect(url_for('agenda_de_eventos'))
    # Se for uma requisição GET, mostrar o formulário de edição com os dados atuais do evento
    with open(EVENTOS_CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)
    evento = linhas[evento_id]
    return render_template('editar_eventoo.html', evento=evento, evento_id=evento_id)

@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):
    with open(DISCIPLINAS_CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)
    # Encontrar e excluir o termo com base no ID
    if 0 <= termo_id < len(linhas):
        del linhas[termo_id]
    # Salvar as alterações de volta no arquivo
    with open(DISCIPLINAS_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)
    return redirect(url_for('disciplinas'))

@app.route('/editar_carga_horaria/<int:termo_id>', methods=['POST'])
def editar_carga_horaria(termo_id):
    nova_carga_horaria = request.form['carga_horaria']
    with open(DISCIPLINAS_CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)
    # Atualizar a carga horária do termo com base no ID
    if 0 <= termo_id < len(linhas):
        linhas[termo_id][2] = nova_carga_horaria
    # Salvar as alterações de volta no arquivo
    with open(DISCIPLINAS_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)
    return redirect(url_for('disciplinas'))

# Rotas para Eventos
@app.route('/novo_evento')
def novo_evento():
    return render_template('novo_evento.html')

@app.route('/agenda_de_eventos')
def agenda_de_eventos():
    eventos_lista = []
    with open(EVENTOS_CSV, newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            eventos_lista.append(l)
    return render_template('agenda_de_eventos.html', eventos=eventos_lista)

@app.route('/criar_evento', methods=['POST'])
def criar_evento():
    data = request.form['data']
    descricao = request.form['descricao']
    tipo = request.form['tipo']
    with open(EVENTOS_CSV, 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([data, descricao, tipo])
    return redirect(url_for('agenda_de_eventos'))

@app.route('/excluir_evento/<int:evento_id>', methods=['POST'])
def excluir_evento(evento_id):
    with open(EVENTOS_CSV, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)
    # Encontrar e excluir o evento com base no ID
    if 0 <= evento_id < len(linhas):
        del linhas[evento_id]
    # Salvar as alterações de volta no arquivo
    with open(EVENTOS_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)
    return redirect(url_for('agenda_de_eventos'))

if __name__ == '__main__':
    app.run()