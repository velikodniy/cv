export const formatDate = (date: string) =>
  new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    timeZone: "UTC",
  }).format(new Date(date));
