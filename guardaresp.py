import cv2
import numpy as np
import os
import time


# output_dir = "temp"
# respostas = {}

# # Coordenadas aproximadas das bolinhas dentro da imagem da questão
# # Você pode ajustar esses valores testando
posicoes_bolinhas_x = [62, 85, 109, 133, 159]  
raio_bolinha = 15  # Raio da bolinha pra pegar o preenchido

alternativas = ["A", "B", "C", "D", "E"]


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



def detectar_respostas(output_dir="temp"):
    print(f"\n🔍 Iniciando detecção de respostas em {output_dir}")
    respostas = {}
    
    # Verificar se a pasta existe
    if not os.path.exists(output_dir):
        print(f"❌ ERRO: Pasta {output_dir} não encontrada!")
        return respostas
    
    # Listar arquivos na pasta
    arquivos = os.listdir(output_dir)
    print(f"📁 Arquivos encontrados: {len(arquivos)}")
    time.sleep(1)
    
    for i in range(1, 61):
        caminho = os.path.join(output_dir, f"questao_{i:02d}.jpg")
        print(f"\n📄 Processando questão {i:02d}")
        
        if not os.path.exists(caminho):
            print(f"❌ Arquivo não encontrado: {caminho}")
            respostas[i] = ""
            continue
            
        imagem = cv2.imread(caminho)
        if imagem is None:
            print(f"❌ Não foi possível ler a imagem: {caminho}")
            respostas[i] = ""
            continue
            
        print(f"✅ Imagem lida: {imagem.shape}")
        time.sleep(0.5)

        # Converter para escala de cinza e aplicar threshold
        print("🎨 Aplicando processamento de imagem...")
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        time.sleep(0.5)

        # Analisar cada alternativa
        print("🔍 Analisando alternativas...")
        preenchimentos = []
        for x in posicoes_bolinhas_x:
            recorte = thresh[:, x-raio_bolinha:x+raio_bolinha]
            preenchido = cv2.countNonZero(recorte)
            preenchimentos.append(preenchido)
            print(f"  Alternativa {alternativas[len(preenchimentos)-1]}: {preenchido} pixels")
            time.sleep(0.2)

        # Verificar qualidade da detecção
        max_pixels = max(preenchimentos)
        min_pixels = min(preenchimentos)
        diferenca = max_pixels - min_pixels
        
        if diferenca < 50:  # Se a diferença for muito pequena
            print(f"⚠️ AVISO: Diferença muito pequena entre alternativas ({diferenca} pixels)")
            print("  Isso pode indicar problemas na máscara ou na detecção")
        
        # Detectar resposta
        idx_maior = np.argmax(preenchimentos)
        resposta = alternativas[idx_maior]
        respostas[i] = resposta
        print(f"✅ Resposta detectada: {resposta}")
        time.sleep(0.5)

    return respostas
