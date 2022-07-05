import pysftp
def sftpExample():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None


    hostname = '138.85.180.211'
    username = 'emitpiy'
    password = ''

    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        sftp.put('C://Users//emitpiy//OneDrive - Ericsson AB//Projects//mlops//ml_template//ml_template//data_given//winequality.csv','/data/ml_pipeline/mlruns/mlflow_artifacts/winequality.csv')  # upload file to public/ on remote
        sftp.close()

sftpExample()