# core-api

### Quickstart

Install dependencies
```
pip install -r requirements.txt
```

Build Azure Cosmos DB Gremlin database
```
python -m scripts.init_codebase.build_gremlin
```

The user needs to configure the following environment variables

```
MONGODB_URI=
GREMLIN_URI=
GREMLIN_USER=
GREMLIN_PASSWORD=
G=
TRANSLATOR_KEY=
TRANSLATOR_ENDPOINT=
TRANSLATOR_LOCATION=
QUANTUM_SUBSCRIPTION_ID=
QUANTUM_NAME=
QUANTUM_LOCATION=
QUANTUM_RESOURCE_ID=
QUANTUM_RESOURCE_GROUP=
```

Run web app

```
python app.py
```

Go to `http://localhost:8080`.

### Note on Transcribing Code in `src/quantum_bundle.py`

Code blocks from the Azure Quantum Quickstart Docs as well as from the Qiskit Docs (https://qiskit.org/textbook/ch-algorithms/grover.html) were transcribed onto this repository for the Grover implementation. However, the final structure of the Grover's algorithm implementation, as well as the cost function procedure, are my own work. 
