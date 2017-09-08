import codecs
from processor import get_processed_data

with codecs.open('text.txt', 'r+', 'utf-8') as f:
    text = f.read()


processed_data = get_processed_data(text)

print processed_data

