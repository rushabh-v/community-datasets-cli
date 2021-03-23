import sys
import requests
import zipfile
import os
import tempfile
import getpass

from community_datasets import config

MODE = sys.argv[1]
CRED = '\033[91m'
CEND = '\033[0m'
CSEL = '\33[7m'
CGRN = '\033[92m'


def call(username, password=None, dataset_name=None, file=None, mode=None):
    if mode is None:
        mode = MODE
    return requests.post(
        config.URL,
        params={
            "code": config.CODE,
            "mode": mode,
            "username": username,
            "password": password,
            "dataset_name": dataset_name,
        },
        files = {"file": file}
    )


def register():
    print(CSEL + "Enter new namespace:" + CEND + " ", end="")
    username = input()
    password = getpass.getpass(CSEL + "Create new password:" + CEND + " ")
    cnf_password = getpass.getpass(CSEL + "Confirm password:" + CEND + " ")

    if password == cnf_password:
        res = call(username, password)
        if res.status_code == 200:
            print(CGRN + res.text + CEND)
        else:
            print(CRED + res.text + CEND)
    else:
        print(CRED + "Passwords didn't match, try again." + CEND)


def add_dataset():
    print(CSEL + "Enter your namespace:" + CEND + " ", end="")
    username = input()
    password = getpass.getpass(CSEL + "Your password:" + CEND + " ")
    print(CSEL + "Enter dataset name:" + CEND + " ", end="")
    dataset_name = input()
    print(CSEL + "Enter path to parent directory the dataset generator scripts:" + CEND + " ", end="")
    dataset_path = input()
    cur_dir = os.getcwd()
    if not os.path.isdir(dataset_path):
        raise Exception(f"No such file or directory: {dataset_path}")

    os.chdir(dataset_path)
    os.system(f"zip -r {dataset_name}.zip *")
    file = open(f"{dataset_name}.zip", "rb")

    res = call(username, password, dataset_name, file)
    if res.status_code == 200:
        print(CGRN + res.text + CEND)
    else:
        print(CRED + res.text + CEND)

    os.remove(f"{dataset_name}.zip")
    os.chdir(cur_dir)


def get_data(username=None, dataset_name=None, return_cls=False, cls_name=None):
    if not username:
        print(CSEL + "Enter username:" + CEND + " ", end="")
        username = input()
    if not dataset_name:
        print(CSEL + "Enter dataset name:" + CEND + " ", end="")
        dataset_name = input()

    res = call(username, password=None, dataset_name=dataset_name, mode="download")
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
            print(CGRN + "Script downloaded." + CEND)
    else:
        print(CRED + res.text + CEND)


if __name__ == "__main__":

    if MODE == "register":
        register()
    elif MODE in ("add", "update"):
        add_dataset()
    elif MODE == "download":
        get_data()
    else:
        raise NotImplementedError()
