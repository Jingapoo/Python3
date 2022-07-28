import xmlrpc.client 
from datetime import datetime as dt


# Login Credentials. 
url = 'https://uat.wirelessvision.com'
db_name = 'wireless_vision_uat_20200630'
username = 'admin'
password = 'B1st@123'

""" 
    This API is pull Data from Odoo to serving the POS interface. 
    xmlrpc/2/common endpoint fetching version information, verifying the connection info is correct before trying to authenticate
    the authentication itself is done through the authenticate function and returns a user identifier(uid) used in authenticated calls instead of login
    Transaction types including 5 categories: Postpaid, Upgrade, Data Feature, Prepaid, Accessory
    Product type for Postpaid including 8 types: AddALine, TFB Lead Activation Old, TFB Lead Activation, Personal Guarantor, B2B, PostPaid 1 & 2, TVision, Sole Proprietorship
    Product type for Upgrade including 1 type: upgrade (getting the total Revenue amount from wireless.dsr.upgrade.line model)
    Product type for Data Feature including 6 types: TMO 1+, Message, International Feature, Other, Data, Device Protection
    Product type for Prepaid including 1 type: Prepaid
    product type for Accessory including 1 type: Accessory (Monthly Access = 0.0)

    The product_type using DSR to get the Revenue: Upgrade, Device Protection, TVision, Prepaid, Accessory
    Revenue Formula: NO Credit Class Type in (Device Protection, prepaid, TVision) using empty String "", but product and added revenue, Data has only added Revenue
"""

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db_name, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))



class odoo_API(object):

    # Product type Names
    UPGRADE = "upgrade"
    DEVICE_PROTECTION = "device protection"
    PREPAID = "prepaid"
    TVISION = "tvision"
    ADDALINE = "addaline"
    B2B = "b2b"
    POSTPAID1AND2 = "postpaid 1 & 2"
    DATA = "data"
    TMO_1PLUS = "tmo 1+"
    MESSAGE = "message"
    INTERNATIONAL_FEATURE = "international feature"
    OTHER = "other"

   
    def product_type_name_to_id(self, product_type):

        """
            Returns the id number of product type
            :params: product_type
            :return: id_number
        """
        assert product_type is not None 

        category_filter = [[['prod_type', '<>', False]]]
        category_fields = {'fields': ['display_name', 'id']}
        search_by_product_category = self.models_execute('product.category', category_filter, category_fields)
        #print(search_by_product_category)

        for dict in search_by_product_category:

            product_display_name = dict['display_name']
            product_id = dict['id']
            if '/' not in product_display_name:

                #print(product_display_name + " " + str(product_id))
                product_type = product_type.casefold().strip()
                product_display_name = product_display_name.casefold().strip()

                if product_type == product_display_name:
                    #print(product_type + " = " + product_display_name + " " + str(product_id))
                    #product_type_combo = product_display_name + "," + str(product_id)
                    #print(product_type_combo)
                    return product_id

                            
    def models_execute(self, model, filters, fields):

        """
            Returns model results
            :params: model
            :params: filters
            :params: fields
        """
        assert model is not None
        assert filters is not None
        assert fields is not None

        results = models.execute_kw(db_name, uid, password, model, 'search_read', filters, fields)

        return results
    

    def filter_products(self, product_code, credit_class_type, product_type, sap_area=None):

        """
            Returns the revenue
            This function is searching by the product_code, getting the product type other than (Upgrade and Accessory, TVision, Data Feature)
            using Product type and credit_class as the filters to get relavant revenue
            :params: product_code = SOC_code
            :params: product_type: except Accessory
            :params: sap_area: Urban, Rural apply to PostPaid Transaction Type, and Data Features, only AddALine(1001) && PostPaid 1 & 2(999) apply to keyword SAP
            Positional argument follows keyword argument
            :params: credit_class_type: Prime, Deposit, NCC, "" 
            :return: revenue dictionary report
            revenue dictionary report: Revenue Calculation Formula, Phone Spiff Formula, Store Area, Added Revenue, Revenue Calculation for Pre to Post,
            Bonus Line Spiff, Bonus Handset Spiff, Additional Spiff     
        """
        assert product_code is not None 
        assert credit_class_type is not None
        assert product_type is not None

        product_type = product_type.lower().strip()
        product_type_id = self.product_type_name_to_id(product_type)
        today = str(dt.today().date())
       
        # product_code_barcode for PostPaid Transaction Type such as PostPaid 1 & 2, AddALine and B2B, Upgrade transaction type, Data Feature Transaction Type, except Device Protection
        product_code_barcode = product_code.upper().strip() 
        #print(product_code_barcode)
        # product_code_str for Prepaid and TVision ONLY!!!
        product_code_str = product_code.lower().strip()


        filters = [[['dsr_prod_type', '=', product_type_id], ['dsr_end_date', '>=', today], ['dsr_credit_class_type', '=', False],['name', 'ilike', sap_area]]]
        filters_upgrade_prepaid = [[['dsr_prod_type', '=', product_type_id], ['dsr_end_date', '>=', today], ['dsr_credit_class_type', '=', False]]]

        fields = {'fields':['dsr_revenue_calc', 'pre_to_post_rev_calc', 'name', 'dsr_rev_product', 'dsr_phone_spiff', 'additional_spiff', 'bonus_line_spiff', 'bonus_handset_spiff', 'dsr_added_rev', 'dsr_end_date', 'dsr_credit_class_type']}
        

        if product_type == self.UPGRADE: #product_type_id == 998: Upgrade
            
            revenue_no_credit_type = self.models_execute('revenue.generate.master', filters_upgrade_prepaid, fields)
            #print(revenue_no_credit_type)

            upgrade_revenue = self.get_total_revenue(product_type, product_code_barcode, revenue_no_credit_type)

            return upgrade_revenue

        elif product_type == self.DEVICE_PROTECTION: #product_type_id == 1002: Device Protection

            filters_device = [[['dsr_rev_product', '=', product_code_barcode], ['dsr_end_date', '>=', today], ['dsr_credit_class_type', '=', False]]]
            revenue_device = self.models_execute('revenue.generate.master', filters_device, fields)
            total_device_revenue = revenue_device[0]['dsr_added_rev']
            
            return total_device_revenue

        
        elif product_type == self.PREPAID: #product_type_id == 1006: Prepaid where sap_area and MRC don't affect revenue

            revenue_no_credit_type = self.models_execute('revenue.generate.master', filters_upgrade_prepaid, fields)
            #print(revenue_no_credit_type)

            prepaid_revenue = self.get_total_revenue(product_type, product_code_str, revenue_no_credit_type)

            return prepaid_revenue

            

        elif product_type == self.TVISION: #product_type_id == 1291: TVision where sap_area and MRC don't affect Revenue, but need to specify sap_area, product_code only contains In Store and Salesforce Lead

            revenue_no_credit_type = self.models_execute('revenue.generate.master', filters, fields)
            #print(revenue_no_credit_type)

            monthly_access_MRC = self.get_revenue_MRC(product_type, product_code_str)

            if 'store' in product_code_str:

                salesforce_revenue = self.get_total_revenue(product_type, product_code_str, revenue_no_credit_type)

                return salesforce_revenue

            if 'salesforce' in product_code_str:

                rev_cal_phone_spiff = revenue_no_credit_type[1]['dsr_revenue_calc'] + revenue_no_credit_type[1]['dsr_phone_spiff']
                added_rev = revenue_no_credit_type[1]['dsr_added_rev']
                total_rev = rev_cal_phone_spiff * monthly_access_MRC + added_rev

                return total_rev

 

        elif product_type in (self.ADDALINE, self.B2B, self.POSTPAID1AND2, self.DATA, self.TMO_1PLUS, self.MESSAGE, self.INTERNATIONAL_FEATURE, self.OTHER): #1001, 1007, 999, 1000, 1294, 1004, 1003, 1005

            product_type_id = self.product_type_name_to_id(product_type)  
            # product_type associate with sap_area, except 1001 and 999 filter by end_date >= today, this is the part can't use DSR due to no end date...
            sap_area = sap_area.strip() # Only capitalize the first word. 

            fields = {'fields':['dsr_revenue_calc', 'pre_to_post_rev_calc', 'name', 'dsr_phone_spiff', 'additional_spiff', 'bonus_line_spiff', 'bonus_handset_spiff', 'dsr_added_rev', 'dsr_end_date', 'dsr_credit_class_type']}
            # Check if product_type has a credit_class_type
            
            filters_credit_type_default = [[['dsr_prod_type', '=', product_type_id], ['dsr_end_date', '>=', today], ['dsr_credit_class_type', '=', False],['name', 'ilike', sap_area]]]

            if credit_class_type:

                credit_class_type = credit_class_type.capitalize().strip()
                filters_credit_type = [[['dsr_prod_type', '=', product_type_id], ['dsr_end_date', '>=', today], ['dsr_credit_class_type', '=', credit_class_type], ['name', 'ilike', sap_area]]]
                revenue_credit_class = self.models_execute('revenue.generate.master', filters_credit_type, fields)
                #print(revenue_credit_class)
                revenue = self.get_total_revenue(product_type, product_code_barcode, revenue_credit_class)
                return revenue

            
            revenue_filter_no_credit_type = self.models_execute('revenue.generate.master', filters_credit_type_default, fields)
            #print(revenue_filter_no_credit_type)

            default_revenue = self.get_total_revenue(product_type, product_code_barcode, revenue_filter_no_credit_type)
            return default_revenue



        else:

            raise Exception("Unknown product type!!")
        

         

    def get_revenue_MRC(self, product_type, product_code):

        """
            Return the monthly access MRC
            :params: product_type
            :params: product_code_barcode
            :return: float
        """
        assert product_type is not None
        assert product_code is not None

        product_type = product_type.lower().strip()
        product_type_id = self.product_type_name_to_id(product_type)

        product_fields = {'fields': ['default_code', 'dsr_prod_code_type', 'dsr_prod_type', 'dsr_second_categ', 'monthly_access'], 'limit':10}

        if product_type in (self.TVISION, self.PREPAID): #TVision and Prepaid

            product_filter = [[['default_code', 'ilike', product_code], ['dsr_prod_type', '=', product_type_id]]]
            search_by_specific = self.models_execute('product.product', product_filter, product_fields)
            #print(search_by_specific)
            monthly_access = search_by_specific[0]['monthly_access']

            if search_by_specific is not None:

                return monthly_access

        if product_type == self.UPGRADE: #Upgrade using the secondary category filter to filter the product type

            upgrade_filter = [[['default_code', '=', product_code], ['dsr_second_categ', '=', product_type_id]]] 
            search_by_second_categ = self.models_execute('product.product', upgrade_filter, product_fields)
            monthly_acc_MRC = search_by_second_categ[0]['monthly_access']

            if search_by_second_categ is not None:

                return monthly_acc_MRC

        
        product_filter = [[['default_code', '=', product_code], ['dsr_prod_type', '=', product_type_id]]]
        search_by_product = self.models_execute('product.product', product_filter, product_fields)
        #print(search_by_product)

        if search_by_product is not None:

             monthly_access_MRC = search_by_product[0]['monthly_access']

             return monthly_access_MRC


        
        

    def get_total_revenue(self, product_type, product_code, revenue_generator):

        """
            Return total revenue
            :params: product_type
            :params: product_code_barcode
            :params: revenue_generator
            :return: float
        """
        assert product_type is not None
        assert product_code is not None
        assert revenue_generator is not None

        total_rev = 0.00
        monthly_access_MRC = self.get_revenue_MRC(product_type, product_code)
        #print(monthly_access_MRC)

        rev_cal_phone_spiff = revenue_generator[0]['dsr_revenue_calc'] + revenue_generator[0]['dsr_phone_spiff']
        added_rev = revenue_generator[0]['dsr_added_rev'] #This is for Data Product_type Additional 15$ Spiff ef
        total_rev = rev_cal_phone_spiff * monthly_access_MRC + added_rev

        return total_rev


    def accessory_sku_commission(self, acc_sku):

        """
            This function takes an accessory SKU, filtered by SKU and end_date
            and return the commission
            :params: acc_sku
            :return: non-expired acc_commission 
        """
        
        sku = acc_sku.upper().strip()
        today = str(dt.today().date())
        accessory_filter = [[['acc_sku', '=', sku], ['end_date', '>=', today]]]
        accessory_fields = {'fields': ['acc_sku', 'acc_commission', 'end_date']}
        search_by_acc = self.models_execute('wireless.acc.sku.master', accessory_filter, accessory_fields)
        #print(search_by_acc)
        if search_by_acc is not None:
            commission = search_by_acc[0]['acc_commission']
            #print(commission) #float
            return commission

        
    def SOC_code_gross_rev(self, SOC_code, credit_class_type, product_type, sap_area):

        """
            Returns the sum of revenue from get_revenue function
            This function is searching by the SOC code, and comparing the total rev Gen.
            :params: SOC_code = product_code
            :return: Total Revenue
        """
        
        assert SOC_code is not None 
        assert credit_class_type is not None
        assert product_type is not None
        assert sap_area is not None

        line_revenue = self.filter_products(SOC_code, credit_class_type, product_type, sap_area)
        
        #print(line_revenue)
        return line_revenue


    def search_products(self, product_code, transaction_type):

        """
            Returns SOC code of the product and name of the product
            :params: SOC_code = product_code
            :params: transaction_type
            :return: SOC code and name of product
        """
        assert product_code is not None
        assert transaction_type is not None

        product_code_barcode = '%' + product_code + '%'.strip() 
        product_code_str = '%' + product_code + '%'.strip()
        transaction_type = transaction_type.capitalize() + '%'.strip()

        if transaction_type == 'Prepaid':
            product_filter = [[['default_code', '=ilike', product_code_str], ['dsr_categ_id', '=', transaction_type]]]
            
        else:
            product_filter = [[['default_code', '=ilike', product_code_barcode], ['dsr_categ_id', '=ilike', transaction_type]]]

        product_fields = {'fields': ['default_code', 'name'], 'limit':10}
        search_by_product = self.models_execute('product.product', product_filter, product_fields)
        #print(search_by_product)
        if search_by_product is not None:
            for dict in search_by_product:
                #print(dict)
                product_code = dict['default_code']
                name_of_product = dict['name']

                results = "SOC code: " + product_code + " " + "Name of Product: " + name_of_product
                #print(results)
                return results

        else:
            print("Sorry, there is no name associated with this product code..:( ")