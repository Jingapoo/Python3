import os
import glob
from pprint import pprint
import logging
import boto3
import openpyxl

try :
    import gnupg
except ImportError as e:
    print(" Please install gnupg module! pip install python-gnupg")


try :
    import boto3
except ImportError as e:
    print(" Please install boto3 module!")



try:
    import openpyxl
except ImportError as e:
    print(" Please install openpyxl module! pip install openpyxl")



ENCRYPTED_FOLDER       = "/home/jingaroo/Desktop/gpg_decryption/downloading_file/"
DECRYPTED_FOLDER       = "/home/jingaroo/Desktop/gpg_decryption/decrypted_file/"
BUCKET_PREFIX_GPG      = "tmobile/EMPLOYEE"
BUCKET_PREFIX_TXT      = "tmobile/TESTING"
BUCKET_FOLDER          = "tmobile/"
BUCKET_DECYPTED_FOLDER = "tmobile/decrypted/"
BUCKET_PROCESSED_FOLDER = "tmobile/processed/"
BUCKET_NAME            = 'wvdb-staging'
GNUPH_HOME             = "/home/jingaroo/.gnupg/"
PASS_PHARSE            = 'allOw+-waTch'



#access one bucket
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(BUCKET_NAME)

logging.basicConfig(level=logging.INFO)



def download_file_from_s3(object_name, target_file_path):
    """Download files from Bucket"""
    assert object_name is not None
    assert target_file_path is not None
    downloading = s3.meta.client.download_file(BUCKET_NAME, object_name, target_file_path)
    return downloading





def decrypt_gpg_file(encrypted_file_path, decrypt_file_path):
    """ DECRYPT THE FILE """
    assert encrypted_file_path is not None
    assert decrypt_file_path is not None
    status = False
    gpg    = gnupg.GPG(gnupghome=GNUPH_HOME)
    with open(encrypted_file_path, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=PASS_PHARSE, output=decrypt_file_path )
    return status





def move_to_processed(encrypted_file_path, processed_file_name):
    """move the original file to process folder"""
    assert encrypted_file_path is not None
    assert processed_file_name is not None

    moving = s3.meta.client.upload_file(encrypted_file_path, BUCKET_NAME, BUCKET_PROCESSED_FOLDER + processed_file_name)
    return moving

def delete_after_moved(file_name_key):
    """delete the file from bucket"""
    assert file_name_key is not None

    deleting = s3.meta.client.delete_object(Bucket=BUCKET_NAME, Key=file_name_key)
    return deleting

def upload_file_to_s3(decrypted_file_path, decrypted_file_name):
    """upload files to AWS S3"""
    assert decrypted_file_path is not None
    assert decrypted_file_name is not None

    uploading = s3.meta.client.upload_file(decrypted_file_path, BUCKET_NAME, BUCKET_DECYPTED_FOLDER + decrypted_file_name)
    return uploading

def empty_my_local_dir(local_path):
    """delete all the files in my local folders"""
    assert local_path is not None

    empty_folder = glob.glob(local_path, recursive=True)
    for f in empty_folder:
        #print(f)
        os.remove(f)
    return empty_folder



def run():
    """MAIN function"""

    # Loop through the bucket and check if any xlsx.gpg exists
    for my_bucket_obj in my_bucket.objects.filter(Prefix=BUCKET_PREFIX_GPG).all():

        encrypted_s3_file_name = my_bucket_obj.key
        encrypted_file         = encrypted_s3_file_name.replace(BUCKET_FOLDER, "")
        encrypted_file_path    = ENCRYPTED_FOLDER + encrypted_file
        decrypted_file_name    = encrypted_file.replace( ".gpg", "")
        decrypted_file_path    = DECRYPTED_FOLDER + decrypted_file_name


        if "xlsx.gpg" in encrypted_file:

            # STEP 1
            # Download the file from S3
            #logging.info('Starting downloading the encrypted file from s3.. '+ BUCKET_NAME + '/'+ BUCKET_FOLDER + ' ... ')
            #download_file_from_s3(encrypted_s3_file_name, encrypted_file_path)
            #logging.info('File '+ encrypted_file_path + ' saved successfully')

            # STEP 2
            # Decrypt the file
            #logging.info('Starting decrypting the file.....')
            #decrypt_gpg_file(encrypted_file_path, decrypted_file_path)
            #logging.info('File '+ decrypted_file_path + ' decrypted successfully')


            # STEP 3
            # Modify Excel worksheet title
            for file in glob.glob(decrypted_file_path):
                print(file)
                wb = openpyxl.load_workbook(file)
                tg_sheet = wb.active
                tg_sheet = wb['Data']
                tg_sheet.title = 'EmployeeData'
                wb.save(file)
            """
            # STEP 4
            # UPLOAD TO S3
            logging.info('Starting uploading the file to S3 bucket..... '+ BUCKET_NAME + '/' + BUCKET_DECYPTED_FOLDER)
            upload_file_to_s3(decrypted_file_path, decrypted_file_name)
            logging.info('File '+ decrypted_file_name + 'uploaded to S3 bucket successfully')

            # STEP 5
            # move the original file to processed folder
            logging.info('Starting moving the file to processed....' + BUCKET_NAME + '/' + BUCKET_PROCESSED_FOLDER)
            move_to_processed(encrypted_file_path, encrypted_file)
            logging.info('File '+ encrypted_file + ' moved successfully')

            # STEP 6
            # DELETE THE FILE
            logging.info('Starting deleting the file ....' + BUCKET_NAME + '/' + BUCKET_FOLDER)
            delete_after_moved(encrypted_s3_file_name)
            logging.info('File '+ encrypted_file + ' deleted successfully')


    for my_bucket_object in my_bucket.objects.filter(Prefix=BUCKET_PREFIX_TXT).all():

        encrypted_s3_file_name_txt = my_bucket_object.key
        encrypted_file_txt         = encrypted_s3_file_name_txt.replace(BUCKET_FOLDER, "")
        encrypted_file_path_txt    = ENCRYPTED_FOLDER + encrypted_file_txt
        decrypted_file_name_txt    = encrypted_file_txt.replace( ".gpg", "")
        decrypted_file_path_txt    = DECRYPTED_FOLDER + decrypted_file_name_txt


        if "txt.gpg" in encrypted_file_txt:

            # STEP 1
            # Download the file from S3
            logging.info('Starting downloading the encrypted file from s3.. '+ BUCKET_NAME + '/'+ BUCKET_FOLDER + ' ... ')
            download_file_from_s3(encrypted_s3_file_name_txt, encrypted_file_path_txt)
            logging.info('File '+ encrypted_file_path_txt + ' saved successfully')

            # STEP 2
            # Decrypt the file
            logging.info('Starting decrypting the file.....')
            decrypt_gpg_file(encrypted_file_path_txt, decrypted_file_path_txt)
            logging.info('File '+ decrypted_file_path_txt + ' decrypted successfully')


            # STEP 3
            # UPLOAD TO S3
            logging.info('Starting uploading the file to S3 bucket..... '+ BUCKET_NAME + '/' + BUCKET_DECYPTED_FOLDER)
            upload_file_to_s3(decrypted_file_path_txt, decrypted_file_name_txt)
            logging.info('File '+ decrypted_file_name_txt + 'uploaded to S3 bucket successfully')

            # STEP 4
            # move the original file to processed folderDECRYPTED_FOLDER
            logging.info('Starting moving the file to processed....' + BUCKET_NAME + '/' + BUCKET_PROCESSED_FOLDER)
            move_to_processed(encrypted_file_path_txt, encrypted_file_txt)
            logging.info('File '+ encrypted_file_txt + ' moved successfully')

            # STEP 5
            # DELETE THE FILE
            logging.info('Starting deleting the file ....' + BUCKET_NAME + '/' + BUCKET_FOLDER)
            delete_after_moved(encrypted_s3_file_name_txt)
            logging.info('File '+ encrypted_file_txt + ' deleted successfully')

#To Erase all the files from ENCRYPTED_FOLDER and DECRYPTED_FOLDER after uploaded to AWS S3
    empty_my_local_dir(ENCRYPTED_FOLDER + '*.gpg')
    empty_my_local_dir(DECRYPTED_FOLDER + '*.xlsx')
    empty_my_local_dir(DECRYPTED_FOLDER + '*.txt')
"""

run()
