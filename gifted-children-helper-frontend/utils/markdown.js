/**
 * Convert Markdown text to HTML.
 * This is a basic implementation and may not cover all Markdown features.
 * You can use a library like `markdown-it` for more advanced Markdown parsing.
 *
 * @param {string} markdown - The Markdown text to convert.
 * @returns {string} - The converted HTML.
 */
export function convertMarkdownToHtml(markdown) {
  markdown = markdown.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold text
  markdown = markdown.replace(/\*(.*?)\*/g, '<em>$1</em>'); // Italic text
  markdown = markdown.replace(/`(.*?)`/g, '<code>$1</code>'); // Inline code

  markdown = markdown.replace(/(?:\r\n|\r|\n)/g, '<br>'); // Line breaks
  markdown = markdown.replace(/^-{3,}/g, '<hr>'); // Horizontal rule
  // titles
  markdown = markdown.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  markdown = markdown.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  markdown = markdown.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  markdown = markdown.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
  markdown = markdown.replace(/^##### (.*$)/gim, '<h5>$1</h5>');
  // bold
  markdown = markdown.replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>');
  markdown = markdown.replace(/^\* (.*$)\*/gim, '<strong>$1</strong>');

  markdown = markdown.replace(/\*(.*)\*/gim, '<em>$1</em>');
  // links
  markdown = markdown.replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2">$1</a>');
  // lists
  markdown = markdown.replace(/^\*(.*)/gim, '<li>$1</li>');
  markdown = markdown.replace(/^\d\.(.*)/gim, '<li>$1</li>');
  markdown = markdown.replace(/<li>(.*)<\/li>/gim, '<ul><li>$1</li></ul>');
  // subrayado
  markdown = markdown.replace(/__(.*)__/gim, '<u>$1</u>');

  return markdown;
}

