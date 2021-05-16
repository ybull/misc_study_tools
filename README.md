# misc_study_tools
Miscellaneous utilities related to my study of Chinese

## Background
During Spring 2020, I started to learn Standard Chinese language.  I'm using
several resources, but the most regular one is Duolingo.com.  I occasionally 
also use the cool Android app "Pleco" which has large bilingual dictionaries, 
and a highly-customizable FlashCard system with quizzes.

Though I am learning a lot from Duolingo, there are several weaknesses in the 
design of their lessons and review quizzes.  Even when I intentionally turn it
to "hard mode" with keyboard input instead of button-clicking, it's not good 
enough. The biggest problem is it will not randomly generate a review quiz 
based on ALL the things I'm supposed to have learned, so the combinations of
characters and words is always narrow, often making it too easy.

So as I was experimenting with hand-typing a file to create a FlashCard set 
containing all the characters and words I am learning, I realized I can 
programmatically extract all of them from my current list of "words" at 
https://www.duolingo.com/words, then import that to Pleco. Pleco is so smart
it will automatically look up the Pinyin and definitions from its dictionary,
so all I need is the 汉字 from that web page.

This way I can periodically and quickly re-generate the FlashCards to include 
all my new terms.  It is trivial to generate diffs from previous versions of
the output, which allow quizzes in Pleco that focus on just the characters and 
words newest to me.

## Anki:
Later, in Spring 2021, I read "Fluent Forever" by Gabriel Wyner and learned 
about the Anki flashcard app which has several advantages for memorization 
compared to Pleco. Although Pleco is specific to Chinese and has great built-in 
dictionary, Anki is far more flexible with what you can put in your flashcards 
and how many ways you can customize the cards themselves -- leading to faster
and more thorough learning. 

## Planned Enhancements:
I'm no longer using Duolingo as my primary source of new words and sentences,
so I need to abstract this design a bit, with several data flows that merge
and result in an Anki-compatible output as well. 

Modify my program(s) to generate updates for the Anki-compatible deck 
compatible with the custom design I made. 

I want to automatically compare the word lists I'm studying with the HSK 
lists to track and display progress toward each HSK level. 

## Related Things:
https://hskhsk.com/word-lists by Alan Davies has text HSK word lists, and 
Pleco-format example sentence files & HSK lists.  

Differently-formatted web-viewable HSK words & characters are at 
http://hskhsk.pythonanywhere.com/hskwords 
http://hskhsk.pythonanywhere.com/hskchars

List characters by radical, optionally filtered by HSK level (Cool!): 
http://hskhsk.pythonanywhere.com/radicals?hsk=1

Anki software and website:
https://apps.ankiweb.net/