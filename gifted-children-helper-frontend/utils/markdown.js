import markdownIt from 'markdown-it';

const md = new markdownIt();

/**
 * Convert Markdown text to HTML.
 * This is a basic implementation and may not cover all Markdown features.
 * You can use a library like `markdown-it` for more advanced Markdown parsing.
 *
 * @param {string} markdown - The Markdown text to convert.
 * @returns {string} - The converted HTML.
 */
export function convertMarkdownToHtml(markdown) {
  return md.render(markdown);
}

