#!/usr/bin/python

import pygame
import time

from miniguild import Scheduler, Actor
#---------------------------------------------------------------------------
import subprocess

FPS = 60


class MapTile(Actor):
    class Behaviour:
        def __init__(self, filename, dimensions, location, display, priority ):
            self.filename = filename
            self.dimensions = dimensions
            self.location = location
            self.display = display
            self.priority = priority
        def main(self):
            yield 1
            image = pygame.image.load(self.filename)
            surface = pygame.transform.scale(image, self.dimensions)
            self.display.render(self.priority, surface, self.location)


class FrameSource(Actor):
    blocking = True
    class Behaviour:
        ffmpeg = "/usr/bin/ffmpeg"
        def __init__(self, filename, fps, dimensions, location, display, priority ):
            self.width, self.height = dimensions
            self.filename = filename
            self.fps = fps
            self.command = [ self.ffmpeg,
                            '-loglevel', 'quiet',
                            '-i', filename,
                            '-f', 'image2pipe',
                            '-s', '%dx%d' % (self.width, self.height),
                            '-pix_fmt', 'rgb24',
                            '-vcodec', 'rawvideo', '-' ]
            self.frame_size = self.width * self.height * 3
            self.location = location
            self.display = display
            self.priority = priority

        def main(self):
            pipe = subprocess.Popen( self.command, stdout=subprocess.PIPE, bufsize=self.frame_size )
            time.sleep(1)
            image  = pygame.Surface( ( self.width, self.height ), pygame.HWSURFACE )
            last_at = 0
            frame_delay = 1000/self.fps
            while True:
                yield 1
                time.sleep(1/(self.fps*2))
                time_now = pygame.time.get_ticks()
                if ( time_now > last_at + frame_delay ):   # Need new frame
                    last_at = time_now
                    try:
                        raw_image = pipe.stdout.read( self.frame_size )
                        self.image = pygame.image.frombuffer(raw_image, (self.width, self.height), 'RGB')
                        self.display.render(self.priority, self.image, self.location)
                        key = self.image.get_at( (8,8) )
                        self.image.set_colorkey(key)
                    except:
                        self.image = pygame.Surface( ( self.width, self.height ), pygame.HWSURFACE )
                        self.image.fill( ( 0,0,0 ) )
                        break


class TimedText(Actor):
    # Send a file at a rate of approximately 50 characters per second
    blocking = True
    class Behaviour:
        def __init__(self, filename):
            self.filename= filename
        def main(self):
            f = open(self.filename)
            d = f.read()
            f.close()
            lines = d.split("\n")
            for line in lines:
                for letter in line:
                    self.output(letter)
                    time.sleep(0.04)
                    yield 1
                self.output("\n")

        def output(self, word):
            pass

class TextDisplay(Actor):
    class Behaviour:
        def __init__(self, dimensions, fontsize, location, display, priority = 0):
            self.width = dimensions[0]
            self.height = dimensions[1]
            self.display = display
            self.location = location
            self.priority = priority
            self.fg = pygame.Color("white")
            self.bg = pygame.Color("grey50")
            self.line = ""


            self.my_font = pygame.font.Font("/mnt/classified/michael/.fonts/MichaelNewHW.ttf", fontsize)
            #self.my_font = pygame.font.Font(None, fontsize)
            self.line_height = self.my_font.get_linesize()
            self.max_lines = int(self.height/self.line_height) - 1
            self.line_width = self.my_font.size("")[0]
            self.lines = []

        def input(self, char):
            if char == "\n":
                self.lines.append(self.line)
                self.line = ""
                return
                
            line = self.line + char
            if self.my_font.size(line)[0] > self.width:
                self.lines.append(self.line)
                line = char

            self.line = line
            self.lines = self.lines[-self.max_lines:]

        def render(self):
            background = pygame.Surface((self.width, self.height))
            background.fill( pygame.Color("grey25") )
            i = 2
            for line in self.lines[::-1]:
                current_line = self.my_font.render(line.rstrip(), 1, self.fg )
                background.blit(current_line, (0, self.height-self.line_height*i))
                i += 1
                
            current_line = self.my_font.render(self.line.rstrip(), 1, self.fg)
            background.blit(current_line, (0, self.height-self.line_height))
            return background

        def main(self):
            while True:
                yield 1
                image = self.render()
                self.display.render(self.priority, image, self.location)

class Controller(Actor):
    blocking = True
    class Behaviour:
        def __init__(self, toshutdown):
            self.toshutdown = toshutdown
        def main(self):
            while True:
                time.sleep(0.1)
                yield 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        for actor in self.toshutdown:
                            actor.stop()
                        return
                    if event.type == pygame.KEYDOWN:
                        if 48 <= event.key <=57:
                            self.toggle(event.key-48)
                        if event.key == pygame.K_m:
                            self.toggle_audio()
                        if event.key == pygame.K_t:
                            self.toggle(2)
                            self.toggle(3)

        def toggle(self, button): # To be overridden
            print("TOGGLE", button)
        def toggle_audio(self): # To be overridden
            print("TOGGLE AUDIO PAUSE")


class MP3Player(Actor):
    class Behaviour:
        def __init__(self, filename):
            pygame.mixer.music.load(filename)
            self.playing = True
            pygame.mixer.music.play(-1)
            print("PLAY")

        def toggle_audio(self):
            if self.playing:
                print("----")
                pygame.mixer.music.pause()
            if not self.playing:
                print("PLAY")
                pygame.mixer.music.unpause()
            self.playing = not self.playing
        def stop(self):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    actor_methods = ["toggle_audio"]


class Display(Actor):
    # This is blocking, but we want to be in the foreground thread, so we won't mark it as blocking
    class Behaviour:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.layers = [None] * 10
            self.visible = [True] * 10
        def main(self):
            display = pygame.display.set_mode((self.width, self.height))
            clock = pygame.time.Clock()
            while True:
                yield 1
                display.fill((0,0,0))
                for index, layer in enumerate(self.layers):
                    if layer is not None:
                        if self.visible[index]:
                            rect, location = layer
                            pygame.Surface.blit(display, rect, location)
                pygame.display.flip()
                clock.tick(FPS)

        def set_visibility(self, visibility):
            for index, value in enumerate(visibility):
                self.visible[index] = value
        def toggle_layer(self, layer):
            print("toggle_layer", layer)
            self.visible[layer] = not self.visible[layer]
        def render(self, index, rect, location):
            self.layers[index] = (rect, location)

        input = render # have input as an alias for render

    actor_methods = ["render", "toggle_layer", "set_visibility", "input"]

if __name__ == "__main__":

    from miniguild import Scheduler, Actor
    pygame.init()
    pygame.mixer.init() 

    s = Scheduler()
    s.blocking = False # Force running in foreground

    tt = TimedText("resources/ulysses.txt")
    display = Display(800, 600)

    mt = MapTile("resources/uk_map.png", (800,600), (0,0), display, 1)
    vid1 = FrameSource("resources/squirrel-cleaned-mVafW9jiEYA.mp4", 30, (576,324), (-50,100), display, 2)
    vid2 = FrameSource("resources/shia-labeouf-ZXsQAXx_ao0.mp4", 24, (576,324), (-50,130), display, 3)
    td = TextDisplay((700,80), 24, (50,450), display, 4)

    mp3 = MP3Player("resources/hippo.mp3")

    display.set_visibility([True,True,True,False,True])

    k = Controller([tt, mt, vid1, vid2, td, mp3, display])
    k.link("toggle", display.toggle_layer)
    k.link("toggle_audio", mp3.toggle_audio)
    s.schedule(mt,display, mp3, td )
    tt.link("output", td.input)

    vid1.background()
    vid2.background()
    k.background()
    tt.background()
    s.run()

if 0:

    # Theoretical Alternative
    
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


    # Note the above assumes the existence of this component:
    class TForm(Actor):
        class Behaviour:
            def __init__(self, transform):
                self.transform
            def input(self, message):
                result = self.transform(message)
                self.output(result)
            def output(self, message): # Expected to be overridden
                pass
        actor_methods = ["input"]

