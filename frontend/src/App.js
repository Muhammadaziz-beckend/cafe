import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Left from "./components/main/left.jsx";
import Right from "./components/main/right.jsx";
import "./static/css/style.css";
import Data from "./data/data";
import OrdersC from "./components/main/orders.jsx";
import OrderItems from "./components/main/ordersItems.jsx";

const App = () => {
  const {
    products,
    setProducts,
    orders,
    setOrder,
    setSearch,
    ordersData,
    setOrderData,
    dataFilter,
    setDataFilter,
    getOrderId,
    setGetOrderId,orderItems
  } = Data();

  return (
    <>
      <Router>
        <Routes>
          {/* auth */}
          <Route path="/login/" />

          {/* auth */}

          {/* main */}

          <Route
            path="/"
            element={
              <>
                <main className="main menu">
                  <div className="container">
                    <div className="main_items">
                      <Left orders={orders} setOrder={setOrder} />
                      <Right
                        products={products}
                        setProducts={setProducts}
                        orders={orders}
                        setOrder={setOrder}
                        setSearch={setSearch}
                      />
                    </div>
                  </div>
                </main>
              </>
            }
          />

          <Route
            path="/orders/"
            element={
              <>
                <main className="main menu">
                  <div className="container">
                    <div className="main_items">
                      <OrderItems
                        order={true}
                        orderItems={orderItems}
                      />
                      <OrdersC
                        setGetOrderId={setGetOrderId}
                        ordersData={ordersData}
                        setOrderData={setOrderData}
                        dataFilter={dataFilter}
                        setDataFilter={setDataFilter}
                      />
                    </div>
                  </div>
                </main>
              </>
            }
          />

          {/* main */}
        </Routes>
      </Router>
    </>
  );
};

export default App;
