<!--
---
	title: Common Stream Encoders
	author: David Klann <dklann@broadcasttool.com>
	date: Mon Mar 13 12:36:33 PM CDT 2023
---
-->
<!-- Create formatted output with one of these commands:
	pandoc --toc --standalone --self-contained -f markdown -t html -o encoders.html encoders.md
	pandoc --toc --standalone --self-contained -f markdown -t latex -o encoders.pdf encoders.md
-->

# Common Stream Encoders #

Stream encoders range from simple, repurposed PC's running open source software
to sophisticated, purpose-built commercial "appliances" that include warranties
and technical support.

<!-- toc -->

## DIY Encoders ##

The do-it-yourself category starts with a simple computer. This can be a
cast-off Intel-based PC or something like a
[Raspberry Pi](https://raspberrypi.org/). The heart of the encoder is the
software that converts an audio signal to the format required by the stream
server (Icecast in the case of the Pacifica Streaming Service).

Here's a short list of software you can acquire to run on your stream encoder
computer. See a more complete list at the
[Icecast Apps](https://icecast.org/apps/#source-clients) page.

- **[B.U.T.T.](https://danielnoethen.de/butt/)**  
  Broadcast Using This Tool runs on the three major operating systems (Linux,
  macOS, and Windows). While each instance of B.U.T.T on a computer can feed
  only one stream server at a time, you can run several instances of the
  software to feed the same audio signal to multiple different stream servers.
  B.U.T.T. is [free software](https://www.gnu.org/philosophy/free-sw.en.html)
  that you can download, use and distribute.

- **[liquidsoap](https://liquidsoap.info/)**  
  Liquidsoap is a media streaming scripting language that, in its simplest use,
  can feed many different streaming servers. Liquidsoap is free software.

- **[Audio Hijack](https://rogueamoeba.com/audiohijack/)**  
  Rogue Amoeba's Audio Hijack is a common macOS tool for manipulating live audio
  on Apple Mac computers. Audio Hijack is proprietary software with a financial
  cost.

- **[Mixxx](https://mixxx.org/)**  
  Mixxx is both an audio file player and an Icecast source client. Mixxx
  includes a DJ-friendly user interface and even works with DJ consoles that
  enable on-air hosts to simulate running their show using old-fashioned
  turntables.

## Commercial Encoders ##

- **[Barix Instreamer](https://www.barix.com/product/instreamer-classic/)**  
  The Barix Instreamer is a low-cost appliance that can encode audio and send it
  to multiple streaming servers. The Instreamer comes in two flavors: the
  "Instreamer Classic" and the "Instreamer ICE". The primary difference between
  the two products is that the Instreamer ICE includes its own on-board Icecast
  server. With enough out-going bandwidth, you can use the Instreamer ICE to
  serve audio to up to one hundred listeners.

- **[Telos Z/IPStream](https://www.telosalliance.com/stream-encoding-processing/telos-alliance-zipstream-r2)**  
  The Z/IPStream is similar to the Instreamer Classic on steroids. The
  Z/IPstream can accept up to eight different audio sources and send to multiple
  stream servers. The Z/IPstream also includes on-board audio processing using
  the Telos Omnia 9 audio processor. This means that your stream audio
  processing can be different from your FM signal audio processing.

- **[Comrex BRIC-Link III](https://www.comrex.com/products/bric-link-iii/)**  
  Like the Barix Instreamer ICE, the BRIC-Link III can operate as both an
  Icecast stream server and a source client (encoder). In a different mode, the
  BRIC-Link III can also send audio to another Comrex device, acting as a
  studio-to-transmitter link.
