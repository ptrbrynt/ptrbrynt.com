---
title: "How to actually do TDD in Flutter"
date: 2022-08-04
slug: posts/how-to-actually-do-tdd-in-flutter
tags:
  - "Flutter"
  - "Software Engineering"
---

This post is the result of a months-long existential crisis about how to do testing in Flutter apps. There are _so many_ resources, tutorials, and opinions on how this should be done, but most of them give what is, in my opinion, bad advice.

The aim of this post is to put forward a case for a change in direction. The Flutter community is barrelling towards a nightmare of unmaintainable test suites, and development practices which waste more time than they save. We need to look at the practices we're encouraging as a community and ensure that we are promoting good engineering that delivers **value** to our customers.

_A lot of the ideas in this post came from a fantastic talk by Ian Cooper at Devternity 2017 called "TDD: Where did it all go wrong?" It's worth watching that video first before trying to apply the ideas to Flutter. Here's the link:_ [_🚀 TDD, Where Did It All Go Wrong (Ian Cooper)_](https://www.youtube.com/watch?v=EZ05e7EMOLM)

## The problems we're trying to solve

1. **Tests hold us hostage.** When we write over-specified tests, we couple them to our implementation details. This means that any changes we make to the implementation are likely to break a bunch of tests. This is extremely frustrating for a development team to have to deal with. It makes things difficult when they're supposed to be easy.

2. **Achieving high coverage is hard.** When we test at class level - which most of the advice says we should - we can get fairly good test coverage without too much trouble. But the last 20% or so is usually extremely difficult to cover, and often gets left out. This means that there is loads of untested code in our project.

3. **Writing tests takes too long.** We seem to spend most of our time writing fiddly tests to cover things that we know should just work.

4. **Maintaining high coverage is hard.** The first three problems combined mean that over time, coverage slowly deteriorates as developers give up covering their changes with appropriate tests.

## Some rules for TDD

If we're going to solve the problems above and still have a well-tested app, we need to learn (or re-learn) some important principles. Some of these were totally new to me; some I knew but didn't understand properly.

1. **A unit is not a class.** Or a method, or a function. A _unit_ is an encapsulation of functionality, which could be implemented as lots of classes, or a single function, or an entire app. It's a super unhelpful word. I've stopped using the phrase "unit tests"; I call them "developer tests" or "automated tests" now.

2. **Test behaviour, not implementation.** You should write tests based on requirements like, "When I type in a valid email and password, then press the login button, I should be taken to the home screen." **Don't** write tests like this: "When I type in a valid email address and password, then press the login button, the `login` method on the `AuthRepository` class should be called with the correct parameters."

3. **UI design is not behaviour.** It is totally impractical and unnecessary to test the design of your app using automated testing techniques such as golden testing. It holds your design hostage and means your tests break anytime you want to tweak something visual which doesn't actually change how the app works. The tooling is also horrible. This is precisely the purpose of human QA.

4. **Tests must not drive code design decisions.** I've seen some well-respected thought leaders in software engineering say that the design of your code should be informed or even dictated by your tests. But this breaks one of the fundamental rules of TDD, which is that tests should _not_ be coupled to the implementation of the behaviour under test. If your tests require you to design your code in a particular way, you've written your tests wrong.

5. **Don't mock your own code.** I've often done this in order to isolate the class I'm testing from its dependencies. It's unnecessary, as we'll discover.

6. **Don't skip the refactoring step.** The red-green-refactor cycle is much more important for TDD than most developers realise.

## An example

Let's build a very simple password reset screen. It has a field for you to enter a username, which can't be blank, and a button which submits the request. If the request fails, we want to show the error message. Otherwise, we want to go back to the login screen.

In this example, the app uses Firebase Auth. Because this is an **external** dependency, we're going to use a test double which mimics the behaviour of the real `FirebaseAuth`implementation. If you were using a different authentication system which worked over HTTP requests, you could use something like `http_mock_adapter` to fake your API responses.

We're also using [Riverpod](https://riverpod.dev/) as our DI solution. These techniques obviously don't require Riverpod, but I've found Riverpod to be the best DI/state management solution, so it's what I use.

### **Step 1: Write a test (or set of tests) that fails**
```dart
    void main() {
      group('reset password screen', () {
        testWidgets(
          '''goes to the login screen when a valid username is entered and the request succeeds''',
          (tester) async {
            final auth = MockFirebaseAuth(signedIn: false);
            
            await tester.pumpWidget(
              ProviderScope(
                overrides: [
                  firebaseAuthProvider.overrideWithValue(auth),
                ],
                child: MyApp(
                  initialRoute: '/login/forgot-password',
                ),
              ),
            );
            
            await tester.enterText(
              find.byKey(const Key('forgot-password-username-field')),
              'username',
            );
            
            await tester.tap(
              find.byKey(const Key('forgot-password-submit-button')),
            );
            
            await tester.pumpAndSettle();
            
            expect(
              find.byType(LoginWidget),
              findsOneWidget,
            );
          },
        );
        
        testWidgets(
          '''displays an error message in a snackbar when the user is not found'''
          (tester) async {
            final auth = MockFirebaseAuth(
              signedIn: false,
              authExceptions: AuthExceptions(
                sendPasswordResetEmail: FirebaseAuthException(code: 'auth/user-not-found')
              ),
            );
            
            await tester.pumpWidget(
              ProviderScope(
                overrides: [
                  firebaseAuthProvider.overrideWithValue(auth),
                ],
                child: MyApp(
                  initialRoute: '/login/forgot-password',
                ),
              ),
            );
            
            await tester.enterText(
              find.byKey(const Key('forgot-password-username-field')),
              'username',
            );
            
            await tester.tap(
              find.byKey(const Key('forgot-password-submit-button')),
            );
            
            await tester.pumpAndSettle();
            
            expect(
              find.text('User not found'),
              findsOneWidget,
            );
          },
        );
        
        testWidgets(
          '''shows a validation error when no username is entered''',
          (tester) async {
            await tester.pumpWidget(
              ProviderScope(
                child: MyApp(
                  initialRoute: '/login/forgot-password',
                ),
              ),
            );
            
            await tester.tap(
              find.byKey(const Key('forgot-password-submit-button')),
            );
            
            await tester.pumpAndSettle();
            
            expect(
              find.descendant(
                of: find.byKey(const Key('forgot-password-username-field')),
                matching: find.text('Please enter your username'),
              ),
              findsOneWidget,
            );
          },
        );
      });
    }
```
Some important things to note about this test:

1. We are running the whole app, rather than only pumping the widget under test. This is so we don't have to bother with any navigation mocking.

2. We always refer to widgets by keys, not by types. This is to ensure we can change the type of widget without the test breaking (e.g. if an `ElevatedButton` becomes a `TextButton`).

3. The exception to this rule is when we check that the `LoginWidget` is visible. I think this is fine as the alternative would be wrangling to find the path of the current route or something.

4. We're not using any mock-style verifications to check that the correct method was called on the `FirebaseAuth` class. This would couple our test to the implementation details, which we must not do.

Run the tests and, of course, they all fail. Let's make them pass.

### Step 2: Make the test pass by making a mess

Here, we just need to write as little code as possible to make sure the test passes.
```dart
    class ForgotPasswordWidget extends ConsumerStatefulWidget {
      const ForgotPasswordWidget({super.key});
      
      @override
      ConsumerState<ForgotPasswordWidget> createState() => _ForgotPasswordWidgetState();
    }
    
    class _ForgotPasswordWidgetState extends ConsumerState<ForgotPasswordWidget>() {
      final _formKey = GlobalKey<FormState>();
      final _usernameController = TextEditingController();
      
      @override
      Widget build(BuildContext context) {
        return Scaffold(
          body: Form(
            key: _formKey,
            child: Column(
              children: [
                TextFormField(
                  key: const Key('forgot-password-username-field'),
                  controller: _usernameController,
                  validator: (value) {
                    if (value!.isEmpty) {
                      return 'Please enter your username';
                    }
                    return null;
                  },
                ),
                ElevatedButton(
                  key: const Key('forgot-password-submit-button'),
                  onPressed: () async {
                    if (_formKey.currentState!.validate()) {
                      final auth = ref.read(firebaseAuthProvider);
                      
                      try {
                        await auth.sendPasswordResetEmail(
                          email: _emailController.text,
                        );
                      } on FirebaseAuthException catch (e) {
                        if (e.code == 'auth/user-not-found') {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('User not found')),
                          );
                        }
                      }
                    }
                  },
                  child: Text('Submit')
                ),
              ],
            ),
          ),
        );
      }
    }
```
💡In a real app, you would also need to ensure you've set your router up correctly.

That's it! The code is sufficient to ensure all our tests pass. A couple of things to note:

1. If we ran this app, it would look terrible. We haven't applied any UI design to it yet. That's okay.

2. Because it's a very simple example, the code looks okay. In a more complex widget, your code might be horrible and messy. That's okay too.

We can now move on to the final step.

### Step 3: Refactor, keeping the tests green all the way

We now come to the most important and useful step of TDD. We have a basic implementation which we can prove is working. Now we can begin refactoring: the process of changing the design of our code and/or the UI **without** changing the behaviour and causing the tests to fail.

Each time we make a change, we can run the tests again to make sure we haven't broken something.

In terms of refactoring, if you're not sure where you might go from here there is a great resource at [refactoring.guru](http://refactoring.guru) which helps you identify opportunities to improve the design of your code. You could extract methods or classes to separate concerns; you could improve variable naming; you could generalise something to make it reusable. The important thing to remember is that **anything you do from here should not change the way the screen behaves, and your tests should pass after every refactoring step.**

This is also the moment at which you apply the UI design. Add fancy animations, loading states, pretty pictures, and all the rest. But don't change the functionality required by your tests.

By the end, you should find that you have **well-designed code that is 100% covered by tests.** If your coverage is below 100%, that _must_ mean that you've written some code that you didn't need to, or introduced new behaviour that isn't tested. **Get rid of anything that you haven't written a test for, or write tests for the stuff you know you need.**

Of course, any external dependencies you're mocking (like `FirebaseAuth` in my example) won't be covered by tests. That's okay - if you're using Riverpod you can just exclude the providers from coverage reports:
```dart
    // coverage:ignore-start
    final firebaseAuthProvider = Provider((_) => FirebaseAuth.instance);
    // coverage:ignore-end
```
You've made a deliberate and good decision never to use this dependency in a test, so ignoring it in coverage reports is totally appropriate and justified.

### The results

1. We have a suite of tests which protects the **behaviour** of our code without locking in its implementation. We can re-implement parts of this code without breaking the tests. We will only need to change the tests if we're changing the behaviour (e.g. if we wanted to disable the Submit button until the user has entered a username).

2. High code coverage is easy to achieve this way. By not mocking our own code, we cover huge swathes of it with very few tests.

3. It was fast, and we got meaningful feedback at every step.

4. The burden of maintaining these tests will be low, and it's easy to keep coverage high.

Adopting this approach allows you to use your tests as a tool rather than a shackle. They give you confidence when refactoring by ensuring nothing more than that the behaviour of your code stays consistent. Tests should _never_ hold you to any particular implementation or design, and our tests don't.

The other important aspect of this approach is that it's astonishingly easy. You write fewer tests, and those tests are a much lower maintenance burden.

All this means you can provide value to your users and customers faster, while still having a well-tested codebase. Truly the best of both worlds.