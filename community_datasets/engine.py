import sys
import requests
import zipfile
import os
import tempfile

from community_datasets import config

MODE = sys.argv[1]
CRED = '\033[91m'
CEND = '\033[0m'
CSEL = '\33[7m'


def call(username, dataset_name=None, file=None, mode=None):
    if mode is None:
        mode = MODE
    return requests.post(
        config.URL,
        params={
            "code": config.CODE,
            "mode": mode,
            "username": username,
            "dataset_name": dataset_name,
        },
        files = {"file": file}
    )


def register():
    print(CSEL + "Enter new username:" + CEND + " ", end="")
    username = input()
    print(call(username).text)


def add_dataset():
    print(CSEL + "Enter new username:" + CEND + " ", end="")
    username = input()
    print(CSEL + "Enter dataset name:" + CEND + " ", end="")
    dataset_name = input()
    print(CSEL + "Enter path to the dataset generator: " + CEND, end="")
    dataset_path = input()
    cur_dir = os.getcwd()
    if not os.path.isdir(dataset_path):
        raise Exception(f"No such file or directory: {dataset_path}")

    os.chdir(dataset_path)
    os.system(f"zip -r {dataset_name}.zip *")
    file = open(f"{dataset_name}.zip", "rb")
    print(call(username, dataset_name, file).text)
    os.remove(f"{dataset_name}.zip")
    os.chdir(cur_dir)


def get_data(username=None, dataset_name=None, return_cls=False, cls_name=None):
    if not username:
        print(CSEL + "Enter username:" + CEND + " ", end="")
        username = input()
    if not dataset_name:
        print(CSEL + "Enter dataset name:" + CEND + " ", end="")
        dataset_name = input()

    res = call(username, dataset_name, mode="download")
    if res.status_code == 200:
        path = tempfile.gettempdir() + "/community_datasets"
        if not os.path.isdir(path):
            os.mkdir(path)

        with open(f"{path}/{dataset_name}.py", "w") as f:
            f.write(res.text)

        if return_cls:
            import sys
            sys.path.append(path)
            statement = f"from {dataset_name} import {cls_name}"
            exec(statement)
            cls = locals()[cls_name]
            return cls
        else:
            return "Script downloaded."
    else:
        raise Exception(res.text)


if __name__ == "__main__":

    if MODE == "register":
        register()
    elif MODE == "add":
        add_dataset()
    elif MODE == "download":
        get_data()
    else:
        raise NotImplementedError()
