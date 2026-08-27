# Importa a ferramenta YOLO do pacote ultralytics
from pyexpat import model

from ultralytics import YOLO

modelo = YOLO("yolov8n.pt")  # Carrega o modelo pré-treinado YOLOv8n

results = modelo("deposiphotos.jpeg")  # Realiza a previsão em uma imagem específica


for result in results:
    result.show()
