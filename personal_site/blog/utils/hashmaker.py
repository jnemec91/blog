import hashlib

def make_32_bit_hash(pk, string):
    # create a 32 bit hash value from the id and email
    hash_value = hashlib.md5(f"{pk}{string}".encode()).hexdigest()
    
    return hash_value

def make_hash_from_model(django_model_object):
    # get the primary key and string representation of the object
    pk = django_model_object.pk
    string = str(django_model_object)
    
    return make_32_bit_hash(pk, string)

if __name__ == '__main__':
    # when running this script, test the functions
    print('Running test runs for the functions in hashmaker.py')
    print(f'Making hash from 1 and test: {make_32_bit_hash(1, "test")}')
    print(f'Making hash from 2 and test: {make_32_bit_hash(2, "test")}')
    print(f'Making hash from 1 and test2: {make_32_bit_hash(1, "test2")}')
    
    class Test:
        def __init__(self, pk, string):
            self.pk = pk
            self.string = string

        def __str__(self):
            return self.string
        

    test_user = Test(1, 'User: test@test.test')
    test_category = Test(1, 'Category: test')
    test_blog_post = Test(1, 'BlogPost: test')

    print(f'Making hash from test object: {make_hash_from_model(test_user)}')
    print(f'Making hash from test object: {make_hash_from_model(test_category)}')
    print(f'Making hash from test object: {make_hash_from_model(test_blog_post)}')
