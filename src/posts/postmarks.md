@@title: Field notes on agent-assisted coding with Claude
@@date: 20260111

  <img src="https://postmarks.nk412.workers.dev?city=Spitalfields&country=London&native=United+Kingdom&symbol=moon&palette=22&wear=11&style=envelope&rotation=-5" width="400">

# Field notes on agent-assisted coding with Claude

[Postmarks](https://nk412.com/postmarks/gallery) is a toy project that lets you build little SVGs, like the one above, with a fun amount of customization.

While the editor is a static page with some knobs and dials, there's also a tiny service that renders these images based on URL query params to allow for easy embedding. I've been meaning to build something like this for a while now to headline my travel posts, and while this may be trivial to some, **I am unfortunately deathly scared of SVG manipulation**.

So, how far can we get with **Claude Code** and **Opus 4.5**?

Clearly pretty far with the above example!


### What I wanted to learn

While I've already been using Claude Code in a work setting for a while now, I wanted to understand how much control I could comfortably let go (and if it made sense to let go), and what works and doesn't for my development flow. In particular, I was keen to understand

- what "coding" on the move feels like, with Claude on Android
- what letting an agent release to "prod" looks like
- how I can better use these tools day to day

As a side goal, I also wanted to document _my_ process. Everyone seems to have a different way of operating with these agents, so here's mine.

**Note:** YMMV!

### First steps

I did **not** begin with a giant `PRD.md`. That would have been a great vibe-coding experiment, but perhaps that's for another post.

Instead it began with a completely empty repo and a Claude code session, with lots of initial back and forth. The first few dozen messages looked like this:

- `make me a blank html page with an SVG envelope with the words "Hello from London"`.
- `make it bigger and give it some shadow`
- `/rewind`
- `just make it slightly bigger`


### Give me them devtools

Turns out, editing SVGs and UIs manually is painful. (subjective)

Editing SVGs and UIs through an LLM with English is significantly worse! (fact)

What was a lot easier was getting access to "developer-mode" tools.

- `give me a slider to control the size`
- `make that slider go from 0-100`

**I find it a lot more productive asking the LLM _to help you_ do what you want, rather than asking it to do what you want.**


### Preemptive nudging

- `make a new worker.js to be deployed with wrangler CLI.`
- `\ESC \ESC \ESC`

_`> Interrupted · What should Claude do instead?`_

- `make a new worker.js to be deployed with wrangler CLI. you might want to extract the drawing logic from @index.html and store it separately so we can reuse it.`

I find guiding Claude on tangential details before it works on the task helps a lot. Would it have figured this out on its own? Possibly. But probably not. In my experience, it's very happy to miss details like this, resulting in duplicate code, especially if it isn't within recent context. It only recognises it later when you question it, giving you the classic _"You're absolutely right"_ moments.

The duplicated code would still work, so it's very easy to miss if the end result is all that you're evaluating by.


### Setting up continuous deployment

Github Pages for static pages (as is this site) is trivial to setup through Actions, and Cloudflare workers lets you run small services on the edge very easily with a generous Free Tier. I got all that set up and populated on Github Secrets and just let Claude know.

- `this repo now has CLOUDFLARE_API_TOKEN and ACCOUNT_ID setup as secrets. add an action to deploy on push to main! go go go`

This is bread and butter for LLMs these days, so no issues here. What it immediately does is allow you to start pushing to `main` and see things live!


### Claude Code on Android

At first glance, this looks like it's Claude Code through your phone, but in reality, **it's just a messaging app**.

Claude Code on your terminal gives you a dozen different keyboard shortcuts, tools, skills, subagents, hooks, different ways to interact, queue background tasks, shell shortcuts, etc. All of that is lost on the phone, both by design of the app as well as the form factor of the phone. It's great for dispatching instructions while you're waiting on the barista, but not so great for back-and-forths or exploring the changes.

What it does work really well for is a subset of tasks:

- Extend already existing patterns in the codebase. (`add a new color swatch with a forest green and sky blue combo!`)
- Small, fire-and-forget tasks. (`change the worker cache TTL to 2 days`)

In my experience, for anything larger or complicated, you're better off with a more hands-on approach, just so you can steer it. The results were not disastrous, but every now and then needed some small cleanup patches later.

#### Example

`Separate wear-and-tear+rotation into two different sliders` [PR](https://github.com/nk412/postmarks/pull/1)

led to the viewbox breaking, and clipping corners, which had to be fixed by a follow up `Fix the clipped corners!` [PR](https://github.com/nk412/postmarks/pull/2)


## Final thoughts

So, how far can we get with **Claude Code** and **Opus 4.5**?

- At the end of the day, I managed to build something I put off for years. That is a giant win, full stop. Everything else feels minor.
- Claude Code on Android is great for ad-hoc and small maintenance tasks, not so much for active new-feature development.
- Working with Claude as an active teammate works better than treating it as a contractor you dispatch off with large tasks.


<br>

##### Go on, give **postmarks** a spin [here](https://nk412.com/postmarks)!
<object data="https://postmarks.nk412.workers.dev?city=NK412&country=%3A%29&symbol=star&palette=7&wear=19&style=label&rotation=8" type="image/svg+xml"></object>
