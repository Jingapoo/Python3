from odoo_API import *
from decimal import Decimal



if __name__ == '__main__':

    ODOO_API = odoo_API()
 
    # get each line of total revenue generated, and sum it up, add accessory commission if any.

    product_type_line = []
    product_type_line.append(ODOO_API.SOC_code_gross_rev('$50 simply prepaid unl talk, Text & 4GB lte', '', 'prepaid', True)) #50
    product_type_line.append(ODOO_API.SOC_code_gross_rev('simply_prepaid_can_mex_unl', '', 'prepaid', True)) #5
    product_type_line.append(ODOO_API.SOC_code_gross_rev('spp50ttuwulx', '', 'prepaid', True)) #50
    product_type_line.append(ODOO_API.SOC_code_gross_rev('tvision - salesforce lead', '', 'tvision', 'rural')) #15
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('tvision - in store', '', 'tvision', 'urban')) #75
    product_type_line.append(ODOO_API.SOC_code_gross_rev('one55tis', 'prime', 'upgrade', 'urban')) #55
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('tmesntl2', 'prime', 'upgrade', 'rural')) #50
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('frltul2lp', 'prime', 'upgrade', 'rural')) #55
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('tmesntl', 'prime', 'upgrade', 'urban')) #65
    product_type_line.append(ODOO_API.SOC_code_gross_rev('intelmcaf', '', 'device protection', True)) #10
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('p3605', '', 'device protection', True)) #30
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('nyp3603', '', 'device protection', True)) #30
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('p360mi3', '', 'device protection', True)) #30
    product_type_line.append(ODOO_API.SOC_code_gross_rev('tmesntl', 'prime', 'postpaid 1 & 2', 'urban')) #243.75
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('nctm1ufm2', 'prime', 'postpaid 1 & 2', 'urban')) #281.25
    product_type_line.append(ODOO_API.SOC_code_gross_rev('magenta', 'prime', 'postpaid 1 & 2', 'urban sap')) #300
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('mgfr7', 'prime', 'postpaid 1 & 2', 'urban sap')) #100
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('ufmscadd', 'prime', 'addaline', 'urban sap')) #120
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('mgpls552', 'prime', 'postpaid 1 & 2', 'rural')) #225.00
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('mgpls0', 'prime', 'tmo 1+', 'rural')) #45
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('esn10gbdt', 'prime', 'data', 'urban')) #37.5
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('znasit15', 'prime', 'international feature', 'urban')) #56.25
    #product_type_line.append(ODOO_API.SOC_code_gross_rev('mg13gbdta', 'prime', 'other', 'urban')) #37.50
    product_type_line.append(ODOO_API.SOC_code_gross_rev('esn10gbdt', '', 'data', 'urban')) #10
    print(product_type_line) # list
    
    #accessory_commission = []
    #accessory_commission.append(ODOO_API.accessory_sku_commission('tmom60602'))
    #accessory_commission.append(ODOO_API.accessory_sku_commission('610214663184'))
    #accessory_commission.append(ODOO_API.accessory_sku_commission('846127191692'))
    #print(accessory_commission)
    #gross_rev = sum(product_type_line) + sum(accessory_commission) 
    #gross_rev_round = round(Decimal(gross_rev),2)
    
    #print(gross_rev_round) 


    #ODOO_API.search_products('6fm', 'postpaid')
    #ODOO_API.search_products('tmc', 'prepaid')
    #ODOO_API.search_products('frltu', 'upgrade')




