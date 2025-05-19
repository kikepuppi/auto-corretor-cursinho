# import cv2
# import numpy as np
# import os
# import shutil
# import stat

# def dividir_blocos_do_gabarito(imagem_path, output_dir="temp"):
#     # Carrega a imagem original
#     image = cv2.imread(imagem_path)
#     original = image.copy()

#     # Pré-processamento para detectar o contorno do bloco
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     _, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV)

#     # Detecta os contornos presentes na imagem
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Procura o maior contorno com proporção retangular semelhante ao gabarito (ajuste aqui se necessário)
#     alvo_contorno = None
#     max_area = 0
#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)
#         area = w * h
#         aspect_ratio = w / h
#         if 1 < aspect_ratio < 1.6 and area > max_area and w > 400 and h > 400:
#             max_area = area
#             alvo_contorno = (x, y, w, h)

#     if alvo_contorno is None:
#         print("❌ Nenhum bloco de gabarito identificado!")
#         return False

#     # Recorta o bloco detectado com base no contorno escolhido
#     x, y, w, h = alvo_contorno
#     bloco = original[y:y+h, x:x+w]

#     # Aplica filtro para destacar bolinhas pretas (fundo branco, bolinha preta)
#     bloco_gray = cv2.cvtColor(bloco, cv2.COLOR_BGR2GRAY)
#     bloco_blur = cv2.GaussianBlur(bloco_gray, (3, 3), 0)
#     _, bloco_filtrado = cv2.threshold(bloco_blur, 180, 255, cv2.THRESH_BINARY_INV)

#     # Cria ou limpa a pasta de saída temporária
#     if os.path.exists(output_dir):
#         shutil.rmtree(output_dir, onerror=lambda func, path, _: os.chmod(path, stat.S_IWRITE))
#     os.makedirs(output_dir)

#     # Define o número de linhas e colunas da grade de questões
#     n_linhas, n_colunas = 15, 4
#     altura = bloco_filtrado.shape[0] // n_linhas
#     largura = bloco_filtrado.shape[1] // n_colunas

#     # Faz a divisão percorrendo coluna por coluna, depois linha (ordem vertical) porque a prova é vertical
#     count = 1
#     for coluna in range(n_colunas):
#         for linha in range(n_linhas):
#             y1 = linha * altura
#             y2 = (linha + 1) * altura
#             x1 = coluna * largura
#             x2 = (coluna + 1) * largura

#             # Recorta a célula da questão do bloco filtrado e salva como imagem separada
#             recorte = bloco_filtrado[y1:y2, x1:x2]
#             caminho = os.path.join(output_dir, f"questao_{count:02d}.jpg")
#             cv2.imwrite(caminho, recorte)
#             count += 1

#     print(f"✅ {count-1} recortes salvos em '{output_dir}' com sucesso!")
#     return True

# # Exemplo de uso direto, apenas para testes
# if __name__ == "__main__":
#     dividir_blocos_do_gabarito("imagens_gabaritos/imagens1_p1.jpg")


import cv2
import numpy as np
import os
import shutil
import stat

def dividir_blocos_do_gabarito(imagem_path, output_dir="temp"):
    image = cv2.imread(imagem_path)
    original = image.copy()

    # Pré-processamento: converter para escala de cinza e aplicar desfoque
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Procurar o maior retângulo com proporção compatível com o bloco de gabarito
    alvo_contorno = None
    max_area = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = w / h
        if 0.9 < aspect_ratio < 1.6 and area > max_area and w > 400 and h > 400:
            max_area = area
            alvo_contorno = (x, y, w, h)

    # Verificação: caso nenhum retângulo válido tenha sido encontrado
    if alvo_contorno is None:
        print("❌ Nenhum bloco de gabarito identificado!")
        return False

    # Recorte do bloco com base no contorno encontrado
    x, y, w, h = alvo_contorno
    bloco = original[y:y+h, x:x+w]

    # Salvar o bloco original para debug (opcional)
    cv2.imwrite(os.path.join(output_dir, "bloco_detectado.jpg"), bloco)

    # Limpar e recriar pasta de saída
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, onerror=lambda func, path, _: os.chmod(path, stat.S_IWRITE))
    os.makedirs(output_dir)

    # Dividir em 15 linhas e 4 colunas (60 questões no total)
    n_linhas, n_colunas = 15, 4
    altura = bloco.shape[0] // n_linhas
    largura = bloco.shape[1] // n_colunas

    # Verificação visual e de proporção para cada recorte de questão
    count = 1
    for coluna in range(n_colunas):
        for linha in range(n_linhas):
            y1 = linha * altura
            y2 = (linha + 1) * altura
            x1 = coluna * largura
            x2 = (coluna + 1) * largura

            recorte = bloco[y1:y2, x1:x2]

            # Verificação de formato e proporção
            recorte_h, recorte_w = recorte.shape[:2]
            proporcao = recorte_w / recorte_h if recorte_h != 0 else 0
            if not (1.5 < proporcao < 5.0):
                print(f"⚠️ Questão {count:02d} com proporção incomum: {proporcao:.2f} (W={recorte_w}, H={recorte_h})")

            # Salvar recorte individual
            recorte_gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)

            _, recorte_thresh = cv2.threshold(recorte_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            caminho = os.path.join(output_dir, f"questao_{count:02d}.jpg")
            cv2.imwrite(caminho, recorte_thresh)
            count += 1

    print(f"✅ {count-1} recortes salvos em '{output_dir}' com sucesso!")
    return True

# Exemplo de uso:
if __name__ == "__main__":
    dividir_blocos_do_gabarito("imagens_gabaritos/imagens1_p24.jpg")
