import cv2
import numpy as np

# Abrir imagem original recortada (sem máscara aplicada)
img = cv2.imread("temp/questao_03.jpg")  # troque o número conforme quiser

# Exibir imagem
cv2.imshow("Questão Recortada", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
