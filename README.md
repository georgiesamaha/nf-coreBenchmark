# nf-coreBenchmark
Benchmarking scripts and config testing 

## Approach 

Create optimised configuration file that can handle nf-core pipelines dynamically adjusting resource allocations based on the needs specified in each pipeline's `base.config` file. Considerations: 

1. Computational nature of each pipeline. RNAseq is CPU intensive, ChIP-seq is IO intensive. Need to understand what the pipeline's bottlebecks are and what it does 
2. Parse and understand `base.config` files. Write a script to extract cpu, memory and time parameters for each. 
3. Perform benchmarking on NCI Gadi and Pawsey Setonix HPCs to understand performance and efficiency. 
4. Use resource management settings like maxRetries, ability to set max number of simultaneous tasks. 

## Parse `base.config` 

Configure Python3 installation using a virtual environment to isolate project and dependencies: 

```
python3 -m pip install --user requests
python3 -m venv env
source env/bin/activate
pip install requests re github
```

Then run: 
```
python3 fetchConfigs.py
```

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


