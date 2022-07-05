import os

dirs = [
    os.path.join("data", "raw"),
    os.path.join("data","processed"),
    "notebooks",
    "saved_models",
    "production_model",
    "src",
    'prediction_service'
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)

    if dir_ in ["saved_models","production_model"]:
        with open(os.path.join(dir_, ".gitignore"), "w") as f:
            f.write('/model.joblib')

