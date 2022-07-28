from CloudWatchService import daily_usage_vs_average_maximum_usage

def test_append_to_file(input_dict, instance_id, mean_of_dict, instance_stats_file):

        """
        Returns a text file which stores all the EC2_INSTANCE_LOG statistics
        This function takes a dictionary input from previous function 
        After loop through the dictionary, saving each record to a list
        then write the list to the text file as testing the output
        Testing purpose only....     
        """
        assert input_dict is not None
        assert instance_id is not None 
        assert mean_of_dict is not None 
        assert instance_stats_file is not None

        EC2_INSTANCE_DICT = daily_usage_vs_average_maximum_usage(input_dict, instance_id, mean_of_dict)
        EC2_INSTANCE_LOG = []
        EC2_INSTANCE_LOG.append(EC2_INSTANCE_DICT)
        #print(EC2_INSTANCE_LOG)
        with open(instance_stats_file, 'a+') as filehandle:
                for list_items in EC2_INSTANCE_LOG:
                        if list_items is not None:
                                #print(list_items)
                                filehandle.write('%s\n' % list_items)