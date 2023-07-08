#!/bin/bash

# You need to add the list of nf-core workflows you want to benchmark
workflows=("nf-core-rnaseq-3.12.0" "nf-core-sarek-3.2.3")

# Path to the benchmark reports directory
reports_dir="/scratch/er01/gs"

# Go through each workflow
for workflow in ${workflows[@]}; do

    # Run each workflow with the '-with-report' option to generate resource usage reports
    nextflow run $workflow -profile test -with-report ${reports_dir}/${workflow}_report.html

    # Here, you might need to parse the generated HTML report to get the resource usage details for each process. 
    # As an alternative, you could use the `-with-trace` option when you run the pipeline to generate a CSV file with resource usage details.
    # Assuming you have done this and now you have a CSV file

    # Path to the benchmark CSV file
    benchmark_csv="${reports_dir}/${workflow}_trace.csv"

    # Go through each line (i.e., each process) in the CSV file
    while IFS=, read -r col1 col2 col3 col4 col5 col6
    do
        # Calculate the SUs
        su=$(echo "$col3 * $col4 * $col5" | bc)

        # Here, you might want to compute the efficiency too. For this, you would need to define what "efficiency" means for you.
        # For example, you could define it as the ratio of actual CPU time used to the total CPU time allocated.
        # Assuming you've calculated it and it's stored in a variable called $efficiency

        # Print the SUs and efficiency
        echo "Process $col1: SU = $su, Efficiency = $efficiency"

    done < "$benchmark_csv"

done
