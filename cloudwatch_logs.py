from datetime import datetime, timedelta
#import datetime #datetime module
import time
import boto3
"""CloudWatch Logs enables user to centralize the logs from all of systems, applications, and AWS services, in a single, highly scalable service. More easily view them, search them for specific error codes or patterns, filter them based on specific fields, or archive them securely for future analysis. CloudWatch Logs enables you to see all of your logs, regardless of their source, as a single and consistent flow of events ordered by time, and you can query them and sort them based on other dimensions, group them by specific fields, create custom computations with a powerful query language, and visualize log data in dashboards. """

LOG_GROUP = 'wv_log_ec2_monitoring'
LOG_STREAM = 'wv_log_ec2_resources_stream'
TIMESTAMP = int(round(time.time() * 1000)) #datetime.now() in millisecond


cloudwatchlogs = boto3.client('logs')


def cloudwatchlog_create_group(log_group_name):
    """
        Returns a response in JSON format
        This function takes log group name as an input.
        and create a group
    """
    response = cloudwatchlogs.create_log_group(logGroupName=log_group_name)
    #print(response)
    return response

def describe_log_group(log_group_name_prefix, limit):
    """
        Returns a response in JSON format
        :param log group name:
        :param limit: the maximum is 50
    """
    response = cloudwatchlogs.describe_log_groups(logGroupNamePrefix=log_group_name_prefix, limit=limit)
    #print(response)
    return response

def cloudwatchlog_create_stream(log_group_name, log_stream_name):
    """
        Returns a response in JSON format
        This function create a stream
        :param log group name:
        :param log stream name:
    """
    response = cloudwatchlogs.create_log_stream(logGroupName= log_group_name, logStreamName=log_stream_name)
    #print(response)
    return response

def describe_log_stream(log_group_name, log_stream_name_prefix, limit):
    """
        Returns a response in JSON format
        :param log group name:
        :param log stream name:
        :param limit: the maximum is 50
    """
    response = cloudwatchlogs.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name_prefix, limit = limit)
    #print(response)
    return response

def put_log_event(log_group_name, log_stream_name, log_event_timestamp, log_event_message, token):
    """
        Returns a response in JSON format
        This function create an event in the log
        :param log group name:
        :param log stream name:
        :param log event time stamp:
        :param log event message:
        :param sequenceToken for the next log event
    """
    response = cloudwatchlogs.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': log_event_timestamp, 'message': log_event_message}], sequenceToken=token)
    print(response) #including the next valid token
    return response

def delete_group(log_group_name):
    """
        Returns a response in JSON format
        This function delete the existing log group
    """
    response = cloudwatchlogs.delete_log_group(logGroupName=log_group_name)
    #print(response)

    return response

def delete_stream(log_group_name, log_stream_name):
    """
        Returns a response in JSON format
        This function delete a stream.
    """
    response = cloudwatchlogs.delete_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    #print(response)
    return response

def pull_logs_by_date_for_past_hour(log_group_name, log_stream_name, start_time_timestamp, end_time_timestamp):
    """
        Returns a response in JSON format
        This function get the log events and pull the logs by the dates.
    """

    response = cloudwatchlogs.get_log_events(logGroupName=LOG_GROUP, logStreamName=log_stream_name, startTime=start_time_timestamp, endTime=end_time_timestamp)

    events = response['events']
    for value in events:
        #timestamps = str(value['timestamp']) #timestamp type is int
        messages = value['message'] # is equivalent to response['events'][1]['message'] type string
        print(messages)

    #print(response)
    return response


if __name__ == '__main__':


    """Cloudwatchlogs"""
    #log_group = cloudwatchlog_create_group(LOG_GROUP)
    #log_stream = cloudwatchlog_create_stream(LOG_GROUP, LOG_STREAM)
    #describe_streams = describe_log_stream(LOG_GROUP, 'wv', 50)
    #SEQUENCE_TOKEN = describe_streams['logStreams'][0]['uploadSequenceToken']
    """first log message, the token is empty string, for the second log message, requires the sequenceToken from the preceding message"""
    #put_events = put_log_event(LOG_GROUP, LOG_STREAM, TIMESTAMP, time.strftime('%Y-%m-%d %H:%M:%S') + "\t" + "'Error': " + 'clwM_005' + "," + " 'message': 'The Instance ID: " + "i-0f613d80929dd0bd0" + " " + "Disk_Space" + " usage is very high!', 'data': " + "{'usage': 365479.0, 'ec2_instance_id': i-0f613d80929dd0bd0}", SEQUENCE_TOKEN)


    past_the_hour = datetime.now() - timedelta(weeks=1)
    timestamp_in_millisec = int((time.mktime(past_the_hour.timetuple()) + past_the_hour.microsecond/1e6)*1000)
    #print(timestamp_in_millisec)
    #print(TIMESTAMP)
    pull_logs_by_date_for_past_hour(LOG_GROUP,LOG_STREAM,timestamp_in_millisec,TIMESTAMP)
