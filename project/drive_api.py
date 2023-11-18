# Copyright 2018 Minds.ai, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import logging
from typing import TypeVar, cast

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
from google.oauth2 import service_account
from mimetypes import guess_type
import io
from .configuration_interfaces import DriveConfig, SystemConfig, APIConfigBase

from .drive_api_exception import DriveAPIException

log = logging.getLogger('app')
S = TypeVar("S", bound=APIConfigBase)


class DriveAPI:
  def __init__(self, drive_config: S, sys_config: S):
    """Initializes instance of DriveAPI class.

    :param drive_config: configuration class containing all parameters needed for Google Drive.
    :param sys_config: configuration class containing all system related parameters.
    """
    self.drive_config = cast(DriveConfig, drive_config)
    self.sys_config = cast(SystemConfig, sys_config)

    self._scopes = ['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata']
    self._service = None

    self.setup()
  def setup(self):
    """Triggers the OAuth2 setup flow for Google API endpoints. Requires the ability to open
    a link within a web browser in order to work.
    """
    creds = None
    credentials_file = 'credenciales-cta-servicio.json'
        
    # Define los alcances (scopes) necesarios para el servicio que vas a utilizar
    self._scopes = ['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata']

    # Carga las credenciales de servicio desde el archivo JSON
    creds = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=self._scopes
    )

    self._service = build('drive', 'v3', credentials=creds)

    log.log(logging.INFO, 'Drive connection established.')
  def upload_file(self, file_path: str, name: str, folder_id: str) -> str:
      """Uploads the given file to the specified folder id in Google Drive.

      :param file_path: Path to file to upload to Google Drive.
      :param name: Final name of the file
      :param folder_id: The Google Drive folder to upload the file to
      :return: The url of the file in Google Drive.
      """
      
      print(f"Starting upload of file: {file_path}")

      if self._service is None:
          # Raise an exception if setup() hasn't been run.
          raise DriveAPIException(name='Service error', reason='setup() method not called.')

      if not file_path or not os.path.exists(file_path):
          # Raise an exception if the specified file doesn't exist.
          print("No encuentra el archivo en el proyecto")
          raise DriveAPIException(
              name='File error', reason=f'{file_path} could not be found.')

      # Google Drive file metadata
      metadata = {'name': name, 'parents': [folder_id]}

      print(f"Guessing MIME type for {file_path}")
      # Guess the mimetype based on file extension
      mimetype, _ = guess_type(file_path)
      if not mimetype:
          mimetype = "application/octet-stream"  # Tipo MIME genérico para datos binarios
      print(f"Guessed MIME type: {mimetype}")

      # Create a new upload of the recording and execute it.
      print(f"Creating MediaFileUpload with MIME type: {mimetype}")

      file_size = os.path.getsize(file_path)
      resumable_upload = file_size >= 1024 * 1024  # True si es mayor o igual a 1MB
      print(f"Resumable upload? {resumable_upload}")
      
      media = MediaFileUpload(file_path,
                              mimetype=mimetype,
                              chunksize=1024*1024,
                              resumable=resumable_upload
                              )

      request = self._service.files().create(body=metadata,
                                            media_body=media,
                                            fields='webViewLink',
                                            supportsTeamDrives=True
                                            )

      if resumable_upload:
          print(f"request {request}")
          response = None
          while response is None:
              status, response = request.next_chunk()
              if status:
                  print(f"Uploaded {int(status.progress() * 100)}%")
      uploaded_file = request.execute()

      log.log(logging.INFO, f'File {file_path} uploaded to Google Drive')

      # Return the url to the file that was just uploaded.
      return uploaded_file.get('webViewLink')
  def get_drive_recordings(self, meeting_id,extension):
        if meeting_id:
            # ID de la carpeta específica a buscar
            folder_id = "1PoFVsTKGO7aL9Gm380GWN-HQW6KnTHSX"

            # Realizar búsqueda del archivo en la carpeta específica
            query = f"'{folder_id}' in parents and name='{meeting_id}.{extension}'"
            page_token = None
            results = self._service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            # Obtener enlace de descarga del archivo
            if results.get('files', []):
                file_id = results['files'][0]['id']

                # Crear permisos para que cualquiera pueda descargar el archivo
                permission = self._service.permissions().create(
                    fileId=file_id,
                    body={'role': 'reader', 'type': 'anyone'},
                    fields='id',
                    supportsAllDrives=True
                ).execute()

                # Crear solicitud de descarga
                request = self._service.files().get_media(fileId=file_id)

                # Crear un objeto io.BytesIO para escribir el contenido descargado
                fh = io.BytesIO()

                # Descargar el archivo
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()

                # Guardar el contenido descargado en un archivo local
                with open(f"{meeting_id}.{extension}", 'wb') as f:
                    fh.seek(0)
                    f.write(fh.read())

                print(f"Archivo descargado exitosamente como {meeting_id}.{extension}")
            else:
                print("No se encontró el archivo.")

            return results

        return None