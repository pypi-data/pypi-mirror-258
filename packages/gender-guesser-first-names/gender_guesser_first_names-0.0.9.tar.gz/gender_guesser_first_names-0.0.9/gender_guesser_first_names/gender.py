import gender_guesser.detector as GENDER

class Detector:
    '''
    * Works for all countries
    * convert mostly_(fe)male to (fe)male
    * Works for composed names by finding the first female or male and ignoring the other ones
    '''
    LA_countries=['Brazil', 'Mexico', 'Argentina','Chile', 'Colombia','Bolivia','Cuba', #5
              'Costa Rica', 'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', #10
               'Nicaragua', 'Panama', 'Paraguay', 'Peru', #15
              'Dominican Republic','Uruguay','Venezuela']
    
    def __init__(self,case_sensitive=False):
        self.case_sensitive = case_sensitive
    #case_sensitive = False
        self.D=GENDER.Detector(case_sensitive=self.case_sensitive)

    def get_country(self,country):
        if country.lower() in [s.lower() for s  in self.LA_countries if s.lower()!='brazil']:
            return 'spain'
        elif country.lower() == 'brazil':
            return 'portugal'
        elif country.lower() in self.D.__class__.COUNTRIES:
            return country.lower()
        else:
            return None

    def get_gender_country(self,name,country=None):
        if country:
            country = self.get_country(country)
            fm=self.D.get_gender(name,country)
            fm=fm.replace('mostly_','')
        else:
            fm='unknown'
        if fm not in ['male','female']:
            fm = self.D.get_gender(name)
            fm=fm.replace('mostly_','')
        return fm  
    
    def get_gender(self,names,country=None):
        for name in names.split():
            fm = self.get_gender_country(name,country=country)
            if fm in ['male','female']:
                break
        return fm

            
d=Detector()
assert d.get_gender('Andrea',country='italy') == 'male'
assert d.get_gender('Andrea',country='spain') == 'female'
assert d.get_gender('Andrea',country='colombia') == 'female'
assert d.get_gender('Diego',country='colombia') == 'male'
assert d.get_gender('Alejandro',country='colombia') == 'male'
assert d.get_gender('Diego Alejandro',country='colombia') == 'male'
# https://www.reddit.com/r/namenerds/comments/178mdjr/names_that_are_different_genders_in_different/
assert d.get_gender('Valery',country='russia') == 'male'
assert d.get_gender('Valery',country='usa') == 'female'
assert d.get_gender('Marian',country='poland') == 'male'
assert d.get_gender('Marian',country='usa') == 'female'
assert d.get_gender('Kim',country='denmark') == 'male'
assert d.get_gender('Kim',country='spanish') == 'female'
assert d.get_gender('Jan',country='germany') == 'male'
assert d.get_gender('Jan',country='usa') == 'female'
