import { useEffect, useState } from "react";
import Get from "../router/get";
import Env from "../utils/env";

const Data = () => {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const { url, token } = Env();
  const [search, setSearch] = useState("");
  const [ordersData, setOrdersData] = useState([]);
  const [dataFilter, setDataFilter] = useState({});

  // Получение продуктов по поисковому запросу
  useEffect(() => {
    Get(`${url}dish/?search=${search}`, token).then((r) => {
      if (r?.status === 200) {
        setProducts(r?.data);
      }
    });
  }, [url, search]);

  // Получение данных заказов
  useEffect(() => {
    Get(`${url}orders/`, token).then((r) => {
      if (r?.status === 200) {
        setOrdersData(r?.data);
      }
    });
  }, [url]);

  // Получение данных выручки на основе фильтра
  useEffect(() => {
    const fetchRevenueData = async () => {
      if (dataFilter && Object.keys(dataFilter).length > 0) {
        const queryString = new URLSearchParams(dataFilter).toString(); // Преобразуем объект в строку запроса
        const response = await Get(
          `${url}orders/revenue/?${queryString}`,
          token
        );
        if (response?.status === 200) {
          setOrdersData(response?.data);
          // Здесь я заменил setProducts на setOrders, так как это скорее всего заказ, а не продукты
        }
      }
    };

    fetchRevenueData();
  }, [dataFilter]); // Следите за изменениями фильтра и других зависимостей

  useEffect(() => {
    
  }, []);

  return {
    products,
    setProducts,
    orders,
    setOrders,
    setSearch,
    ordersData,
    setOrdersData,
    dataFilter,
    setDataFilter,
  };
};

export default Data;
