import cv2
import sys
import os
from ultralytics import YOLO


def detectar_objetos_video(source):
    """Detecta objetos em um vídeo usando YOLOv8."""
    modelo = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {source}")
        sys.exit(1)

    print("Pressione 'q' para sair")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        resultados = modelo(frame, verbose=False)

        for result in resultados:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confianca = float(box.conf[0])
                classe_id = int(box.cls[0])
                nome_classe = modelo.names[classe_id]

                if confianca < 0.5:
                    continue

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                texto = f"{nome_classe} {confianca:.2f}"
                (w, h), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), (0, 255, 0), -1)
                cv2.putText(frame, texto, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

        cv2.imshow("Detecção de Objetos - YOLOv8", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def baixar_video_teste():
    """Baixa um vídeo de teste público da internet."""
    import requests
    import warnings
    warnings.filterwarnings('ignore')

    nome = "video_teste.mp4"

    if os.path.exists(nome) and os.path.getsize(nome) > 10000:
        print(f"Vídeo de teste já existe: {nome}")
        return nome

    url = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4"

    print("Baixando vídeo de teste...")
    r = requests.get(url, verify=False, stream=True, timeout=30)
    with open(nome, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Download concluído: {nome}")
    return nome


def baixar_video_youtube(url):
    """Baixa vídeo do YouTube usando yt-dlp."""
    import subprocess

    print("Baixando vídeo do YouTube...")
    nome = "video_youtube.mp4"

    if os.path.exists(nome) and os.path.getsize(nome) > 10000:
        print(f"Vídeo já existe: {nome}")
        return nome

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--js-runtimes", "node",
        "--remote-components", "ejs:github",
        "-f", "231",
        "-o", nome,
        url
    ]

    resultado = subprocess.run(cmd, capture_output=True, text=True)

    if resultado.returncode != 0:
        print(f"Erro: {resultado.stderr}")
        sys.exit(1)

    print(f"Download concluído: {nome}")
    return nome


if __name__ == "__main__":
    print("=== Detecção de Objetos em Vídeo ===")
    print("1 - Vídeo local")
    print("2 - Vídeo do YouTube (URL)")
    print("3 - Vídeo de teste (download automático)")
    print("4 - Câmera web")

    opcao = input("\nEscolha uma opção (1-4): ").strip()

    if opcao == "1":
        caminho = input("Caminho do vídeo: ").strip()
        detectar_objetos_video(caminho)

    elif opcao == "2":
        url = input("URL do YouTube [Enter para usar padrão]: ").strip()
        if not url:
            url = "https://www.youtube.com/watch?v=6r5D5Gs2lvY"
        caminho_video = baixar_video_youtube(url)
        detectar_objetos_video(caminho_video)

    elif opcao == "3":
        caminho_video = baixar_video_teste()
        detectar_objetos_video(caminho_video)

    elif opcao == "4":
        detectar_objetos_video(0)

    else:
        print("Opção inválida!")
