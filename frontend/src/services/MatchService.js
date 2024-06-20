import http from '../http-common'

class MatchService {
  getAll () {
    return http.get('/api/v1/matches/')
      .then((res) => {
        return res.data
      })
  }

  get (id) {
    return http.get(`/api/v1/matches/${id}`)
      .then((res) => {
        return res.data
      })
  }

  create (data) {
    return http.post('/api/v1/matches/', data)
      .then((res) => {
        return res.data
      })
  }

  update (id, data) {
    return http.patch(`/api/v1/matches/${id}`, data)
      .then((res) => {
        return res.data
      })
  }

  delete (id) {
    return http.delete(`/api/v1/matches/${id}`)
      .then((res) => {
        return res.data
      })
  }
}

export default new MatchService()
