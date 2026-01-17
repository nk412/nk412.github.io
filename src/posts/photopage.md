@@title:photopage
@@date:20260115
@@unlisted

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