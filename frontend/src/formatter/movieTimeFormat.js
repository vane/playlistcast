const movieTimeFormat = (t) => {
  let out = '';
  // show only seconds
  if (t < 60) {
    return t < 10 ? `0${t}` : t;
  }
  // show minutes:seconds
  const seconds = t % 60;
  let minutes = Math.floor(t / 60);
  if (minutes < 60) {
    out = seconds < 10 ? `0${seconds}` : seconds;
    out = `${minutes < 10 ? `0${minutes}` : minutes}:${out}`;
    return out;
  }
  // show hours:minutes:seconds
  minutes %= 60;
  const hours = Math.floor(t / 3600);
  out = seconds < 10 ? `0${seconds}` : seconds;
  out = `${minutes < 10 ? `0${minutes}` : minutes}:${out}`;
  out = `${hours < 10 ? `0${hours}` : hours}:${out}`;
  return out;
};

export default movieTimeFormat;
