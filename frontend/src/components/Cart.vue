<template>
  <div class="root">
    <header class="header">
      <h1>Sport matches</h1>
      <div v-if="logged" class="user-info">
        <span>👤 {{ username }}</span>
        <span>💰 {{ money.toFixed(2) }}</span>
        <div id="add-money-box">
          <input type="number" id="money-input" placeholder="Enter amount" step="0.01">
          <button id="add-btn" @click="addMoney()">Añadir</button>
        </div>
        <button class="view-cart" @click="is_showing_cart ? closeCart() : viewCart()">
          <span v-if="is_showing_cart">Cerrar cistella</span>
          <span v-else>Veure cistella</span>
          <span v-if="cartItemCount > 0">({{ cartItemCount }})</span>
        </button>
        <button class="logout" @click="logout()">Log Out</button>
      </div>
      <div v-else>
        <button class="login" @click="login()">Log In</button>
      </div>
    </header>

    <body>
    <div v-if="is_showing_cart" class="cart-container">
      <div v-if="cartItems.length > 0" class="cart">
        <table class="table">
          <thead>
          <tr>
            <th>Sport</th>
            <th>Competition</th>
            <th>Match</th>
            <th>Quantity</th>
            <th>Price(&euro;)</th>
            <th>Total(&euro;)</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in cartItems" :key="index">
            <td>{{ item.sport }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.match }}</td>
            <td>
              <button class="btn-decrease" @click="decreaseItem(index)">-</button>
              {{ item.quantity }}
              <button class="btn-increase" @click="increaseItem(index)">+</button>
            </td>
            <td>{{ item.price }}</td>
            <td>{{ item.price * item.quantity }}</td>
            <td><button class="btn-remove" @click="removeItem(index)">Eliminar entrada</button></td>
          </tr>
          </tbody>
        </table>
        <div class="actions">
          <button class="btn-back" @click="closeCart()">Enrere</button>
          <button class="btn-checkout" @click="buy_items()">Finalitzar la compra</button>
        </div>
      </div>
      <p v-else>La teva cistella és buida.</p>
    </div>

    <div v-else class="matches-container">
      <div v-if="matches.length === 0">No matches available</div>
      <div class="card" v-for="(match, index) in showMatches" :key="match.id">
        <img :src="match.image" alt="Imagen del partido">
        <div class="card-content">
          <h2>{{ match.sport }} - {{ match.category }}</h2>
          <p>{{ match.competition }}</p>
          <p>{{ match.teams }}</p>
          <p>{{ match.date }}</p>
          <p>{{ match.price }} €</p>
          <p>Entradas disponibles: {{ match.tickets }}</p>
          <button v-if="logged" @click="addToCart(index)">Afegeix a la cistella</button>
        </div>
      </div>
    </div>
  </body>
  </div>
</template>
<script>
import axios from 'axios'
import OrderService from '../services/OrderService'
import MatchService from '../services/MatchService'
export default {
  data () {
    return {
      logged: false,
      username: '',
      money: 0.00,
      token: '',
      matches: [],
      showMatches: [],
      is_showing_cart: false,
      cartItems: [],
      cartItemCount: 0,
      id: 0
    }
  },
  methods: {
    async fetchMatches () {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/matches')
        this.matches = response.data
      } catch (error) {
        console.error('Error fetching matches:', error)
      }
    },
    async getMatchLocalTeam (localId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/teams/${localId}`)
        return response.data
      } catch (error) {
        console.error('Error fetching local team:', error)
      }
    },
    async getMatchVisitorTeam (visitorId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/teams/${visitorId}`)
        return response.data
      } catch (error) {
        console.error('Error fetching visitor team:', error)
      }
    },
    async getMatchCompetition (competitionId) {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/competitions/${competitionId}`)
        return response.data
      } catch (error) {
        console.error('Error fetching competition:', error)
      }
    },
    async processMatches () {
      try {
        // Extrae los datos reales de la propiedad 'data'
        const matchesData = this.matches.data

        for (const match of matchesData) {
          const competition = await this.getMatchCompetition(match.competition_id)

          let image
          switch (competition.sport) {
            case 'football':
              image = require('@/assets/football_img.png')
              break
            case 'basketball':
              image = require('@/assets/basketball_img.png')
              break
            case 'volleyball':
              image = require('@/assets/volleyball_img.png')
              break
            case 'futsal':
              image = require('@/assets/futsal_img.png')
              break
            default:
              image = ''
              break
          }

          const showMatch = {
            id: match.id,
            sport: competition.sport,
            category: competition.category,
            competition: competition.name,
            teams: `${match.local_team} vs ${match.visitor_team}`,
            date: match.date,
            price: match.price,
            tickets: match.total_available_tickets,
            image: image
          }

          this.showMatches.push(showMatch)
        }
      } catch (error) {
        console.error('Error processing matches:', error)
      }
    },
    async initialize () {
      this.logged = this.$route.query.logged === 'true'
      this.username = this.$route.query.username || ''
      this.token = this.$route.query.token || ''
      if (this.logged === undefined) {
        this.logged = false
      }
      if (this.logged) {
        this.money = await this.getMoney()
        this.id = await this.getId()
      }

      await this.fetchMatches()
      await this.processMatches()
    },
    async getId () {
      const response = await axios.get(`http://localhost:8000/api/v1/users/me`, {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      })
      const user = response.data
      return user.id
    },
    async getMoney () {
      const response = await axios.get(`http://localhost:8000/api/v1/accounts/account`, {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      })
      const account = response.data
      return account.available_money
    },
    closeCart () {
      this.is_showing_cart = false
    },
    viewCart () {
      this.is_showing_cart = true
    },
    removeItem (cartIndex) {
      this.cartItemCount -= this.cartItems[cartIndex].quantity // Actualiza el conteo
      this.showMatches[this.cartItems[cartIndex].matchIndex].tickets += this.cartItems[cartIndex].quantity
      this.cartItems.splice(cartIndex, 1)
    },
    increaseItem (cartIndex) {
      if (this.showMatches[this.cartItems[cartIndex].matchIndex].tickets === 0) {
        alert('No tickets available for this match')
        return
      }
      this.cartItems[cartIndex].quantity++
      this.showMatches[this.cartItems[cartIndex].matchIndex].tickets--
      this.cartItemCount++
    },
    decreaseItem (cartIndex) {
      if (this.cartItems[cartIndex].quantity > 1) {
        this.cartItems[cartIndex].quantity--
        this.showMatches[this.cartItems[cartIndex].matchIndex].tickets++
        this.cartItemCount--
      }
    },
    async buy_items () {
      const amount = this.cartItems.reduce((total, item) => total + item.price * item.quantity, 0)
      if (amount > this.money) {
        alert('Not enough money')
        return
      }

      let totalTickets = 0
      for (let cartIndex = this.cartItems.length - 1; cartIndex >= 0; cartIndex--) {
        const dataOrder = {
          'tickets_bought': this.cartItems[cartIndex].quantity,
          'match_id': this.cartItems[cartIndex].match_id
        }
        OrderService.createOrder(dataOrder, this.token)

        const dataMatch = {
          'total_available_tickets': this.showMatches[this.cartItems[cartIndex].matchIndex].tickets
        }
        let idMatch = this.cartItems[cartIndex].match_id
        console.log('idMatch:', idMatch)
        MatchService.update(idMatch, dataMatch)
        totalTickets += this.cartItems[cartIndex].quantity
        this.cartItems.splice(cartIndex, 1)
      }
      this.cartItemCount -= totalTickets
      let userData = {
        'id': this.id,
        'available_money': this.money - amount
      }
      await OrderService.updateAccount(userData, this.token)
      this.money = await this.getMoney()
    },
    logout () {
      this.logged = false
      this.$router.push('/')
    },
    login () {
      this.$router.push('/userlogin')
    },
    async addMoney () {
      let userData = {}
      const amount = parseFloat(document.getElementById('money-input').value)
      if (!isNaN(amount)) {
        if (this.money + amount < 0) {
          userData = {
            'id': this.id,
            'available_money': 0
          }
        } else {
          userData = {
            'id': this.id,
            'available_money': this.money + amount
          }
        }
        await OrderService.updateAccount(userData, this.token)
        this.money = await this.getMoney()
      }
    },
    addToCart (index) {
      const match = this.showMatches[index]
      const cartItem = {
        match_id: match.id,
        sport: match.sport,
        name: match.competition,
        match: match.teams,
        quantity: 1,
        price: match.price,
        matchIndex: index
      }

      if (match.tickets === 0) {
        alert('No tickets available for this match')
        return
      }

      let existItem = false
      for (let cartIndex = 0; cartIndex < this.cartItems.length; cartIndex++) {
        if (match.id === this.cartItems[cartIndex].match_id) {
          this.increaseItem(cartIndex)
          existItem = true
          break
        }
      }
      if (!existItem) {
        this.cartItems.push(cartItem)
        match.tickets--
        this.cartItemCount++
      }
    }
  },
  async mounted () {
    await this.initialize()
  }
}
</script>

<style scoped>

.root{
}

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

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

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 10px;
  font-size: 18px;
}

.login {
  background-color: #ffc107;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 5px;
}

.logout {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 5px;
}

.view-cart,
.close-cart {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 5px;
  position: relative;
}

.view-cart::after,
.close-cart::after {
  content: attr(data-count);
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  position: absolute;
  top: -10px;
  right: -10px;
  display: none;
}

.view-cart[data-count]:not([data-count="0"])::after,
.close-cart[data-count]:not([data-count="0"])::after {
  display: inline-block;
}

.cart-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  margin: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cart table {
  width: 100%;
  border-collapse: collapse;
}

.cart th {
  font-weight: bold;
  text-align: center; /* Center-align header text */
  background-color: #f2f2f2;
  padding: 10px;
}

.cart td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  text-align: center; /* Center-align cell text */
  vertical-align: middle; /* Vertical-align cell content */
}

.btn-increase {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 2px 6px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px;
}

.btn-decrease {
  background-color: #dc3545;
  color: white;
  border: none;
}

.btn-increase {
  background-color: #28a745;
  color: white;
  border: none;
}

.btn-remove {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
}

.actions {
  display: flex;
  justify-content: space-between;
  padding: 20px 0;
}

.btn-back {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.btn-checkout {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.matches-container {
  background-color: #ffcccb;
  padding: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center; /* Center all the cards */
}

/* Estilo para las cartas de los partidos */
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px;
  padding: 20px;
  width: 300px;
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.05);
}

.card img {
  width: 100%;
  border-radius: 10px;
  margin-bottom: 20px;
}

.card-content {
  text-align: center;
}

.card-content h2 {
  font-size: 1.5em;
  margin: 10px 0;
}

.card-content p {
  margin: 5px 0;
  font-size: 1em;
}

.card-content button {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.card-content button:hover {
  background-color: #0056b3;
}
</style>
