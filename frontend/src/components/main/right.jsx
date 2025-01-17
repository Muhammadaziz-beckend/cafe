import { useEffect, useState } from "react";
import Search from "../../static/images/Vector (20).svg";

const Product = ({ id, image, name, price, orders, setOrder }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const existingOrderIndex = orders.findIndex((item) => item?.dish_id === id);
    setCount(orders[existingOrderIndex]?.count || 0);
  }, [orders]);

  const setOrderFun = (count) => {
    let updatedOrders = [...(orders || [])]; // Копируем текущие заказы
    const existingOrderIndex = updatedOrders.findIndex(
      (item) => item?.dish_id === id
    );

    if (existingOrderIndex !== -1) {
      // Если объект с таким id уже существует, обновляем его count
      updatedOrders[existingOrderIndex].count = count;
    } else {
      // Если объекта нет, добавляем его
      updatedOrders.push({ dish_id:id, count, name, price });
    }

    setOrder(updatedOrders); // Обновляем заказы
  };

  const increment = () => {
    const newCount = count + 1;
    setCount(newCount);
    setOrderFun(newCount); // Обновляем orders через setOrderFun
  };

  const decrement = () => {
    const newCount = Math.max(count - 1, 0); // Убедимся, что count не меньше 0
    setCount(newCount);
    setOrderFun(newCount); // Обновляем orders через setOrderFun
  };

  return (
    <div className="blok">
      <div className="top">
        <img src={image} alt="" />
      </div>
      <div className="bottom_top">
        <span>{name}</span>
      </div>
      <div className="bottom_bottom">
        <div className="blok_add_product">
          <button className="del" onClick={decrement}>
            -
          </button>
          <div className="count">{count}</div>
          <button className="add" onClick={increment}>
            +
          </button>
        </div>
        <span>Цена: {Math.ceil(price)}</span>
      </div>
    </div>
  );
};

const Right = ({ products, setProducts, orders, setOrder, setSearch }) => {
  const handelSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    const searchValue = formData.get("search").trim();

    setSearch(searchValue);
  };

  return (
    <>
      <div className="right">
        <div className="container_right">
          <div className="right_items">
            <div className="header_main_right">
              <form
                method="post"
                onSubmit={handelSubmit}
                className="blok_search"
              >
                <label className="label_input">
                  <input
                    type="text"
                    className="input"
                    name="search"
                    placeholder="Введите запрос"
                  />
                  <button type="submit">
                    <img src={Search} />
                  </button>
                </label>
              </form>
            </div>

            <div className="blok_items_right">
              {products?.map((item) => (
                <Product
                  key={item?.id} // Уникальный ключ для каждого продукта
                  id={item?.id}
                  image={item?.image}
                  name={item?.name}
                  price={item?.price}
                  orders={orders}
                  setOrder={setOrder}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Right;
