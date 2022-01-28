import os
from textblob import TextBlob
import csv
import glob


# Create a function to get the subjectivity
def getSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity

def write_csv_text_data(list_text_data_hadoop):
    """write csv for hadoop"""
    # create folder csv if nos exists
    final_directory = os.path.join(os.getcwd(), 'csv')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    # get the last csv for get file number data
    last_csv = glob.glob(f"{final_directory}/*")
    # get number
    if last_csv == [] :
        number_last_csv = 0
    else :
        number_last_csv = last_csv[-1].split("/")[-1].split(".")[0].split("data")[-1]

    # path csv create
    path = f'{final_directory}/data{int(number_last_csv) + 1}.csv'

    # write data text in csv
    if list_text_data_hadoop != []:
        keys = list_text_data_hadoop[0].keys()
        with open(path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list_text_data_hadoop)