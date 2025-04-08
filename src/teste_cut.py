import cv2
import numpy as np
import os

def cortar_questoes(imagem_path, output_dir):
    """
    Corta a imagem da prova em questões individuais.
    
    Args:
        imagem_path (str): Caminho para a imagem da prova
        output_dir (str): Diretório para salvar as questões cortadas
        
    Returns:
        bool: True se o corte foi bem-sucedido, False caso contrário
    """
    # Criar diretório de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Carregar imagem
    img = cv2.imread(imagem_path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem {imagem_path}")
        return False
    
    # Obter dimensões da imagem
    height, width, _ = img.shape
    
    # Definir dimensões para o corte
    # Assumindo que a prova tem 60 questões em 6 linhas e 10 colunas
    num_linhas = 6
    num_colunas = 10
    
    # Calcular dimensões de cada questão
    questao_height = height // num_linhas
    questao_width = width // num_colunas
    
    # Cortar cada questão
    for linha in range(num_linhas):
        for coluna in range(num_colunas):
            # Calcular coordenadas
            y_inicio = linha * questao_height
            y_fim = (linha + 1) * questao_height
            x_inicio = coluna * questao_width
            x_fim = (coluna + 1) * questao_width
            
            # Extrair questão
            questao = img[y_inicio:y_fim, x_inicio:x_fim]
            
            # Calcular número da questão (1-60)
            num_questao = linha * num_colunas + coluna + 1
            
            # Salvar questão
            output_path = os.path.join(output_dir, f'questao_{num_questao:02d}.jpg')
            cv2.imwrite(output_path, questao)
    
    return True
