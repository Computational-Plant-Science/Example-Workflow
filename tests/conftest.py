'''
    Fake the workflows registrar class

    https://stackoverflow.com/questions/43162722/mocking-a-module-import-in-pytest
'''
import sys

class Registrar:
    def register(self,name,description,app_name,icon_loc):
        return None

module = type(sys)('workflows')
module.registrar = Registrar()
sys.modules['workflows'] = module
