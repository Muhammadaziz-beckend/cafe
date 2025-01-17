import axios from "axios";

const Delete = async (url, token) => {
  const config = {
    headers: {
      Authorization: `Token ${token}`, // Добавляем токен в заголовок
    },
  };

  try {
    const res = await axios.delete(url, token ? config : "");

    return res;
  } catch (error) {
    console.log(error);
    return error;
  }
};

export default Delete;
