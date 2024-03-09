
# Dependencies Installation
Run the **install_dependencies.sh** script to install the dependencies.
```
sh install_dependencies.sh
```
# Scrapping HTML Files.
Run the **scrap.sh** script to download reports in the form of HTML files.
```
sh scrap.sh -r <list_of_report_names> -y <list_of_years>
```
Here is an example.
```
sh scrap.sh -r 1.1.1 14.1. -y 2021-2022 2022-2023
```
# Report numbers that can be scrapped.
* 1.1.1
* 5.1.1
* 5.1.5
* 7.1.1
* 7.1.2
* 14.1.
* 6.1.1
* 7.2.1
* 6.9.

# Generating the reports from the scrapped html files
First make sure that you have a folder named html in the current directory which would contain the folders for the individual report numbers mentioned above
Run the **generate_reports.py** file to generate the csv_files folder which would contains the csv files for the individual report numbers
```
generate_reports.py
```
Run **merge_report1.py** to get report1, and the csv file csv_files/515.csv can be copied and renamed as report2.csv
```
merge_report1.py
```
