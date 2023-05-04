from sqlalchemy import create_engine, MetaData
import logging
import sqlalchemy
import boto3
import base64
import json
from botocore.exceptions import ClientError

from typing import Generator
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SECRETSMANAGER_RDS_PG_ID = 'mdm-boton-dev-secretrds-CNX'


class DB:
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """

        if DB.__instance is not None:
            raise Exception(
                "This class is a singleton, use DB.create()")
        else:
            DB.__instance = self
        self.engine = self.create_engine()

    @staticmethod
    def create():
        if DB.__instance is None:
            DB.__instance = DB()

        return DB.__instance

    @staticmethod
    def get_secret(secret_name):
        client = boto3.client('secretsmanager')

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

            return json.loads(secret)

    def get_credentials(self):
        """ Fetch credentials from either environment variables (for testing) or AWS Secret Manager"""
        if SECRETSMANAGER_RDS_PG_ID is None:
            return {
                'username': ('postgres'),
                'password': ('some_password'),
                'host': ('POSTGRESQL_HOST', 'localhost'),
                'port': (5432),
                'database': ('user_database'),
            }

        # get all access credentials from secrets manager
        credentials = DB.get_secret(SECRETSMANAGER_RDS_PG_ID)

        return {
            'username': credentials['username'],
            'password': credentials['password']
        }

    def create_engine(self):
        credentials = DB.get_credentials(self)

        return sqlalchemy.create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
            engine='postgresql+psycopg2',
            user=credentials['username'],
            password=credentials['password'],
            host='aw1074001-mdm-boton-dev-clusteraurora.cluster-cfipykvuspbv.us-east-1.rds.amazonaws.com',
            port='5432',
            database='mdmckddb'
        ),
            pool_size=200,
            max_overflow=0
        )

    def connect(self):
        return self.engine.connect()


meta = MetaData(schema="mdmkey")

engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{database}'.format(
    engine='postgresql+psycopg2',
    user='username',
    password='password',
    host='aw1074001-mdm-boton-dev-clusteraurora.cluster-cfipykvuspbv.us-east-1.rds.amazonaws.com',
    port='5432',
    database='mdmckddb'
),
    pool_size=200,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
