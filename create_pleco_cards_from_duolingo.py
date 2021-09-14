"""
Script to create Pleco FlashCards from a Duolingo word list.

Copyright 2020, J.Weible

Currently I am using Duolingo.com and the Android app "Pleco" as some of the
tools to help with learning Chinese. Pleco has large bilingual dictionaries,
and a highly-customizable FlashCard system with quizzes.

Though I am learning a lot from Duolingo, there are several weaknesses in the
design of their lessons and review quizzes.  Even when I intentionally turn it
to "hard mode" with keyboard input instead of the choose-and-click, it's not
good enough.  The biggest problem is it will not randomly generate a review
quiz based on ALL the things I'm supposed to have learned, so the combinations
of characters and words is always narrow, often making it too easy.  Thus it
often thinks I have learned words that I can't remember or pronounce the
next day.

So as I was experimenting with hand-typing a file to create a corresponding
Pleco FlashCard set containing ALL of the characters and words I am learning,
I realized I can programmatically extract all of them from my current list of
"words" at https://www.duolingo.com/words, then import that to Pleco.

Pleco is so smart it will automatically look up the Pinyin and definitions
from its dictionary during import, so all I need is the 汉字 from that web page.

This way I can periodically and quickly re-generate the FlashCards to include
all my new terms.  I tag the output file by date, and could produce diffs if
I want to set up quizzes in Pleco that focus only on the characters/words new
to me.
"""


import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException


def fetch_duolingo_words_page() -> list:
    """The obfuscated crap design for the Duolingo webpage is so littered with
    JavaScript-generated dynamic content that even Firefox and Chrome won't
    save the page correctly if done manually using "Save Page As..." .

    So this uses Selenium to remote-control the browser to fetch the data from
    it.  At the moment, this means I must enter the Duolingo credentials
    at the console when prompted by this program.
    # TODO: Save cookies from Selenium to effectively cache the credentials?

    :return: the words from the list (only the Chinese 汉字）
    """
    try:
        browser = webdriver.Chrome(executable_path='./chromedriver')
    except SessionNotCreatedException as ex:
        print(ex)
        return

    browser.get('https://www.duolingo.com/learn')
    time.sleep(2)
    button = browser.find_element_by_xpath("//a[text()='I ALREADY HAVE AN ACCOUNT']")
    if button:
        # need to log into Duolingo...
        button.click()  # Activates button to go to the login page.
        email_field = browser.find_element_by_css_selector("input[data-test='email-input']")
        username = input('Enter Duolingo username: ')
        email_field.send_keys(username)

        pwd_field = browser.find_element_by_css_selector("input[data-test='password-input']")
        password = input('Enter Duolingo password: ')
        pwd_field.send_keys(password + Keys.ENTER)
        time.sleep(5)

    browser.get('https://www.duolingo.com/words')
    time.sleep(3)

    # Get all the Chinese characters/words in the table:
    xpath_q = "//span[contains(@class, '_3_ODH')]"
    elements = browser.find_elements_by_xpath(xpath_q)
    results = [e.text for e in elements]  # extract the text nodes in the spans
    browser.close()
    return results


def sort_and_deduplicate_words(words: list) -> list:
    """Given a list of Chinese words, sort it after de-duplicating. For some
    reason, Duolingo lists a few words multiple times.

    I realize this is just using standard sort collation, which may not
    be ideal.  It doesn't matter here, I just want them sorted in a
    predictable way so that diffs of output files from different dates will
    not be chaotic.

    :param words: the list of Chinese words from Duolingo
    :return: a modified list of the words

    >>> sort_and_deduplicate_words(['这','这儿','这里','认识', '这', '说'])
    ['认识', '说', '这', '这儿', '这里']
    >>> sort_and_deduplicate_words(['中国', '不客气', '不客气'])
    ['不客气', '中国']
    """
    return sorted(set(words))


def get_missing_single_characters(words: list) -> list:
    """Some characters I'm supposed to learn are only listed as part of a
    multi-character word or phrase, not included in Duolingo's word list
    individually.

    I wish to add those as separate items to my Pleco flash cards, to aid
    recognition and to help understand the derivations of compound words.

    For example, Duolingo includes 电话 = telephone, but so far has not taught me
        电 = electricity; electric; lightning
    and 话 = speech; talk; language; dialect.

    Results: In my first use of this, it added 183 new characters from a list
    of only 311 words!

    :param words: The current list of words.
    :return: list of ONLY the characters to add.

    >>> get_missing_single_characters(['这','这儿','这里','认识','说'])
    ['儿', '认', '识', '里']
    >>> get_missing_single_characters(['天', '明天', '明'])
    []
    >>> get_missing_single_characters(['不', '一', '一点儿','不客气'])
    ['儿', '客', '气', '点']
    """
    # split words list into single-character words vs multi-character:
    singles = [w for w in words if len(w) == 1]
    multis = [w for w in words if len(w) > 1]

    # Jam all multi-character words into a single string:
    multis = ''.join(multis)
    # split by character and get unique characters present:
    uniques = set(multis)

    new_chars = sorted([c for c in uniques if c not in singles])
    return new_chars


def create_pleco_import_file(outfilename=None):
    """This is the main function. It generates a text file based on the
    current date, unless one is given.

    :param outfilename: default will be 'pleco_duolingo_2020-##-##.txt"""
    entries = fetch_duolingo_words_page()
    print('Results as listed at Duolingo:')
    print(entries)

    count_orig = len(entries)
    entries = sort_and_deduplicate_words(entries)
    count_dedup = len(entries)
    new_entries = get_missing_single_characters(entries)
    count_expanded = len(new_entries)
    # Note, I'm intentionally NOT re-sorting the full list after expanding,
    # so that I can easily see in the text file which characters were added
    # this way.

    today = datetime.datetime.now().isoformat()[:10]
    if outfilename is None:
        outfilename = 'pleco_duolingo_{}.txt'.format(today)
    with open(outfilename, 'w', encoding='utf-8') as outfile:
        print('exporting to file: {}'.format(outfilename))

        # Embed a Pleco Card Category by date
        print('//Duo{}'.format(today), file=outfile)
        for item in entries:
            print(item, file=outfile)
            print(item)  # to console
        # Embed another Card Category for the supplementary characters:
        print('//Duo{}+'.format(today), file=outfile)
        for item in new_entries:
            print(item, file=outfile)
            print(item)  # to console

    print("Word counts: \n")
    print("Duolingo: {} \tDedup'd: {} \tExpanded: {}".format(
            count_orig, count_dedup, count_expanded))


if __name__ == '__main__':

    create_pleco_import_file()

    # TODO: This is fine for now, but would be better to automate this and
    #  have it change the Card Category to include 'NEW'.
    print('\nRemember if you want to create a usable diff from a previous date, ')
    print('the command to use looks like this:')
    print('comm -13 old_pleco_filename new_pleco_filename')