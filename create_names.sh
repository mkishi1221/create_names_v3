#!/bin/bash

project_id=$1

if [ -z "$project_id" ]
then
    printf "Enter project ID or press enter to escape: "
    read -r  project_id

    if [ -z "$project_id" ]
    then
        exit
    fi
fi

project_path="projects/$project_id"

if [ ! -d $project_path ];
then
    printf "Project files with name \"$project_id\" not detected. Press Y to create new project files, press N to look for existing project or press enter to escape: "
    read -r  affirm

    if [[ $affirm == "Y" || $afirm == "y" ]];
    then
        mkdir -p $project_path/data/others

        echo "Project folders created: place relevant data in data folder and run script again."
        exit
    
    elif [[ $affirm == "N" || $afirm == "n" ]];
    then
        printf "Enter project ID or press enter to escape: "
        read -r  project_id
        project_path="projects/$project_id"

        if [ -z "$project_id" ]
        then
            exit
        elif [ ! -d $project_path ]
        then
            echo "Project files with name $project_id not found. Exiting script..."
        fi

    else
        exit
    fi
fi

# Calculate time elapsed
date
start_time=`gdate +%s%3N`

# Clear tmp files
rm -rf $project_path/tmp/keyword_generator/*
rm -rf $project_path/tmp/name_generator/*
rm -rf $project_path/tmp/domain_checker/*
rm -rf $project_path/results/${project_id}_names.xlsx
rm -rf $project_path/results/${project_id}_domains.xlsx
mkdir -p $project_path/tmp/keyword_generator
mkdir -p $project_path/tmp/logs
mkdir -p $project_path/results/

# Generate word list from source text
# Words to be sorted by POS, length and other factors in the future to accomodate more complex name-generating algorithms.
echo "Starting name generator..."
python3 name_generator/name_generator.py \
    $project_id

# Calculate time elapsed
end_time=`gdate +%s%3N`
min_elapsed=$(echo "scale=0; (${end_time}-${start_time})/1000/60" | bc )
sec_elapsed=$(echo "scale=3; ((${end_time}-${start_time})/1000)-(${min_elapsed}*60)" | bc )
echo "All files processed. Total: ${min_elapsed}min, ${sec_elapsed}sec." 
date
