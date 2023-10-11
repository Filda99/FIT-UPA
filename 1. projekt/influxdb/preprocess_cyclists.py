import csv
from datetime import datetime

# Define the input datetime string
def convertToTimestamp(input_datetime_str):
    # Define the input datetime format
    input_format = "%Y/%m/%d %H:%M:%S+00"
    # Parse the input datetime string
    input_datetime = datetime.strptime(input_datetime_str, input_format)
    # Calculate the Unix epoch timestamp in seconds
    unix_timestamp = int(input_datetime.timestamp())
    # Print the Unix epoch timestamp
    # print(unix_timestamp)
    return(unix_timestamp)

#########################################################
# Open the input CSV file
with open('cykl.csv', 'r') as input_file:
    csv_reader = csv.DictReader(input_file)

    # Open an output file to write the reformatted data
    with open('reformatted.txt', 'w') as output_file:

        for row in csv_reader:
            datum_cas = row['DATUM_CAS']
            pocet_prujezdu_zleva = row['POCET_PRUJEZDU_ZLEVA']
            pocet_prujezdu_zprava = row['POCET_PRUJEZDU_ZPRAVA']
            id_lokality = row['ID_LOKALITY']

            reformatted_date = convertToTimestamp(datum_cas)
            int_as_string = str(reformatted_date)
            # Remove carriage returns from the string representation
            cleaned_string = int_as_string.strip()
            # Convert the cleaned string back to an integer
            reformatted_date = int(cleaned_string)

            # Format the data in InfluxDB line protocol format
            influxdb_line = f'cyclistsCount,location={id_lokality} cyclistsFromLeft={pocet_prujezdu_zleva},cyclistsFromRight={pocet_prujezdu_zprava} {reformatted_date}\n'

            # Write the reformatted line to the output file
            output_file.write(influxdb_line)


print("Data has been reformatted and saved to 'formatted_data.txt'.")
