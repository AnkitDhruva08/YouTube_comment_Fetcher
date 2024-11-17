import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import FetchDataForm from './pages/ProductsListPage'
import NavBar from './components/Navbar'
import Login from './pages/LoginPage'
import Register from './pages/RegisterPage'
import CardUpdatePage from './pages/CardUpdatePage'
import CardDetailsPage from './pages/CardDetailsPage'
import AccountPage from './pages/AccountPage'
import AccountUpdatePage from './pages/AccountUpdatePage'
import DeleteUserAccountPage from './pages/DeleteUserAccountPage'
import AllAddressesOfUserPage from './pages/AllAddressesOfUserPage'
import AddressUpdatePage from './pages/AddressUpdatePage'
import OrdersListPage from './pages/OrdersListPage'
import NotFound from './pages/NotFoundPage'


const App = () => {

  return (
    <div>
      <Router>
        <NavBar />
        <div className="container mt-4">
          <Switch>
            <Route path="/" component={FetchDataForm} exact />
          
            <Route path="/login" component={Login} exact />
            <Route path="/register" component={Register} exact />
            <Route path="/account" component={AccountPage} exact />
            <Route path="/account/update/" component={AccountUpdatePage} exact />
            <Route path="/account/delete/" component={DeleteUserAccountPage} exact />
            <Route path="/stripe-card-details" component={CardDetailsPage} exact />
            <Route path="/stripe-card-update" component={CardUpdatePage} exact />
            <Route path="/all-addresses/" component={AllAddressesOfUserPage} exact />
            <Route path="/all-addresses/:id/" component={AddressUpdatePage} exact />
            <Route path="/all-orders/" component={OrdersListPage} exact />
            <Route path="" component={NotFound} exact />
          </Switch>
        </div>
      </Router>
    </div >
  )
}

export default App
