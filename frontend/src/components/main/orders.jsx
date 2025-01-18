import { useEffect, useState } from "react";
import FilterDate from "../../static/images/data-filter.svg";
import FilterLines from "../../static/images/filter-lines.svg";

const Product = ({
  id,
  table_number,
  owner,
  status,
  total_price,
  created_at,
  updated_at,
}) => {
  const statusMap = {
    pending: "В ожидании",
    paid: "Готово",
    ready: "Оплачено",
  };

  const formatDate = (dateString) => {
    const months = [
      "января",
      "февраля",
      "марта",
      "апреля",
      "мая",
      "июня",
      "июля",
      "августа",
      "сентября",
      "октября",
      "ноября",
      "декабря",
    ];

    const date = new Date(dateString);

    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");

    return `${day} ${month} ${year} г. ${hours}:${minutes}`;
  };

  return (
    <tr class="hover:bg-gray-100 cur">
      <td class="border border-gray-400 px-4 py-2">{id}</td>
      <td class="border border-gray-400 px-4 py-2">{table_number}</td>
      <td class="border border-gray-400 px-4 py-2">{owner?.username}</td>
      <td class="border border-gray-400 px-4 py-2">{total_price}</td>
      <td class="border border-gray-400 px-4 py-2">
        <select className="bg-white border rounded px-2 py-1">
          <option value="pending" selected={status === "pending"}>
            {statusMap.pending}
          </option>
          <option value="paid" selected={status === "paid"}>
            {statusMap.paid}
          </option>
          <option value="ready" selected={status === "ready"}>
            {statusMap.ready}
          </option>
        </select>
      </td>
      <td class="border border-gray-400 px-4 py-2">{formatDate(created_at)}</td>
      <td class="border border-gray-400 px-4 py-2">{formatDate(updated_at)}</td>
    </tr>
  );
};

const OrdersC = ({ ordersData, setOrderData, dataFilter, setDataFilter }) => {
  const handelSubmit = (event) => {
    event.preventDefault();
  
    const formData = new FormData(event.target);
    let data = {};
  
    for (let [key, value] of formData.entries()) {
      // Преобразование даты, если ключ соответствует полю для даты
      if (key === 'start_time') {
        const date = new Date(value); // Преобразуем значение в объект Date
        data[key] = date.toISOString(); // Преобразуем в формат ISO строки (например, 2024-11-27T20:46:00.000Z)
      } else {
        data[key] = value;
      }
    }
  
    setDataFilter(data);
  };
  

  return (
    <>
      <div className="orders right">
        <div className="right_container">
          <div className="orders_items overflow_overlay relative">
            <div className="header_main_right flex items-start gap-4  mb-4">
              <form
                onSubmit={handelSubmit}
                method="post"
                className="flex gap-4"
              >
                <label className="label">
                  от
                  <input
                    type="datetime-local"
                    name="start_time"
                    placeholder="sdasd"
                    className="w-25 rounded-xl p-2"
                    required
                  />
                </label>
                <label className="label">
                  до
                  <input
                    type="datetime-local"
                    name="end_time"
                    placeholder="sdasd"
                    className="w-25 rounded-xl p-2"
                  />
                </label>
                <button
                  type="submit"
                  className="submit bg-blue-600 text-neutral-100 p-2  rounded-xl"
                >
                  Фильтровать
                </button>
              </form>
            </div>
            <table className="table-auto border-collapse border border-gray-400 w-full text-sm text-gray-800">
              <thead>
                <tr class="bg-gray-200 text-left">
                  <th class="border border-gray-400 px-4 py-2">ID</th>
                  <th class="border border-gray-400 px-4 py-2">Номер стола</th>
                  <th class="border border-gray-400 px-4 py-2">Кассир</th>
                  <th class="border border-gray-400 px-4 py-2">Общая цена</th>
                  <th class="border border-gray-400 px-4 py-2">Статус</th>
                  <th class="border border-gray-300 px-4 py-2 flex gap-4">
                    Дата создания
                    <div className="filter_date">
                      <img src={FilterDate} alt="" />
                    </div>
                  </th>
                  <th class="border border-gray-400 px-4 py-2">
                    Дата обновления
                  </th>
                </tr>
              </thead>
              <tbody>
                {ordersData?.map((item) => (
                  <>
                    <Product
                      key={item?.id}
                      id={item?.id}
                      owner={item?.owner}
                      table_number={item?.table_number}
                      status={item?.status}
                      total_price={item?.total_price}
                      created_at={item?.created_at}
                      updated_at={item?.created_at}
                    />
                  </>
                ))}
              </tbody>
            </table>

            <div className="blok_info_total_price fixed bottom-2 right-5 text-xl font-semibold">
              <span>Общая цена: </span>
              <span>
                {ordersData.reduce(
                  (acc, item) => (acc += Number(item?.total_price)),
                  0
                )}
              </span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default OrdersC;
