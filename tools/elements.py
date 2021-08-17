
 
# Using readlines()
file1 = open('elements.txt', 'r')
file2 = open("elements_ui.txt", "w")

Lines = file1.readlines()
 
# Strips the newline character
list_elements = []
list_keys = []

for line in Lines:
    list_elements.append(line.strip())

for element in list_elements:
    key = '_' + element.upper() + '_'
    list_keys.append(key)

file2.write('\tdef __init__(self, popup):\n')
file2.write('\t\t#initialize elements\n') 
for element in list_elements:
    x = '\t\tself.__{} = ""\n'.format(element)
    file2.write(x)

file2.write('\n\t\t#set initial elements\n')
idx = 0  
for element in list_elements:
    x = '\t\tself.__popup.Element("{}").update(value = self.__{})\n'.format(list_keys[idx],element)
    file2.write(x)
    idx += 1

file2.write('\n\t\t#avoid focus\n')
idx = 0  
for element in list_elements:
    x = '\t\tself.__popup["{}"].Widget.config(takefocus=0) \n'.format(list_keys[idx])
    file2.write(x)
    idx += 1


file2.write('\n\t#setters')
idx = 0  
for element in list_elements:
    x = '\n\tdef set_{}(self, {}):\n\t\tself.__{} = {}\n\t\tself.__popup.Element("{}").update(value = self.__{})\n'.\
            format(element,element,element,element,list_keys[idx],element)
    file2.write(x)
    idx += 1

file2.write('\n\t#getters')
idx = 0  
for element in list_elements:
    x = '\n\tdef get_{}(self):\n\t\tself.__{} = self.__popup.Element("{}").get()\n\t\treturn self.__{}\n'.\
            format(element,element,list_keys[idx],element)
    file2.write(x)
    idx += 1
   
file2.write('\n\t#property')
idx = 0  
for element in list_elements:
    x = '\n\t{} = property(get_{}, set_{})'.\
            format(element,element,element)
    file2.write(x)
    idx += 1

file2.write('\n')

    