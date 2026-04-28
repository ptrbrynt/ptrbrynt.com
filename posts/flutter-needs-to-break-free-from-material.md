---
title: "Flutter needs to break free from Material"
date: 2023-05-16
slug: posts/flutter-needs-to-break-free-from-material
tags:
  - "Flutter"
  - "Software Engineering"
---

I've been lucky to work on a large number of Flutter apps from scratch. Each time, we have done what we believed to be the right thing: started with a `MaterialApp` and tweaked it to suit the style of our app.

I think a lot of Flutter devs do the same thing. After all, what are our other options? It doesn't always make sense to start by building our own component library; that stuff takes time, and the Material library has a huge amount of functionality and customisability built-in. If you're trying to get a new project to market fast, you'd be pretty daft not to use a pre-built component library. And right now, Material seems to be the only widely available and well-maintained option.

Why is this a problem? Well, I think there are two issues. The first is that this behaviour is blurring the line between Flutter and Material. It seems like Flutter assumes most people will use Material, because functionality you would think is non-specific to Material sometimes ends up being Material-exclusive. For example, the Form API is only implemented for Material-specific `TextFormField` widgets and doesn't support the generic `EditableText` widget out-of-the-box.

This then becomes a self-fulfilling prophecy; as the Material library gets more functionality that doesn't come with vanilla Flutter, more folks just use the Material library. And the more folks default to it, the more effort is spent on it rather than putting effort into improving the non-Material functionality in vanilla Flutter. So that leads to Material getting even more functionality, further locking in developers.

However, as developers have felt more and more locked into Material, the more demand there has been for extra customisability. Everyone is essentially trying to shoehorn their own app designs to fit the opinionated Material design language. So the Material developers have been forced to add extra features and customisability options to the package (e.g. `ThemeExtensions`). This is great, except that it's created a massive API surface for Material themes which is extremely difficult to understand and use. On the one hand you're forced into using a preset list of text styles (`headlineLarge`, `bodyMedium` and so on), but you're also given the option of changing the text style for individual Text widgets, breaking the whole typography system. If Material was true to its design language, you would be limited to only using text styles defined by the theme, but because this doesn't fit everyone's individual design needs, per-widget customisation had to be supported.

At its core, I think this problem comes down to an identity crisis in the Material library. It's simultaneously trying to be an implementation of the very opinionated Material design system, while also supporting enough customisation for developers to be able to implement their own design systems using the tools provided by the Material library.

## **The solution**

I think the solution is for the community to start rolling out Material-free component libraries. These can be opinionated or not, but it's the first and most important step towards Flutter breaking free from Material. Not only will this make life better for Flutter developers (more choice is always better); it will also allow the Material library to become the best version of itself, potentially toning down some of its customisability options and doubling down on its opinionated design style.

Ultimately, Material should be a choice and not something you just use by default. I'd even go so far as to say that it should be unbundled from Flutter, and if you want to use it you would need to explicitly add it as a dependency. That would be a great signal to developers that Material isn't the only option, and you should go out and find the component library or design system that works best for you.

I'm happily getting the ball rolling by working on my own Material-free component library for Flutter. Catalyst UI will be an unopinionated component library, drawing plenty of inspiration from Tailwind UI. I'm having lots of fun with it so far and I'm excited for a future in which Flutter developers have more choice over the style of UI they want for their apps.