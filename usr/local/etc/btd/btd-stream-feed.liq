#!/usr/bin/liquidsoap

## This script is intended to be launched by Rivendell.
## See rdadmin->Manage Hosts->[HOSTNAME]->Jack Settings->Jack Clients

# Because ... Rivendell ... because ... JACK
set( "init.allow_root", true )

## Log dir
set( "log.file.path", "/var/log/liquidsoap/btd-stream-feed.log" )

## PID file location for this instance of liquidsoap
set( "init.daemon.pidfile.path", "/usr/local/etc/btd/liquidsoap.pid" )

## Use the telnet server for run-time access
set( "server.telnet", true )

## Get input from JACK
## NB: pay attention to JACK connections!
feed = input.jack(
  id = "encode-in",
  buffer_size = 1,
  clock_safe = true,
  server = "default"
)

##############################################################################
## Settings used in the output stream, passed on the command line.
strID   = "str01"
strProt = argv( 1 )
strHost = argv( 2 )
strPort = int_of_string( argv( 3 ))
strMnt  = argv( 4 )
strUser = argv( 5 )
strPass = argv( 6 )
strDesc = "Streaming Audio"
strURL  = "http://example.com/"

## create a new clock that will handle all the stream outputs
clock.assign_new (
  id = "stream",
  sync = true,
  [
    # output the to the transmitter icecast stream server in MP3 format
    output.icecast (
      start = true,
      id = strID,
      protocol = strProt,
      host = strHost,
      port = strPort,
      user = strUser,
      mount = strMnt,
      password = strPass,
      url = strURL,
      description = strDesc,

      # (unlabeled) format:
      # internal_quality: Lame algorithms internal quality. A value
      # between 0 and 9, 0 being highest quality and 9 the worst
      # (default: 2).
      %mp3( samplerate = 44100, stereo = true, bitrate = 128, internal_quality = 1 ),

      # (unlabeled) source:
      # buffer is necessary when using the internal liquidsoap clock
      mksafe( buffer( buffer = 0.25, max = 0.5, feed ))
    )
###
###    # Example of a local OGG Vorbis archive of the audio signal:
###
###    # Create an archive file of the stream
###    #  "/audio/archive/%Y/%m/%d/%H-%M-%S.ogg"
###    #,
###    output.file (
###      id = "archive",
###      append = true,
###
###      # close, then re-open the file at the top of each hour
###      reopen_when = { 0m0s },
###
###      # (unlabeled) format
###      %vorbis( samplerate = 48000, channels = 2, quality = 0.25 ),
###
###      # (unlabeled) filename
###      "/audio/archive/%Y/%m/%d/%H-%M-%S.ogg",
###
###      # (unlabeled) source
###      amplify( 10.0, mksafe( buffer( feed )))
###    )
  ]
)
