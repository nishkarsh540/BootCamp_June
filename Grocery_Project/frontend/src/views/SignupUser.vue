<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="signupUser">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div class="form-group">
        <input type="radio" id="user" value="user" v-model="role" required />
        <label for="user">User</label>
        <input type="radio" id="store-manager" value="store_manager" v-model="role" />
        <label for="store-manager">Store Manager</label>
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role: 'user', // Default role is 'user'
      errorMessage: ''
    };
  },
  methods: {
    async signupUser() {
      try {
        await axios.post('http://127.0.0.1:5000/api/signup', {
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role
        });
        // Redirect to login page or another page after successful signup
        this.$router.push('/login');
      } catch (error) {
        this.errorMessage = error.response ? error.response.data.message : 'Signup failed. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
}
.form-group input[type="radio"] {
  margin-right: 5px;
}
.form-group input[type="radio"] + label {
  margin-right: 15px;
}
.form-group input[type="radio"]:checked + label {
  font-weight: bold;
}
.form-group input[type="password"],
.form-group input[type="text"],
.form-group input[type="email"] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.error-message {
  margin-top: 15px;
  color: #dc3545;
}
</style>
