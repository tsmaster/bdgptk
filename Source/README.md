# Source

Source Code for Big Dice Games' Plotter Toolkit (bdgptk)

This is where the Python 3 source code is found that makes up the
toolkit.

## algx.py

An implementation of Knuth's "Algorithm X", a recursive
backtracker that can solve exact cover problems reasonably
efficiently.

Admittedly, not super relevant to most plotter projects, but it's
cool.


## bdgmath.py

A perhaps-too-heavy folder of math routines, which includes my own
(sigh) vector library, a few matrix utilities, and some other
math-related utilities.

## bridson.py

This might be the thing that most motivated having a toolkit, I found
myself using Bridson's Blue Noise algorithm over and over again to get
a random distribution of points that were roughly equally
spaced. Super handy for drawing a bunch of things that aren't right on
top of each other.

This implementation is using a modification to the algorithm that
gives faster results for the 2d case, where Bridson's original paper
extended upwards to arbitrary dimension.

## curve.py

Maybe you want to draw a circular arc, or a quadratic or cubic bezier
spline. This allows you to iterate along each of those curves with a
hopefully simple interface, and consistent across each of these kinds
of curves.

## drawutil.py

Miscellaneous stuff. This is the junk drawer where things go if they
don't have a better, more obvious, home. Or, if I haven't used them in
a while, and the obvious home wasn't obvious at the start.

## edgepool.py

One thing that I've learned in my short experience with making
drawings to be drawn on a plotter is that it's super handy to be able
to join individual line segments up into paths, and it's super handy
to sort those paths so that you're not moving the pen all around your
draw surface getting to where you want to be drawing.

So, an EdgePool is a container that collects line segments or
polylines, strings them together, and then returns them in a hopefully
better order than they were submitted.

There's no connection to Deadpool, the foul-mouthed Marvel
character. But you're free to think of him if you like.

## hershey.py

An implementation of Hershey fonts. I should document what fonts are
here, because that seemed like hit-and-miss when I grabbed the
repository.

# hex.py

I love me some hexagon grids. This (re-)implements some of that code
that I rewrite over and over again. Hat tip to Amit's Red Blob Games
Hexagon Grids documentation, which is super awesome.

https://www.redblobgames.com/grids/hexagons/
https://www.redblobgames.com/grids/hexagons/implementation.html
https://www.redblobgames.com/grids/hexagons/more-pixel-to-hex.html

I prefer cubic representation with points up.

Also, triangular grids are related, so if I need to draw a triangular
grid, that'll use this stuff, too.

# interp.py

Linear interpolation is easy.

Cosine interpolation can be better for some things.

For UI implementations, the rule of thumb I've heard is "shotgun into
a pillow", ie leave the start fast, then ease in to the end slow. But
we aren't writing UI code right now, are we? Or are we?

# marchingsquares.py

Marching Squares is a way to turn a bunch of samples on a grid into a
bunch of contours. If your grid is on a 3d lattice, your contours can
be surfaces. This can be handy for constructive solid geometry (CSG).

I also used this with Signed Distance Fields (SDF), qv.

On a square 2d grid, there's an ambiguity when you have a saddle, two
high points on one diagonal, and two low points on another
diagonal. There are heuristics you can use to resolve or at least come
up with a decision that you like.

I decided to use a Delaunay Triangulation of a Bridson Blue Noise grid
(see above) as my source grid and see if I got better or worse
results. Not much different, but the code was simpler. So that's
something.


# person.py

I drew a couple of stick figures more than once in Genuary 2021, so I
lifted that code here. Probably not super useful to other
people. Unless you need people. And people that need people are the
best people in the world.

# SDF_2d/

This is a directory of Signed Distance Field code. See the
subdirectory's README.md for more information.

