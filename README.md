# earth-speaks

Tools used for research in curation and analysis of Earth data.

## Installation

- Install Python 3 
- Make a new Python 3 environment (with Python 3.6 this is `python3 -m venv /path/to/new/virtual/environment`)
- Activate the environment with `source env/bin/activate`
- Update pip with `pip install --upgrade pip`
- Install dependencies with `pip install -r requirements.txt`
- Set Jupyter notebooks to use the environment's python with `python -m ipykernel install --user`
- Fill in the private `credentials/` folder
- Some scripts communicate with cloud instances that you may have to set up - see `amazon.md`

## Organization

```
analysis/
  ... code for running various gensim models on collected data
cleaning/
  serialize.py         - methods turn JSON-like structures into text
  nature/
     convert.py        - methods to turn Nature articles into documents
common.py              - common functions
credentials/           - stores JSON files of various formats with credentials
                       - not checked into repo
data/
  ... collect data from mining to this unchecked directory
elastic/
  elastic-manage.ipynb - tools for creating indices
  elastic-ingest.py    - tool for massively parallel data ingestion
mining/
  authenticate.ipynb   - run to refresh credentials for cookie-based mining
  ... each data source has a subdirectory with methods to populate data/
resources/
  ... misc files such as information needs observed from nature papers,
      and AWS code
turk/
  
```

## Data sources
Currently the system has two data sources included: NASA EarthData and _Nature.com_ journal papers on climate. To most accurately answer human queries about the earth we may want to consider other sources.

## Amazon Machine Images (AMIs)
Amazon AMI's are clonable cloud computers that exist in a frozen state but remain ready to spring to life when needed. This project relies on certain types of AWS instances that have been preserved as AMI's:

- _Repository AMI_: Contains this repository and some mined data from _Nature.com_ papers.
- _Elasticsearch Node AMI_: An instance that has been optimized to perform as an Elasticsearch node with Kibana.
- _Elasticsearch Proxy AMI_: An instance running the NGINX server software that lies between system users and the Elasticsearch node(s) for protection. Also serves analyzer debugging web page. 

For more details about bringing these AMI's to life and allowing them to talk to each other, see `amazon.md`.

## Intended Workflow
1. Run scripts found in `mining` to populate data in `data/` directory, either locally or from EC2 instances set up from the repo AMI.
2. Use the Elasticsearch node AMI to set up one or more EC2 instances to function as an Elasticsearch cluster. Then set up the Elasticsearch proxy AMI to authenticate and proxy traffic to the cluster (see amazon README)
3. Use `elastic-manage.ipynb` to set up one or more indices on the newly created node(s). Test analyzers using the analysis tester page (included already in the Proxy AMI, source is in `resources/`)
4. Either locally or in parallel across Repository AMI EC2 instances, ingest data to the Elasticsearch cluster (or use a reindex command if an existing index exists with the data already).
5. Given a budget for providing ground-truth, use scripts in `turk/` to create MTurk HIT's (mini internet jobs) from the existing systems using pooling strategies.
6. Use scripts in `analysis/` to investigate ways of improving the system. Use the continuous evaluation notebook to estimate the effectiveness and validation cost of new and improved systems.
7. Return to step 3. Aim is to improve until we have a system that returns resources capable of actually answering the natural language queries.
8. Optionally set up a pricing alarm using `resources/aws-lambda-watch.py` to keep a closer eye on charges incurred by the system.

## Code improvements needed
- Structured data to doc2vec
- Selenium redo credentials
	- Failure detection of file downloads
- For NASA: Make datum files not entries in a pickled object - should not be so memory reliant.
- More robust creation of HIT's
