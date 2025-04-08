# Corretor de Provas - Insper Data

Sistema de correção automática de provas com suporte a múltiplas disciplinas e análise de resultados.

## Funcionalidades

- Configuração de gabarito e disciplinas
- Upload de múltiplas provas
- Correção automática
- Dashboard com análise de resultados
- Gráficos de desempenho por disciplina
- Distribuição de notas

## Requisitos

- Python 3.8 ou superior
- Flask
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/corretor-provas.git
cd corretor-provas
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse o sistema em `http://localhost:5000`

3. Configure o gabarito e as disciplinas:
   - Selecione as respostas corretas para cada questão
   - Adicione as disciplinas e suas respectivas questões

4. Faça upload das provas:
   - Os arquivos devem ser nomeados com o nome do aluno
   - Formatos suportados: JPG, JPEG, PNG, PDF

5. Visualize os resultados no dashboard:
   - Notas por aluno
   - Médias por disciplina
   - Distribuição de notas

## Estrutura do Projeto

```
corretor-provas/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
├── static/            # Arquivos estáticos
│   ├── css/          # Estilos CSS
│   └── js/           # Scripts JavaScript
├── templates/         # Templates HTML
├── uploads/          # Diretório para uploads
└── temp/             # Arquivos temporários
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request