import pysftp
def sftpExample():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None


    hostname = '<>'
    username = '<>'
    password = ''

    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        sftp.put('./winequality.csv','/data/ml_pipeline/mlruns/mlflow_artifacts/winequality.csv')  # upload file to public/ on remote
        sftp.close()

sftpExample()