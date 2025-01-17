import { useState } from "react";
import { NavLink } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import Post from "../../router/post";
import Env from "../../utils/env";

const OrdersC = ({ name, count, price }) => {
  return (
    <>
      <div className="item">
        <span>{name}</span>
        <span className="text_center">{count}</span>
        <span className="text_center">{price} ₽</span>
        <span className="text_center">{count * price} ₽</span>
      </div>
    </>
  );
};

const Left = ({ orders, setOrder ,order}) => {
  const [numberTable, setNumberTable] = useState(null);
  const { url, token } = Env();

  const handleInputChange = (event) => {
    setNumberTable(event.target.value); // обновляем состояние
  };

  const handelSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    if (!numberTable) {
      toast.info("Номер стола должен быть указанный", {
        position: "top-left",
      });
      return;
    }

    const res = await Post(
      `${url}orders/`,
      {
        table_number: numberTable,
      },
      token
    );

    if (!(res?.status == 201)) {
      toast.error("что-то пошло не так попробуйте снова", {
        position: "top-left",
      });
      return;
    }

    const post = await Post(
      `${url}orders_items/`,
      {
        order_id: res?.data?.id,
        products: orders,
      },
      token
    );
    if (post?.status == 201) {
      toast.info("Заказ сохранён успешно!");
      return setOrder([]);
    }
  };

  return (
    <>
      <div className="left">
        <div className="container_left">
          <div className="left_main_header">
            <NavLink to={"/orders/"} className={`orders ${order ? "active": ""}`}>
              Заказы
            </NavLink>
            <NavLink to={"/"} className={`crate_order ${order ? "": "active"}`}>
              Оформить заказ
            </NavLink>
          </div>
          <div className="left_items">
            <div className="left_header">
              <span className="name">Названия</span>
              <span className="count">Кол-во</span>
              <span className="price">Цена</span>
              <span className="total_price">Итог</span>
            </div>
            <div className="left_list">
              {orders?.map((item) => (
                <>
                  <OrdersC
                    name={item?.name}
                    count={item?.count}
                    price={item?.price}
                  />
                </>
              ))}

              <div className="total_price_main">
                <div className="blok_info">
                  <h2>К оплате</h2>
                  <h3>
                    {orders?.reduce(
                      (acc, item) => (acc += Number(item?.price * item?.count)),
                      0
                    )}
                    ₽
                  </h3>
                </div>
                <form
                  method="post"
                  className="blok_set_order"
                  onSubmit={handelSubmit}
                >
                  <input
                    type="number"
                    value={numberTable}
                    onChange={handleInputChange}
                    placeholder="Номер стола"
                  />
                  <button type="submit">Оформить заказ</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ToastContainer />
    </>
  );
};

export default Left;
