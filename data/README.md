# data

This directory will hold all data used during project

## instructions for downloading data

csv files
-test set values https://s3.amazonaws.com/drivendata-prod/data/7/public/702ddfc5-68cd-4d1d-a0de-f5f566f76d91.csv
-training set labels https://s3.amazonaws.com/drivendata-prod/data/7/public/0bf8bc6e-30d0-4c50-956a-603fc693d966.csv
-training set values https://s3.amazonaws.com/drivendata-prod/data/7/public/4910797b-ee55-40a7-8668-10efd5c1b960.csv

## values information:
-amount_tsh - Total static head (amount water available to waterpoint)
-date_recorded - The date the row was entered
-funder - Who funded the well
-gps_height - Altitude of the well
-installer - Organization that installed the well
-longitude - GPS coordinate
-latitude - GPS coordinate
-wpt_name - Name of the waterpoint if there is one
-num_private -
-basin - Geographic water basin
-subvillage - Geographic location
-region - Geographic location
-region_code - Geographic location (coded)
-district_code - Geographic location (coded)
-lga - Geographic location
-ward - Geographic location
-population - Population around the well
-public_meeting - True/False
-recorded_by - Group entering this row of data
-scheme_management - Who operates the waterpoint
-scheme_name - Who operates the waterpoint
-permit - If the waterpoint is permitted
-construction_year - Year the waterpoint was constructed
-extraction_type - The kind of extraction the waterpoint uses
-extraction_type_group - The kind of extraction the waterpoint uses
-extraction_type_class - The kind of extraction the waterpoint uses
-management - How the waterpoint is managed
-management_group - How the waterpoint is managed
-payment - What the water costs
-payment_type - What the water costs
-water_quality - The quality of the water
-quality_group - The quality of the water
-quantity - The quantity of water
-quantity_group - The quantity of water
-source - The source of the water
-source_type - The source of the water
-source_class - The source of the water
-waterpoint_type - The kind of waterpoint
-waterpoint_type_group - The kind of waterpoint

## labels information:
-functional - the waterpoint is operational and there are no repairs needed
-functional needs repair - the waterpoint is operational, but needs repairs
-non functional - the waterpoint is not operational

values and labels information can be obtained at https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/25/#features_list
