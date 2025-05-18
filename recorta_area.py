import cv2

image_path = "image.jpg"  # pode ser a imagem já redimensionada, se quiser
image = cv2.imread(image_path)
#image_resized = cv2.resize(image, (2480, 3508))  # ajuste se necessário

scale = 0.2 # ou 0.4 dependendo do tamanho da imagem
image_resized = cv2.resize(image, None, fx=scale, fy=scale)

pontos = []
drawing = False

def marcar_pontos(event, x, y, flags, param):
    global drawing, pontos
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos = [(x, y)]
        drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        pontos.append((x, y))
        drawing = False
        cv2.rectangle(image_resized, pontos[0], pontos[1], (0, 255, 0), 2)
        cv2.imshow("Selecione a área do gabarito", image_resized)
        print(f"\n🔍 Coordenadas encontradas:")
        print(f"x1, y1 = {pontos[0][0]}, {pontos[0][1]}")
        print(f"x2, y2 = {pontos[1][0]}, {pontos[1][1]}")
        print(f"→ Use isso no seu recorte fixo!")

cv2.imshow("Selecione a área do gabarito", image_resized)
cv2.setMouseCallback("Selecione a área do gabarito", marcar_pontos)
cv2.waitKey(0)
cv2.destroyAllWindows()
