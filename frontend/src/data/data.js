import { useEffect, useState } from "react";
import Get from "../router/get";
import Env from "../utils/env";

const Data = () => {
  const [products, setProducts] = useState([]);
  const [orders, setOrder] = useState([]);
  const { url, token } = Env();
  const [search,setSearch] = useState("")

  useEffect(() => {
    Get(`${url}dish/?search=${search}`, token).then((r) => {
      if (r?.status == 200) {
        setProducts(r?.data);
      }
    });
  }, [url,search]);

  return {
    products,
    setProducts,
    orders,
    setOrder,
    setSearch,
  };
};

export default Data;
