import os
import time
import pandas as pd
import shutil
import stat
from processador_pdf import converter_pdfs
from mask_generator_base import gerar_masks
from guardaresp import detectar_respostas

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def processar_imagem(imagem_path, output_dir="temp"):
    print(f"\n Processando: {imagem_path}")
    
    # Gerar máscaras
    if not gerar_masks(imagem_path, output_dir):
        print(f"❌ Erro ao processar imagem: {imagem_path}")
        return None
        
    # Aguardar um momento para garantir que os arquivos foram salvos
    time.sleep(2)
    
    # Detectar respostas
    respostas = detectar_respostas(output_dir)
    
    # Limpar pasta temp
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    return respostas

def main():
    # 1. Converter PDFs em imagens
    print("\n Convertendo PDFs em imagens...")
    imagens = converter_pdfs()
    
    if not imagens:
        print("❌ Nenhuma imagem foi gerada!")
        return
    
    # 2. Processar gabarito primeiro
    gabarito_path = os.path.join("imagens_gabaritos", "gabarito_p1.jpg")
    print("\n Processando gabarito...")
    respostas_gabarito = processar_imagem(gabarito_path)
    
    if not respostas_gabarito:
        print("❌ Erro ao processar gabarito!")
        return
    
    # 3. Criar DataFrame com as respostas
    # Primeiro criar as colunas Q01, Q02, etc.
    colunas = [f"Q{i:02d}" for i in range(1, 61)]
    
    # DataFrame para armazenar todas as respostas
    df = pd.DataFrame(columns=colunas)
    
    # Adicionar gabarito como primeira linha
    gabarito_dict = {f"Q{i:02d}": respostas_gabarito[i] for i in range(1, 61)}
    df.loc["Gabarito"] = gabarito_dict
    
    # 4. Processar cada prova
    for i, imagem_path in enumerate(imagens, 1):
        if "gabarito" in imagem_path:
            continue  # Pular o gabarito pois já foi processado
            
        print(f"\n🔄 Processando prova {i}")
        respostas = processar_imagem(imagem_path)
        
        for i in range(len(respostas)):
            # Converter respostas para o formato do DataFrame
            prova_dict = {f"Q{i:02d}": respostas[i] for i in range(1, 61)}
            df.loc[f"Prova_{i}"] = prova_dict
            print(f"✅ Prova {i} processada com sucesso!")
    
    # 5. Salvar resultados
    if not df.empty:
        df.to_csv('respostas.csv')
        print("\n Todas as provas foram processadas!")
        print(" Resultados salvos em respostas.csv")
        print("\n Exemplo do CSV:")
        print(df.head())
    else:
        print("\n❌ Nenhuma prova foi processada com sucesso!")

if __name__ == "__main__":
    main()
