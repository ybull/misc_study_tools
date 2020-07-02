# misc_study_tools
Miscellaneous utilities related to my study of Chinese

During Spring 2020, I started to learn Standard Chinese language.  I'm using
several resources, but the most regular one is Duolingo.com.  I also use the 
cool Android app "Pleco" which has large bilingual dictionaries, and a 
highly-customizable FlashCard system with quizzes.

Though I am learning a lot from Duolingo, there are several weaknesses in the 
design of their lessons and review quizzes.  Even when I intentionally turn it
to "hard mode" with keyboard input instead of button-clicking, it's not good 
enough.  The biggest problem is it will not randomly generate a review quiz 
based on ALL the things I'm supposed to have learned, so the combinations of
characters and words is always narrow, often making it too easy.

So as I was experimenting with hand-typing a file to create a FlashCard set 
containing ALL of the characters and words I am learning, I realized I can 
programmatically extract all of them from my current list of "words" at 
https://www.duolingo.com/words, then import that to Pleco.  Pleco is so smart
it will automatically look up the Pinyin and definitions from its dictionary,
so all I need is the 汉字 from that web page.

This way I can periodically and quickly re-generate the FlashCards to include 
all my new terms.  I may also enhance this to tag them by when they were 
added by doing diffs with previous versions. That would allow quizzes in Pleco
that focus on characters/words new to me in stages.
