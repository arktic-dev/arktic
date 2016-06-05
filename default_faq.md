

### CONTENTS


1: Viewing This FAQ  
2: New Question?  
3: June 2016 Update   
4: What We Need You To Do  
5: Transcription Procedure  
6: Feedback And Conventions  
7: Things That Might Bother You  
8: Timesavers  
9: Transcription Rules (Summary)  
10: Normal Transcription Rules  
11: Miscellaneous Questions And Points  
12: Using The System  
13: Transcription Tags  


### 1: VIEWING THIS FAQ

Use command-plus (Mac) or ctrl-plus (Windows) to zoom in.  
Use command-minus (Mac) or ctrl-minus (Windows) to zoom out.  
Use command-f (Mac) or ctrl-f (Windows) to search for specific section titles and move to them. 



### 2: NEW QUESTION?



Email St John with your new question.



### 3: JUNE 2016 UPDATE

Changes:

1) Please try to guess fragmented words. For example, if someone says "advi advisor", transcribe this as "advisor [fragment] advisor". Similarly, if the first part of the word was not said by the caller, e.g. "change my [noise] ariff", transcribe this as "change my [noise] tariff [fragment]". If you can't easily guess the completed word, just transcribe the part that you can hear e.g. don't complete "re" in "calling about a re [noise] [bad-audio]", as it could be "return" or "replacement". Transcribe it instead as "calling about a re [fragment] [noise] [bad-audio]". 

2) We don't need to correct missing apostrophes and plural 's', if these don't actually change the meaning of the phrase. Examples: Caller says "pay bill", the system generates "pay bills". Caller says "i need a replacement", the system generates "i need a replacements". Caller says "don't worry about it", the system generates "dont worry about it". You can leave these system guesses as they are. These two particular system mistakes occur a lot but don't change the category of the transcription, so not correcting them saves a lot of time. 

3) If there are multiple consecutive touch-tone beeps in a row, you only need to put [dtmf] once. 

4) If you can, include a best guess for words cut off by the start or end of the audio recording. However, you need to enclose it in parentheses. For example "lo i'm calling to say i'm not happy" should be transcribed as "~(hello) i'm calling to say i'm not happy". If the cut-off occurs at the end, put the tilde on the other side e.g. "make a paym" should be transcribed as "make a (payment)~". A space between the parenthesis and the tilde is fine e.g. "make a (payment) ~".

5) The [loud-side-speech] tag is no longer very useful and has been removed. 

6) When there's only a noise and no actual speech, please put [noise] [no-speech]. However, for a cough or a breath noise by itself, you no longer have to add [no-speech]. Transcribe these as just [cough] or [breath-noise]. 



### 4: WHAT WE NEED YOU TO DO

We produce speech recognition systems. This system will interact with callers and attempt to understand them.

These systems must be tested using real information produced by actual people. Your job is to help us transcribe a large number of interactions between the caller and the system.

When transcription is complete, a speech scientist will build a speech system and test it using your work. The scientist will rarely listen to the audio files. He/she will instead read your transcription and compare it to the result that the system produces. This helps him/her quickly find the source of a problem with the speech system.

We have a number of conventions that describe the transcription more completely to help him/her do this.
For example, let's say that you listen to an audio file and transcribe it as "help me with something else [noise]".
The speech system, meanwhile, thinks that the noise is speech and transcribes the audio incorrectly as "help me with something else delivery".

When the scientist compares the two results, he/she sees:

TRANSCRIPTION: help me with something else [noise]	
SYSTEM RESULT: help me with something else delivery

This makes the problem obvious. The scientist can then change the speech system to make it more accurate.

Normally, we actually run the basic version of the speech system first. It is often faster for you to correct its guesses rather than type everything out yourself. 


### 5: TRANSCRIPTION PROCEDURE

1) Press tab to play/repeat audio item. This also activates the text box that you type into.

2) Press enter to copy down the predicted text (guessed by software and shown in the "original utterance" line) if it is close enough to be useful. This only works if the "modified utterance" line and the text box are empty. Sometimes this will be "blank", which won't be copied down (the system hasn't been able to guess anything).

3) Transcribe the item (or edit the predicted transcription). Type into the text box. Press enter to move this text into the "modified utterance line". Use right/left arrow keys to move between words in the modified utterance. If there is text in the text box, the right/left arrow keys switch to moving through the text. Similarly, backspace deletes a character in the text box or (if there is no text in the text box) deletes the highlighted word in the modified utterance.

4) Press enter to save the transcription (it is sent off to the webserver). The icon will turn from white to green.

5) Press enter to move to the next item (even if the next item is shown as a spinning orange disc, it will often work).

6) Use up/down arrow keys to move between items. This doesn't work if there's any text in the text box. 

Almost every function can be done via a keyboard shortcut rather than by using the mouse. 


### 6: FEEDBACK AND CONVENTIONS

Broadly speaking, you've all done good work. The tags haven't been applied perfectly, but this is not as important as just transcribing the actual words that are spoken. 

Interestingly enough, spelling errors are not a big problem for me. The same goes for using tildes (~) to denote fragments or using capitals/numerals/punctuation. I've written proofreading code that catches 99% of these and allows me to correct them in a reasonable amount of time.

**Important feedback** 

I much prefer that you try to avoid doing any of the following (as for these, I must listen to lots of the audio again myself, which takes a long time):

1) An easy mistake is to press enter immediately when you first hear the audio and you haven't done any transcription (the text box and the modified utterance are empty). This copies down the software-predicted transcription from the original utterance line to the modified utterance line (which is often a huge timesaver). However, if you do this, then transcribe the audio, then press enter again, you add your transcription to the guessed one, resulting in a "double transcription" that is very hard for me to see and correct.

2) Please don't use [noise] or [fragment] to transcribe a short segment of speech that can't be understood. Use [unintelligible] instead.

3) Please don't use [background-noise] if anyone is talking in the background. Use [side-speech] instead. I know I said indistinct background hubbub (e.g. coffeeshop noise) could be marked [background-noise], but let's just go with [side-speech] from now on.
 
4) Please don't use [unintelligible] for someone talking in the background. Use [side-speech] instead.

5) If the waveform shows a small bubble near the end, please listen to it. Sometimes it is quiet speech, not just noise. Remember, we care most about the raw transcription of words, not the tags.

6) It is much better to put [unintelligible] than guess unreliably. Use parentheses () around the word if you can guess easily. 


**Less crucial feedback**

1) Please use the shortcut keys for tags rather than typing them out yourself. Some of my code relies on the tags being spelt in a particular way e.g. "[breath-noise]" and does not work if you miss out the hyphen "[breath noise]" or accidentally misspell the tag "[breah-noise]".

2) Please don't use [skipped] if you can't understand the caller but the call is quite short e.g. 5-8 words. Use [unintelligible] instead. Add [unsure] if you think I might be able to understand the person.

3) If you use [skipped], please don't add anything else to it. [skipped] should be the whole of the transcription.

4) Don't use [side-speech] to label your transcription as not being directed at the system e.g. "[side-speech] I'll see you at the cinema". Within a transcription, [side-speech] is used to show the position of a word/phrase/sentence that was not relevant and not necessary to transcribe.

5) Don't use [no-speech] if anyone talks in the background, however quietly or briefly.

6) [mispronunciation] and [fragment] are only used immediately after the word that was mispronounced or only partly spoken.

7) You don't need to put [hesitation] unless the caller actually makes a noise e.g. "uh", "um", "er" etc. If they pause for e.g. 2-3 seconds, put [pause]. However, you only need to use [pause] for the caller, not for other people, so just put "[side-speech]" instead of "[side-speech] [pause] [side-speech]".

8) Please use tildes (~) only at the start and end of a transcription, never in the middle. They denote words cut off by the start/end of the audio file itself, not words cut off by the caller or by audio quality.

9) When there's only a noise and no actual speech, please put [noise] [no-speech]. 

10) [no-speech] is fine by itself if background noise is faint.

11) If there is any speech in the background, just put [side-speech], rather than [side-speech] [no-speech].

12) Telephone touchpad sounds are transcribed as [dtmf], not [noise]. If you've ever listened to someone texting where each touch of a key makes a audible beep, that's the sound.

13) Please do use [bad-audio] whenever it happens. You only need to use it once in a transcription. 



### 7: THINGS THAT MIGHT BOTHER YOU

1. **Transcription can be boring.** -- We recommend using tomato-timer.com and setting the timer to 5 or 10 minutes. Then take a 1 minute break. Experiment until you find a working pattern that is comfortable that you can maintain for long periods of time. Every so often you should stand up and walk around the room. It's much, much better to produce a consistent rate of output than to do mad dashes and exhaust yourself.

2. **Ergonomics** -- A good working position is essential. You should not be hunched over your screen. Ideally, your screen should be raised to eye height and you should type using an external keyboard. You should have room to stretch out your legs and lean against the back of your chair.

3. **Swearing/Anger** -- Sometimes the people who call into a speech system are angry (or become angry when using the system). They might swear and be generally rude and aggressive. Even though you know it is not directed at you personally, this can affect your mood or make you uncomfortable. Unfortunately, if they are talking directly to the system, this must still be transcribed. If it makes it easier, think of how a customer service representative must maintain an even temper when dealing with many clients in many different moods. Deal with the difficult customer, then take a short break.






### 8: TIMESAVERS

Here is a list of things that will save you time, decrease your frustration, and increase your hourly rate of pay:

1) If there are multiple consecutive noises in a row, put [noise] once. The same applies to [dtmf], [hesitation], [cough], [breath-noise], [side-speech], and [unintelligible]. For example, "[side-speech] [side-speech] pay a bill" should just be transcribed as "[side-speech] pay a bill". However, "[side-speech] pay a bill [side-speech]" should not be shortened to "[side-speech] pay a bill", as the [side-speech]s are separated by speech to the system. 

2) Use the auto-complete. It is shared among all transcribers. To add a phrase to the auto-complete, type it into the text box and press ctrl-enter. To delete an entry, type it in (or select it using the auto-complete), and press ctrl-minus. The deletion won't take effect until you reload the page. The auto-complete doesn't handle single words, only phrases. Also, I'm afraid that every time we move to a new batch (about once every 2000 items), the auto-complete is wiped. The auto-complete system needs to be improved, but this will have to be done later. 

3) If you type in numbers by themselves e.g. "123" and press enter, they are expanded to "one two three". Note that this only works if the text you type in consists only of digits. "123" will work, but "123hello" or "12 york street" will not. 

4) Don't transcribe any side speech that is unrelated to the system. Generally, you can guess whether the caller is talking to someone else or to the system. Mark it as [side-speech].

5) Letters don't need to be spelled out. If someone says "h n j" just transcribe it as "h n j" not as "aitch en jay".

6) Using [unsure] only once for a transcription is fine. You also don't need to worry about where it goes inside the transcription.

7) You only need to use [bad-audio] once per transcription. Ideally, put it at the point where the audio quality first degrades, but this is not crucial. 

8) Use [skipped] for anything over about 15 words said directly to the system. The rule of thumb is that if it's taking you 4 times longer than normal to transcribe it, skip it. If the transcription is too long to fit on our display, skip it. 

9) The data-gathering system may record a few seconds of silence at the end of an utterance. You don't have to listen to this all the way through. Just move to the next utterance when the waveform viewer shows that you've finished this one.

In general, please do remember that almost everything has a keyboard shortcut. Using these will save you a lot of time.



### 9: TRANSCRIPTION RULES (SUMMARY)


- It's more important to transcribe all the words said to the system than to get the tags exactly right. However, don't use [noise], [fragment], or [background-noise] to mark any speech. Use [side-speech]. 
- If you're not sure/happy about a transcription, add [unsure] to the end of it.
- Use lower case. Spellings should be in lower case separated by spaces.
- No punctuation or special symbols except hyphens and apostrophes.
- No abbreviations unless spoken, even common ones like "mr". Write titles in full.
- Use full words for everything including numbers, dates, amounts etc.
- Always type dictionary words. Use this set of non-dictionary words:
ok, yeah, yep, nope, uh huh, dunno, wanna, lemme, gimme, innit, ain't
- Type exactly what you hear even if it is ungrammatical or skips or repeats words.
- While viewing the transcription page you can use ctrl-space to access the list of shortcuts. 



### 10: NORMAL TRANSCRIPTION RULES

- Use lower case for all transcriptions.	Spelled letters should be in lower case separated by spaces, with no period after them.	
e.g. "my postcode is c b twelve five a q"	
NOT: "My postcode is CB12 5AQ."	
e.g. "my name is isa spelt i s a"	
NOT: "My name is Isa, spelt I-S-A."	

- No punctuation or special symbols except hyphens and apostrophes where these would normally be used.	 
e.g. i'm not sure, i don't know, mother-in-law, self-evident	
Q: Should I always use hyphens? For example, when a caller says "thirty-first of april" or "twenty-second of may"?	
A: No. Don't make an effort to use hyphens, generally. For the system programmer, it doesn't help and sometimes hinders.

- Use full words for everything including numbers, dates, amounts etc.	
--- Numbers	
e.g. "oh", "zero", "nothing" or "nought" - whichever was spoken	
NOT: "0"	
e.g. "a hundred" or "one hundred" - whichever was spoken	
NOT: "100"	
e.g.	"twenty four double three"	
NOT: "24 33"	
--- Percentages	
e.g. "six point oh four percent", "two percent"	
NOT: 6.04%, 2%	
--- Currency amounts – type all units as words, no symbols like £ or $.	
e.g. "twelve pounds ten p", "a hundred and five u s dollars"	
NOT: £12.10, US$105	
--- Dates	
e.g. "monday january the eighteenth two thousand and twelve"	
NOT: "Monday, January 18th 2012."

- No abbreviations unless spoken as such, even common ones such as "st" and "dr", and titles.	
e.g. mister, missus, miss, doctor, reverend, professor	
NOT: Mr, Mrs, Ms, Dr, Rev, Prof	
e.g. saint louis street	 
NOT: St Louis St	
e.g. doctor fosters drive	
NOT: Dr Fosters Dr	

- Type exactly what you hear even if it is ungrammatical or skips or repeats words.	
e.g. "ok right so so the code hang on it [hesitation] it’s two one zero five"	
NOT: "OK, right, sooo the code – hang on – it’s 2105."

- Mispronounced words - spell these correctly but use the [mispronunciation] after the word.	
Don’t invent spellings to try to represent the way mispronounced words sound.	
e.g. "i'd like reservations [mispronunciation] oops sorry reservations"	
NOT: "I'd like reversations, oops sorry, reservations"	
--- Long-drawn-out speech (because of speaker uncertainty) e.g. "yeeees, … well" is transcribed as "yes [mispronunciation] well".

- Caller says "dunno" instead of "don't know".	
--- Transcribe this as "dunno". Speech systems cope with these contractions: dunno, gonna, wanna. However, you should transcribe "don wanna" as "don't [mispronunciation] wanna". The system won't understand new contractions. It only copes with the contractions that someone has programmed into it.	
--- Also, you can use this set of non-dictionary words: ok, yeah, yep, nope, dunno, wanna, lemme, gimme, gonna	
--- do NOT use: yea, yeap, nopey, duno, wana, leme, gime, gunna

- Someone (who is not the caller) is speaking during some or all of the interaction.	
--- Mark this as [side speech], not [background noise]. For the system, speech is very different to a steady background noise.






### 11: MISCELLANEOUS QUESTIONS AND POINTS

- Q: Should I use "ok" or "okay"?	
A: "ok", because it's shorter. But don't bother correcting "okay" to "ok".

- Baby noises and dogs barking should be transcribed as [side-speech]. This is because a speech system sometimes finds these confusing and thinks that they are human speech. 

- Normally, when someone pronounces something incorrectly (or in a very thick regional accent), we mark this with [mispronunciation] e.g. "help me with summat else" is transcribed as "help me with something [mispronunciation] else".  
--- However, there are a couple of exceptions:  
--- The transcription "sort me bill out" is fine, as "me" is an actual word, not just a mispronunciation.  
--- The "g" is often left off the ending "ing". This is not a problem, as it's very close to the official pronunciation. So "nothin" can be transcribed as "nothing", rather than "nothing [mispronunciation]". Similarly, when someone shortens "to" to "t" e.g. "going t- the shop", writing "to" without the mispronunciation tag is fine. However, "i fink so" should be transcribed as "i think [mispronunciation] so", as the pronunciation has changed quite a lot. 

- "bout" is often said instead of "about". This should be transcribed as "about [mispronunciation]". Similarly, people often say "cos" or "cause" instead of "because". Again, we write this as "because [mispronunciation]". Logically, these should be fragments, but they are so accepted that we treat them as standard mispronunciations. 

- The caller says "Yeah that'll do".	
Q: Should I put "Yeah that will [mispronunciation] do"?	
A: No. The system can cope with standard grammatical contractions such as "that'll" for "that will".

- Q: Should I correct "nuffin" to "nothing [mispronunciation]"?	
A: yes.

- The caller says "I'll call ya".	
Q: How should I transcribe this?	
A: "I'll call you [mispronunciation]".

- The caller says "mm-hm" or "uh-huh".	
--- Mark these as [hesitation]. They do actually mean "yes", but the system is never going to able to distinguish these reliably from normal hesitations.



### 12: USING THE SYSTEM

Our system currently only works for the Google Chrome browser. 

Your transcriptions are "saved" (sent to the webserver) when you press enter to move to the next item. Their icon will turn from white to green. 

You need a good internet connection to use our system. We plan to expand it to handle spotty connections, but this is not possible right now. 

Sometimes, not all the audio files load. I find it is best to do the ones I can, then reload, then do the ones that were not loaded the first time.

Ways to improve your connection:
<<<<<<< HEAD

- Be closer to your wifi router  

- Change the position of your computer (wifi waves vary in intensity within even a single room)  

- Connect to your router with an ethernet cable  
=======
1) Be closer to your wifi router	
2) Change the position of your computer (wifi waves vary in intensity within even a single room)	
3) Connect to your router with an ethernet cable	
>>>>>>> d3972676168842f47f69ee1330f38823d3bcbcfd

You can use this website to check your web connection speed. 
http://www.speedtest.net/

I am afraid that occasionally, the web server will be overloaded, and some transcription messages to it may be lost in transit. When you press enter at the end of a job to move to the next one, your current job will be reloaded, with the lost transcriptions in white rather than green. This is irritating, but fixing it will also require serious development work. 

Internally, the transcriptions are stored in batches of about 2000 items. They are delivered in groups of 50 to you. When we reach the end of a batch, I sweep up the remaining open jobs and complete them. However, your transcription total is unaffected (it's the number of items you transcribed, rather than the number of jobs you completed), so you don't need to make an effort to avoid leaving jobs half-completed. 





### 13: TRANSCRIPTION TAGS

We call the annotations in square brackets "tags".

All of these tags can be added via a keyboard shortcut. While transcribing, press ctrl-space to show/hide the list of shortcuts. 

**Tag List**

~

()

[accent]

[background-noise] 

[bad-audio]

[breath-noise]

[cough]

[dtmf]

[fragment]

[hangup]

[hesitation]

[mispronunciation]

[noise]

[no-speech] 

[pause]

[prompt-echo]

[side-speech]

[skipped]

[unintelligible]

[unsure]


**Tag Descriptions**

- ~ = audio cut-off  
A word is cut off by the start or end of the audio file. 

- () = best guess  
If the word is not completely clear, but you can guess it, enclose it with parentheses. If you can't easily guess it, put [unintelligible]. 

- [accent]  
Caller has a strong accent or speech dialect.

- [background-noise]  
Any noticeable background noise that continues for a while. 

- [bad-audio]  
Any audio quality/distortion issues. Examples: Audio fading out (and in), distortion, breaking up of phone line, muffled speech due to bad phone line. Only mark this once per transcription. Try to place it where the problem begins. 

- [breath-noise]  
Loud breath, sigh, wind on microphone.

- [cough]  
Cough, clear throat, laugh, sneeze.

- [dtmf]  
The sound(s) of telephone touch tones being pressed on a telephone keypad. 

- [fragment]  
The caller did not say a complete word. Add this tag directly after the partially-spoken word.

- [hangup]  
Any audible hangup noise.

- [hesitation]  
"um", "er", "uh", "uh-huh", "mm-hm", etc. 

- [mispronunciation]  
The caller mispronounced a word. Add this tag directly after the mispronounced word.

- [noise]  
Door slam, car horn, something dropped on the floor

- [no-speech]  
The audio item does contain anything recognisable as speech. Nonetheless, [dtmf], [noise], [hangup] and other events should be marked if they occur.

- [pause]  
Long pause (e.g. at least 2 seconds) during speech by the caller to the system.

- [prompt-echo]  
The audio contains some or all of a speech system prompt. A prompt is anything the system says to a caller, e.g. "Please say your account number". The O2 prompt wording before the recording is (roughly): "To help us make some improvements, in just a few words, please tell us why you are calling today, for example, to top up or to check on an upgrade" There are several different versions. Any other recordings, like TV/train announcements etc should be [side-speech]

- [side-speech]  
Any speech by the caller not directed at the system. Any intelligible speech from a bystander. Examples: People talking, background speech, radio, TV, automatic train announcements.

- [skipped]  
Skip the transcription entirely if the caller "rambles" or if the transcription is too long to fit properly on the transcription page. 

- [unintelligible]  
Use this to mark any speech that you can't understand.

- [unsure]  
If you're not sure/happy about a transcription, add the tag [unsure] to it. This only needs to be added once. 










