Twitter Wars!
=====================

Requirements
-------------

You should have ``requests`` installed.

Get twitts
----------
I've use the twitter API and in particular the ``geocode`` argument in order
to get twitts from a specific region. London and Exeter are defined as a
point and an approximate radious.

Clean twitts
------------
To clean the twitts text I've use a couple of regexp to remove mentions, urls,
hashtags and phone numbers.

Analize twitts
--------------
Calling an external API to determine if a word is correct or not could be
really expensive, so I've use the internal dictionary all unix distributions
use to do spellcheking. This ara huge files containing common English words
and names. I'm using Mac and these files are located in ``/usr/share/dict/``,
if you are using any other linux distribution you should specify where these
files are.

For every of these files I create a ``Dictionary`` object I'll use later to
check if every word inside the tweet is "valid" or not.

For every word in the text I call ``Dictionary.score`` to check if it's valid
or not using `0` as not found score. As soon as a dictionary scores a word I
don't score it again.

Every Dictionary has different multipliers so, ``connectives`` only score ``0.5``
and more complex words (like the ones inside ``web2``) score ``2``.

The score is based on the multiplication of the len of the word and the
dictionary multiplier.

The city that gets a higher score, Wins!

Usage
-----

$python twitter.py [--count NUMBER]

You can use ``--count`` to choose how many twitts you want to process.

Example
-------

Example run::

    $ python twitter.py
    London
    ##################################################
    (0.00) @rachelos_x ok birdddy xxxxxx
    (6.00) RT @AlirezaMilani: Media hesitant to call perpetrators terrorists. After all, they have not been confirmed as Muslims yet.
    (4.00) #5WordsiHateToHear Go and get a life.
    (6.00) RT @BigBoyler: People of Ireland are thinking of you Boston.
    (8.00) RT @TekkaBooSon: This will just give all those morbidly obese people in America another reason not to go jogging...
    (3.00) RT @CNNImpact: Hotline for those searching for loved ones at the #BostonMarathon: (617) 635-4500 announced by Police Commisioner Davis
    (3.00) RT @OwenJones84: @FootyExpert Literally at a loss
    (6.00) RT @Davidpenn14: I wish you could programme your twitter feed to block any MIC, Essex or Bieber talk
    (6.00) RT @FJUiCEryan: #PrayForBoston Hate the evil in this world.. #NoUnity
    (7.00) @Hannah_Rouch fun for all the family

    Exeter
    ##################################################
    (6.00) @SophieGT @jenniferlewis96 I love all of the girls apart from the new three
    (7.00) Feels like I've watched made in Chelsea tonight what with being on twitter
    (0.00) RT @TheMightyBrocks: @HarvesterUK Harvester. You're shit. @tingle240 agrees.
    (7.00) RT @justj4mie: This photo is chilling #prayforboston http://t.co/3wUEPhNduF
    (7.00) over thinking is going to kill me
    (4.00) My only fear in life, Dentists..
    (6.00) fs, some people are thick as shit, why would anyone call off the London marathon!?
    (6.00) @Sheridansmith1 What's green and goes up and down? A gooseberry in a lift.
    (7.00) RT @justj4mie: This photo is chilling #prayforboston http://t.co/3wUEPhNduF
    (6.00) what a bad world we all live in, bombings at a charity run.. what is wrong with people, awful news #prayforboston

    London score: 49
    Exeter score: 56
