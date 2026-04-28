---
title: "Wix Studio is terrible"
date: 2024-06-07
slug: posts/wix-studio-is-terrible
tags:
  - "Tech"
---

I had a task this week: to make a website for a friend.

All he wanted was a few static pages, then one CMS-connected page displaying a list of items, with a couple of links and embedded media. He didn’t want to have to fiddle about with the website building tools; if he could just add the data to a table and have it populate his site, he would be happy.

My first thought was, “This is exactly the kind of thing you should be able to do with a no-code site building tool.”

Dearest reader, I was wrong.

## Over-promise and under-deliver

Wix Studio is the platform I decided to use. On its face, it has all the features I needed: a CMS feature with the ability to create your own data structures, and Repeaters allowing you to display data from your CMS tables.

It even promises to use AI to make your website responsive across different screen sizes.

The problem is that this might be the worst piece of software I have ever used. The CMS features are weirdly limited; for example, you can’t show or hide elements in a repeater based on a condition (e.g. if this field is empty, don’t display this button). You _can_ create a table which neatly displays the CMS data, but you can’t customise how any of the field are displayed; if a field contains a link, you can’t turn it into a button. It’s just a plaintext link that isn’t even clickable.

Oh, and the responsive AI flat-out doesn’t work. I wanted to include an embedded audio file for each CMS entry, but the element is not resizeable at all, so it overflows on smaller screens. And the AI makes _terrible_ decisions about how to scale things for smaller screens.

I would have provided a screenshot of this garbage, but in my rage I destroyed everything.

## The only other option

There are plenty of amazing website building tools. I personally love Squarespace. But it doesn’t have the CMS features I need.

That said, it turns out that I can build the site I want incredibly easily using [Strapi](http://strapi.io/) and [Jekyll](https://jekyllrb.com/). So that’s what I’m doing. And I’m enjoying it very much.

## Who is Wix Studio for?

This then begs the question, who is the intended audience for Wix Studio? Even if it worked (which it doesn’t), the extremely complex tooling is apparently aimed at agencies making websites for clients. But if you need tools this complex, you probably need at least _some_ custom code, and so you’ll be hiring a developer. At which point, why not just build the site from scratch and have it completely bespoke?

On the other end of the spectrum, if all you want is a simple website with some static pages, you are going to be so frustrated with Wix Studio’s cumbersome UX that you’ll give up and use something else.

The conclusion: nobody should use Wix Studio. Code it from scratch, or use Squarespace.