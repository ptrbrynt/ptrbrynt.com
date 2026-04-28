---
title: "In the real world, refactoring is a software engineer’s secret weapon"
date: 2023-11-14
slug: posts/in-the-real-world-refactoring-is-a-software-engineers-secret-weapon
tags:
  - "Software Engineering"
---

> Refactoring is a systematic process of improving code without creating new functionality that can transform mess into clean code and simple design.

If you've been doing software development for long enough, you probably know how to build a codebase from scratch using industry best practices. You can take that blank canvas and turn it into something beautifully crafted, thoroughly covered with tests, and maintainable for years to come.

But, dear reader, I regret to inform you that if you develop software professionally, you will rarely need these skills.

It is extremely uncommon to find a job which will let you start a codebase from scratch. Almost invariably, the first task at a new software job involves taking an existing codebase and learning to work within it.

When I started my current role at [Qured](https://qured.com), I came across this problem. I was to inherit a codebase which had been developed by a consultancy. And this codebase had _problems_.

But in my previous job, I had been spoiled. I previously worked for a development agency, where most of our projects were new builds. We had total control over the architectural decisions and day-to-day enforcement of code standards. We wrote some amazing code.

So when I came into my new job, I saw this codebase and panicked. My first instinct was to say, "This thing needs rebuilding." I couldn't face the idea of working with this codebase every day.

But I realised that, in the real world, we can't just take 12 months out of a busy product pipeline to start an app from scratch. The code may not have been good, but the app was released and was being used by real people. It contained a lot of complex business logic, handling all kinds of edge cases that could only have been discovered by putting the app into the wild and letting real users break it.

And it worked. So my job was to keep it working while improving our ability to maintain and iterate on the code.

This is where refactoring comes in. Refactoring is a set of techniques which allows you to improve an existing codebase, making it more maintainable and easier to understand. Refactoring is a very important tool if you want to ensure your codebase is set up to support your product roadmap in the future.

## Learning to refactor

Refactoring is not the same as building a project from scratch. Being able to improve an existing codebase involves several skills:

1. Being able to explain the business case for refactoring, given that many of the changes you make won't affect the user experience or introduce any new functionality

2. Being able to identify and prioritise the changes you want to make

3. Assessing the risk of any changes you're making

4. Being able to effectively verify you haven't broken anything in the process, which may or may not involve the use of automated tests

5. Understanding what is wrong with the code, what the improved version looks like, and the steps required to get there

6. Good version control skills

An amazing resource I discovered was [Refactoring Guru](https://refactoring.guru/). This website lists various "code smells" and links them to refactoring techniques which can be used to fix them. It also includes a handy list of design patterns, which can be applied to your codebase to improve the architectural design.

## Pitfalls

When refactoring, it's easy to _think_ you're helping when you actually may be introducing more complexity.

For example, a common and perhaps obvious move would be to abstract the functionality of a third-party library using the [facade pattern](https://refactoring.guru/design-patterns/facade). This pattern hides the implementation details of a piece of functionality from the classes which depend on it.

But this pattern can often introduce additional complexity. In my experience, writing more code rarely leads to a simpler, more maintainable outcome.

### Facade Pattern example

Let's say we find this class in our codebase:

    class RegisterViewModel {
        RegisterViewModel(this._auth);
    
        final FirebaseAuth _auth;
    
        Future<void> register({
            required String email, 
            required String password,
        }) async {
            await _auth.registerWithEmailAndPassword(
                email: email,
                password: password,
            );
            await _auth.signIn(
                email: email,
                password: password,
            );
        }
    }

You might look at this and think, "I can refactor this so that the ViewModel doesn't have to directly depend on Firebase, which will allow me to switch to a different authentication system in the future." This is a fair conclusion, so let's see what that might look like:

    class AuthRepository {
        AuthRepository(this._auth);
    
        final FirebaseAuth _auth;
    
        Future<void> register({
            required String email, 
            required String password,
        }) async {
            await _auth.registerWithEmailAndPassword(
                email: email,
                password: password,
            );
            await _auth.signIn(
                email: email,
                password: password,
            );
        }
    }
    
    class RegisterViewModel {
        RegisterViewModel(this._authRepository);
    
        final AuthRepository _authRepository;
    
        Future<void> register({
            required String email, 
            required String password,
        }) async {
            await _authRepository.register(
                email: email,
                password: password,
            );
        }
    }

A legitimate argument could be made that our introduction of the facade pattern has improved the design of this code. But has our codebase truly benefitted from this change? The second, refactored version has more code than the first version. Additionally, the inner workings of the registration functionality are obscured from the ViewModel class; a developer working here may not realise that the `register` method creates an account and signs in as part of the same method.

Indeed, there is an argument to be made that this is an "anti-refactor". There is a refactoring pattern known as "[removing the middle man](https://refactoring.guru/remove-middle-man)" which aims to avoid precisely the kind of structure we've introduced here.

The lesson here is to be cautious; don't just apply refactoring patterns because you see an opportunity. Take a step back and make sure the change you're making will _reduce_ complexity, not increase it.

## Roll your sleeves up

As with many software skills, the best way to learn is to practice using real code. Here are some ideas:

- Find a personal project from a few years ago and bring it up-to-date

- Use online training exercises like [these](https://understandlegacycode.com/blog/5-coding-exercises-to-practice-refactoring-legacy-code/)

- Study open-source projects on [GitHub](https://github.com/) and make improvements. You could even submit your improvements as pull requests to get feedback!

- If you get very familiar with an open-source project, you can start contributing code reviews for other contributors

And some important tips:

- Learn and practice design patterns and common refactoring methods

- Take things in small steps

- Break down big refactoring tasks into smaller pieces of work

- Take the opportunity to incorporate test-driven development. Refactoring shouldn't change any functionality (unless you find a bug along the way), so writing a test before you start refactoring can improve confidence in the changes you're making, help to build another skillset, and improve overall test coverage.

- Your IDE probably has tools available to help with refactoring, such as symbol renaming, method/class extraction, and other useful tricks.

- Work in pairs and talk through your decisions with a colleague/friend.

_If you're more of a book person, Martin Fowler has written the canonical guide to refactoring - you can find out more_ [_here_](https://refactoring.com)_._

## Wrap-up

Refactoring is a vital skill for software engineers, as it allows them to improve existing codebases without affecting functionality. But many of us undervalue these skills.

By learning to identify code smells, prioritizing changes, and effectively applying design patterns and refactoring methods, developers can enhance the maintainability of software projects, making them fit for the future. While building a project from scratch may be ideal, refactoring is the secret weapon for tackling real-world challenges and ensuring long-term success.