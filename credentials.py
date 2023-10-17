from dotenv import load_dotenv
import os

load_dotenv()

USER_SQL_SINQIA_A = str(os.getenv('USER_SQL_SINQIA_A'))
PASS_SQL_SINQIA_A = str(os.getenv('PASS_SQL_SINQIA_A'))

USER_SQL_SINQIA_B = str(os.getenv('USER_SQL_SINQIA_B'))
PASS_SQL_SINQIA_B = str(os.getenv('PASS_SQL_SINQIA_B'))  # hml: boffice@2023
PASS_SQL_SINQIA_B = ''

USER_SQL_SINQIA_WM = str(os.getenv('USER_SQL_SINQIA_WM'))
PASS_SQL_SINQIA_WM = str(os.getenv('PASS_SQL_SINQIA_WM'))

USER_DB_ATIVA = str(os.getenv('USER_DB_ATIVA'))
PASS_DB_ATIVA = str(os.getenv('PASS_DB_ATIVA'))
DSN = str(os.getenv('DSN'))
SRV_SINQIA_HML = str(os.getenv('SRV_SINQIA_HML'))
SRV_SINQIA_PROD = str(os.getenv('SRV_SINQIA_PROD'))
PASS_CENTRAL_OP = str(os.getenv('PASS_CENTRAL_OP'))

URL_SINQIA = str(os.getenv('URL_SINQIA'))
