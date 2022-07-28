#!/usr/bin/python3

import os
import glob
import gnupg
from pprint import pprint
import boto3
import openpyxl


ENCRYPTED_FOLDER       = "/home/jingaroo/Desktop/gpg_decryption/downloading_file/"
DECRYPTED_FOLDER       = "/home/jingaroo/Desktop/gpg_decryption/decrypted_file/"
#access one bucket
s3 = boto3.resource('s3')
#my_bucket = s3.Bucket('wvdb-staging')
"""
def decrypt_gpg_file(input_file, decrypt_file):

    gpg = gnupg.GPG(gnupghome='/home/jingaroo/.gnupg/')

    input_file_path = "/home/jingaroo/Desktop/gpg_decryption/downloading_file/" + input_file
    output_file_path = '/home/jingaroo/Desktop/gpg_decryption/decrypted_file/'
    with open(input_file_path, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase='allOw+-waTch', output=output_file_path + decrypt_file)

    return status
"""
"""
# This function is to loop through a directory and print the name of the files
# r=root, d=directories, f = files
#for r, d, f in os.walk(DECRYPTED_FOLDER):
    #for file in f:
        #print(file)
        wb = openpyxl.load_workbook(os.path.join(local_decrypted_path,file))
        if wb:
            tg_sheet = wb.active
            tg_sheet = wb['Data']
            tg_sheet.title = 'EmployeeData'
            wb.save(os.path.join(local_decrypted_path,file))

"""
 #The above function and below one works the same way 
decrypted_folder_path = DECRYPTED_FOLDER + "*.xlsx"
for file in glob.glob(decrypted_folder_path):
    print(file)
    wb = openpyxl.load_workbook(file)
    tg_sheet = wb.active
    tg_sheet = wb['Data']
    tg_sheet.title = 'EmployeeData'
    wb.save(file)
        #decrypt_gpg_file(file, file)
        #upload_file_to_s3(DECRYPTED_FOLDER + file, file)
        #move_to_processed(ENCRYPTED_FOLDER + file, file)




"""This function is to empty the directory delete all the files
def empty_my_local_dir(local_path):
    #delete all the files in my local folders
    assert local_path is not None

    empty_folder = glob.glob(local_path, recursive=True)
    for f in empty_folder:
        #print(f)
        os.remove(f)
    return empty_folder


for my_bucket_obj in my_bucket.objects.filter(Prefix="tmobile/EMPLOYEE").all():
    print(my_bucket_obj)

    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_10_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_11_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_13_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_14_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_15_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_16_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_17_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_18_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_19_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_20_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_21_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_22_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_23_0830PT_Wireless_Vision_LLC.txt.gpg')
    s3.meta.client.delete_object(Bucket='wvdb-staging', Key='tmobile/decrypted/TESTINGFIL01_2020_02_24_0830PT_Wireless_Vision_LLC.txt.gpg')
"""
    #encrypted_s3_file_name = my_bucket_obj.key
    #print(encrypted_s3_file_name)
    #s3.meta.client.delete_object(Bucket='wvdb-staging', Key=encrypted_s3_file_name)
#for my_bucket in my_bucket.objects.all():
    #print(my_bucket)

#key_data = open('Wireless_Vision_LLC_KeyPair_Backup_2020.asc').read()
#import_keys = gpg.import_keys(key_data)
#pprint(import_keys.results)

#public_keys = gpg.list_keys()
#private_keys = gpg.list_keys(True) #list secret keys
#for f in public_keys:
    #print(f['fingerprint'])
#pprint(public_keys)
#pprint(private_keys)

#def download_file_from_s3(object_name, file_name):

    #Download files from Bucket
    #downloading = s3.meta.client.download_file('wvssotest', object_name, '/home/jingaroo/Desktop/download_file_from_s3/'+ file_name)
    #return downloading



#def upload_file_to_s3(decrypt_file):

    #upload files to AWS S3
    #uploading = s3.meta.client.upload_file(DECRYPTED_FOLDER + decrypt_file, 'wvdb-staging', 'tmobile/decrypted/' + decrypt_file)
    #return uploading


#gpg.delete_keys("B59F31722D73E417C6AB43E33820182B0651F271")
#gpg.delete_keys("B59F31722D73E417C6AB43E33820182B0651F271", True, passphrase='allOw+-waTch') #private keys

#def encrypt_gpg_file(input_file, encrypted_file):

    #open(input_file,'w').write("!!!")
    #with open(input_file, 'rb') as f:
        #status = gpg.encrypt_file(f, recipients=['jruan@wirelessvision.com'], output=encrypted_file)
    #return status
    #print(status.status)
