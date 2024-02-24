import unittest
from gender_guesser_first_names import gender
import json

f=open('data/test_gender.json','r')
j=json.load(f)
f.close()

D=gender.Detector(case_sensitive=False)

kk = [d.update({'g':D.get_gender(d.get('names'),country=d.get('country'))}) for d in j]

class Test_hello(unittest.TestCase):
    def test__working(self):
        self.assertEqual('Hello, World!',
                         'Hello, World!', True)

        T = len([ d.get('g') for d in j if d.get('gender') == d.get('g') ])
        U = len([ d.get('g') for d in j if d.get('g') =='unknown' ])
        E = len([ d.get('g') for d in j if d.get('gender') != d.get('g') 
                                 and d.get('g') !='unknown' ])
        
        self.assertEqual(T , 3629, True) # Total 
        self.assertEqual(U , 298, True) # Failed  U/T → 8%
        self.assertEqual(E , 40, True) # Error E/T → 1%


if __name__ == '__main__':
    unittest.main()
