# module_to_import_to.py

import module_to_import

print("module 1: ", __name__)

module_to_import.greet(module_to_import.name,
                       module_to_import.second_name,
                       module_to_import.profession)



# #oppure

# from module_to_import import greet, name, second_name, profession

# greet(name,second_name,profession)
