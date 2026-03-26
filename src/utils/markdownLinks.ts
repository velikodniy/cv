const escapeHtml = (str: string) =>
  str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

export const processMarkdownLinks = (text: string) => {
  return text.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    (_, linkText, url) =>
      `<a href="${encodeURI(url)}" target="_blank" rel="noopener">${
        escapeHtml(linkText)
      }</a>`,
  ).replace(
    /(<a\s[^>]*>.*?<\/a>)|([^<]+)/g,
    (_, tag, plain) => tag ?? escapeHtml(plain),
  );
};
