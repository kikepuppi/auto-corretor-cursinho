from teste_cut import cortar_questoes
from teste_detect import cortar_e_analisar
from teste_compare import compare_resp
import os

gabarito = {1: 5, 2: 2, 3: 2, 4: 4, 5: 3, 6: 4, 7: 3, 8: 1, 9: 1, 10: 2, 11: 4, 12: 3, 13: 5, 14: 2, 15: 4, 16: 4, 17: 2, 18: 3, 19: 5, 20: 1, 21: 3, 22: 5, 23: 1, 24: 4, 25: 4, 26: 5, 27: 4, 28: 5, 29: 5, 30: 4, 31: 2, 32: 3, 33: 5, 34: 5, 35: 3, 36: 4, 37: 1, 38: 2, 39: 4, 40: 2, 41: 4, 42: 3, 43: 1, 44: 5, 45: 5, 46: 3, 47: 5, 48: 1, 49: 1, 50: 3, 51: 3, 52: 3, 53: 4, 54: 0, 55: 5, 56: 4, 57: 2, 58: 3, 59: 3, 60: 3}

if __name__ == "__main__":
    # Caminho da imagem da prova
    imagem_path = "teste_2.jpg"

    # Pasta onde as questões cortadas serão salvas
    output_dir = "temp/questoes_cortadas"

    # Cortar as questões e salvar
    cortar_questoes(imagem_path, output_dir)

    # Dicionário para armazenar as respostas
    respostas = {}

    # Iterar pelas 60 questões
    for questao_num in range(1, 61):
        # Caminho da imagem da questão
        imagem_path = os.path.join(output_dir, f"questao_{questao_num:02d}.jpg")

        # Pastas onde os pedaços serão salvos
        output_dir_originais = "temp/pedacos_originais"
        output_dir_binarizadas = "temp/pedacos_binarizados"

        # Cortar e analisar os pedaços
        respostas[questao_num] = cortar_e_analisar(imagem_path, output_dir_originais, output_dir_binarizadas)

    compare_resp(respostas, gabarito)
        