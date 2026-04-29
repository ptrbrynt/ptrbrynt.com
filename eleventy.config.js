const { feedPlugin } = require("@11ty/eleventy-plugin-rss");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const { eleventyImageTransformPlugin } = require("@11ty/eleventy-img");

module.exports = async function (eleventyConfig) {
  eleventyConfig.addFilter("date", require("./src/filters/date.js"));

  eleventyConfig.addPassthroughCopy({ public: "/" });
  eleventyConfig.addPassthroughCopy("images");

  eleventyConfig.addPlugin(feedPlugin, {
    type: "atom",
    collection: {
      name: "post",
      limit: 0,
    },
    metadata: {
      language: "en",
      title: "Peter Bryant",
      base: "https://ptrbrynt.com",
      author: {
        name: "Peter Bryant",
        email: "pb@ptrbrynt.com",
      },
    },
  });

  eleventyConfig.addPlugin(syntaxHighlight);

  eleventyConfig.addPlugin(eleventyImageTransformPlugin);

  const { IdAttributePlugin } = await import("@11ty/eleventy");

  eleventyConfig.addPlugin(IdAttributePlugin);

  eleventyConfig.addCollection("post", function (collectionsApi) {
    return collectionsApi.getFilteredByGlob("posts/*.md").sort(function (a, b) {
      return b.date - a.date;
    });
  });
};
