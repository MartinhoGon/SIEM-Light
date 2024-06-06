from api.models import Helper, Alert
from api.logger import get_logger
from api.utils import Parser
from datetime import datetime
import os

def parseLogFiles():
    logger = get_logger()
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("{} - Started parsing the syslog folder.".format(formatted_datetime))
    helper = Helper.objects.first()
    if helper.is_using_rsyslog:
        # Case its running rsyslog
        # Gets the folder were the remote logs are
        remotelogs_folder = "/var/log/remotelogs/" 
        try:
            for root, dirs, files in os.walk(remotelogs_folder):
                for file_name in files:
                    # if file_name.endswith('.log'):  # Check if the file is a log file
                    file_path = os.path.join(root, file_name)
                    logger.info("Parsing file '{}'.".format(file_path))
                    ip_datetime_pairs = Parser.extractLogInfo(file_path)
                    Alert.validateIpsFromRsyslog(ip_datetime_pairs, file_path)
        except Exception as e:
            logger.error("An error occorred while parsing the rsyslog files. {}".format(e))
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("{} - Ended parsing the syslog folder.".format(formatted_datetime))
            



