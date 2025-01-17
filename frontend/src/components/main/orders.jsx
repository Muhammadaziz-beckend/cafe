import { useEffect, useState } from "react";
import FilterDate from "../../static/images/data-filter.svg";
import FilterLines from "../../static/images/filter-lines.svg";

const Product = ({}) => {};

const OrdersC = ({}) => {
  const handelSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
  };

  return (
    <>
      <div className="orders right">
        <div className="right_container">
          <div className="orders_items">
            <div className="header_main_right">
                
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default OrdersC;
