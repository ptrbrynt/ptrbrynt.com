module.exports = {
  eleventyComputed: {
    year: (data) => {
      return new Date(data.page.date).getFullYear();
    },
  },
};
