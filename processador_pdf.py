from pdf2image import convert_from_path
import os

entrada = "imagens_pdf"
saida = "imagens_gabaritos"

# os.makedirs(saida, exist_ok=True)

# for arquivo in os.listdir(entrada):
#     if arquivo.endswith(".pdf"):
#         nome_base = os.path.splitext(arquivo)[0]
#         paginas = convert_from_path(os.path.join(entrada, arquivo), dpi=300)

#         for i, pagina in enumerate(paginas):
#             pagina.save(os.path.join(saida, f"{nome_base}_p{i+1}.jpg"), "JPEG")

#         #print quantidade de paginas
#         print(f"✅ {len(paginas)} páginas convertidas para imagens!")
#         len_paginas = len(paginas)

# print("✅ Todas as páginas convertidas para imagens!")


def converter_pdfs(entrada="imagens_pdf", saida="imagens_gabaritos"):
    from pdf2image import convert_from_path
    import os

    os.makedirs(saida, exist_ok=True)
    imagens = []

    for arquivo in os.listdir(entrada):
        if arquivo.endswith(".pdf"):
            nome_base = os.path.splitext(arquivo)[0]
            paginas = convert_from_path(os.path.join(entrada, arquivo), dpi=300)

            for i, pagina in enumerate(paginas):
                caminho_img = os.path.join(saida, f"{nome_base}_p{i+1}.jpg")
                pagina.save(caminho_img, "JPEG")
                imagens.append(caminho_img)

            print(f"✅ {len(paginas)} páginas convertidas de {arquivo}")

    return imagens
