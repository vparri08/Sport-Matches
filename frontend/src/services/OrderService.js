import http from '../http-common'

class OrderService {
  createOrder (data, token) {
    return http.post('/api/v1/accounts/order', data, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then((res) => {
        return res.data
      })
  }

  getOrder (username, token) {
    return http.get(`/api/v1/accounts/orders/${username}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then((res) => {
        return res.data
      })
  }

  update (data, token) {
    return http.patch(`/api/v1/accounts/order/${data.id}`, data, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
  }

  updateAccount (data, token) {
    return http.patch(`/api/v1/accounts/account`, data, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then((res) => {
        return res.data
      })
  }
}

export default new OrderService()
