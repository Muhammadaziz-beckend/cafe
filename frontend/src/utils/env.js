const Env = () => {
  const url = "http://127.0.0.1:8000/api/v1/";
  const user = localStorage.getItem("user");
  const get_user_token = () => {
    if (typeof user == "string") {
      return JSON.parse(user)?.token;
    }

    return user?.token;
  };

  return {
    url,
    token: "b7d511a8904865039dabdcf5e47b1902c052d6e2",
  };
};

export default Env;
