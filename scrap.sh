#!/bin/sh

#checking if report names and years both are given or not by checking if -r and -y is present in commandline arguments or not
if ! ((echo "$@" | grep -q -e '-r') && (echo "$@" | grep -q -e '-y';)) then
    echo "Usage: $0 -r <list_of_report_names> -y <list_of_years>"
    exit 1
fi

# Initialize variables
report_names=""
years=""

# Parse command line arguments to get list of report names and years
while [ "$#" -gt 0 ]; do
    case "$1" in
        -r)
            shift
            while [ "$1" != "-y" ] && [ "$#" -gt 0 ]; do
                report_names="$report_names $1"
                shift
            done
            ;;
        -y)
            shift
            while [ "$#" -gt 0 ]; do
                years="$years $1"
                shift
            done
            ;;
        *)
            shift
            ;;
    esac
done


for report in $report_names; do
  for year in $years; do
    echo "Getting report $report for year $year"
    python scrap.py -r $report -y $year
    echo ""
  done
done


