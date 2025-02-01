export const formatTime = (createdAt) => {
  const now = new Date();
  const createdDate = new Date(createdAt);
  const differenceInSeconds = Math.floor((now - createdDate) / 1000);

  if (differenceInSeconds < 60) {
    return "Agora a pouco";
  } else if (differenceInSeconds < 3600) {
    const minutes = Math.floor(differenceInSeconds / 60);
    return `Há ${minutes} minuto${minutes > 1 ? "s" : ""}`;
  } else if (differenceInSeconds < 86400) {
    const hours = Math.floor(differenceInSeconds / 3600);
    return `Há ${hours} hora${hours > 1 ? "s" : ""}`;
  } else {
    const days = Math.floor(differenceInSeconds / 86400);
    return `Há ${days} dia${days > 1 ? "s" : ""}`;
  }
};
