import os
import pysftp
import argparse
from get_data import read_params
import datetime
import logging

# import logging
logging.basicConfig(filename='./logs/mlrun.log', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')


def transfer_artifacts(config_path):
    config = read_params(config_path)
    hostname= str(config['remote_server_details']['hostname'])
    username = str(config['remote_server_details']['username'])
    password = str(config['remote_server_details']['password'])
    model_directory = config['webapp_model_dir']
    local_path = os.path.join(os.getcwd(), model_directory, "model.joblib")
    remote_path = config['remote_server_details']['remote_model_location'] + "/model.joblib"
    print(f"saving '{local_path}'")
    print(f"saving to '{remote_path}'")

    # print(os.getcwd())
    # print(local_path)
    # print(remote_path)

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None


    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        sftp.put(
            local_path,
            remote_path)  # upload file to public/ on remote
        sftp.close()

    logging.info('New model sent to production at: ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_arg = args.parse_args()
    transfer_artifacts(config_path=parsed_arg.config)