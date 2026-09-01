@@title: Style guide
@@date:19700101
@@unlisted
@@essay

# A photo page
To demonstrate custom markdown directives to aid with designing a photo-essay or blog.

### Here is a heading, nice and bold
::image:tube.avif(This would be a caption, neatly placed just below the image.)

This is a regular paragraph of text right below it.
Notice that it's not the same as the caption.
The caption is in slightly muted italics while this is not.
Sometimes, you just want to start with an opening header image, and then set tone with a small paragraph of text,
maybe use some _italics_ or some **bold** for emphasis. You pull the reader in.

#### What if you want images laid out next to each other?
On narrow mobile devices, they get stacked on top of each other.

::image:recipe.avif,ice.avif(They too can have a shared caption, in the style of journals. L: A recipe on the wall, R: A leaf in glacier ice.)

You can also take an image and center and square it up. You don't need to edit an image, but instead just use CSS tricks for it.
::image-sq:negroni.avif

::image:reflection.avif,walk.avif(Another shared caption between two landscape shots. L: A Rains store, R: Nice headphones)
::image:bar.avif


This would be a conclusion.

#### Magazine-style directives
For photo essays in the spirit of print magazines. A kicker and dek set up a piece like this:

::kicker(PHOTO ESSAY · STYLE GUIDE)
### The long way home
::dek(A standfirst sits under the title in larger muted italics, easing the reader in before the essay begins.)

::dropcap(Drop caps mark the start of a section. The first letter is set large in the display font, purely with CSS, and the rest of the paragraph wraps around it the way an opening paragraph would in print.)

::pullquote(A pull quote lifts a striking line out of the essay and sets it big.)

A full-bleed image runs edge-to-edge of the screen, breaking out of the text column. Requires the `@@essay` flag, which centers the page column:

::bleed:walk.avif(Full-bleed, with the caption held back to the text column width.)

And a side caption sits in the margin next to the photo, stacking below it on mobile:

::image-side:negroni.avif(A side caption, aligned to the bottom of the image like a plate note.)

There is also a `@@theme: dark` flag for night photography, which flips the page to a dark background.
