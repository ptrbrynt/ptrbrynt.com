---
title: Behold the recursive number to Roman numeral converter
date: 2026-05-14T17:05+01:00
---
I just read [this post](https://sava.rocks/blog/behold-the-number-to-roman-numeral-converter/) on how to convert a number to a Roman numeral. The post outlines an iterative method, which works and is very fun.

It got me thinking though. I've always had a strange interest in recursive algorithms. There is something very satisfying to me about writing a recursive method that works.

If you don't know or need a reminder, a *recursive* algorithm is one which *calls itself*. A famous example is the Fibonacci sequence, which computes the value of the next number in the sequence by adding up the previous two. If you know the sequence starts with a pair of 1s, then it's pretty easy to write a recursive function which can compute the *n*th value in the sequence:

```dart
int fib(int n) => switch (n) {
  0 || 1 => 1,
  final n => fib(n - 1) + fib(n - 2),
};
```

So I wondered whether it was possible to convert something to Roman numerals recursively. Turns out, it super is and I love it.

```dart
const romanSymbols = <int, String>{
  1000: 'M',
  900: 'CM',
  500: 'D',
  400: 'CD',
  100: 'C',
  90: 'XC',
  50: 'L',
  40: 'XL',
  10: 'X',
  9: 'IX',
  5: 'V',
  4: 'IV',
  1: 'I',
};

extension RomanNumerals on int {
  String get asRomanNumerals {
    for (final value in romanSymbols.keys) {
      if (this >= value) {
        return romanSymbols[value]! + (this - value).asRomanNumerals;
      }
    }
    return '';
  }
}
```

You call this by doing `10.asRomanNumerals`, and it works!

## How it works

> Disclosure: I was struggling to write this walkthrough so I asked Claude for some help.

The code has two parts:

**The symbol map** defines every meaningful Roman numeral value — not just the obvious ones like 1000 (M), 500 (D), 100 (C), etc., but also the subtractive combinations like 900 (CM), 400 (CD), and 9 (IX). These are the cases where a smaller symbol placed before a larger one means "subtract", so rather than handling that as special logic, they're just baked directly into the map as their own entries. The map is ordered from largest to smallest, which is key to how the conversion works.

**The extension** adds an `asRomanNumerals` property to every integer in Dart, so you can call something like `2024.asRomanNumerals` directly. When called, it walks through the map from largest value to smallest, and as soon as it finds a value that fits into the current number, it takes that Roman symbol and calls itself recursively on whatever is left over. For example, 14 is greater than 10, so it takes "X" and recurses on 4 — which matches "IV" — giving "XIV". This repeats until the number has been fully accounted for and nothing remains.

- - -

I built this as a little command-line application — source code is [here](https://github.com/ptrbrynt/roman_numerals).

I love making silly things like this with code. It reminds me of why I got into it in the first place.
