# import cv2
# import numpy as np
# import os
# import time


# output_dir = "temp"
# respostas = {}

# # Coordenadas aproximadas das bolinhas dentro da imagem da questão
# # Você pode ajustar esses valores testando
# posicoes_bolinhas_x = [62, 85, 109, 133, 159]  
# raio_bolinha = 15  # Raio da bolinha pra pegar o preenchido

# alternativas = ["A", "B", "C", "D", "E"]


# #vai de 1 até o numero de paginas do pdf
# #o len de paginas está em processador_pdf.py


# def processar_imagem():
#     for i in range(1, 60):
#         caminho = f"{output_dir}/questao_{i:02d}.jpg"
#         imagem = cv2.imread(caminho)
#         gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

#         preenchimentos = []

#         for x in posicoes_bolinhas_x:
#             # Recorte da região da bolinha
#             recorte = thresh[:, x-raio_bolinha:x+raio_bolinha]
#             # Soma dos pixels brancos (quanto mais branco, mais preenchido)
#             preenchido = cv2.countNonZero(recorte)
#             preenchimentos.append(preenchido)

#         # Detectar qual bolinha teve maior preenchimento
#         idx_maior = np.argmax(preenchimentos)
#         resposta = alternativas[idx_maior]

#         respostas[i] = resposta

# processar_imagem()



# # Mostrar respostas detectadas
# for numero, letra in respostas.items():
#     print(f"Questão {numero:02d} → Resposta marcada: {letra}")
 

import cv2
import numpy as np
import os

import cv2
import numpy as np
import os

def detectar_respostas(output_dir="temp"):
    print(f"\n🔍 Iniciando detecção de respostas em {output_dir}")
    respostas = {}
    alternativas = ["A", "B", "C", "D", "E"]

    if not os.path.exists(output_dir):
        print(f"❌ ERRO: Pasta {output_dir} não encontrada!")
        return respostas

    for i in range(1, 61):
        caminho = os.path.join(output_dir, f"questao_{i:02d}.jpg")
        if not os.path.exists(caminho):
            respostas[i] = ""
            continue

        imagem = cv2.imread(caminho)
        if imagem is None:
            respostas[i] = ""
            continue

        # Pré-processamento
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Encontrar contornos
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bolinhas = []
        for c in contornos:
            (x, y, w, h) = cv2.boundingRect(c)
            area = cv2.contourArea(c)
            ar = w / float(h)

            # Critérios para considerar como bolinha marcada
            if 40 < w < 60 and 40 < h < 60 and 0.8 < ar < 1.2 and 1000 < area < 3000:
                # Verifica se a bolinha está dentro da região de interesse
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                total = cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=mask))
                bolinhas.append((x, total))

        # Validar quantidade de bolinhas detectadas
        if not bolinhas or len(bolinhas) < 5:
            print(f"❌ Questão {i:02d}: bolinhas insuficientes detectadas")
            respostas[i] = ""
            continue

        # Ordenar por posição horizontal e selecionar a mais preenchida
        bolinhas = sorted(bolinhas, key=lambda x: x[0])
        idx_maior = np.argmax([b[1] for b in bolinhas])
        resposta = alternativas[idx_maior] if idx_maior < len(alternativas) else ""
        respostas[i] = resposta
        print(f"✅ Questão {i:02d} → {resposta}")

    return respostas


