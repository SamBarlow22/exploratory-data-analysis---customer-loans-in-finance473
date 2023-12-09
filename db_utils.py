import yaml
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

class RDSDatabaseConnector:
    def __init__(self, file_path='credentials.yaml'):
        # Load credentials from file
        self.credentials = self.load_credentials(file_path)
        if not self.credentials:
            raise ValueError("Failed to load credentials.")

        # Set up attributes
        self.host = self.credentials.get('RDS_HOST')
        self.password = self.credentials.get('RDS_PASSWORD')
        self.user = self.credentials.get('RDS_USER')
        self.database = self.credentials.get('RDS_DATABASE')
        self.port = self.credentials.get('RDS_PORT')
        self.engine = None

    def load_credentials(self, file_path='credentials.yaml'):
        try:
            with open(file_path, 'r') as file:
                credentials = yaml.safe_load(file)
                return credentials
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
            return None
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")
            return None

    def init_engine(self):
        if not self.engine:
            connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string)
            print("Engine initialized")

    def extract_loan_payments_data(self):
        self.init_engine()  # Ensure the engine is initialized before extracting data
        loan_payments_query = "SELECT * FROM loan_payments"
        return self.execute_query(loan_payments_query)

    def execute_query(self, query):
        try:
            result = pd.read_sql_query(query, self.engine)
            return result
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None

    def save_to_csv(self, dataframe, file_path='/Users/sambarlow/AI_Core/Finance_Project/loan_payments_data.csv'):
        try:
            dataframe.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")
        except Exception as e:
            print(f"Error saving data to CSV: {str(e)}")


test = RDSDatabaseConnector()  # Creates an instance of the RDSDatabaseConnector
data = test.extract_loan_payments_data()  # Extract loan payments data
test.save_to_csv(data) # Saves to csv file


