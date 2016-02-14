""" Globals """


""" Globals """

"""
Assuming conf.hcl lives in the apps' root directory
"""

"""
Generate fields list
"""
def fields():
    f = read_hcl(os.getcwd() + '/' + 'conf.hcl')
    fields = [ str(field) for field in f['conf']['fields'] ]
    return fields


"""
Generate features list
"""
def features():
    f = read_hcl(os.getcwd() + '/' + 'conf.hcl')
    features = [ str(feature) for feature in f['conf']['features'] ]
    return features


"""
Generate data source directory
"""
def input_directory():
    f = read_hcl(os.getcwd() + '/' + 'conf.hcl')
    input_directory = str(f['conf']['data'])
    return input_directory


"""
Generate output filename
"""
def output_filename():
    f = read_hcl(os.getcwd() + '/' + 'conf.hcl')
    output_filename = str(f['conf']['output'])
    return output_filename


"""
Generate sni_csv
"""
def sni_csv():
    f = read_hcl(os.getcwd() + '/' + 'conf.hcl')
    sni_csv = str(f['conf']['sni_csv'])
    return sni_csv
