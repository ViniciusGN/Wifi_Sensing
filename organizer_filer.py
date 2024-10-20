import os
import shutil

# Define o caminho base onde as pastas já existem
caminho_base = r"C:/Users/User/Desktop/Documentos/Sensing/Wifi_Sensing/NTU-Fi-HumanID/Heatmaps/"
numero_pastas = 15

# Loop para organizar arquivos em subpastas a, b e c
for i in range(1, numero_pastas + 1):
    # Formata o número da pasta com zeros à esquerda
    pasta_num = f"{i:03}"
    pasta_path = os.path.join(caminho_base, pasta_num)
    
    # Verifica se a pasta principal existe
    if os.path.exists(pasta_path):
        # Cria subpastas a, b e c
        for letra in ['a', 'b', 'c']:
            subpasta = os.path.join(pasta_path, letra)
            os.makedirs(subpasta, exist_ok=True)  # Cria a subpasta se não existir
            
            # Move arquivos .png para a subpasta correspondente
            for arquivo in os.listdir(pasta_path):
                if arquivo.endswith('.png'):
                    # Define o caminho completo do arquivo
                    caminho_arquivo = os.path.join(pasta_path, arquivo)
                    
                    # Move o arquivo para a subpasta (a, b ou c)
                    novo_caminho = os.path.join(subpasta, arquivo)
                    shutil.move(caminho_arquivo, novo_caminho)

print("Arquivos organizados nas subpastas a, b e c com sucesso!")
