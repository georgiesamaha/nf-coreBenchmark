# nf-coreBenchmark
Benchmarking scripts and config testing 

## Set up 

Load following modules to use nf-core and download workflow code base and containers:
```
module load nextflow 
module load python3 
module load singularity 
```

Set Singularity cache directory: 
```
NXF_SINGULARITY_CACHEDIR': /scratch/er01/gs5517/singularity
```

## Fetch configs 

Configure Python3 installation using a virtual environment to isolate project and dependencies: 

```
python3 -m pip install --user requests
python3 -m venv env
source env/bin/activate
pip install requests
pip install prettytable
```

Run script to output summary of all nf-core pipeline's withLabel resource settings. Only provides cpu, time, memory for process_single, process_low, process_medium, process_high, process_highmemory. 

```
python3 fetchConfigs.py
```
