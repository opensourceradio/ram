<!--
---
	title: Pacifica Streaming Service
	author: David Klann <dklann@broadcasttool.com>
	date: Mon Mar 13 12:12:22 PM CDT 2023
---
-->
<!-- Create formatted output with one of these commands:
	pandoc --toc --standalone --self-contained -f markdown -t html -o index.html index.md
	pandoc --toc --standalone --self-contained -f markdown -t latex -o index.pdf index.md
-->
# Pacifica Streaming Service #

The Pacifica Internet Technology Package includes web streaming of your
station's terrestrial radio signal. Note that
[SoundExchange](https://soundexchange.com/) treats simulcast web streaming of a
station's radio signal differently from web-only streams. The primary intention
of the Pacifica streaming service is to enable simulcasting of stations'
existing AM or FM signals.

<!--toc-->

## Service Overview ##

Pacific Affiliates Network uses the industry-standard
[Icecast](https://icecast.org/) web streaming service.

As stated in the
[Icecast Introduction](https://icecast.org/docs/icecast-2.4.1/introduction.html):

    There are two major parts to most streaming media servers: the component
    providing the content (what we call source clients) and the component which
    is responsible for serving that content to listeners (this is the function
    of icecast).

As of the time of this writing, Pacifica Affiliates Network runs Icecast version
2.4.4.

## Station Requirements ##

In order to stream your station's signal on the Internet, you need to provide a
device that can convert your audio signal to the digital format required by
Icecast. This device is commonly referred to as a _stream encoder_ (or just
_encoder_). In Icecast parlance, this device is also called a "_source client_".

A stream encoder is essentially a computer that has one or more audio inputs as
well as Internet connectivity. Encoders come in many shapes, sizes, and levels
of sophistication. It's pretty straight-forward to build your own, DIY-style.
You can also purchase purpose-built encoders from the usual broadcast technology
suppliers. See some common encoders in [this list](encoders.md).
