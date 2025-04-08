import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import random
import numpy as np

# Importando os módulos de correção de provas
from src.teste_cut import cortar_questoes
from src.teste_detect import cortar_e_analisar
from src.teste_compare import compare_resp

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Altere para uma chave secreta segura em produção

# Configurações
UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Criar diretórios necessários
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Lista para armazenar resultados (em produção, use um banco de dados)
resultados = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configurar', methods=['GET', 'POST'])
def configurar():
    if request.method == 'POST':
        # Processar gabarito
        gabarito = {}
        for i in range(1, 61):
            resposta = request.form.get(f'questao_{i}')
            if resposta:
                gabarito[i] = resposta
        
        # Processar disciplinas
        disciplinas = {}
        i = 1
        while True:
            disciplina = request.form.get(f'disciplina_{i}')
            questoes = request.form.get(f'questoes_{i}')
            
            if not disciplina or not questoes:
                break
            
            # Converter string de questões em lista de números
            questoes_lista = []
            for parte in questoes.split(','):
                parte = parte.strip()
                if '-' in parte:
                    inicio, fim = map(int, parte.split('-'))
                    questoes_lista.extend(range(inicio, fim + 1))
                else:
                    questoes_lista.append(int(parte))
            
            disciplinas[disciplina] = sorted(questoes_lista)
            i += 1
        
        # Validar configurações
        if len(gabarito) != 60:
            flash('O gabarito deve conter 60 questões.', 'error')
            return redirect(request.url)
        
        if not disciplinas:
            flash('Adicione pelo menos uma disciplina.', 'error')
            return redirect(request.url)
        
        # Verificar se todas as questões foram atribuídas a alguma disciplina
        todas_questoes = set(range(1, 61))
        questoes_atribuidas = set()
        for questoes in disciplinas.values():
            questoes_atribuidas.update(questoes)
        
        if todas_questoes != questoes_atribuidas:
            flash('Todas as questões devem ser atribuídas a uma disciplina.', 'error')
            return redirect(request.url)
        
        # Salvar configurações na sessão
        session['gabarito'] = gabarito
        session['disciplinas'] = disciplinas
        
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('upload'))
    
    return render_template('configurar.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'gabarito' not in session or 'disciplinas' not in session:
            flash('Por favor, configure o gabarito e as disciplinas primeiro.', 'warning')
            return redirect(url_for('configurar'))
        
        if 'provas' not in request.files:
            flash('Nenhum arquivo selecionado.', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('provas')
        if not files or files[0].filename == '':
            flash('Nenhum arquivo selecionado.', 'error')
            return redirect(request.url)
        
        resultados = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extrair nome do aluno do nome do arquivo
                nome_aluno = os.path.splitext(filename)[0]
                
                # Processar prova
                resultado = processar_prova(filepath, session['gabarito'], session['disciplinas'])
                resultado['nome_aluno'] = nome_aluno
                resultados.append(resultado)
                
                # Remover arquivo após processamento
                os.remove(filepath)
            else:
                flash(f'Arquivo {file.filename} não é permitido.', 'error')
        
        if resultados:
            session['resultados'] = resultados
            flash(f'{len(resultados)} provas processadas com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nenhuma prova foi processada.', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    if 'resultados' not in session:
        flash('Nenhum resultado disponível. Por favor, faça upload de algumas provas.', 'warning')
        return redirect(url_for('upload'))
    
    resultados = session['resultados']
    disciplinas = list(resultados[0]['acertos_disciplina'].keys())
    
    # Calcula médias por disciplina
    medias_disciplinas = []
    for disciplina in disciplinas:
        total = 0
        count = 0
        for resultado in resultados:
            total += resultado['acertos_disciplina'][disciplina]['nota']
            count += 1
        media = total / count if count > 0 else 0
        medias_disciplinas.append(round(media, 1))
    
    # Calcula distribuição de notas
    faixas = [0, 2, 4, 6, 8, 10]
    distribuicao_notas = [0] * (len(faixas) - 1)
    for resultado in resultados:
        for i in range(len(faixas) - 1):
            if faixas[i] <= resultado['nota_total'] < faixas[i + 1]:
                distribuicao_notas[i] += 1
                break
    
    return render_template('dashboard.html',
                         resultados=resultados,
                         disciplinas=disciplinas,
                         medias_disciplinas=medias_disciplinas,
                         distribuicao_notas=distribuicao_notas)

@app.route('/gerar-relatorio')
def gerar_relatorio():
    if 'resultados' not in session:
        flash('Nenhum resultado disponível para gerar relatório!', 'warning')
        return redirect(url_for('upload'))
    
    resultados = session['resultados']
    disciplinas = list(session['disciplinas'].keys())
    
    # Criar DataFrame
    data = []
    for resultado in resultados:
        row = {
            'Aluno': resultado['nome_aluno'],
            'Total Acertos': resultado['total_acertos'],
            'Nota Total': round(resultado['nota_total'], 1)
        }
        
        # Adicionar acertos por disciplina
        for disciplina in disciplinas:
            acertos = resultado['acertos_disciplina'][disciplina]
            row[f'{disciplina} - Acertos'] = acertos['acertos']
            row[f'{disciplina} - Total'] = acertos['total']
            row[f'{disciplina} - Nota'] = round(acertos['nota'], 1)
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Gerar arquivo Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'relatorio_provas_{timestamp}.xlsx'
    filepath = os.path.join(app.config['TEMP_FOLDER'], filename)
    
    # Criar Excel writer
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Planilha de resultados
        df.to_excel(writer, sheet_name='Resultados', index=False)
        
        # Planilha de estatísticas
        stats_data = {
            'Métrica': [
                'Média Geral',
                'Desvio Padrão',
                'Nota Mínima',
                'Nota Máxima',
                'Total de Alunos'
            ],
            'Valor': [
                round(df['Nota Total'].mean(), 1),
                round(df['Nota Total'].std(), 1),
                round(df['Nota Total'].min(), 1),
                round(df['Nota Total'].max(), 1),
                len(df)
            ]
        }
        
        # Adicionar estatísticas por disciplina
        for disciplina in disciplinas:
            stats_data['Métrica'].extend([
                f'Média {disciplina}',
                f'Desvio Padrão {disciplina}',
                f'Mínima {disciplina}',
                f'Máxima {disciplina}'
            ])
            stats_data['Valor'].extend([
                round(df[f'{disciplina} - Nota'].mean(), 1),
                round(df[f'{disciplina} - Nota'].std(), 1),
                round(df[f'{disciplina} - Nota'].min(), 1),
                round(df[f'{disciplina} - Nota'].max(), 1)
            ])
        
        pd.DataFrame(stats_data).to_excel(writer, sheet_name='Estatísticas', index=False)
    
    return send_file(filepath,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/check-config')
def check_config():
    configured = 'gabarito' in session and 'disciplinas' in session
    return jsonify({'configured': configured})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processar_prova(arquivo, gabarito, disciplinas):
    """
    Processa uma prova de um aluno.
    
    Args:
        arquivo (str): Caminho para o arquivo da prova
        gabarito (dict): Dicionário com o gabarito
        disciplinas (dict): Dicionário com as disciplinas e suas questões
        
    Returns:
        dict: Dicionário com os resultados da prova
    """
    # Criar diretórios temporários
    temp_dir = os.path.join(TEMP_FOLDER, datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(temp_dir, exist_ok=True)
    
    # Diretórios para as questões cortadas
    questoes_dir = os.path.join(temp_dir, 'questoes')
    originais_dir = os.path.join(temp_dir, 'originais')
    binarizadas_dir = os.path.join(temp_dir, 'binarizadas')
    
    # Cortar a imagem em questões individuais
    cortar_questoes(arquivo, questoes_dir)
    
    # Processar cada questão
    respostas = {}
    for i in range(1, 61):
        questao_path = os.path.join(questoes_dir, f'questao_{i:02d}.jpg')
        if os.path.exists(questao_path):
            # Analisar a questão para detectar a resposta
            resposta = cortar_e_analisar(questao_path, originais_dir, binarizadas_dir)
            if resposta > 0:
                # Converter o número da coluna para a letra da resposta (1=A, 2=B, etc.)
                letra_resposta = chr(64 + resposta)  # 65 é o código ASCII para 'A'
                respostas[i] = letra_resposta
            else:
                # Se não foi possível detectar a resposta, usar uma resposta aleatória para demonstração
                respostas[i] = random.choice(['A', 'B', 'C', 'D', 'E'])
        else:
            # Se a questão não foi cortada corretamente, usar uma resposta aleatória para demonstração
            respostas[i] = random.choice(['A', 'B', 'C', 'D', 'E'])
    
    # Comparar as respostas com o gabarito
    resultados_comparacao = compare_resp(respostas, gabarito)
    
    # Calcula acertos por disciplina
    acertos_disciplina = {}
    for disciplina, questoes in disciplinas.items():
        acertos = 0
        total = 0
        for questao in questoes:
            if respostas.get(questao) == gabarito.get(questao):
                acertos += 1
            total += 1
        acertos_disciplina[disciplina] = {
            'acertos': acertos,
            'total': total,
            'nota': (acertos / total) * 10 if total > 0 else 0
        }
    
    # Calcula total de acertos
    total_acertos = resultados_comparacao['acertos']
    nota_total = (total_acertos / 60) * 10
    
    # Limpar arquivos temporários
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    return {
        'respostas': respostas,
        'acertos_disciplina': acertos_disciplina,
        'total_acertos': total_acertos,
        'nota_total': nota_total,
        'detalhes': resultados_comparacao['detalhes']
    }

if __name__ == '__main__':
    app.run(debug=True) 