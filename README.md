# dragonflies with birds and python

This is a ~~silly~~ *pretty basic* video editing library that stands on top of `ffmpeg`. Also has it's own scripting language and interpreter called `tiva` to ease the job of editing video.  

## Why the name?

This project started as an attempt to investigate about color spaces inspired by Wolfgang Lehmann's [Dragonflies with birds and snake](https://vimeo.com/137458201) video.  

## Motivation

Simply because the video editors that I've found for GNU/Linux didn't addressed my (basic) needs:  

* cut
* paste
* **avoid crashing**

So I ended writing some sort of DSL-ish library to work with `ffmpeg`. Then I remembered about [MoviePy](http://zulko.github.io/moviepy/), a fantastic Python module to edit videos. `¯\_(シ)_/¯`.  

## What's tiva?

**tiva** stands for `tiva isn't video art`. Is the interpreter that parses `.tv` code in order to manipulate videos.  
The `.tv` code is pretty simple since it only has 4 verbs: `cut`, `paste`, `blend`, and `apply`. Each verb has a set of *arguments* to perform the action:

### `cut`

Simply cuts chunks of a video.

* `using` determines the *video input*
* `start` determines the starting point to cut
* `duration` determines the length of the video
* `render` determines the *video output*

```
cut
{
    using "video_test.mp4"
    start "00:00:00"
    duration "00:00:10"
    render "video_cut.mp4"
}
```

### `paste`

Appends videos into one.

* `using` determines the *video input*, since it *glues* together more than one video one needs to pass more than one video separated by a space
* `render` determines the *video output*

```
paste
{
    using "video_a.mp4" "video_b.mp4"
    render "video_paste.mp4"
}
```

### `blend`

Instead of appending, it will blend the videos together one on top of the other. Finishes when the longest video ends.

* `using` determines the *video input*, since it *blends* together more than one video one needs to pass more than one video separated by a space
* `render` determines the *video output*

```
blend
{
    using "video_a.mp4" "video_b.mp4"
    render "video_blend.mp4"
}
```

### `apply`

Applies `ffmpeg` filters to the video. It's possible to pass more than one filter at a time.

* `using` determines the *video input*
* `fx` determines the filters to be applied
* `render` determines the *video output*

```
# Just one filter
blend
{
    using "video_a.mp4"
    fx "reverse"
    render "video_reverse.mp4"
}

# More than one filter
blend
{
    using "video_a.mp4"
    fx "reverse" "blur"
    render "video_reverse_blur.mp4"
}
```

The valid filters are separated in two categories: with-arguments and without-arguments.  
Without-arguments:  

* `mirror`, applies a *mirror effect*  
* `greyscale`, converts to b/w  
* `sepia`, converts to sepia  
* `vintage`, gives a *vintage* look  
* `wires`, it draws the border of the objects  
* `paint`, gives a painting look  
* `negative`, inverts the color  
* `hflip`, horizontal flip  
* `vflip`, vertical flip  
* `kern`, kernel deinterling  
* `burning`, gives a burned effect  
* `negalum`, inverts the colors but based on its luminance  
* `noise`, adds noise  
* `reverse`, goes backwards  
* `portrait`, changes the video from landscape to portrait  
* `vignette`, adds a vignette to the video  
* `zoom`, zooms from the center  

With-arguments:  

* `blur`, simple Blur. By default it has a ratio of 5  
* `magnify`, magnifies a video. By default 2x  
* `random`, randomises frames of a video. By default, every 8 frames  
* `overlay`, shuffles the video. By default every 8 frames  
* `tblend`, blends frames (similar to the GIMP of Photoshop), valid values [here](https://ffmpeg.org/ffmpeg-filters.html#blend_002c-tblend)  
* `faster`, speeds up the video. By default 2x  
* `slower`, slows down the video. By default 2x  
