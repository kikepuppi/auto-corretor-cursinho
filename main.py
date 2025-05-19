from processador_pdf import converter_pdfs
#from mask_generator_base import gerar_masks
from guardaresp import detectar_respostas
from teste import dividir_blocos_do_gabarito
import csv
import os

# Caminhos
entrada_pdf = "imagens_pdf"
saida_img = "imagens_gabaritos"
temp_dir = "temp"
csv_saida = "respostas.csv"

# Etapa 1: converter PDFs em imagens
imagens_convertidas = converter_pdfs(entrada=entrada_pdf, saida=saida_img)

# Etapa 2: processar imagens
respostas_csv = []
gabarito = None

for imagem_path in sorted(imagens_convertidas):
    nome_arquivo = os.path.basename(imagem_path)
    nome_base = nome_arquivo.split("_p")[0]

    print(f"\n📄 Processando: {nome_arquivo}")

    dividir_blocos_do_gabarito(imagem_path, output_dir=temp_dir)
    respostas = detectar_respostas(output_dir=temp_dir)
    lista_respostas = [respostas[i] for i in range(1, 61)]

    if nome_base == "gabarito" and gabarito is None:
        gabarito = lista_respostas
    else:
        respostas_csv.append(lista_respostas)

# Etapa 3: salvar CSV
colunas = [f"q{i+1}" for i in range(60)]
with open(csv_saida, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(colunas)
    writer.writerow(gabarito)
    for linha in respostas_csv:
        writer.writerow(linha)

print(f"\n✅ Respostas salvas com sucesso em {csv_saida}!")