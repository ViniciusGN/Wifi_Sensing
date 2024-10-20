import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob, cv2
import shutil

# Função para carregar dados do arquivo .mat
def load_csi_data(file_path):
    """
    Carrega os dados CSI de um arquivo .mat.
    
    Args:
        file_path (str): Caminho para o arquivo .mat.
    
    Returns:
        amplitude (ndarray): Amplitude absoluta dos dados CSI.
        csi_amp_data (ndarray): Dados CSI originais.
    """
    # Carregar o arquivo .mat
    mat_data = scipy.io.loadmat(file_path)
    return mat_data['CSIamp']


def plot_heatmap2(file_path, heatmap_folder, prefix):
    # Carregar os dados de CSI
    data = load_csi_data(file_path)
    
    # Verificar se o número de linhas é divisível por 3 blocos de 114 linhas
    if data.shape[0] != 342:
        raise ValueError("O dataset não tem o número correto de linhas (342).")
    
    # Separar os dados em blocos de 114 linhas cada
    bloco_1 = data[0:114]   # Linhas 1 a 114
    bloco_2 = data[114:228] # Linhas 115 a 228
    bloco_3 = data[228:342] # Linhas 229 a 342
    
    # Combinar os blocos em uma lista para facilitar o loop
    blocos = [bloco_1, bloco_2, bloco_3]
    
    # Gerar um heatmap para cada bloco
    for i, bloco in enumerate(blocos):
        plt.figure(figsize=(10, 6))
        plt.imshow(bloco, aspect='auto', cmap='hot', interpolation='nearest')
        plt.colorbar(label='Amplitude')
        plt.title(f'Heatmap {i + 1} - Bloco {i + 1}')
        plt.xlabel('Unidades de Coleta')
        plt.ylabel('Subportadoras')
        
        # Definir o caminho de saída específico por prefixo e índice
        heatmap_path = os.path.join(heatmap_folder, f'{i + 1}_{prefix}.png')
        plt.savefig(heatmap_path)
        plt.close()
        print(f"Heatmap {i + 1} salvo em {heatmap_path}")

def video_creator(caminho_pasta):
    """
    Cria um vídeo a partir das imagens em uma pasta.

    Args:
        caminho_pasta (str): Caminho da pasta que contém as imagens.

    Returns:
        None
    """
    # Verifica se a pasta existe
    if not os.path.exists(caminho_pasta):
        print("Pasta não encontrada.")
        return

    # Obtém a lista de arquivos de imagem na pasta
    arquivos_imagem = glob.glob(os.path.join(caminho_pasta, "*.jpg"))

    # Verifica se há imagens na pasta
    if not arquivos_imagem:
        print("Nenhuma imagem encontrada na pasta.")
        return

    # Define as configurações do vídeo
    largura = 640
    altura = 480
    fps = 30

    # Cria um objeto VideoWriter
    video_writer = cv2.VideoWriter(
        os.path.join(caminho_pasta, "video.mp4"),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (largura, altura)
    )

    # Lê as imagens e as adiciona ao vídeo
    for arquivo_imagem in arquivos_imagem:
        imagem = cv2.imread(arquivo_imagem)
        imagem = cv2.resize(imagem, (largura, altura))
        video_writer.write(imagem)

    # Libera o objeto VideoWriter
    video_writer.release()

    print("Vídeo criado com sucesso!")

def copy_files(src_folder, dst_folder, prefix):
    """
    Copia os arquivos de uma pasta para outra.

    Args:
        src_folder (str): Caminho da pasta de origem.
        dst_folder (str): Caminho da pasta de destino.
        prefix (str): Prefixo dos arquivos a serem copiados.

    Returns:
        None
    """
    for file in os.listdir(src_folder):
        if file.startswith(prefix):
            shutil.copy(os.path.join(src_folder, file), dst_folder)

def main():
    # Caminho para a pasta contendo os arquivos
    folder_path = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/train_amp/'
    
    # Caminho para a pasta onde os heatmaps serão salvos
    heatmap_folder = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/Heatmaps/'
    
    # Verifica se a pasta para os heatmaps existe, se não, cria
    if not os.path.exists(heatmap_folder):
        os.makedirs(heatmap_folder)
    
    # Listas de prefixos de arquivos
    prefixes = ['a', 'b', 'c']
    
    # Gerar heatmaps para os arquivos de a13 a a19, b13 a b 19, c13 a c19
    for folder in os.listdir(folder_path):
        if folder.isdigit():  # Verifica se a pasta é numerada (001 a 015)
            folder_path_specific = os.path.join(folder_path, folder)
            heatmap_folder_specific = os.path.join(heatmap_folder, folder)
            if not os.path.exists(heatmap_folder_specific):
                os.makedirs(heatmap_folder_specific)
            for prefix in prefixes:
                for i in range(13, 20):
                    # Nome do arquivo
                    file_name = f'{prefix}{i}.mat'
                    file_path = os.path.join(folder_path_specific, file_name)
                    
                    # Gerar os heatmaps para o arquivo atual
                    plot_heatmap2(file_path, heatmap_folder_specific, f'{prefix}{i}')
    
    # Copiar arquivos para a pasta Video_Maker_a_train
    video_maker_folder = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/Video_Maker_a_train/'
    if not os.path.exists(video_maker_folder):
        os.makedirs(video_maker_folder)
    for folder in os.listdir(heatmap_folder):
        if folder.isdigit():  # Verifica se a pasta é numerada (001 a 015)
            heatmap_folder_specific = os.path.join(heatmap_folder, folder)
            copy_files(heatmap_folder_specific, video_maker_folder, '3_a')
    
    # Criar vídeo
    video_creator(video_maker_folder)

if __name__ == "__main__":
    main()