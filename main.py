import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob
import shutil
import imageio
import cv2 as cv

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

# Função para gerar heatmap agregado das atividades
def plot_heatmap_multifiles(folder_path, num_files):
    """
    Gera um heatmap agregado para os dados CSI de múltiplos arquivos.
    
    Args:
        folder_path (str): Caminho para a pasta contendo os arquivos.
        num_files (int): Número de arquivos a serem agregados.
    """
    aggregated_amplitude = None

    # Carrega e agrega os dados dos arquivos
    for i in range(13, 13 + num_files):  # Ajustando para começar de 13
        file_name = f'a{i:02}.mat'  # Formatação correta do nome do arquivo
        file_path = os.path.join(folder_path, file_name)
        
        if not os.path.exists(file_path):  # Verifica se o arquivo existe
            print(f"Arquivo não encontrado: {file_path}")
            continue  # Pula para o próximo arquivo se não for encontrado
        
        amplitude, _ = load_csi_data(file_path)

        # Agrega os dados
        if aggregated_amplitude is None:
            aggregated_amplitude = amplitude
        else:
            aggregated_amplitude += amplitude  # Você pode mudar para outra operação como np.mean()

    # Normaliza a amplitude agregada, se necessário
    if aggregated_amplitude is not None:
        aggregated_amplitude /= num_files  # Dividir pela quantidade de arquivos para média

        # Gera o heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(aggregated_amplitude, cmap="viridis", cbar=True)
        plt.title('Heatmap Agregado das Amplitudes CSI')
        plt.xlabel('Packet Index')
        plt.ylabel('Subcarrier Index')
        plt.show()
    else:
        print("Nenhum dado foi agregado para o heatmap.")
        
# Função para gerar heatmap para um único arquivo
def plot_heatmap1(file_path):
    """
    Gera um heatmap para os dados CSI de um único arquivo.
    
    Args:
        file_path (str): Caminho para o arquivo .mat.
    """
    # Carrega os dados
    amplitude, _ = load_csi_data(file_path)

    # Gera o heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(amplitude, cmap="viridis", cbar=True)
    plt.title(f'Heatmap das Amplitudes CSI para {os.path.basename(file_path)}')
    plt.xlabel('Packet Index')
    plt.ylabel('Subcarrier Index')
    plt.show()

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

def create_video_from_images(path, pattern, output_video_name='output_video.mp4', fps=1):
    # Verifica se o diretório raiz existe
    if not os.path.exists(path):
        print(f"O caminho {path} não existe.")
        return

    all_images = []

    # Verifica se há subpastas
    subfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    if subfolders:
        # Caso haja subpastas, percorre cada uma delas
        for folder in subfolders:
            folder_path = os.path.join(path, folder)
            # Obtém imagens que começam com o padrão especificado e têm extensão .png
            images = [f for f in os.listdir(folder_path) if f.startswith(pattern) and f.endswith('.png')]
            # Ordena as imagens para garantir a sequência correta
            images.sort()
            all_images.extend([os.path.join(folder_path, img) for img in images])
    else:
        # Caso não haja subpastas, verifica as imagens diretamente na pasta fornecida
        images = [f for f in os.listdir(path) if f.startswith(pattern) and f.endswith('.png')]
        images.sort()
        all_images.extend([os.path.join(path, img) for img in images])

    # Verifica se foram encontradas imagens
    if not all_images:
        print("Nenhuma imagem encontrada.")
        return

    # Cria o vídeo
    with imageio.get_writer(output_video_name, fps=fps) as writer:
        for image_path in all_images:
            frame = imageio.imread(image_path)
            writer.append_data(frame)

    print(f"Vídeo criado com sucesso: {output_video_name}")

def main():
    # Caminho para a pasta contendo os arquivos
    base_folder_path = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/train_amp/'
    
    # Caminho para a pasta onde os heatmaps serão salvos
    heatmap_folder = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/Heatmaps/'
    
    # Verifica se a pasta para os heatmaps existe, se não, cria
    if not os.path.exists(heatmap_folder):
        os.makedirs(heatmap_folder)
    
    # Listas de prefixos de arquivos
    prefixes = ['a', 'b', 'c']
    
    # Gerar heatmaps para os arquivos de a13 a a19, b13 a b19, c13 a c19
    for folder_num in range(1, 16):  # Para pastas 001 a 015
        folder_path = os.path.join(base_folder_path, f'{folder_num:03}')  # Formata como 001, 002, ..., 015
        if not os.path.exists(folder_path):
            print(f"Pasta {folder_path} não encontrada. Pulando...")
            continue

        # Criar pasta correspondente para heatmaps
        specific_heatmap_folder = os.path.join(heatmap_folder, f'{folder_num:03}')
        if not os.path.exists(specific_heatmap_folder):
            os.makedirs(specific_heatmap_folder)

        for prefix in prefixes:
            for i in range(13, 20):
                # Nome do arquivo
                file_name = f'{prefix}{i}.mat'
                file_path = os.path.join(folder_path, file_name)
                
                # Verifica se o arquivo existe antes de tentar gerar o heatmap
                if os.path.exists(file_path):
                    # Gerar os heatmaps para o arquivo atual
                    plot_heatmap2(file_path, specific_heatmap_folder, f'{prefix}{i}')
                else:
                    print(f"Arquivo {file_path} não encontrado. Pulando...")

if __name__ == "__main__":
    # main()
    create_video_from_images("C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/Heatmaps/Video_Maker_a_train/type2_001", "2_", "output_video.mp4", 4)
    
    # # Caminho para a pasta contendo os arquivos
    # folder_path = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/train_amp/001/'
    
    # # Caminho para a pasta onde os heatmaps serão salvos
    # heatmap_folder = 'C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/Heatmaps/'
    
    # # Verifica se a pasta para os heatmaps existe, se não, cria
    # if not os.path.exists(heatmap_folder):
    #     os.makedirs(heatmap_folder)
        
    # # Carregar e processar o arquivo .mat
    # file_name = 'a13.mat'
    # file_path = os.path.join(folder_path, file_name)
    # print(load_csi_data(file_path))
    
    # # Gerar os heatmaps
    # plot_heatmap2(file_path, heatmap_folder)    

# def plot_heatmap2(file_path, heatmap_folder):
#     # Carregar o arquivo .mat
#     mat_data = scipy.io.loadmat(file_path)  # Corrigir essa linha 
       
#     data = mat_data['CSIamp']
    
#     # Dividir o dataset em 3 subconjuntos de 114 linhas
#     split_data = np.split(data, 3)
    
#     # Separar o dataset sendo um ciclo de 3 conjuntos
     
    
#     # Gerar um heatmap para cada subconjunto
#     for i, subset in enumerate(split_data):
#         plt.figure(figsize=(10, 6))
#         plt.imshow(subset, aspect='auto', cmap='hot', interpolation='nearest')
#         plt.colorbar(label='Amplitude')
#         plt.title(f'Heatmap {i + 1} - Linhas {i * 114 + 1} a {(i + 1) * 114}')
#         plt.xlabel('Unidades de Coleta')
#         plt.ylabel('Subportadoras')
        
#         # Salvar o heatmap
#         heatmap_path = os.path.join(heatmap_folder, f'heatmap_{i + 1}.png')
#         plt.savefig(heatmap_path)
#         plt.close()
#         print(f"Heatmap {i + 1} salvo em {heatmap_path}")