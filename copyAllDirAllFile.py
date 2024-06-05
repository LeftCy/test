import os
from azure.storage.blob import BlobServiceClient

# Azuriteのデフォルトアカウントとキー
account_name = 'devstoreaccount1'
account_key = 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='

# アップロードするディレクトリのパスとコンテナ名を指定
upload_path = ''  # 任意のローカルディレクトリを指定
container_name = ''  # 任意のコンテナ名を指定

# BlobServiceClientを作成
blob_service_client = BlobServiceClient(account_url=f'http://localhost:10000/{account_name}', credential=account_key)

# コンテナが存在しない場合は作成
container_client = blob_service_client.get_container_client(container_name)
if not container_client.exists():
    container_client.create_container()

# ディレクトリとファイルを再帰的にアップロードする関数
def upload_directory_to_blob(upload_path, container_name):
    for root, dirs, files in os.walk(upload_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            blob_path = os.path.relpath(file_path, upload_path)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f'"{file_path}" をコンテナ "{container_name}" にアップロードしました。')

# アップロード処理を実行
upload_directory_to_blob(upload_path, container_name)
