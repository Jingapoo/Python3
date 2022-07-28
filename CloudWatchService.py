import boto3
import math
import time
import re 

"""CloudWatch is a monitoring and observability service that collects data at every layer of the performance stack, including metrics and logs, events.
It also visualize applications and infrastrcture using automated dashboards. It analyze metrics, logs and traces to better understand how to improve application performance. 

CloudWatch Logs enables user to centralize the logs from all of systems, applications, and AWS services, in a single, highly scalable service.
More easily view them, search them for specific error codes or patterns, filter them based on specific fields, or archive them securely for future analysis. 
CloudWatch Logs enables you to see all of your logs, regardless of their source, as a single and consistent flow of events ordered by time, and you can query them and sort them based on other dimensions, group them by specific fields, create custom computations with a powerful query language, and visualize log data in dashboards. """

seconds_in_every_5_mins_of_past_hour = 300 #getting past an hour
seconds_in_every_15_mins_of_past_2_weeks = 900
eighty_percent = 80.0
TIMESTAMP = int(round(time.time() * 1000)) #datetime.now() in millisecond


cloudwatch = boto3.client('cloudwatch')
cloudwatchlogs = boto3.client('logs')
ec2 = boto3.resource('ec2')


"""Cloudwatch"""
class CloudWatchService(object):

    def get_the_running_instance_id(self):

        """
            Returns a list of instance ID
            This function is pulling all the running instance ID from EC2, 
            and put them in a list. 
        """

        instance_id_list = []

        for instance in ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values':['running']}]):
            #print(instance.id) #string
            instance_id_list.append(instance.id)
    
        return instance_id_list
        #print(instance_id_list)


    def get_instance_name_tag(self, instance_id):

        """
            This function is taking a given instance ID,
            return the instance name from the name tag.
            :params instance_id:
            :return tag_value = instance_id name:
        """

        for tag in ec2.Instance(instance_id).tags:
            if 'Name' in tag['Key']:
                name = tag['Value']
       
        #print(name)
        return name

 

    def mean_of_maximum_usage(self, input_json):

        """
            Returns the mean of all the maximum values for the past 2 weeks
            This function takes an input as JSON format and
            get the maximum utilization, calculates the total sum of
            the maximum values and divided by the number of maximum values.
            :param input_json
        """
        assert input_json is not None

        num_value_list = []
        data_points = input_json['Datapoints']
        if data_points:
            for data in data_points:
                max_usage = data['Maximum']
                num_value_list.append(max_usage)

            average_of_maximum_usage = sum(num_value_list)/len(num_value_list)
            #print(average_of_maximum_usage) #list

            return average_of_maximum_usage



    def daily_usage_vs_average_maximum_usage(self, input_dict, instance_id, mean_of_usage_dict):

        """
            Returns a text file which stores all the EC2_INSTANCE_LOG statistics
            This function takes an input as JSON form and 
            compare to the mean of usage for the past 2 weeks.
            if the daily usage is greater than average usage as well as greater than 80%, it stores the data records  
            :param input_dict
            :param instance_id
            :param mean_of_usage_dict   
        """
        assert input_dict is not None
        assert instance_id is not None 
        assert mean_of_usage_dict is not None 

        mean_of_usage = self.mean_of_maximum_usage(mean_of_usage_dict)# Call a function self.function() is like this.function() in JAVA
        data_points = input_dict['Datapoints']
        if data_points:
            for data in data_points:
                max_usage = data['Maximum']
                abnormal_usage = {}

                eighty_percent_of_min = 0.0
                if mean_of_usage == 0.0:
                    eighty_percent_of_min = 0.0
                else:
                    eighty_percent_of_min = abs((mean_of_usage - max_usage)/mean_of_usage) * 100
                
                if (max_usage > mean_of_usage) and (max_usage > eighty_percent):
                    #print(max_usage)
                    abnormal_usage['max_usage'] = max_usage
                    abnormal_usage['ec2_instance_id'] = instance_id

                if (max_usage < mean_of_usage) and (eighty_percent_of_min > eighty_percent):

                    abnormal_usage['mini_usage'] = max_usage
                    abnormal_usage['ec2_instance_id'] = instance_id

                
                if len(abnormal_usage) != 0:
                    #print(abnormal_usage)
                    return abnormal_usage


    
    def cloudwatch_list_metrics(self, namespace, metric_name, dimensions_name):

        """
            Returns a list of metrics in a JSON format
            This function is pulling the dimensions value associated with dimensions name
            :param namespace: 'AWS/EC2'
            :param metric_name: CPUUtilization
            :param dimensions_name: 'InstanceId'
        """
        assert namespace is not None
        assert metric_name is not None 
        assert dimensions_name is not None

        response = cloudwatch.list_metrics(Namespace=namespace,MetricName=metric_name, Dimensions=[{'Name': dimensions_name}])
        #print(response)
        return response


    def cloudwatch_metric_statistics(self, namespace, metric_name, dimensions_name, dimensions_value, start_time, end_time, period, statistics, unit, file_system_name=None, file_system_value=None, mount_path_name=None, mount_path_value=None):

        """
            Returns the maximum utilization's statistics as a JSON format
            Keyword argument
            :param namespace: 'AWS/EC2'
            :param metric_name: CPUUtilization, NetworkIn, NetworkOut, Memory Utilization
            :param dimensions_name: 'InstanceId'
            :param dimensions_value: id
            :param start_time: startTime
            :param end_time: endTime
            :param period: in seconds
            :param statistics: Maximum, Minimum
            :param unit: Percentage
            Positional argument follows keyword argument
            :param file_system_name: Optional
            :param file_system_value: Optional
            :param mount_path_name: Optional
            :param mount_path_value: Optional
        """
        assert namespace is not None
        assert metric_name is not None 
        assert dimensions_name is not None
        assert dimensions_value is not None
        assert start_time is not None 
        assert end_time is not None 
        assert period is not None 
        assert statistics is not None 
        assert unit is not None 


        response_dict = cloudwatch.get_metric_statistics(Namespace=namespace,MetricName=metric_name, Dimensions=[{'Name': dimensions_name, 'Value': dimensions_value}, {'Name': file_system_name, 'Value': file_system_value},{'Name': mount_path_name, 'Value': mount_path_value}], StartTime=start_time, EndTime=end_time, Period=period, Statistics=[statistics], Unit=unit)
        #print(response_dict)
        return response_dict


   
    """Cloudwatch Logs"""
    def cloudwatchlog_create_group(self, log_group_name):

        """
            Returns a response in JSON format
            This function takes log group name as an input.
            and create a group
            :param log_group_name:
        """
        assert log_group_name is not None
    
        response = cloudwatchlogs.create_log_group(logGroupName=log_group_name)
        #print(response)
        return response

    def describe_log_group(self, log_group_name_prefix, limit):

        """
            Returns a response in JSON format
            :param log group name:
            :param limit: the maximum is 50
        """
        assert log_group_name_prefix is not None
        assert limit is not None 

        response = cloudwatchlogs.describe_log_groups(logGroupNamePrefix=log_group_name_prefix, limit=limit)
        #print(response)
        return response

    def cloudwatchlog_create_stream(self, log_group_name, log_stream_name):

        """
            Returns a response in JSON format
            This function create a stream
            :param log group name:
            :param log stream name:
        """
        assert log_group_name is not None 
        assert log_stream_name is not None 

        response = cloudwatchlogs.create_log_stream(logGroupName= log_group_name, logStreamName=log_stream_name)
        #print(response)
        return response

    def describe_log_stream(self, log_group_name, log_stream_name_prefix, limit):

        """
            Returns a response in JSON format
            :param log group name:
            :param log stream name:
            :param limit: the maximum is 50
        """
        assert log_group_name is not None 
        assert log_stream_name_prefix is not None 
        assert limit is not None 

        response = cloudwatchlogs.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name_prefix, limit=limit)
        #print(response)
        return response

    def put_log_events(self, log_group_name, log_stream_name, log_event_timestamp, log_event_message, token):

        """
            Returns a response in JSON format
            This function create an event in the log
            :param log group name:
            :param log stream name:
            :param log event time stamp:
            :param log event message:
            :param sequenceToken for the next log event
        """
        assert log_group_name is not None 
        assert log_stream_name is not None 
        assert log_event_timestamp is not None 
        assert log_event_message is not None 
        assert token is not None 

        response = cloudwatchlogs.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': log_event_timestamp, 'message': log_event_message}], sequenceToken=token)
        #print(response) #including the next valid token
        return response

    def delete_group(self, log_group_name):

        """
            Returns a response in JSON format
            This function delete the existing log group
            :param: log_group_name
        """
        assert log_group_name is not None 

        response = cloudwatchlogs.delete_log_group(logGroupName=log_group_name)
        #print(response)

        return response

    def delete_stream(self, log_group_name, log_stream_name):

        """
            Returns a response in JSON format
            This function delete a stream.
            :param log_group_name:
            :param log_stream_name:
        """
        assert log_group_name is not None 
        assert log_stream_name is not None 

        response = cloudwatchlogs.delete_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        #print(response)
        return response

   

    def get_token(self, log_group_name, log_stream_name_prefix, limit):

        """
            Returns the Next Token
            :param log_group_name
            :param log_stream_name_prefix
            :param limit
        """
        assert log_group_name is not None 
        assert log_stream_name_prefix is not None 
        assert limit is not None 

        describe_streams = self.describe_log_stream(log_group_name, log_stream_name_prefix, limit)
        if describe_streams:
            SEQUENCE_TOKEN = describe_streams['logStreams'][0]['uploadSequenceToken']
            return SEQUENCE_TOKEN
   

   
    def push_events_to_log_stream(self, daily_usage_dict, mean_of_usage_dict, log_group_name, limit, error_code, instance_id, metric_name, sequence_token):

        """
            Returns a response in JSON format
            This function accepts a dictionary and convert it to string
            and push the events to the log stream
            :param daily_usage_dict:
            :param mean_of_usage_dict:
            :param log_group_name:
            :param limit:
            :param error_code:
            :param instance_id:
            :param metric_name:
        """
        assert daily_usage_dict is not None
        assert mean_of_usage_dict is not None
        assert log_group_name is not None 
        assert limit is not None
        assert error_code is not None 
        assert instance_id is not None 
        assert metric_name is not None 
        
        input_dict = self.daily_usage_vs_average_maximum_usage(daily_usage_dict, instance_id, mean_of_usage_dict)
       
        
        if input_dict:
            dict_to_str = str(input_dict)
            match_max_usage = re.search(r'max_\w+', dict_to_str)
            match_mini_usage = re.search(r'mini_\w+', dict_to_str)
            if match_max_usage:
                log_event_message = time.strftime('%Y-%m-%d %H:%M:%S') + "\t" + "'Error': " + error_code + "," + " 'message': 'The Instance ID: " + instance_id + " " + metric_name + " usage is very high!', 'data': " + dict_to_str
                return self.put_log_events(log_group_name, 'wv_log_ec2_resources_stream', TIMESTAMP, log_event_message, sequence_token)
            if match_mini_usage:
                log_event_message = time.strftime('%Y-%m-%d %H:%M:%S') + "\t" + "'Error': " + error_code + "," + " 'message': 'The Instance ID: " + instance_id + " " + metric_name + " usage is very low!', 'data': " + dict_to_str
                return self.put_log_events(log_group_name, 'wv_log_ec2_resources_stream', TIMESTAMP, log_event_message, sequence_token)
    


    def pull_logs_by_error_code(self, log_group_name, log_stream_name, start_time_timestamp, end_time_timestamp):

        """
            Returns error codes and assocated messages
            This function get the log events and pull error by code.
            :param log_group_name:
            :param log_stream_name:
            :param start_time_timestamp:
            :param end_time_timestamp:
        """
        assert log_group_name is not None 
        assert log_stream_name is not None 
        assert start_time_timestamp is not None 
        assert end_time_timestamp is not None 

        response = cloudwatchlogs.get_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, startTime=start_time_timestamp, endTime=end_time_timestamp)

        error_message_list = []
        events = response['events']
        if events:
            for value in events:
                messages = value['message']
                error_code = messages[29:33]

                if error_code == 'clwM': #20 is end of the '\t'

                    error_message_list.append(messages)
                
        #print(error_message_list)
        return error_message_list