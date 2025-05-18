import cv2
import numpy as np
import os
import shutil
import stat
import time



# # Configurações
# image = cv2.imread("imagens_gabaritos/imagens1_p1.jpg")
# image_path = "imagens_gabaritos/imagens1_p1.jpg"
# output_dir = "temp"
# n_linhas = 15
# n_colunas = 4

# scale = 0.3
# image_resized = cv2.resize(image, None, fx=scale, fy=scale)

# # 2. Recorte fixo da área de questões
# # ajustei os valores com o recorta_area.py
# y1, y2 = 435, 990
# x1, x2 = 40, 710
# bloco = image_resized[y1:y2, x1:x2]
# cv2.imshow("Bloco recortado", bloco)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# # Função para remover permissão de readonly (Windows)
# def remove_readonly(func, path, _):
#     os.chmod(path, stat.S_IWRITE)
#     func(path)

# # Apagar pasta temp
# if os.path.exists(output_dir):
#     shutil.rmtree(output_dir, onerror=remove_readonly)
# os.makedirs(output_dir)

# # Carregar imagem e preparar
# #image = cv2.imread(image_path)
# h, w = bloco.shape[:2]

# n_linhas, n_colunas = 15, 4
# altura = bloco.shape[0] // n_linhas
# largura = bloco.shape[1] // n_colunas

# # Converter pra HSV e aplicar máscara
# hsv = cv2.cvtColor(bloco, cv2.COLOR_BGR2HSV)
# lower_black = np.array([0, 0, 0])
# upper_black = np.array([180, 255, 80])
# mask_hsv = cv2.inRange(hsv, lower_black, upper_black)

# print(f"Imagem: {w}x{h}")
# print(f"Recorte: {n_linhas} linhas × {n_colunas} colunas → {largura}x{altura} cada")

# # Recortar, aplicar máscara e salvar
# for linha in range(n_linhas):
#     for coluna in range(n_colunas):
#         y1 = linha * altura
#         y2 = (linha + 1) * altura
#         x1 = coluna * largura
#         x2 = (coluna + 1) * largura

#         # Recorte
#         recorte_img = image[y1:y2, x1:x2]
#         recorte_mask = mask_hsv[y1:y2, x1:x2]

#         # Aplicar a máscara
#         resultado = cv2.bitwise_and(recorte_img, recorte_img, mask=recorte_mask)


#         # Calcular número da questão respeitando o padrão correto
#         numero_questao = linha + 1 + coluna * n_linhas

#         nome = f"questao_{numero_questao:02d}.jpg"
#         caminho = os.path.join(output_dir, nome)
#         cv2.imwrite(caminho, resultado)

# print(f"✅ Imagens salvas em '{output_dir}' com posições corretas!")


def gerar_masks(image_path, output_dir="temp"):
    import cv2
    import numpy as np
    import os
    import shutil
    import stat
    import time

    print(f"\n Iniciando processamento de: {image_path}")

    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    # Carregar e redimensionar imagem
    print("📥 Carregando imagem...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ ERRO: Não foi possível ler a imagem: {image_path}")
        return False
        
    print(f"✅ Imagem carregada: {image.shape}")
    time.sleep(1)  # Aguardar para visualizar
    
    print("🔄 Redimensionando imagem...")
    scale = 0.3
    image_resized = cv2.resize(image, None, fx=scale, fy=scale)
    print(f"✅ Imagem redimensionada: {image_resized.shape}")
    time.sleep(1)

    # Recorte fixo da área de questões
    print("✂️ Recortando área de questões...")
    y1, y2 = 435, 990
    x1, x2 = 40, 710
    bloco = image_resized[y1:y2, x1:x2]
    print(f"✅ Área recortada: {bloco.shape}")
    time.sleep(1)

    # Converter pra HSV e aplicar máscara
    print(" Aplicando filtro HSV...")
    hsv = cv2.cvtColor(bloco, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 80])
    mask_hsv = cv2.inRange(hsv, lower_black, upper_black)
    print("✅ Filtro HSV aplicado")
    time.sleep(1)

    # Configurar grade
    print("📏 Configurando grade de questões...")
    n_linhas, n_colunas = 15, 4
    altura = bloco.shape[0] // n_linhas
    largura = bloco.shape[1] // n_colunas
    print(f"✅ Grade configurada: {n_linhas}x{n_colunas} questões")
    time.sleep(1)

    # Limpar pasta de saída
    if os.path.exists(output_dir):
        print(f"🗑️ Limpando pasta {output_dir}")
        shutil.rmtree(output_dir, onerror=remove_readonly)
    os.makedirs(output_dir)
    print(f"✅ Pasta {output_dir} criada")
    time.sleep(1)

    # Recortar e salvar cada questão
    print("\n✂️ Iniciando recorte das questões...")
    for linha in range(n_linhas):
        for coluna in range(n_colunas):
            # Calcular número da questão
            numero_questao = linha + 1 + coluna * n_linhas
            print(f"\n📝 Processando questão {numero_questao:02d}")
            
            # Calcular coordenadas do recorte
            y1_questao = linha * altura
            y2_questao = (linha + 1) * altura
            x1_questao = coluna * largura
            x2_questao = (coluna + 1) * largura

            # Recortar da imagem original
            print(f"  ✂️ Recortando região...")
            recorte_img = bloco[y1_questao:y2_questao, x1_questao:x2_questao]
            recorte_mask = mask_hsv[y1_questao:y2_questao, x1_questao:x2_questao]
            
            # Aplicar máscara
            print(f"  🎨 Aplicando máscara...")
            resultado = cv2.bitwise_and(recorte_img, recorte_img, mask=recorte_mask)
            
            # Salvar resultado
            caminho = os.path.join(output_dir, f"questao_{numero_questao:02d}.jpg")
            cv2.imwrite(caminho, resultado)
            print(f"  ✅ Questão {numero_questao:02d} salva: {resultado.shape}")
            time.sleep(0.5)  # Pequena pausa entre questões

    print(f"\n✨ Processo concluído! {n_linhas * n_colunas} questões salvas em {output_dir}")
    return True
