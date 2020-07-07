I've used code from the Case Study in the following scripts: Audit_streets, audit_zip, create_and_connect_to_db, prepare_for_database, sample, and schema. 

The Audit_Streets script is used to audit the street names for abbreviations and invalid characters. It contains the update_name function that is used to correct abbreviations in the prepare_for_database script. 

The audit_zip script is similar to audit_streets. It audits and corrects zip codes and the update_zipcode function is used in the prepare_for_database script. 

create_and_connect_to_db script is used to create the SQL database and create and populate the tables used. 

prepare_for_database is used to parse the XML file and import it into csv files while using update_name and update_zip to fix any errors. 

Sample is used to take a sample of the xml file for testing

schema contains the SQL schema used for the databse. 