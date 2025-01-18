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
  const [getOrderId, setGetOrderId] = useState();
  const [orderItems, setOrderItems] = useState([]);

  // Получение продуктов по поисковому запросу
  useEffect(() => {
    Get(`${url}dish/?search=${search}`, token).then((r) => {
      if (r?.status === 200) {
        setProducts(r?.data);
      }
    });
  }, [url, search]);

  const getOrders = async () => {
    await Get(`${url}orders/`, token).then((r) => {
      if (r?.status === 200) {
        setOrdersData(r?.data);
      }
    });
  };

  // Получение данных заказов
  useEffect(() => {
    getOrders();
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
        } else {
          return getOrders();
        }
      } else {
        // Если dataFilter пустой, вызываем getOrders()
        return getOrders();
      }
    };
    fetchRevenueData();
  }, [dataFilter]); // Следите за изменениями фильтра и других зависимостей

  useEffect(() => {
    Get(`${url}orders/${getOrderId}/order_items/`).then((r) => {
      if (r?.status == 200) setOrderItems(r?.data);
    });
  }, [getOrderId]);

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
    setGetOrderId,
    orderItems,
  };
};

export default Data;
