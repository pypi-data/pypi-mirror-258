i-Got
=======

`i-Got <https://github.com/iniself/igot>`__ is a tiny command-line utility to
download media contents (videos, audios, images) from the Web, in case
there is no other handy way to do it.

Here's how you use ``igot`` to download a video from `this web
page <http://www.fsf.org/blogs/rms/20140407-geneva-tedx-talk-free-software-free-society>`__:

.. code:: console

    $ igot http://www.fsf.org/blogs/rms/20140407-geneva-tedx-talk-free-software-free-society
    Site:       fsf.org
    Title:      TEDxGE2014_Stallman05_LQ
    Type:       WebM video (video/webm)
    Size:       27.12 MiB (28435804 Bytes)

    Downloading TEDxGE2014_Stallman05_LQ.webm ...
    100.0% ( 27.1/27.1 MB) ├████████████████████████████████████████┤[1/1]   12 MB/s

And here's why you might want to use it:

-  You enjoyed something on the Internet, and just want to download them
   for your own pleasure.
-  You watch your favorite videos online from your computer, but you are
   prohibited from saving them. You feel that you have no control over
   your own computer. (And it's not how an open Web is supposed to
   work.)
-  You want to get rid of any closed-source technology or proprietary
   JavaScript code, and disallow things like Flash running on your
   computer.
-  You are an adherent of hacker culture and free software.

What ``igot`` can do for you:

-  Download videos / audios from popular websites such as YouTube,
   Youku, Niconico, and a bunch more. (See the `full list of supported
   sites <#supported-sites>`__)
-  Stream an online video in your media player. No web browser, no more
   ads.
-  Download images (of interest) by scraping a web page.
-  Download arbitrary non-HTML contents, i.e., binary files.

Interested? `Install it <#installation>`__ now and `get started by
examples <#getting-started>`__.

Are you a Python programmer? Then check out `the
source <https://github.com/iniself/igot>`__ and fork it!