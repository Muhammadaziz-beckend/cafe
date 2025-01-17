import { useState } from "react";
import { NavLink } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import Post from "../../router/post";
import Env from "../../utils/env";

const OrderItems = ({ order }) => {
  const { url, token } = Env();

  return (
    <>
      <div className="order_items left">
        <div className="container_left">
          <div className="left_main_header">
            <NavLink
              to={"/orders/"}
              className={`orders ${order ? "active" : ""}`}
            >
              Заказы
            </NavLink>
            <NavLink
              to={"/"}
              className={`crate_order ${order ? "" : "active"}`}
            >
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

            <div className="total_price_main">
              <div className="blok_info">
                <h2>Общая сумма</h2>
                <h3>0 ₽</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ToastContainer />
    </>
  );
};

export default OrderItems;
