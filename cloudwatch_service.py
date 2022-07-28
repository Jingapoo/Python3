from datetime import datetime, timedelta
import time
import boto3
import csv
import math


seconds_in_every_5_mins_of_past_hour = 300 #getting past an hour
seconds_in_every_15_mins_of_past_2_weeks = 900
"""CloudWatch is a monitoring and observability service that collects data at every layer of the performance stack, including metrics and logs, events.
It also visualize applications and infrastrcture using automated dashboards. It analyze metrics, logs and traces to better understand how to improve application performance. """

NAMESPACE = 'AWS/EC2'
DIMENSIONS_NAME = 'InstanceId'
DIMENSIONS_VALUE =  ['i-0d3ca72d3b03e667f', 'i-038eb6bd7b4ce2aca', 'i-0f613d80929dd0bd0', 'i-05d5cfb8f1c4d926a']

cloudwatch = boto3.client('cloudwatch')


def get_the_instance_id(list_of_metrics_json):

    """
        Returns a list of instance ID
        This function is pulling the dimensions value(instance ID)
        :param list_of_metrics_json:
    """
    instance_id_list = []
    metrics = list_of_metrics_json['Metrics']
    for data in metrics:
        #print(data['Dimensions'][0]['Value']) #type string
        instance_id = data['Dimensions'][0]['Value']
        instance_id_list.append(instance_id)
        
    #print(instance_id_list)
    return instance_id_list
        
    

def save_to_csv_file(input_dict,instance_id,output_csv):

    data_points = input_dict['Datapoints'] #return a list of dictionaries is equivalent to #for key in input_dict.keys() & {'Datapoints'}:
    for data in data_points: #is equivalent to #for v in input_dict[key]:
        list_of_values = list(data.values()) # dict_values convert to list
        list_of_values.insert(0,instance_id) #insert Instance Id in the list
        past_an_hour = list_of_values[1]
        max_string = str(list_of_values[2])
        formatting = format(past_an_hour, '%b-%d-%Y %H:%M:%S')
        #Modify list of values
        list_of_values[1] = formatting
        list_of_values[2] = max_string

        with open(output_csv, 'a', newline='') as output_file:
            wr = csv.writer(output_file, dialect='excel')
            wr.writerow(list_of_values)


def mean_of_maximum_usage(input_json):

    """
        Returns the mean of all the maximum values for the past 2 weeks
        This function takes an input as JSON format and
        get the maximum CPU utilization, calculates the total sum of
        the maximum values and divided by the number of maximum values.
    """

    num_value_list = []
    data_points = input_json['Datapoints']
    for data in data_points:
        max_usage = data['Maximum']
        num_value_list.append(max_usage)

    average_of_maximum_usage = sum(num_value_list)/len(num_value_list)
    #print(average_of_maximum_usage) #list

    return average_of_maximum_usage



def daily_usage_vs_average_maximum_usage(input_dict, instance_id, dict, EC2_instance_stats):


    """
        Returns a text file which stores all the EC2_INSTANCE_LOG statistics
        This function takes an input as JSON formThis function takes an input as JSON format and
        get the daily maximum CPU utilization, and compare to the mean of CPU utilization
        for the past 2 weeks.
        if the daily usage is greater than average usage, it stores the data records
        to the text file.at and
        get the daily maximum CPU utilization, and compare to the mean of CPU utilization
        for the past 2 weeks.
        if the daily usage is greater than average usage, it stores the data records
        to the text file.
    """

    mean_of_usage = mean_of_maximum_usage(dict)
    EC2_INSTANCE_LOG = []
    data_points = input_dict['Datapoints']
    for data in data_points:
        max_usage = data['Maximum']
        abnormal_CPU_usage = {}

        if mean_of_usage == 0.0:
            eighty_percent_of_min = 0.0
        else:
            eighty_percent_of_min = abs((mean_of_usage - max_usage)/mean_of_usage) * 100

        #print("mean of usage: "+ str(mean_of_usage), "mini_usage: " + str(max_usage), "80 percent of minimum: "+ str(eighty_percent_of_min))

        if (max_usage < mean_of_usage) and (eighty_percent_of_min > 80.0):
            #print(max_usage)
            abnormal_CPU_usage['max_usage'] = max_usage
            abnormal_CPU_usage['ec2_instance_id'] = instance_id
            print(list(abnormal_CPU_usage.keys())[0])
            #if abnormal_CPU_usage.keys() == 'max_usage':
                #print("OK")
            #if abnormal_CPU_usage.keys() == 'mini_usage':
                #print("MM")
            EC2_INSTANCE_LOG.append(abnormal_CPU_usage)


    with open(EC2_instance_stats, 'a+') as filehandle:
        for list_items in EC2_INSTANCE_LOG:
            #if len(EC2_INSTANCE_LOG) != 0:
            #print(EC2_INSTANCE_LOG)
            filehandle.write('%s\n' % list_items)

def cloudwatch_metric_statistics(namespace, metric_name, dimensions_name, dimensions_value, start_time, end_time, period, statistics, unit):

    """
        Returns CPU maximum statistics as a JSON format
        :param namespace: 'AWS/EC2'
        :param metric_name: CPUUtilization
        :param dimensions_name: 'InstanceId'
        :param dimensions_value: id
        :param start_time: startTime
        :param end_time: endTime
        :param period: in seconds
        :param statistics: Maximum
        :param unit: Percentage
    """
    response_dict = cloudwatch.get_metric_statistics(Namespace=namespace,MetricName=metric_name, Dimensions=[{'Name': dimensions_name, 'Value': dimensions_value},], StartTime=start_time, EndTime=end_time, Period=period, Statistics=[statistics], Unit=unit)
    #print(response_dict)
    return response_dict

def cloudwatch_list_metrics(namespace, metric_name, dimensions_name):

    """
        Returns a list of metrics in a JSON format
        This function is pulling the dimensions value associated with dimensions name
        :param namespace: 'AWS/EC2'
        :param metric_name: CPUUtilization
        :param dimensions_name: 'InstanceId'
    """
    response = cloudwatch.list_metrics(Namespace=namespace,MetricName=metric_name, Dimensions=[{'Name': dimensions_name}])
    #print(response)
    return response


if __name__ == '__main__':

    metrics = cloudwatch_list_metrics(NAMESPACE,'CPUUtilization', DIMENSIONS_NAME)
    dimensions_value = get_the_instance_id(metrics)


    for instance_id in dimensions_value:
        CPU_ultilization_max = cloudwatch_metric_statistics(NAMESPACE,'CPUUtilization', DIMENSIONS_NAME, instance_id, datetime.now() - timedelta(hours=1), datetime.now(), seconds_in_every_5_mins_of_past_hour, 'Maximum', 'Percent')
        CPU_ultilization_mean_2_weeks = cloudwatch_metric_statistics(NAMESPACE,'CPUUtilization', DIMENSIONS_NAME, instance_id, datetime.now() - timedelta(weeks=2), datetime.now(), seconds_in_every_15_mins_of_past_2_weeks, 'Maximum', 'Percent')

        daily_usage_vs_average_maximum_usage(CPU_ultilization_max, instance_id, CPU_ultilization_mean_2_weeks, 'EC2_INSTANCE_STATS.txt')



    #Network_In = cloudwatch_metric_statistics(NAMESPACE,'NetworkIn', DIMENSIONS_NAME, DIMENSIONS_VALUE, datetime.now() - timedelta(hours=1), datetime.now(), seconds_in_every_5_mins_of_past_hour, 'Maximum', 'Bytes')

    #Network_Out = cloudwatch_metric_statistics(NAMESPACE,'NetworkOut',  DIMENSIONS_NAME, DIMENSIONS_VALUE, datetime.now() - timedelta(hours=1), datetime.now(), seconds_in_every_5_mins_of_past_hour, 'Maximum', 'Bytes')



    #save_to_csv_file(CPU_ultilization_max, 'i-0d3ca72d3b03e667f', 'maximum_CPU_Ultilization.csv')
    #save_to_csv_file(Network_In, 'maximum_network_in.csv')
    #save_to_csv_file(Network_Out, 'maximum_network_out.csv')
