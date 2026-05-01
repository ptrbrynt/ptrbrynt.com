// Source - https://stackoverflow.com/a/78200088
// Posted by Brian
// Retrieved 2026-04-28, License - CC BY-SA 4.0

const { DateTime, Settings } = require("luxon");

// Add a friendly date filter to nunjucks.
// Defaults to format of LLLL dd, yyyy unless an alternate is passed as a parameter.
// {{ date | friendlyDate('OPTIONAL FORMAT STRING') }}
// List of supported tokens: https://moment.github.io/luxon/docs/manual/formatting.html#table-of-tokens

Settings.defaultLocale = "en-GB";

module.exports = (dateObj, format = "DDD") => {
  const options = { zone: "Europe/London" };
  if (dateObj instanceof Date) {
    return DateTime.fromJSDate(dateObj, options).toFormat(format);
  } else {
    return DateTime.fromISO(dateObj, options).toFormat(format);
  }
};
