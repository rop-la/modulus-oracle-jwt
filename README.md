# Modulus Oracle & JWT (Demo)

## To run the web

You need [Docker](https://docs.docker.com/engine/install/) installed.

1. Clone the repository

```
git clone https://github.com/rop-la/modulus-oracle-jwt.git
```

2. Change the directory

```
cd modulus-oracle-jwt
```

3. Run with Docker (as root)

```
sudo ./run.sh
```

## To run the script

1. Create a virtual environment

```
virtualenv -p python3 venv
```

2. Activate the virtual environment

```
source venv/bin/activate
```

3. Install requirements

```
pip install -r requirements.txt
```

4. Run the script

```
python modulus-oracle-jwt.py
```
