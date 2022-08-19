# Find phone number from a List
phonebook = [
    ('John Doe', '555-555-555'),
    ('John AAA', '111-555-555'),
    ('Albert Doe', '555-555-888'),    
    ('Albert AAA', '111-555-888'), 
    ('John BBB', '222-555-888')           
]

def find_phone(phonebook, name):
    for n, p in phonebook:
        if n ==name:
            return p
    return None

print("John Doe's phone number is: " + str(find_phone(phonebook, 'John Doe')) )

print("Richard's phone number is: " + str(find_phone(phonebook, 'Richard')))

# Find unique First Names with lists and sets
print("Testing for\n")
print("Find unique First Names with lists and sets")
# The name would be in the format of : 'First_name Sure_name'

def list_unique_names(phonebook):
    print("Get the number of unique first name by list:")
    unique_names = []
    for name, phone in phonebook:
        first_name, sure_name = name.split(" ")
        already_in = False

        for unique_name in unique_names:
            if unique_name == first_name:
                already_in = True
                break
        if not already_in:
            unique_names.append(first_name)
    #print(unique_names)
    return len(unique_names)


def set_unique_names(phonebook):
    print("Get the number of unique first name by set:")
    unique_names = set()
    for name, phone in phonebook:
        first_name, sure_name = name.split(" ")

        unique_names.add(first_name)
    # print("All the first names are: \n" + unique_names)

    return len(unique_names)

a = set_unique_names(phonebook)

print("The totals unique first names is: " + str(a) )

b = list_unique_names(phonebook)
print("The totals unique first names is: " + str(b) )
