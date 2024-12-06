import os

def save_files(files, upload_folder):
    """
    Salva arquivos enviados para o servidor e retorna uma lista de URLs para download.
    """
    file_urls = []
    for file in files:
        if file.filename == '':
            continue

        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        file_urls.append(f"/download/{file.filename}")

    return file_urls


def get_file_path(upload_folder, filename):
    """
    Verifica se o arquivo existe e retorna o caminho completo.
    """
    file_path = os.path.join(upload_folder, filename)
    return file_path if os.path.exists(file_path) else None