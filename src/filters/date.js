// Source - https://stackoverflow.com/a/78200088
// Posted by Brian
// Retrieved 2026-04-28, License - CC BY-SA 4.0

const { DateTime } = require("luxon");

// Add a friendly date filter to nunjucks.
// Defaults to format of LLLL dd, yyyy unless an alternate is passed as a parameter.
// {{ date | friendlyDate('OPTIONAL FORMAT STRING') }}
// List of supported tokens: https://moment.github.io/luxon/docs/manual/formatting.html#table-of-tokens

module.exports = (dateObj, format = "DDD") => {
  if (dateObj instanceof Date) {
    return DateTime.fromJSDate(dateObj, {
      zone: "utc",
      locale: "en",
    })
      .setLocale("en-GB")
      .toFormat(format);
  } else {
    return DateTime.fromISO(dateObj, {
      zone: "utc",
      locale: "en",
    })
      .setLocale("en-GB")
      .toFormat(format);
  }
};
