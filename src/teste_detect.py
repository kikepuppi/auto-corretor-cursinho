import cv2
import numpy as np
import os

def cortar_e_analisar(imagem_path, orig_dir, bin_dir):
    """
    Corta a imagem em pedaços verticais e analisa cada pedaço para detectar a resposta.
    
    Args:
        imagem_path (str): Caminho para a imagem da questão
        orig_dir (str): Diretório para salvar as imagens originais
        bin_dir (str): Diretório para salvar as imagens binarizadas
        
    Returns:
        str: Resposta detectada (A, B, C, D ou E) ou None se não detectar
    """
    # Carregar imagem
    img = cv2.imread(imagem_path)
    if img is None:
        return None
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar threshold adaptativo
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Salvar imagens para debug
    base_name = os.path.splitext(os.path.basename(imagem_path))[0]
    cv2.imwrite(os.path.join(orig_dir, f'{base_name}_orig.jpg'), gray)
    cv2.imwrite(os.path.join(bin_dir, f'{base_name}_bin.jpg'), binary)
    
    # Dividir em 5 colunas (A, B, C, D, E)
    height, width = binary.shape
    col_width = width // 5
    
    # Lista para armazenar a quantidade de pixels brancos em cada coluna
    white_pixels = []
    
    # Analisar cada coluna
    for i in range(5):
        start_x = i * col_width
        end_x = (i + 1) * col_width
        
        # Extrair coluna
        col = binary[:, start_x:end_x]
        
        # Contar pixels brancos
        white_count = np.sum(col == 255)
        white_pixels.append(white_count)
    
    # Encontrar a coluna com mais pixels brancos
    max_white = max(white_pixels)
    max_index = white_pixels.index(max_white)
    
    # Se a quantidade de pixels brancos for significativa
    if max_white > 1500:  # Ajuste este valor conforme necessário
        # Mapear índice para letra (0=A, 1=B, 2=C, 3=D, 4=E)
        resposta = chr(65 + max_index)  # 65 é o código ASCII para 'A'
        return resposta
    
    return None