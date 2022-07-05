import os


dirs = [
    os.path.join("data", "raw"),
    os.path.join("data","processed"),
    "notebooks",
    "saved_models",
    "production_model",
    "src",
    'prediction_service',
    'static',
    'templates',
    'logs'
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)

    if dir_ in ["saved_models","production_model"]:
        with open(os.path.join(dir_, ".gitignore"), "w") as f:
            f.write('/model.joblib')
    else:
        with open(os.path.join(dir_, ".gitkeep"), "w") as f:
            pass


files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py"),
    os.path.join("prediction_service", "__init__.py"),
    os.path.join("logs", "mlrun.log")
]

for file_ in files:
    with open(file_, "w") as f:
        pass