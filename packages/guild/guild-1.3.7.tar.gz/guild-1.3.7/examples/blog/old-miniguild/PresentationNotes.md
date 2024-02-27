So, actors, kamaelia, mini-guild

So the context is Kamaelia, Guild, Actors and REB.
#---------------------------------------------------------------------------

Before starting talk, demonstrate this:

* ./fflex.py

Backdrop:

    # Create components that have no notion of where they are linked to
    tt = TimedText("resources/ulysses.txt")
    display = Display(800, 600)

    ukmap = MapTile("resources/uk_map.png", (800,600), (0,0))
    vid1 = FrameSource("resources/squirrel-cleaned-mVafW9jiEYA.mp4", 30, (576,324))
    vid2 = FrameSource("resources/shia-labeouf-ZXsQAXx_ao0.mp4", 24, (576,324))
    textdisplay = TextDisplay((700,80), 24)
    mp3 = MP3Player("resources/hippo.mp3")

    # Specific link up

    control = Controller([tt, ukmap, vid1, vid2, td, mp3, display])

    # Generic link up
    # Note also we place the images here, and also give them priorities at this point instead.

    Pipeline( ukmap,  TForm(lambda image: (1, image, (0, 0)) ),  display)
    Pipeline( vid1,   TForm(lambda image: (2, image, (-50, 100)) ),  display)
    Pipeline( vid3,   TForm(lambda image: (3, image, (-50, 130)) ),  display)
    Pipeline( tt, textdisplay, TForm(lambda image: (4, image, (50, 450)) ), display)
    
    Graphline({
            (control, "toggle") : (display, "toggle_layer"),
            (control, "toggle_audio") : (mp3, "toggle_audio")
        })



* What are Actors?
    - Short overview
* What was Kamaelia?
    - Ignite talk
* What is Guild?
    - Actors + late binding + STM + 

Why Mini-* ?

* MiniAxon
* MiniActor
* MiniGuild

Where we're headed is this:

* ./miniguild.py
* ./producer-consumer.py |head -100
* ./door.py
* ./benchmark.py 1000 1000
* ./network.py

* ./fflex.py
   - This is a mockup of an actor based version of something forecaster flex like
   - Display is loosely similar to render context
       - accepts surfaces to draw, and draws them at locations, with a z-index
       - This also includes a priority (z-index)
       - The last image per priority is cached by z-index
       - Display is updated 60 FPS
   - Video 1 - updates with a framerate of 30 FPS
   - Video 2 - updates with a framerate of 24 FPS
   - The text rendered ticker - sends data at ~ 50 letters/second
   - Text displayer - updates in sync with the display - so 60FPS
   - The Map updates once so has an effective FPS of 0
   - The MP3Player plays alongside this
   - Controller sends messages to the display:
      - to toggle visibility
      - to pause/unpause the MP3 playback

   - Note: Since actor-like based, somewhat more coupled than a kamaelia system
   - Note: Most of these actors break the official rules of actors because
     they are active, not reactive.  This seems to be a common problem/issue
     in multimedia applications.

Note:

1. Has an illustration at the bottom of the file what the more
   Kamaelia-like mockup
   This hasn't been implemented (due to time)

2. A number of networking components have also been 

