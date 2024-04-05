A Prometheus exporter for NTI ENVIROMUX® Environment Monitoring System (EMS) with 1-Wire Sensor Interface. 
Made using Python3.10

The script looks for the ip address of the EMS and uses a webscraper to convert data into prometheus metrics. At the moment it only scrapes for internal sensors. 
If there are future requests for external sensor pulling I can implement that.

#Setup
