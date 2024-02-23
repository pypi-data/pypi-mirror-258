import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_to_table_records
import pandas as pd
from datetime import datetime

class FastlaneLogger:
    def __init__(self, key_vault_url, db_name, cluster_url_key, client_id_key, client_secret_key, authority_id_key, email_key, email_password_key):
        self.db_name = db_name
        self.key_vault_url = key_vault_url
        self.email_address = self._get_secret(email_key)
        self.email_password = self._get_secret(email_password_key)
        self.client = self._create_client(cluster_url_key, client_id_key, client_secret_key, authority_id_key)

    def _get_secret(self, secret_name):
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=self.key_vault_url, credential=credential)
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value

    def _create_client(self, cluster_url_key, client_id_key, client_secret_key, authority_id_key):
        try:
            cluster_url = self._get_secret(cluster_url_key)
            client_id = self._get_secret(client_id_key)
            client_secret = self._get_secret(client_secret_key)
            authority_id = self._get_secret(authority_id_key)

            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                cluster_url, client_id, client_secret, authority_id)
            return KustoClient(kcsb)
        except Exception as e:
            self._send_alert(f"Error creating Kusto client: {e}")
            raise

    def _send_alert(self, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = self.email_address  # O la dirección de correo electrónico del destinatario
            msg['Subject'] = "Kusto Logger Alert"
            body = message
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(self.email_address, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_address, self.email_address, text)
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")

    def _validate_data(self, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        if not data:
            raise ValueError("Data dictionary is empty")

    def _insert_data(self, table_name, data):
        try:
            self._validate_data(data)
            # Check if status is 'Failed'
            if data.get("Status") == "Failed":
                self._send_alert(f"Failure detected in {table_name}: {data}")

            df = pd.DataFrame([data])
            records = dataframe_to_table_records(df)
            query = f".ingest inline into table {table_name} <|"
            self.client.execute(self.db_name, query, records)
        except ValueError as ve:
            self._send_alert(f"Validation error: {ve}")
        except KustoServiceError as kse:
            self._send_alert(f"Kusto service error: {kse}")
        except Exception as e:
            self._send_alert(f"Unexpected error: {e}")

    def log_execution(self, execution_data):
        self._insert_data("ExecutionLog", execution_data)

    def log_data_load(self, load_data):
        self._insert_data("DataLoadLog", load_data)

    def log_data_transformation(self, transformation_data):
        self._insert_data("DataTransformationLog", transformation_data)

# Uso de la clase (ejemplo)
Fastlane_logger = FastlaneLogger(
    key_vault_url="https://your_key_vault_name.vault.azure.net",
    db_name="YourDatabaseName",
    cluster_url_key="KustoClusterUrl",
    client_id_key="KustoClientId",
    client_secret_key="KustoClientSecret",
    authority_id_key="KustoAuthorityId"
)

# ... Ejemplos de Logging para ExecutionLog...

# Inicio de un Notebook
Fastlane_logger.log_execution({
    "ExecutionID": "exec101",
    "NotebookName": "DataAnalysisNotebook",
    "StartTime": datetime.now(),
    "EndTime": None,
    "Duration": None,
    "Status": "In Progress",
    "ErrorMessage": "",
    "User": "analyst@example.com"
})

# Finalización Exitosa de un Notebook
Fastlane_logger.log_execution({
    "ExecutionID": "exec102",
    "NotebookName": "DataCleaningNotebook",
    "StartTime": datetime(2024, 2, 20, 9, 0, 0),
    "EndTime": datetime(2024, 2, 20, 9, 30, 0),
    "Duration": "00:30:00",
    "Status": "Completed",
    "ErrorMessage": "",
    "User": "datacleaner@example.com"
})

# Error Durante la Ejecución de un Notebook
Fastlane_logger.log_execution({
    "ExecutionID": "exec103",
    "NotebookName": "DataModelingNotebook",
    "StartTime": datetime(2024, 2, 20, 10, 0, 0),
    "EndTime": datetime(2024, 2, 20, 10, 15, 0),
    "Duration": "00:15:00",
    "Status": "Failed",
    "ErrorMessage": "Model training failed due to insufficient data",
    "User": "datamodeler@example.com"
})

# ... Ejemplos de Logging para DataLoadLog...

# Carga de Datos Exitosa:
Fastlane_logger.log_data_load({
    "LoadID": "load201",
    "Source": "ExternalAPI",
    "Destination": "DataWarehouse",
    "Volume": 500.0,
    "StartTime": datetime.now(),
    "EndTime": datetime.now(),
    "Status": "Success",
    "ErrorMessage": ""
})

# Carga de Datos con Error:
Fastlane_logger.log_data_load({
    "LoadID": "load202",
    "Source": "LocalFile",
    "Destination": "DataLake",
    "Volume": 200.0,
    "StartTime": datetime.now(),
    "EndTime": datetime.now(),
    "Status": "Failed",
    "ErrorMessage": "Archivo corrupto"
})

# ... Ejemplos de Logging para DataTrasnformationLog...

#Transformación de Datos Completada:
Fastlane_logger.log_data_transformation({
    "TransformationID": "trans301",
    "Description": "Normalización de datos",
    "VolumeInput": 1000.0,
    "VolumeOutput": 950.0,
    "StartTime": datetime.now(),
    "EndTime": datetime.now(),
    "Duration": "00:10:00",
    "Status": "Completed",
    "ErrorMessage": ""
})

# Transformación con Error en el Script:
Fastlane_logger.log_data_transformation({
    "TransformationID": "trans302",
    "Description": "Limpieza de datos",
    "VolumeInput": 800.0,
    "VolumeOutput": 0.0,
    "StartTime": datetime.now(),
    "EndTime": datetime.now(),
    "Duration": "00:05:00",
    "Status": "Failed",
    "ErrorMessage": "Error en el script de transformación"
})
