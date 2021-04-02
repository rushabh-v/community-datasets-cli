# community-datasets-cli
   \- POC for GSoC proposal

## Installation

Run,
1. `git clone https://github.com/rushabh-v/community-datasets-cli`
2. `cd community-datasets-cli`
3. `python setup.py install`

## Usage

- **Register a namespace**

  1. Run `community_datasets register`
  2. Enter a new namespace and create a password

- **Deploy a dataset**

  1. Run `community_datasets deploy`
  2. Enter Your registered namespace,
  password,
  dataset name, and
  path to the dataset generator scripts

- **Load a dataset**
  1. Run this [colab notebook](https://colab.research.google.com/drive/1uDaq6EmSlm97ud7kkEBNChL2eQnADtnU?usp=sharing) and replace namespace and ds_name with your namespace and the dataset name of your deployed dataset.
  - I had to make [certain changes](https://github.com/rushabh-v/datasets/commit/6214af9825ea5c767106a39170b8e064b1a9368d) in the builder classes of TFDS, in order to make tfds.load compatible with my demo.
