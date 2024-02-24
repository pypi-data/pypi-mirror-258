# gender-guesser with first names and full countries

![Python package](https://github.com/colav-playground/gender_guesser_first_names/workflows/Python%20package/badge.svg)
![Upload Python Package](https://github.com/colav-playground/gender_guesser_first_names/workflows/Upload%20Python%20Package/badge.svg)

Changes [`gender_guesser`](https://pypi.org/project/gender-guesser/) by:
* Works for all countries
* Convert mostly_(fe)male to (fe)male
* Works for composed names by finding the first female or male and ignoring the other ones

## Install
```bash
$ pip install gender-guesser-first-names
```
## USAGE
```python
>>> from gender_guesser_first_names import gender
>>> d=gender.Detector(case_sensitive=False)
>>> d.get_gender('Andrea Maria',country='italy')
'male'
```
