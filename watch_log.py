import boto3
from CloudWatchService import *
from datetime import datetime, timedelta
import time
import re
from config import *

""" The purpose of this class is to monitor logs in cloudwatch and send a notification whenever there is a specifice error code """

simple_email_service = boto3.client('ses')
PAST_THE_HOUR = datetime.now() - timedelta(hours=24)
TIMESTAMP_MILLISEC = int((time.mktime(PAST_THE_HOUR.timetuple()) + PAST_THE_HOUR.microsecond/1e6)*1000)
LOG_GROUP = 'wv_log_ec2_monitoring'
LOG_STREAM = 'wv_log_ec2_resources_stream'



class Notification(object):


    def send_customized_email(self, to_address, cc_address, subject_data, text_data, source):

        """
            This function composes an email message and immediately queues it for sending.
            :param to_address:
            :param cc_address:
            :param subject_data:
            :param text_data:
            :param source: verified email address sender
        """
       
        response = simple_email_service.send_email(Destination={'ToAddresses':[to_address,], 'CcAddresses':[cc_address,],}, Message={'Body':{'Text':{'Data':text_data,},}, 'Subject':{'Data': subject_data,},}, Source=source)

        #print(response)
        return response


if __name__ == "__main__":

    cloudwatchservice  = CloudWatchService()
    watchlog = Notification()
    error_messages = cloudwatchservice.pull_logs_by_error_code(LOG_GROUP, LOG_STREAM, TIMESTAMP_MILLISEC, TIMESTAMP)

    admin_email_list = Admin_email.split(",")
    #for emails in admin_email_list:
        #print(emails)
    #print(admin_email_list) #convert sting to a list
    
    subject_data = "Cloudwatch Error - "
    text_data = "Hello!" + "\n" + "\n" + "Just to let you know, we've seen more of the following error over the past hour." + "\n\n"

    
    for errors in error_messages:
        #print(errors)
        match_error = re.search(r'clwM_\w+', errors)
        if match_error:
            error_code = match_error.group()
            #print(error_code)

        match_id = re.search(r'i-\w+', errors)
        if match_id:
            instance_id = match_id.group()
            #print(instance_id)

        instance_tag_name = cloudwatchservice.get_instance_name_tag(instance_id)

        if error_code and instance_tag_name:

            subject = subject_data + error_code + " - " + instance_tag_name
            #print(subject)
            text_errors = text_data + "Description:"+ "\n\n" + errors[50:] + "\n\n" + "For more details, please visit AWS Cloudwatch website."
            #print(text_errors)
            
            for emails in admin_email_list:

                watchlog.send_customized_email(emails, emails, subject, text_errors, emails)
            

    