<template>
<div class="root">
  <header class="header">
      <h1>Sport matches</h1>
  </header>
  <div class="login-container">
    <h2>Sign In</h2>
    <form @submit.prevent="login_user">
      <div class="form-label-group">
        <label for="inputUsername">Username</label>
        <input
          type="text"
          id="inputUsername"
          class="form-control"
          placeholder="Username"
          required
          autofocus
          v-model="username"
        />
      </div>
      <div class="form-label-group">
        <label for="inputPassword">Password</label>
        <input
          type="password"
          id="inputPassword"
          class="form-control"
          placeholder="Password"
          required
          v-model="password"
        />
      </div>
      <div class="buttons">
        <button type="submit" class="btn btn-primary">Sign In</button>
        <button type="button" class="btn btn-success" @click="register_user">Create Account</button>
        <button type="button" class="btn btn-secondary" @click="back_matches">Back To Matches</button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      username: null,
      password: null,
      token: null,
      is_authenticated: false,
      money: 0.0
    }
  },
  methods: {
    login_user (event) {
      const data = 'username=' + this.username + '&password=' + this.password
      const path = process.env.API_URL + '/api/v1/login/access-token'
      axios.post(path, data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
        .then((res) => {
          this.logged = true
          this.token = res.data.access_token
          this.$router.push({ path: '/', query: { username: this.username, logged: this.logged, token: this.token } })
        })
        .catch((error) => {
          console.error(error)
          alert('Username or Password incorrect')
        })
    },
    register_user () {
      this.$router.push('/create-account')
    },
    back_matches (event) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.login-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

.form-label-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

.btn {
  width: 32%;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}
</style>
