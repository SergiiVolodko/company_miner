import re
import lxml
from lxml.html.clean import Cleaner

class HtmlHelper:
    @staticmethod
    def remove_all_tags(html):
        TAG_RE = re.compile('<[^>]+>')
        text = TAG_RE.sub('', html)
        return text
    
    @staticmethod
    def clean_html(html):
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True 
        return cleaner.clean_html(html)
    
    @staticmethod
    def format_cleaned_text(text):
        text = text.replace('\n', ' ')
        text = text.replace('\t', '').replace('   ', '').replace('  ', ' ')
        # Uncamelcase
        text = re.sub("([a-z])([A-Z])","\g<1> \g<2>",text)
        return text