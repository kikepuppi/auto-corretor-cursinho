import cv2

output_dir = "temp"
numero_questao = 2  # Muda o número da questão que quer ver

caminho = f"{output_dir}/questao_{numero_questao:02d}.jpg"
imagem = cv2.imread(caminho)

# Função que mostra a posição do mouse
def show_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenada X={x}, Y={y}")

cv2.imshow(f"Questao {numero_questao}", imagem)
cv2.setMouseCallback(f"Questao {numero_questao}", show_xy)

cv2.waitKey(0)
cv2.destroyAllWindows()
