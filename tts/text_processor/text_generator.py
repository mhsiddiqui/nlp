import csv
import os
from dateutil import parser
from nlp.settings import BASE_DIR
from tts.text_processor.number_strings import GetStringType


TEXT_PROCESSOR_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCE_PATH = os.path.join(TEXT_PROCESSOR_PATH, 'resources')


class GenerateUrduText(object):

    def __init__(self, string, string_type=None):
        self.string = string
        self.string_type = string_type
        print RESOURCE_PATH
        self.number_mappings = self._get_mappings(RESOURCE_PATH + '/number.csv')
        self.arabic_numerals_mappings = self._get_mappings(RESOURCE_PATH + '/arabic.csv')
        self.english_mappings = self._get_mappings(RESOURCE_PATH + '/english.csv')
        self.month_mappings = self._get_mappings(RESOURCE_PATH + '/month.csv')

    def _get_mappings(self, file_name):
        mapping_dict = {}
        with open(file_name, 'rb') as f:
            mappings = csv.reader(f)
            for row in mappings:
                mapping_dict.update({row[0]: row[1]})
        return mapping_dict

    def generate_text(self):
        if not self.string_type:
            self.string_type = GetStringType(self.string).get_string_type()
        urdu_string = getattr(self, '_get_%s_urdu_string' % self.string_type)()
        return urdu_string

    def _get_date_urdu_string(self):
        date_object = parser.parse(self.string)
        year = self._get_number_urdu_string(date_object.year)
        day = self._get_number_urdu_string(date_object.day)
        month = self.month_mappings.get(str(date_object.month))
        return '%s %s %s' % (day, month, year)

    def _get_time_urdu_string(self):
        splitted = self.string.split(':')
        hours_in_urdu = self._get_number_urdu_string(splitted[0])
        minutes_str = 'minute' if int(splitted[1]) == 1 else 'minutes'
        minutes_in_urdu = self._get_number_urdu_string(splitted[1])
        seconds_in_urdu = ''
        if len(splitted) == 3:
            second_str = 'second' if int(splitted[1]) == 1 else 'seconds'
            seconds_in_urdu = '%s %s' % (self._get_number_urdu_string(splitted[2]),
                                         self.english_mappings.get(second_str))

        time_in_word = '%s %s %s %s %s' % (hours_in_urdu, self.english_mappings.get('baj_kar'),
                                           minutes_in_urdu, self.english_mappings.get(minutes_str),
                                           seconds_in_urdu)
        return time_in_word

    def _get_number_urdu_string(self, number=None):
        if not number:
            number = self.string
        if str(number) in self.number_mappings.keys():
            return self.number_mappings.get(str(number))
        else:
            if float(number).is_integer():
                return self._get_number_in_word(int(number))
            else:
                floating_value = '.' + str(number).split('.')[1]
                integer_value = int(float(number))
                integer_value_in_word = self._get_number_in_word(integer_value)
                floating_value_in_word = self._get_floating_point_in_urdu(floating_value)
                return '%s %s' % (integer_value_in_word, floating_value_in_word)

    def _get_number_in_word(self, number):
        all_factored_numbers = []
        facored_out, number = self._get_number_factors(number, 100000000000)
        all_factored_numbers += facored_out
        facored_out, number = self._get_number_factors(number, 1000000000)
        all_factored_numbers += facored_out
        facored_out, number = self._get_number_factors(number, 10000000)
        all_factored_numbers += facored_out
        facored_out, number = self._get_number_factors(number, 100000)
        all_factored_numbers += facored_out
        facored_out, number = self._get_number_factors(number, 1000)
        all_factored_numbers += facored_out
        facored_out, number = self._get_number_factors(number, 100)
        all_factored_numbers += facored_out
        all_factored_numbers.append(number)
        number_in_word = ''
        for num in all_factored_numbers:
            number_in_word += ' %s' % self.number_mappings.get(str(num))
        return number_in_word

    def _get_number_factors(self, number, factor):
        number_in_word = []
        if number > factor != 0:
            number_in_word.append(str(number / factor))
            number_in_word.append(factor)
            number %= factor
        return number_in_word, number

    def _get_floating_point_in_urdu(self, floating_point):
        floating_point_string = ''
        for num in str(floating_point):
            floating_point_string += ' %s' % self.number_mappings.get(num)
        return floating_point_string
